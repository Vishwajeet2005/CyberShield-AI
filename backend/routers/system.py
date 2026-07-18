import asyncio
import json
from datetime import datetime, timezone
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from utils.simulator import simulator
from utils.audit_log import check_integrity, total_entries
import config

router = APIRouter(tags=["System"])

@router.get("/api/system/status")
async def system_status():
    now = datetime.now(timezone.utc).isoformat()
    metrics = simulator.get_metrics()
    return {
        "platform": config.APP_NAME,
        "version": config.VERSION,
        "overall_status": "operational",
        "uptime_hours": metrics["uptime_hours"],
        "modules": [
            {"name": "BADE", "status": "operational", "last_heartbeat": now, "processed_events": 1_420_000, "error_count": 0},
            {"name": "AAPA", "status": "operational", "last_heartbeat": now, "processed_events": 2_847,    "error_count": 0},
            {"name": "AIRO", "status": "operational", "last_heartbeat": now, "processed_events": 34,       "error_count": 0},
            {"name": "VPA",  "status": "operational", "last_heartbeat": now, "processed_events": 15_220,   "error_count": 0},
            {"name": "CRDT", "status": "operational", "last_heartbeat": now, "processed_events": 2,        "error_count": 0},
        ],
        "timestamp": now,
        "audit_log": {
            "entries": total_entries(),
            "integrity": check_integrity()["valid"],
        }
    }

@router.get("/api/system/metrics")
async def system_metrics():
    return simulator.get_metrics()

@router.get("/api/events/stream")
async def event_stream():
    """Server-Sent Events stream — pushes updates every 3 seconds."""
    async def generate():
        while True:
            alerts = simulator.get_alerts(limit=5)
            metrics = simulator.get_metrics()
            payload = {
                "type": "update",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "latest_alert": alerts[0] if alerts else None,
                "metrics": metrics,
                "alert_count": len(alerts),
            }
            yield f"data: {json.dumps(payload)}\n\n"
            await asyncio.sleep(3)

    return StreamingResponse(generate(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
