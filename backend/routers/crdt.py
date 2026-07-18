from fastapi import APIRouter, Query
from services.crdt_service import get_topology, get_attack_paths, get_chokepoints, run_scenario
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
    return get_attack_paths(source, target, max_paths)

@router.get("/chokepoints")
async def chokepoints(top_n: int = Query(5, ge=1, le=10)):
    return get_chokepoints(top_n)

@router.post("/simulate")
async def simulate(req: ScenarioRequest):
    return run_scenario(req.scenario_name)
