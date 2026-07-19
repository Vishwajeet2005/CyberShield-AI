"""
CyberShield AI — Neo4j Graph Service (CRDT Upgrade)
====================================================
Replaces the in-memory NetworkX graph with a persistent Neo4j graph database.
Enables Cypher-native attack path queries, real-time CVE-to-node linkage,
and betweenness centrality-based chokepoint analysis.

Falls back gracefully to NetworkX if Neo4j is unavailable (e.g. Docker not running).
"""

import logging
from typing import Optional, Dict, List, Any

logger = logging.getLogger("cybershield.neo4j")

# ─── Config ───────────────────────────────────────────────────────────────────

NEO4J_URI      = "bolt://localhost:7687"
NEO4J_USER     = "neo4j"
NEO4J_PASSWORD = "cybershield123"

# ─── Connection ───────────────────────────────────────────────────────────────

_driver = None

def get_driver():
    global _driver
    if _driver is not None:
        return _driver
    try:
        from neo4j import GraphDatabase
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        _driver.verify_connectivity()
        logger.info("Neo4j connected at %s", NEO4J_URI)
        return _driver
    except Exception as e:
        logger.warning("Neo4j unavailable (%s). CRDT will use NetworkX fallback.", e)
        _driver = None
        return None


def is_available() -> bool:
    return get_driver() is not None


# ─── Schema Bootstrap ─────────────────────────────────────────────────────────

BOOTSTRAP_CYPHER = [
    # Constraints
    "CREATE CONSTRAINT asset_id IF NOT EXISTS FOR (a:Asset) REQUIRE a.id IS UNIQUE",
    # Indexes
    "CREATE INDEX asset_segment IF NOT EXISTS FOR (a:Asset) ON (a.segment)",
    "CREATE INDEX asset_criticality IF NOT EXISTS FOR (a:Asset) ON (a.criticality)",
]

def bootstrap_schema():
    driver = get_driver()
    if not driver:
        return
    with driver.session() as session:
        for stmt in BOOTSTRAP_CYPHER:
            try:
                session.run(stmt)
            except Exception:
                pass  # Constraint/index may already exist
    logger.info("Neo4j schema bootstrapped.")


# ─── Load Topology ────────────────────────────────────────────────────────────

def load_topology(nodes: List[Dict], edges: List[Dict]):
    """
    Write the digital twin topology into Neo4j.
    Idempotent — uses MERGE so safe to call on restart.
    """
    driver = get_driver()
    if not driver:
        return

    with driver.session() as session:
        # Nodes
        for n in nodes:
            session.run("""
                MERGE (a:Asset {id: $id})
                SET a.label       = $label,
                    a.type        = $type,
                    a.segment     = $segment,
                    a.criticality = $criticality,
                    a.ip          = $ip,
                    a.os          = $os
            """, id=n.get("id", ""), label=n.get("label", ""), type=n.get("type", "server"),
                 segment=n.get("segment", "INTERNAL"), criticality=n.get("criticality", "LOW"),
                 ip=n.get("ip", ""), os=n.get("os", ""))

        # CVE relationships
        for n in nodes:
            for cve in n.get("cves", []):
                session.run("""
                    MERGE (c:CVE {id: $cve_id})
                    MERGE (a:Asset {id: $asset_id})
                    MERGE (a)-[:VULNERABLE_TO]->(c)
                """, cve_id=cve, asset_id=n.get("id", ""))

        # Edges
        for e in edges:
            session.run("""
                MATCH (src:Asset {id: $source})
                MATCH (dst:Asset {id: $target})
                MERGE (src)-[r:CONNECTS_TO {protocol: $protocol, port: $port}]->(dst)
                SET r.encrypted           = $encrypted,
                    r.firewall_protected  = $firewall_protected
            """, source=e.get("source"), target=e.get("target"),
                 protocol=e.get("protocol", "TCP"), port=e.get("port", 0),
                 encrypted=e.get("encrypted", False),
                 firewall_protected=e.get("firewall_protected", False))

    logger.info("Neo4j topology loaded: %d nodes, %d edges", len(nodes), len(edges))


# ─── Attack Path Query ─────────────────────────────────────────────────────────

def get_attack_paths(source_id: str, target_id: str, max_depth: int = 6) -> List[Dict]:
    """
    Find all attack paths from source to target using Cypher shortest path.
    Returns list of paths with node sequences and total hop count.
    """
    driver = get_driver()
    if not driver:
        return []

    with driver.session() as session:
        result = session.run("""
            MATCH (src:Asset {id: $source}), (dst:Asset {id: $target}),
                  p = allShortestPaths((src)-[:CONNECTS_TO*1..$max_depth]->(dst))
            RETURN [n IN nodes(p) | n.id]   AS node_ids,
                   [n IN nodes(p) | n.label] AS node_labels,
                   length(p)                 AS hops
            LIMIT 5
        """, source=source_id, target=target_id, max_depth=max_depth)

        paths = []
        for record in result:
            paths.append({
                "node_ids":    record["node_ids"],
                "node_labels": record["node_labels"],
                "hops":        record["hops"],
            })
        return paths


# ─── Chokepoints (Betweenness) ─────────────────────────────────────────────────

def get_chokepoints(top_n: int = 10) -> List[Dict]:
    """
    Identify chokepoint nodes using betweenness centrality via GDS plugin.
    Falls back to degree centrality if GDS is not installed.
    """
    driver = get_driver()
    if not driver:
        return []

    with driver.session() as session:
        # Try GDS betweenness first
        try:
            result = session.run("""
                CALL gds.betweenness.stream({
                    nodeProjection: 'Asset',
                    relationshipProjection: 'CONNECTS_TO'
                })
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).id    AS node_id,
                       gds.util.asNode(nodeId).label AS label,
                       gds.util.asNode(nodeId).criticality AS criticality,
                       score
                ORDER BY score DESC
                LIMIT $top_n
            """, top_n=top_n)
            return [dict(r) for r in result]
        except Exception:
            pass

        # Fallback: degree centrality (count of connections)
        result = session.run("""
            MATCH (a:Asset)
            OPTIONAL MATCH (a)-[r:CONNECTS_TO]->()
            WITH a, count(r) AS out_degree
            OPTIONAL MATCH ()-[r2:CONNECTS_TO]->(a)
            RETURN a.id AS node_id, a.label AS label, a.criticality AS criticality,
                   out_degree + count(r2) AS score
            ORDER BY score DESC
            LIMIT $top_n
        """, top_n=top_n)
        return [dict(r) for r in result]


# ─── Live CVE Linkage ──────────────────────────────────────────────────────────

def link_cve_to_node(asset_id: str, cve_id: str):
    """Add a live CVE → Asset link in Neo4j when new CVEs are discovered."""
    driver = get_driver()
    if not driver:
        return
    with driver.session() as session:
        session.run("""
            MERGE (c:CVE {id: $cve_id})
            MERGE (a:Asset {id: $asset_id})
            MERGE (a)-[:VULNERABLE_TO]->(c)
        """, cve_id=cve_id, asset_id=asset_id)


def mark_node_compromised(asset_id: str, incident_id: str):
    """Mark a node as compromised in the digital twin (real-time attack progression)."""
    driver = get_driver()
    if not driver:
        return
    with driver.session() as session:
        session.run("""
            MATCH (a:Asset {id: $asset_id})
            SET a.compromised = true,
                a.incident_id = $incident_id,
                a.compromised_at = timestamp()
        """, asset_id=asset_id, incident_id=incident_id)
    logger.warning("Neo4j: Node %s marked COMPROMISED (incident: %s)", asset_id, incident_id)


def get_lateral_movement_paths(compromised_node_id: str) -> List[Dict]:
    """
    From a compromised node, find all reachable high-criticality targets
    via lateral movement (2-4 hops through INTERNAL segments).
    """
    driver = get_driver()
    if not driver:
        return []
    with driver.session() as session:
        result = session.run("""
            MATCH (start:Asset {id: $start}),
                  p = (start)-[:CONNECTS_TO*2..4]->(target:Asset)
            WHERE target.criticality IN ['HIGH', 'CRITICAL']
              AND target.id <> $start
            RETURN target.id        AS target_id,
                   target.label     AS target_label,
                   target.criticality AS criticality,
                   length(p)        AS hops,
                   [n IN nodes(p) | n.id] AS path
            ORDER BY
                CASE target.criticality WHEN 'CRITICAL' THEN 0 ELSE 1 END,
                hops
            LIMIT 10
        """, start=compromised_node_id)
        return [dict(r) for r in result]


def close():
    global _driver
    if _driver:
        _driver.close()
        _driver = None
