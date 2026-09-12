import asyncio
import json
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from utils.simulator import simulator
from utils.audit_log import check_integrity, total_entries
import config
import uuid
import time
from datetime import datetime, timezone

router = APIRouter(tags=["System"])

@router.post("/api/system/demo-trigger")
async def demo_trigger():
    # Inject a new APT41 Incident into the simulator
    new_inc_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
    new_inc = {
        "id": new_inc_id,
        "title": "Lateral Movement via SMB (APT41 Match)",
        "description": "BADE detected highly anomalous behavior (Score 87/100) from AIIMS-DC-01. AAPA correlated TTPs (T1059.001, T1021.002, T1078) to APT41 with 91% confidence.",
        "severity": "CRITICAL",
        "status": "OPEN",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "affected_entities": ["AIIMS-DC-01", "10.0.4.15", "10.0.4.22"],
        "playbook_id": "pb-lat-001",
        "actions_taken": [],
        "attributed_actor": "APT41",
        "confidence": 0.91,
        "current_ttps": ["T1059.001", "T1021.002", "T1078"],
        "predicted_next_ttps": ["T1486"]
    }
    simulator._incidents.insert(0, new_inc)
    return {"status": "success", "incident_id": new_inc_id}

@router.get("/api/system/status")
async def system_status():
    now = datetime.now(timezone.utc).isoformat()
    metrics = simulator.get_metrics()
    return {
        "platform": config.APP_NAME,
        "version":  config.VERSION,
        "overall_status": "operational",
        "uptime_hours": metrics["uptime_hours"],
        "infrastructure": {
            "neo4j":      False,
            "kafka":      False,
            "clickhouse": False,
            "pytorch_ae": True,   # Autoencoder scorer is always loaded if model exists
        },
        "modules": [
            {"name": "BADE", "status": "operational", "last_heartbeat": now},
            {"name": "AAPA", "status": "operational", "last_heartbeat": now},
            {"name": "AIRO", "status": "operational", "last_heartbeat": now},
            {"name": "VPA",  "status": "operational", "last_heartbeat": now},
            {"name": "CRDT", "status": "operational", "last_heartbeat": now,
             "graph_engine": "networkx"},
        ],
        "timestamp": now,
        "audit_log": {
            "entries":   total_entries(),
            "integrity": check_integrity()["valid"],
        }
    }

@router.get("/api/system/metrics")
async def system_metrics():
    base = simulator.get_metrics()
    base["metrics_source"] = "in_memory"
    return base

@router.get("/api/events/stream")
async def event_stream():
    """Server-Sent Events stream — pushes updates every 3 seconds."""
    async def generate():
        while True:
            alerts  = simulator.get_alerts(limit=5)
            metrics = simulator.get_metrics()
            payload = {
                "type":         "update",
                "timestamp":    datetime.now(timezone.utc).isoformat(),
                "latest_alert": alerts[0] if alerts else None,
                "metrics":      metrics,
                "alert_count":  len(alerts),
                "infrastructure": {
                    "neo4j":      False,
                    "kafka":      False,
                    "clickhouse": False,
                }
            }
            yield f"data: {json.dumps(payload)}\n\n"
            await asyncio.sleep(3)

    return StreamingResponse(generate(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
