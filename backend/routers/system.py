import asyncio
import json
from datetime import datetime, timezone
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from utils.simulator import simulator
from utils.audit_log import check_integrity, total_entries
from db.clickhouse_client import get_real_metrics, is_available as ch_available
from services import neo4j_service
from kafka.pipeline import kafka_producer
import config

router = APIRouter(tags=["System"])

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
            "neo4j":      neo4j_service.is_available(),
            "kafka":      kafka_producer._available,
            "clickhouse": ch_available(),
            "pytorch_ae": True,   # Autoencoder scorer is always loaded if model exists
        },
        "modules": [
            {"name": "BADE", "status": "operational", "last_heartbeat": now},
            {"name": "AAPA", "status": "operational", "last_heartbeat": now},
            {"name": "AIRO", "status": "operational", "last_heartbeat": now},
            {"name": "VPA",  "status": "operational", "last_heartbeat": now},
            {"name": "CRDT", "status": "operational", "last_heartbeat": now,
             "graph_engine": "neo4j" if neo4j_service.is_available() else "networkx"},
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

    # Enrich with real ClickHouse analytics if available
    if ch_available():
        ch_metrics = get_real_metrics()
        if ch_metrics:
            base["mttd"]            = ch_metrics.get("mttd", base.get("mttd_hours"))
            base["mttr"]            = ch_metrics.get("mttr", base.get("mttr_hours"))
            base["alerts_24h"]      = ch_metrics.get("alerts_24h", base.get("alerts_today"))
            base["avg_anomaly_score"] = ch_metrics.get("avg_anomaly_score")
            base["metrics_source"]  = "clickhouse"
    else:
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
                    "neo4j":      neo4j_service.is_available(),
                    "kafka":      kafka_producer._available,
                    "clickhouse": ch_available(),
                }
            }
            yield f"data: {json.dumps(payload)}\n\n"
            await asyncio.sleep(3)

    return StreamingResponse(generate(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
