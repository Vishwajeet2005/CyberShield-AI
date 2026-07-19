import asyncio
from fastapi import APIRouter, Body, HTTPException
from typing import Dict, Any, List
from services.aapa_service import aapa_service

router = APIRouter(prefix="/api/aapa", tags=["AAPA"])

RAG_TIMEOUT_SECONDS = 10

@router.post("/analyze")
async def analyze(
    entity: Dict[str, Any] = Body(..., min_length=1),
    alerts: List[Dict] = Body(default=[])
):
    """
    RAG-powered Attribution Endpoint.
    Uses Chroma DB for MITRE ATT&CK retrieval and Groq for reasoning.
    Hard timeout: 10 seconds — prevents worker pool exhaustion from hanging Groq calls.
    """
    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(aapa_service.analyze_entity, entity, alerts),
            timeout=RAG_TIMEOUT_SECONDS
        )
        return result
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail=f"Attribution timed out after {RAG_TIMEOUT_SECONDS}s. Groq API may be unreachable."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
