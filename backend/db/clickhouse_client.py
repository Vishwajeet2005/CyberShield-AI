"""
CyberShield AI — ClickHouse Analytical Database Client
=======================================================
Replaces SQLite for high-throughput event analytics.
Stores:
  - audit_log        : all AIRO actions (append-only, hash-chained)
  - anomaly_events   : all scored telemetry events from BADE
  - system_metrics   : time-series metrics for MTTD/MTTR calculation

Falls back gracefully to SQLite if ClickHouse is unavailable.
"""

import logging
import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

logger = logging.getLogger("cybershield.clickhouse")

CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = 8123
CLICKHOUSE_DB   = "cybershield"
CLICKHOUSE_USER = "default"
CLICKHOUSE_PASS = "cybershield123"

# ─── Connection ───────────────────────────────────────────────────────────────

_client = None

def get_client():
    global _client
    if _client is not None:
        return _client
    try:
        import clickhouse_connect
        _client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            database=CLICKHOUSE_DB,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASS,
            connect_timeout=3,
        )
        _client.ping()
        logger.info("ClickHouse connected at %s:%s", CLICKHOUSE_HOST, CLICKHOUSE_PORT)
        return _client
    except Exception as e:
        logger.warning("ClickHouse unavailable (%s). Audit log will use SQLite fallback.", e)
        _client = None
        return None


def is_available() -> bool:
    return get_client() is not None


# ─── Schema ───────────────────────────────────────────────────────────────────

DDL_STATEMENTS = [
    f"CREATE DATABASE IF NOT EXISTS {CLICKHOUSE_DB}",

    # Audit log — MergeTree for append-only forensic log
    f"""
    CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB}.audit_log (
        id              UUID           DEFAULT generateUUIDv4(),
        timestamp       DateTime64(3)  DEFAULT now64(),
        action          String,
        actor           String,
        target          String,
        result          String,
        module          LowCardinality(String),
        hash            FixedString(64),
        previous_hash   FixedString(64)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(timestamp)
    ORDER BY (timestamp, module)
    """,

    # Anomaly events — TimeSeries for MTTD calculation
    f"""
    CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB}.anomaly_events (
        event_id        UUID           DEFAULT generateUUIDv4(),
        timestamp       DateTime64(3)  DEFAULT now64(),
        entity_id       String,
        entity_type     LowCardinality(String),
        anomaly_score   Float32,
        if_score        Float32,
        ae_score        Nullable(Float32),
        severity        LowCardinality(String),
        features        String,        -- JSON blob
        incident_id     Nullable(String)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(timestamp)
    ORDER BY (timestamp, entity_id)
    """,

    # System metrics — for real MTTD/MTTR aggregation
    f"""
    CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB}.incidents_timeline (
        incident_id     String,
        entity_id       String,
        created_at      DateTime64(3),
        first_alert_at  DateTime64(3),
        resolved_at     Nullable(DateTime64(3)),
        severity        LowCardinality(String)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(created_at)
    ORDER BY (created_at, incident_id)
    """,
]

def bootstrap_schema():
    client = get_client()
    if not client:
        return
    for ddl in DDL_STATEMENTS:
        try:
            client.command(ddl.strip())
        except Exception as e:
            logger.warning("ClickHouse DDL error (non-critical): %s", e)
    logger.info("ClickHouse schema bootstrapped.")


# ─── Audit Log ────────────────────────────────────────────────────────────────

def append_audit_entry(action: str, actor: str, target: str,
                        result: str, module: str,
                        hash_val: str, prev_hash: str) -> bool:
    """
    Append a tamper-evident entry to the ClickHouse audit log.
    Returns True on success, False on failure (fallback to SQLite).
    """
    client = get_client()
    if not client:
        return False
    try:
        client.insert(
            f"{CLICKHOUSE_DB}.audit_log",
            [[action, actor, target, result, module, hash_val, prev_hash]],
            column_names=["action", "actor", "target", "result", "module", "hash", "previous_hash"]
        )
        return True
    except Exception as e:
        logger.error("ClickHouse audit insert failed: %s", e)
        return False


def get_audit_log(limit: int = 100, offset: int = 0) -> List[Dict]:
    """Return audit entries from ClickHouse, newest first."""
    client = get_client()
    if not client:
        return []
    try:
        result = client.query(f"""
            SELECT toString(id) AS id,
                   formatDateTime(timestamp, '%Y-%m-%dT%H:%i:%S') AS timestamp,
                   action, actor, target, result, module, hash, previous_hash
            FROM {CLICKHOUSE_DB}.audit_log
            ORDER BY timestamp DESC
            LIMIT {limit} OFFSET {offset}
        """)
        keys = ["id", "timestamp", "action", "actor", "target", "result", "module", "hash", "previous_hash"]
        return [dict(zip(keys, row)) for row in result.result_rows]
    except Exception as e:
        logger.error("ClickHouse audit query failed: %s", e)
        return []


# ─── Anomaly Event Ingestion ──────────────────────────────────────────────────

def record_anomaly(entity_id: str, entity_type: str, anomaly_score: float,
                   if_score: float, severity: str, features: dict,
                   ae_score: Optional[float] = None,
                   incident_id: Optional[str] = None) -> bool:
    """Write a scored anomaly event to ClickHouse for time-series analysis."""
    client = get_client()
    if not client:
        return False
    try:
        client.insert(
            f"{CLICKHOUSE_DB}.anomaly_events",
            [[entity_id, entity_type, float(anomaly_score), float(if_score),
              float(ae_score) if ae_score else None,
              severity, json.dumps(features), incident_id]],
            column_names=["entity_id", "entity_type", "anomaly_score", "if_score",
                          "ae_score", "severity", "features", "incident_id"]
        )
        return True
    except Exception as e:
        logger.error("ClickHouse anomaly insert failed: %s", e)
        return False


# ─── Real MTTD / MTTR Metrics ─────────────────────────────────────────────────

def get_real_metrics() -> Dict[str, Any]:
    """
    Calculate real MTTD and MTTR from ClickHouse time-series data.
    Falls back to None values if insufficient data.
    """
    client = get_client()
    if not client:
        return {}

    try:
        # MTTD: average time from first anomaly to incident creation
        mttd_result = client.query(f"""
            SELECT
                AVG(dateDiff('minute', first_alert_at, created_at)) AS avg_mttd_minutes,
                COUNT() AS incident_count
            FROM {CLICKHOUSE_DB}.incidents_timeline
            WHERE created_at >= now() - INTERVAL 24 HOUR
        """)
        mttd_row = mttd_result.result_rows[0] if mttd_result.result_rows else (None, 0)

        # MTTR: average time from incident creation to resolution
        mttr_result = client.query(f"""
            SELECT AVG(dateDiff('minute', created_at, resolved_at)) AS avg_mttr_minutes
            FROM {CLICKHOUSE_DB}.incidents_timeline
            WHERE resolved_at IS NOT NULL
              AND created_at >= now() - INTERVAL 24 HOUR
        """)
        mttr_row = mttr_result.result_rows[0] if mttr_result.result_rows else (None,)

        # Alert volume
        alert_result = client.query(f"""
            SELECT
                COUNT() AS total_alerts,
                COUNTIf(severity = 'CRITICAL') AS critical_count,
                COUNTIf(severity = 'HIGH')     AS high_count,
                AVG(anomaly_score)             AS avg_score
            FROM {CLICKHOUSE_DB}.anomaly_events
            WHERE timestamp >= now() - INTERVAL 24 HOUR
        """)
        alert_row = alert_result.result_rows[0] if alert_result.result_rows else (0, 0, 0, 0)

        def _fmt_minutes(m):
            if m is None:
                return None
            h = int(m) // 60
            mn = int(m) % 60
            return f"{h}h {mn}m" if h else f"{mn}m"

        return {
            "mttd":            _fmt_minutes(mttd_row[0]),
            "mttr":            _fmt_minutes(mttr_row[0]),
            "alerts_24h":      int(alert_row[0]),
            "critical_alerts": int(alert_row[1]),
            "high_alerts":     int(alert_row[2]),
            "avg_anomaly_score": round(float(alert_row[3] or 0), 1),
            "data_source":     "clickhouse",
        }

    except Exception as e:
        logger.error("ClickHouse metrics query failed: %s", e)
        return {}


def record_incident_timeline(incident_id: str, entity_id: str,
                              created_at: str, first_alert_at: str,
                              severity: str):
    client = get_client()
    if not client:
        return
    try:
        client.insert(
            f"{CLICKHOUSE_DB}.incidents_timeline",
            [[incident_id, entity_id, created_at, first_alert_at, None, severity]],
            column_names=["incident_id", "entity_id", "created_at",
                          "first_alert_at", "resolved_at", "severity"]
        )
    except Exception as e:
        logger.error("ClickHouse timeline insert failed: %s", e)


def mark_incident_resolved(incident_id: str):
    client = get_client()
    if not client:
        return
    try:
        client.command(f"""
            ALTER TABLE {CLICKHOUSE_DB}.incidents_timeline
            UPDATE resolved_at = now64()
            WHERE incident_id = '{incident_id}'
        """)
    except Exception as e:
        logger.error("ClickHouse incident resolve failed: %s", e)
