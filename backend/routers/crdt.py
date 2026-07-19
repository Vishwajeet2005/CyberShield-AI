"""
CyberShield AI — CRDT Router
Uses Neo4j when available, falls back to NetworkX.
"""
from fastapi import APIRouter, Query
from services import neo4j_service
from services.crdt_service import get_topology, get_attack_paths as nx_attack_paths, get_chokepoints as nx_chokepoints, run_scenario
from models import ScenarioRequest

router = APIRouter(prefix="/api/crdt", tags=["CRDT"])

@router.get("/topology")
async def topology():
    return get_topology()

@router.get("/attack-paths")
async def attack_paths(
    source: str = Query("INTERNET"),
    target: str = Query("AIIMS-EMR-SERVER"),
    max_paths: int = Query(3, ge=1, le=5)
):
    # Use Neo4j Cypher if available, else NetworkX
    if neo4j_service.is_available():
        paths = neo4j_service.get_attack_paths(source, target, max_depth=8)
        return {"source": source, "target": target, "paths": paths, "engine": "neo4j"}
    return nx_attack_paths(source, target, max_paths)

@router.get("/chokepoints")
async def chokepoints(top_n: int = Query(5, ge=1, le=10)):
    if neo4j_service.is_available():
        return {"chokepoints": neo4j_service.get_chokepoints(top_n), "engine": "neo4j"}
    return nx_chokepoints(top_n)

@router.get("/lateral-movement/{node_id}")
async def lateral_movement(node_id: str):
    """Find reachable high-value targets from a potentially compromised node."""
    if neo4j_service.is_available():
        paths = neo4j_service.get_lateral_movement_paths(node_id)
        return {"compromised_node": node_id, "reachable_targets": paths, "engine": "neo4j"}
    return {"compromised_node": node_id, "reachable_targets": [], "engine": "networkx_fallback"}

@router.post("/mark-compromised/{node_id}")
async def mark_compromised(node_id: str, incident_id: str = Query(...)):
    """Mark a node as compromised in the digital twin after AIRO containment."""
    neo4j_service.mark_node_compromised(node_id, incident_id)
    return {"status": "marked", "node_id": node_id, "incident_id": incident_id}

@router.post("/simulate")
async def simulate(req: ScenarioRequest):
    return run_scenario(req.scenario_name)
