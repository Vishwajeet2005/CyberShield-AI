"""
CyberShield AI — SQLite Immutable Audit Log Database
Hash-chained append-only log for court-admissible evidence.
"""

import sqlite3
import hashlib
import json
from datetime import datetime, timezone
from config import AUDIT_DB_PATH

# ─────────────────────────────────────────────
# Schema
# ─────────────────────────────────────────────

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS audit_entries (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp     TEXT    NOT NULL,
    action        TEXT    NOT NULL,
    actor         TEXT    NOT NULL,
    target        TEXT    NOT NULL,
    result        TEXT    NOT NULL,
    hash          TEXT    NOT NULL,
    previous_hash TEXT    NOT NULL,
    module        TEXT    NOT NULL
);
"""

SEED_ENTRIES = [
    ("Platform initialized", "system", "CyberShield AI v1.0.0", "SUCCESS", "SYSTEM"),
    ("BADE engine started — 25 entities loaded", "bade_engine", "entity_registry", "SUCCESS", "BADE"),
    ("Isolation Forest model trained on 12 features", "bade_engine", "anomaly_model", "SUCCESS", "BADE"),
    ("MITRE ATT&CK knowledge graph loaded — 4 actor profiles", "aapa_engine", "neo4j_graph", "SUCCESS", "AAPA"),
    ("CISA KEV feed fetched — 1148 active vulnerabilities", "vpa_engine", "cisa_kev_feed", "SUCCESS", "VPA"),
    ("NVD CVE feed refreshed — 220 new CVEs indexed", "vpa_engine", "nvd_api", "SUCCESS", "VPA"),
    ("Network topology loaded — 30 nodes, 45 edges", "crdt_engine", "digital_twin", "SUCCESS", "CRDT"),
    ("Anomaly alert raised: WORKSTATION-HR-01 score=82", "bade_engine", "WORKSTATION-HR-01", "ALERT_RAISED", "BADE"),
    ("APT41 attribution: confidence=91% for lateral movement", "aapa_engine", "incident-001", "ATTRIBUTED", "AAPA"),
    ("Playbook LATERAL_MOVEMENT_CONTAINMENT triggered", "airo_engine", "incident-001", "PLAYBOOK_STARTED", "AIRO"),
    ("Action executed: Block IP 185.220.101.47 at perimeter firewall", "airo_engine", "paloalto-fw-01", "COMPLETED", "AIRO"),
    ("Action executed: Isolate endpoint WORKSTATION-HR-01", "airo_engine", "WORKSTATION-HR-01", "COMPLETED", "AIRO"),
    ("Action executed: Revoke all sessions for user rajesh.kumar@aiims.edu", "airo_engine", "ad-dc-01", "COMPLETED", "AIRO"),
    ("HIGH blast-radius action queued: Domain-wide lockdown — awaiting approval", "airo_engine", "incident-001", "AWAITING_APPROVAL", "AIRO"),
    ("CERT-In preliminary report generated for incident-001", "airo_engine", "cert-in-report-001", "REPORT_GENERATED", "AIRO"),
]


# ─────────────────────────────────────────────
# Hash chain helpers
# ─────────────────────────────────────────────

GENESIS_HASH = "0" * 64  # SHA-256 of genesis block

def _compute_hash(previous_hash: str, timestamp: str, action: str,
                  actor: str, target: str, result: str, module: str) -> str:
    payload = json.dumps({
        "previous_hash": previous_hash,
        "timestamp": timestamp,
        "action": action,
        "actor": actor,
        "target": target,
        "result": result,
        "module": module,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def _get_last_hash(conn: sqlite3.Connection) -> str:
    cur = conn.execute("SELECT hash FROM audit_entries ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    return row[0] if row else GENESIS_HASH


# ─────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────

def init_db() -> None:
    """Initialise the database and seed with demo entries if empty."""
    conn = sqlite3.connect(AUDIT_DB_PATH)
    conn.execute(CREATE_TABLE_SQL)
    conn.commit()

    cur = conn.execute("SELECT COUNT(*) FROM audit_entries")
    count = cur.fetchone()[0]
    if count == 0:
        # Seed with historical entries spanning the last 4 hours
        base_ts = datetime.now(timezone.utc)
        for i, (action, actor, target, result, module) in enumerate(SEED_ENTRIES):
            # Spread entries backwards in time (oldest first)
            offset_minutes = (len(SEED_ENTRIES) - i) * 15
            ts = base_ts.replace(
                minute=max(0, base_ts.minute - offset_minutes % 60),
                hour=max(0, base_ts.hour - offset_minutes // 60),
            ).isoformat()
            prev_hash = _get_last_hash(conn)
            entry_hash = _compute_hash(prev_hash, ts, action, actor, target, result, module)
            conn.execute(
                "INSERT INTO audit_entries (timestamp,action,actor,target,result,hash,previous_hash,module) "
                "VALUES (?,?,?,?,?,?,?,?)",
                (ts, action, actor, target, result, entry_hash, prev_hash, module)
            )
            conn.commit()

    conn.close()


def append_audit_entry(action: str, actor: str, target: str,
                        result: str, module: str) -> dict:
    """Append a tamper-evident entry to the audit log. Returns the new entry."""
    conn = sqlite3.connect(AUDIT_DB_PATH)
    ts = datetime.now(timezone.utc).isoformat()
    prev_hash = _get_last_hash(conn)
    entry_hash = _compute_hash(prev_hash, ts, action, actor, target, result, module)

    cur = conn.execute(
        "INSERT INTO audit_entries (timestamp,action,actor,target,result,hash,previous_hash,module) "
        "VALUES (?,?,?,?,?,?,?,?) RETURNING id",
        (ts, action, actor, target, result, entry_hash, prev_hash, module)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return {
        "id": new_id,
        "timestamp": ts,
        "action": action,
        "actor": actor,
        "target": target,
        "result": result,
        "hash": entry_hash,
        "previous_hash": prev_hash,
        "module": module,
    }


def get_audit_log(limit: int = 100, offset: int = 0) -> list:
    """Return audit entries, newest first."""
    conn = sqlite3.connect(AUDIT_DB_PATH)
    cur = conn.execute(
        "SELECT id,timestamp,action,actor,target,result,hash,previous_hash,module "
        "FROM audit_entries ORDER BY id DESC LIMIT ? OFFSET ?",
        (limit, offset)
    )
    rows = cur.fetchall()
    conn.close()
    keys = ["id", "timestamp", "action", "actor", "target", "result", "hash", "previous_hash", "module"]
    return [dict(zip(keys, row)) for row in rows]


def get_entry_count() -> int:
    conn = sqlite3.connect(AUDIT_DB_PATH)
    cur = conn.execute("SELECT COUNT(*) FROM audit_entries")
    count = cur.fetchone()[0]
    conn.close()
    return count


def verify_chain_integrity() -> dict:
    """Walk the full chain and verify every hash. Returns {valid, broken_at, total}."""
    conn = sqlite3.connect(AUDIT_DB_PATH)
    cur = conn.execute(
        "SELECT id,timestamp,action,actor,target,result,hash,previous_hash,module "
        "FROM audit_entries ORDER BY id ASC"
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return {"valid": True, "broken_at": None, "total": 0}

    expected_prev = GENESIS_HASH
    for row in rows:
        rid, ts, action, actor, target, result, stored_hash, prev_hash, module = row
        if prev_hash != expected_prev:
            return {"valid": False, "broken_at": rid, "total": len(rows)}
        computed = _compute_hash(prev_hash, ts, action, actor, target, result, module)
        if computed != stored_hash:
            return {"valid": False, "broken_at": rid, "total": len(rows)}
        expected_prev = stored_hash

    return {"valid": True, "broken_at": None, "total": len(rows)}
