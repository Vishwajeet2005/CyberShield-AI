"""
CyberShield AI — Audit Log Utility
Wraps database.py with structured AuditEntry objects.
"""

from database import append_audit_entry, get_audit_log as _db_get, verify_chain_integrity, get_entry_count
from models import AuditEntry
from typing import List


def log_action(action: str, actor: str, target: str, result: str, module: str) -> AuditEntry:
    """Append a tamper-evident entry and return it as an AuditEntry model."""
    entry = append_audit_entry(action, actor, target, result, module)
    return AuditEntry(**entry)


def get_full_log(limit: int = 100, offset: int = 0) -> List[AuditEntry]:
    """Return audit entries as AuditEntry models (newest first)."""
    rows = _db_get(limit=limit, offset=offset)
    return [AuditEntry(**r) for r in rows]


def check_integrity() -> dict:
    """Verify the hash chain. Returns {valid, broken_at, total}."""
    return verify_chain_integrity()


def total_entries() -> int:
    return get_entry_count()
