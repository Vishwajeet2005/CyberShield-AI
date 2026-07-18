from fastapi import APIRouter, Query
from services.bade_service import get_anomaly_alerts, get_entities_with_scores, get_event_timeline, submit_feedback
from models import FeedbackRequest

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
