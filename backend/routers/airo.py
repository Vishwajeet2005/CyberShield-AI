from fastapi import APIRouter, Query
from services.airo_service import (
    get_incidents, get_playbooks, execute_action, approve_action,
    get_audit_log_entries, generate_cert_in_report
)
from models import ExecuteActionRequest, ApproveActionRequest

router = APIRouter(prefix="/api/airo", tags=["AIRO"])

@router.get("/incidents")
async def incidents():
    return get_incidents()

@router.get("/playbooks")
async def playbooks():
    return get_playbooks()

@router.post("/execute")
async def execute(req: ExecuteActionRequest):
    return execute_action(req.incident_id, req.action_id, req.actor)

@router.post("/approve")
async def approve(req: ApproveActionRequest):
    return approve_action(req.action_id, req.approver, req.decision, req.notes or "")

@router.get("/audit-log")
async def audit_log(limit: int = Query(100, ge=1, le=500), offset: int = Query(0, ge=0)):
    entries = get_audit_log_entries(limit=limit, offset=offset)
    return [e.dict() for e in entries]

@router.get("/report/{incident_id}")
async def cert_in_report(incident_id: str):
    return generate_cert_in_report(incident_id)
