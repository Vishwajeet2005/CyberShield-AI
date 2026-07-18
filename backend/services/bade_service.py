"""
CyberShield AI — BADE Service
Anomaly detection, entity scoring, timeline generation, and analyst feedback.
"""

import uuid
import random
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict

from utils.simulator import simulator
from utils.audit_log import log_action
from models import Alert, Entity, TimelineEvent, FeedbackResponse, Severity, EntityType, RiskLevel


def get_anomaly_alerts(limit: int = 50) -> List[Alert]:
    raw = simulator.get_alerts(limit=limit)
    alerts = []
    for a in raw:
        try:
            alerts.append(Alert(
                id=a["id"],
                timestamp=a["timestamp"],
                severity=Severity(a["severity"]),
                entity_id=a["entity_id"],
                entity_name=a["entity_name"],
                entity_type=a["entity_type"],
                score=a["score"],
                description=a["description"],
                module=a.get("module", "BADE"),
                ttps=a.get("ttps", []),
                status=a.get("status", "open"),
                mitre_tactics=a.get("mitre_tactics", []),
            ))
        except Exception:
            continue
    return alerts


def get_entities_with_scores() -> List[Entity]:
    raw = simulator.get_entities()
    entities = []
    for e in raw:
        try:
            etype_str = e["type"]
            if etype_str not in [t.value for t in EntityType]:
                etype_str = "user"
            entities.append(Entity(
                id=e["id"],
                name=e["name"],
                type=EntityType(etype_str),
                ip_address=e["ip_address"],
                os=e.get("os", "Unknown"),
                department=e.get("department", "Unknown"),
                baseline_score=e["baseline_score"],
                current_score=e["current_score"],
                deviation=e["deviation"],
                risk_level=RiskLevel(e["risk_level"]),
                last_seen=e["last_seen"],
                alert_count=e.get("alert_count", 0),
            ))
        except Exception:
            continue
    return entities


def get_event_timeline(hours: int = 24) -> List[TimelineEvent]:
    """Generate a realistic 24-hour event timeline with 60+ events."""
    events = []
    now = datetime.now(timezone.utc)
    entities = simulator.get_entities()

    event_templates = [
        ("user_logon",       "low",      "Successful logon",               "User {entity} authenticated from {ip}"),
        ("user_logon_fail",  "medium",   "Failed authentication",          "User {entity} failed login (invalid credentials) from {ip}"),
        ("process_create",   "low",      "Process creation",               "New process spawned: cmd.exe /c net user — by {entity}"),
        ("file_access",      "low",      "Sensitive file access",          "{entity} accessed confidential HR data: salary_report_2026.xlsx"),
        ("network_conn",     "low",      "Network connection",             "{entity} established connection to {ip}:443 (HTTPS)"),
        ("powershell_exec",  "high",     "PowerShell execution",           "{entity} executed encoded PowerShell: bypass AMSI restriction"),
        ("lateral_move",     "critical", "Lateral movement detected",      "{entity} authenticated to FILE-SERVER-02 via SMB with stolen credentials"),
        ("privesc",          "high",     "Privilege escalation",           "{entity} added to Domain Admins group unexpectedly"),
        ("data_exfil",       "high",     "Data exfiltration attempt",      "{entity} transferred 4.7GB to external IP 185.220.101.47"),
        ("sched_task",       "high",     "Malicious scheduled task",       "{entity} created task 'WindowsUpdateHelper' running encoded PowerShell"),
        ("reg_mod",          "medium",   "Registry modification",          "{entity} added Run key: HKCU\\..\\Run\\svchost32"),
        ("dns_anomaly",      "medium",   "Anomalous DNS query",            "{entity} made 4200 DNS queries/hr to unknown domains (baseline: 45/hr)"),
        ("c2_beacon",        "critical", "C2 beacon detected",             "{entity} is beaconing to 185.220.101.47 every 60 seconds (APT41 C2)"),
        ("av_alert",         "medium",   "Antivirus alert",                "AV detected and quarantined: Trojan.ShadowPad on {entity}"),
        ("account_created",  "high",     "Unexpected account creation",    "New local admin account 'supportdesk99' created on {entity}"),
    ]

    # Generate events distributed over the last 24 hours
    for i in range(80):
        offset_minutes = random.randint(0, hours * 60)
        ts = (now - timedelta(minutes=offset_minutes)).isoformat()
        entity = random.choice(entities)
        template = random.choice(event_templates)

        src_ip = f"10.{random.randint(1,3)}.{random.randint(1,50)}.{random.randint(1,254)}"
        dst_ip = f"10.{random.randint(2,100)}.{random.randint(1,50)}.{random.randint(1,254)}"

        desc = template[3].format(entity=entity["name"], ip=src_ip)

        sev_map = {"low": Severity.LOW, "medium": Severity.MEDIUM, "high": Severity.HIGH, "critical": Severity.CRITICAL}

        events.append(TimelineEvent(
            id=f"evt-{uuid.uuid4().hex[:8]}",
            timestamp=ts,
            event_type=template[0],
            entity_id=entity["id"],
            entity_name=entity["name"],
            severity=sev_map[template[1]],
            description=desc,
            source_ip=src_ip,
            destination_ip=dst_ip,
            process=random.choice(["cmd.exe", "powershell.exe", "explorer.exe", "svchost.exe", "python.exe", None]),
        ))

    events.sort(key=lambda e: e.timestamp, reverse=True)
    return events


def submit_feedback(alert_id: str, feedback_type: str, analyst_notes: Optional[str] = None) -> FeedbackResponse:
    """Process TP/FP analyst feedback and adjust scoring."""
    alerts = simulator.get_alerts()
    alert = next((a for a in alerts if a["id"] == alert_id), None)

    if not alert:
        return FeedbackResponse(success=False, message="Alert not found", alert_id=alert_id)

    if feedback_type == "false_positive":
        new_status = "false_positive"
        score_adjustment = -15.0
        new_score = max(0, alert["score"] + score_adjustment)
        result_msg = f"Marked as false positive. Score adjusted from {alert['score']} to {new_score}. Entity baseline will be updated."
    else:  # true_positive
        new_status = "investigating"
        score_adjustment = 5.0
        new_score = min(100, alert["score"] + score_adjustment)
        result_msg = f"Confirmed true positive. Score reinforced to {new_score}. Playbook recommendation triggered."

    simulator.update_alert_status(alert_id, new_status)
    log_action(
        action=f"Analyst feedback: {feedback_type} for alert {alert_id}",
        actor="soc_analyst",
        target=alert["entity_name"],
        result=result_msg,
        module="BADE"
    )

    return FeedbackResponse(
        success=True,
        message=result_msg,
        alert_id=alert_id,
        new_score=new_score,
    )
