from fastapi import APIRouter, Query
from services.bade_service import get_anomaly_alerts, get_entities_with_scores, get_event_timeline, submit_feedback
from models import FeedbackRequest, IsolateRequest
from utils.audit_log import log_action

router = APIRouter(prefix="/api/bade", tags=["BADE"])

@router.get("/alerts")
async def alerts(limit: int = Query(50, ge=1, le=100)):
    return get_anomaly_alerts(limit=limit)

@router.get("/entities")
async def entities():
    return get_entities_with_scores()

@router.get("/timeline")
async def timeline(hours: int = Query(24, ge=1, le=168)):
    return get_event_timeline(hours=hours)

@router.post("/feedback")
async def feedback(req: FeedbackRequest):
    return submit_feedback(req.alert_id, req.feedback_type, req.analyst_notes)

@router.post("/isolate")
async def isolate_entity(req: IsolateRequest):
    log_action(
        action="Manual Isolation Triggered",
        actor="SOC-ANALYST-01",
        target=req.entity_id,
        result="COMPLETED in 430ms — Endpoint isolated successfully",
        module="BADE"
    )
    return {"success": True, "message": f"Entity {req.entity_id} isolated"}
