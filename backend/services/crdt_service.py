"""
CyberShield AI — CRDT Service
NetworkX-based digital twin with attack path enumeration and chokepoint analysis.
"""

import networkx as nx
from typing import List, Optional, Dict, Any

from data.topology import NODES, EDGES, PRE_BUILT_SCENARIOS, NODES_BY_ID
from models import NetworkNode, NetworkEdge, AttackPath, Chokepoint, ScenarioResult

# ─────────────────────────────────────────────
# Graph construction
# ─────────────────────────────────────────────

def _build_graph() -> nx.DiGraph:
    G = nx.DiGraph()
    for node in NODES:
        G.add_node(node["id"], **node)
    for edge in EDGES:
        # Edge weight = attack difficulty (lower = easier for attacker)
        weight = 1.0
        if edge.get("firewall_protected"):
            weight += 2.0
        if edge.get("encrypted"):
            weight += 0.5
        G.add_edge(edge["source"], edge["target"], weight=weight, **edge)
    return G


_graph: Optional[nx.DiGraph] = None
_chokepoints_cache: Optional[List[Chokepoint]] = None


def build_digital_twin():
    global _graph, _chokepoints_cache
    _graph = _build_graph()
    _chokepoints_cache = None  # Reset cache


def _get_graph() -> nx.DiGraph:
    global _graph
    if _graph is None:
        _graph = _build_graph()
    return _graph


# ─────────────────────────────────────────────
# API functions
# ─────────────────────────────────────────────

def get_topology() -> Dict:
    G = _get_graph()
    nodes = []
    for node_id, data in G.nodes(data=True):
        nodes.append({
            "id": node_id,
            "label": data.get("label", node_id),
            "type": data.get("type", "server"),
            "ip": data.get("ip", ""),
            "vulnerabilities": data.get("vulnerabilities", []),
            "controls": data.get("controls", []),
            "criticality": data.get("criticality", 5),
            "os": data.get("os"),
            "department": data.get("department"),
            "is_chokepoint": False,
        })

    edges = []
    for src, dst, data in G.edges(data=True):
        edges.append({
            "source": src,
            "target": dst,
            "protocol": data.get("protocol", "TCP"),
            "port": data.get("port", 0),
            "encrypted": data.get("encrypted", False),
            "firewall_protected": data.get("firewall_protected", False),
        })

    # Mark chokepoints
    choke_ids = {c.node_id for c in get_chokepoints()}
    for n in nodes:
        if n["id"] in choke_ids:
            n["is_chokepoint"] = True

    return {"nodes": nodes, "edges": edges, "node_count": len(nodes), "edge_count": len(edges)}


def get_attack_paths(source_node: str, target_node: str, max_paths: int = 3) -> List[AttackPath]:
    G = _get_graph()

    if source_node not in G or target_node not in G:
        # Try to find reasonable defaults
        source_node = "INTERNET"
        target_node = "AIIMS-EMR-SERVER"

    paths = []
    try:
        # Enumerate simple paths (no repeated nodes)
        all_paths = list(nx.all_simple_paths(G, source=source_node, target=target_node, cutoff=8))
        all_paths = all_paths[:max_paths * 3]  # take more than needed, then rank

        for path in all_paths:
            risk = _calculate_path_risk(G, path)
            effort = "low" if risk > 70 else ("medium" if risk > 40 else "high")
            edges = [{"source": path[i], "target": path[i+1]} for i in range(len(path)-1)]

            # Find weakest control
            weakest = None
            min_protection = 99
            for i in range(len(path) - 1):
                edge_data = G.edges.get((path[i], path[i+1]), {})
                protection = (2 if edge_data.get("firewall_protected") else 0) + (1 if edge_data.get("encrypted") else 0)
                if protection < min_protection:
                    min_protection = protection
                    weakest = f"{path[i]} → {path[i+1]} ({edge_data.get('protocol', 'TCP')}:{edge_data.get('port', 0)})"

            desc = _describe_path(path)
            paths.append(AttackPath(
                path_nodes=path,
                path_edges=edges,
                risk_score=risk,
                effort=effort,
                description=desc,
                step_count=len(path) - 1,
                weakest_control=weakest,
            ))

        paths.sort(key=lambda p: p.risk_score, reverse=True)
        return paths[:max_paths]

    except (nx.NetworkXError, nx.NodeNotFound):
        return []


def _calculate_path_risk(G: nx.DiGraph, path: List[str]) -> float:
    """Risk score = avg vulnerability count along path / avg protections × 100."""
    if len(path) < 2:
        return 0.0

    total_vulns = 0
    total_controls = 0
    total_protection = 0

    for node_id in path:
        node_data = G.nodes.get(node_id, {})
        total_vulns += len(node_data.get("vulnerabilities", []))
        total_controls += len(node_data.get("controls", []))

    for i in range(len(path) - 1):
        edge_data = G.edges.get((path[i], path[i+1]), {})
        total_protection += 2 if edge_data.get("firewall_protected") else 0
        total_protection += 1 if edge_data.get("encrypted") else 0

    vuln_score = (total_vulns * 15) / max(1, len(path))
    control_penalty = max(0, 20 - total_protection * 5)
    raw = vuln_score + control_penalty
    return round(min(100, max(0, raw)), 1)


def _describe_path(path: List[str]) -> str:
    labels = [NODES_BY_ID.get(n, {}).get("label", n) for n in path]
    return " → ".join(labels[:4]) + (f" → ... ({len(path)-1} steps total)" if len(path) > 4 else f" ({len(path)-1} steps)")


def get_chokepoints(top_n: int = 5) -> List[Chokepoint]:
    global _chokepoints_cache
    if _chokepoints_cache:
        return _chokepoints_cache

    G = _get_graph()
    try:
        centrality = nx.betweenness_centrality(G, weight="weight", normalized=True)
    except Exception:
        centrality = {n: 0.0 for n in G.nodes()}

    # Count paths through each node using simple path enumeration (sample)
    paths_through = {n: 0 for n in G.nodes()}
    try:
        sample_sources = ["INTERNET", "WORKSTATION-HR-01", "CLOUD-CONNECTOR", "DMZ-WEBSERVER"]
        sample_targets = ["AIIMS-EMR-SERVER", "DOMAIN-CONTROLLER-01", "SCADA-SERVER", "BACKUP-SERVER"]
        for src in sample_sources:
            for tgt in sample_targets:
                if src != tgt and src in G and tgt in G:
                    for path in nx.all_simple_paths(G, src, tgt, cutoff=7):
                        for n in path[1:-1]:  # Exclude endpoints
                            paths_through[n] = paths_through.get(n, 0) + 1
    except Exception:
        pass

    # Build chokepoint list from top betweenness centrality nodes (exclude external/leaf nodes)
    exclude = {"INTERNET"}
    ranked = [
        (n, c) for n, c in centrality.items()
        if n not in exclude and c > 0.0
    ]
    ranked.sort(key=lambda x: x[1], reverse=True)

    choke_recs = {
        "FW-INTERNAL":         "This is the primary chokepoint between workstations and servers. Strengthen rule base and enable IPS.",
        "CORE-SWITCH":         "All traffic passes through this switch. Enable NetFlow monitoring and port security.",
        "DOMAIN-CONTROLLER-01":"Compromise of this DC grants attacker control over all domain accounts. Enforce Tier-0 admin model.",
        "FW-PERIMETER":        "All internet traffic enters here. Keep PAN-OS patched and enable threat prevention profiles.",
        "OT-GATEWAY":          "Only connection between IT and OT networks. Verify data diode is truly unidirectional.",
        "CLOUD-CONNECTOR":     "Bridge to cloud services. Apply zero-trust access policies and monitor API calls.",
    }

    chokepoints = []
    for node_id, cent in ranked[:top_n]:
        node = NODES_BY_ID.get(node_id, {})
        chokepoints.append(Chokepoint(
            node_id=node_id,
            node_label=node.get("label", node_id),
            betweenness_centrality=round(cent, 4),
            paths_through=paths_through.get(node_id, 0),
            controls=node.get("controls", []),
            recommendation=choke_recs.get(node_id, f"Monitor {node.get('label', node_id)} closely. Any compromise creates high blast radius."),
        ))

    _chokepoints_cache = chokepoints
    return chokepoints


def run_scenario(scenario_name: str) -> ScenarioResult:
    scenario = PRE_BUILT_SCENARIOS.get(scenario_name)
    if not scenario:
        scenario_name = "lateral_movement"
        scenario = PRE_BUILT_SCENARIOS["lateral_movement"]

    entry = scenario["entry_point"]
    target = scenario["target"]
    attack_paths = get_attack_paths(entry, target, max_paths=3)
    chokepoints = get_chokepoints()

    # Identify relevant chokepoints (those on attack paths)
    path_nodes = set()
    for p in attack_paths:
        path_nodes.update(p.path_nodes)
    relevant_choke = [c for c in chokepoints if c.node_id in path_nodes]

    return ScenarioResult(
        scenario_name=scenario_name,
        description=scenario["description"],
        entry_point=entry,
        target=target,
        attack_paths=attack_paths,
        chokepoints=relevant_choke or chokepoints[:3],
        ttp_chain=scenario.get("ttp_chain", []),
        risk_level=scenario.get("risk_level", "high"),
        recommended_mitigations=scenario.get("recommended_mitigations", []),
    )
