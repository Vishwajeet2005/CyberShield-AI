from fastapi import APIRouter, Body
from typing import Dict, Any, List
from services.aapa_service import aapa_service

router = APIRouter(prefix="/api/aapa", tags=["AAPA"])

@router.post("/analyze")
async def analyze(
    entity: Dict[str, Any] = Body(...),
    alerts: List[Dict] = Body(default=[])
):
    """
    RAG-powered Attribution Endpoint.
    Uses Chroma DB for MITRE ATT&CK retrieval and Claude for reasoning.
    """
    return aapa_service.analyze_entity(entity, alerts)
