from fastapi import APIRouter, Query
from typing import Optional, List
from services.aapa_service import get_threat_actors, get_attribution_hypotheses, get_next_moves, analyze_ttps
from models import TTpAnalysisRequest

router = APIRouter(prefix="/api/aapa", tags=["AAPA"])

@router.get("/attribution")
async def attribution(ttps: Optional[str] = Query(None)):
    observed = ttps.split(",") if ttps else None
    return get_attribution_hypotheses(observed)

@router.get("/actors")
async def actors():
    return get_threat_actors()

@router.get("/next-moves")
async def next_moves(actor_id: str = Query("apt41")):
    return get_next_moves(actor_id)

@router.post("/analyze")
async def analyze(req: TTpAnalysisRequest):
    return analyze_ttps(req.ttps)
