"""
CyberShield AI — AIRO Service
Playbook orchestration, blast-radius gating, approvals, CERT-In report generation.
"""

import uuid
import time
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any

from utils.simulator import simulator
from utils.audit_log import log_action, get_full_log
from data.playbooks import PLAYBOOKS, PLAYBOOKS_BY_ID
from models import (
    Incident, Playbook, PlaybookStep, PlaybookAction, AuditEntry,
    CertInReport, IncidentStatus, ActionStatus, BlastRadius, Severity
)
import config

# In-memory pending approvals: {action_id: {action details}}
_pending_approvals: Dict[str, Dict] = {}


def get_incidents() -> List[Dict]:
    return simulator.get_incidents()


def get_playbooks() -> List[Dict]:
    return PLAYBOOKS


def execute_action(incident_id: str, action_id: str, actor: str = "system") -> Dict:
    """
    Execute a playbook action with blast-radius gating.
    LOW  → auto-execute
    MEDIUM → execute + notify SOC
    HIGH → queue for human approval
    """
    incident = simulator.get_incident_by_id(incident_id)
    if not incident:
        return {"success": False, "message": f"Incident {incident_id} not found"}

    # Find the action in the incident's playbook
    playbook_id = incident.get("playbook_id")
    if not playbook_id:
        return {"success": False, "message": "No playbook assigned to this incident"}

    playbook = PLAYBOOKS_BY_ID.get(playbook_id)
    if not playbook:
        return {"success": False, "message": f"Playbook {playbook_id} not found"}

    step = next((s for s in playbook["steps"] if s["id"] == action_id), None)
    if not step:
        return {"success": False, "message": f"Action {action_id} not found in playbook"}

    blast_radius = step["blast_radius"]
    action_record = {
        "id": f"act-{uuid.uuid4().hex[:8]}",
        "incident_id": incident_id,
        "playbook_id": playbook_id,
        "action_type": step["action_type"],
        "target": incident.get("affected_entities", ["unknown"])[0],
        "blast_radius": blast_radius,
        "executed_at": None,
        "execution_time_ms": None,
        "result": None,
        "rollback_available": True,
        "approved_by": None,
    }

    if blast_radius == "high":
        # Queue for human approval
        action_record["status"] = "awaiting_approval"
        _pending_approvals[action_record["id"]] = {
            **action_record,
            "step": step,
            "queued_at": datetime.now(timezone.utc).isoformat(),
            "approver_deadline": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(),
        }
        simulator.add_incident_action(incident_id, action_record)
        log_action(
            action=f"HIGH blast-radius action queued: {step['name']}",
            actor=actor,
            target=incident.get("affected_entities", ["unknown"])[0],
            result="AWAITING_APPROVAL — 10-minute approval window open",
            module="AIRO"
        )
        return {
            "success": True,
            "status": "awaiting_approval",
            "action_id": action_record["id"],
            "message": f"HIGH blast-radius action '{step['name']}' queued for human approval. 10-minute window.",
            "blast_radius": blast_radius,
            "approver_deadline": _pending_approvals[action_record["id"]]["approver_deadline"],
        }

    # LOW or MEDIUM — execute immediately
    start_ts = time.monotonic()
    action_record["status"] = "executing"
    action_record["executed_at"] = datetime.now(timezone.utc).isoformat()

    # Simulate execution (real system would call SOAR API)
    result_text = _simulate_action_result(step["action_type"], action_record["target"])
    exec_ms = int((time.monotonic() - start_ts) * 1000) + 400  # add 400ms for API latency

    action_record["status"] = "completed"
    action_record["execution_time_ms"] = exec_ms
    action_record["result"] = result_text

    simulator.add_incident_action(incident_id, action_record)
    simulator.increment_containments()

    log_action(
        action=f"Action executed: {step['name']}",
        actor=actor,
        target=action_record["target"],
        result=f"COMPLETED in {exec_ms}ms — {result_text}",
        module="AIRO"
    )

    return {
        "success": True,
        "status": "completed",
        "action_id": action_record["id"],
        "execution_time_ms": exec_ms,
        "result": result_text,
        "blast_radius": blast_radius,
        "rollback_available": True,
        "message": f"Action '{step['name']}' executed successfully in {exec_ms}ms.",
    }


def approve_action(action_id: str, approver: str, decision: str, notes: str = "") -> Dict:
    """Approve or reject a HIGH blast-radius action."""
    pending = _pending_approvals.get(action_id)
    if not pending:
        return {"success": False, "message": f"No pending approval found for action {action_id}"}

    incident_id = pending["incident_id"]

    if decision == "reject":
        simulator.update_action_status(incident_id, action_id, "rejected", "Action rejected by approver.")
        del _pending_approvals[action_id]
        log_action(
            action=f"HIGH blast-radius action REJECTED by {approver}",
            actor=approver,
            target=pending.get("target", "unknown"),
            result=f"REJECTED — Notes: {notes or 'No reason provided'}",
            module="AIRO"
        )
        return {"success": True, "status": "rejected", "message": f"Action {action_id} rejected by {approver}."}

    # Approved — execute
    step = pending["step"]
    start_ts = time.monotonic()
    result_text = _simulate_action_result(step["action_type"], pending.get("target", "unknown"))
    exec_ms = int((time.monotonic() - start_ts) * 1000) + 800

    simulator.update_action_status(
        incident_id, action_id, "completed",
        f"APPROVED by {approver} — {result_text}"
    )
    simulator.increment_containments()
    del _pending_approvals[action_id]

    log_action(
        action=f"HIGH blast-radius action APPROVED and EXECUTED: {step['name']}",
        actor=approver,
        target=pending.get("target", "unknown"),
        result=f"COMPLETED in {exec_ms}ms — {result_text}",
        module="AIRO"
    )

    return {
        "success": True,
        "status": "completed",
        "action_id": action_id,
        "approved_by": approver,
        "execution_time_ms": exec_ms,
        "result": result_text,
        "message": f"Action approved by {approver} and executed in {exec_ms}ms.",
    }


def get_audit_log_entries(limit: int = 100, offset: int = 0) -> List[AuditEntry]:
    return get_full_log(limit=limit, offset=offset)


def generate_cert_in_report(incident_id: str) -> CertInReport:
    """Generate mandatory CERT-In format incident report."""
    incident = simulator.get_incident_by_id(incident_id)
    if not incident:
        # Generate a generic report
        incident = {"id": incident_id, "title": "Security Incident", "severity": "high",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "affected_entities": ["Unknown"], "ttps": [], "actions_taken": []}

    now = datetime.now(timezone.utc)
    report_deadline = (now + timedelta(hours=config.CERT_IN_REPORTING_HOURS)).isoformat()

    actions_taken = [
        f"Step {i+1}: {a.get('action_type', 'Unknown')} on {a.get('target', 'Unknown')} — {a.get('status', 'unknown')}"
        for i, a in enumerate(incident.get("actions_taken", []))
    ]

    # Map TTPs to attack vector description
    ttps = incident.get("ttps", [])
    attack_vector = "Spearphishing (T1566.001) → Lateral Movement (T1021.002) → Credential Theft (T1078)"
    if "T1486" in ttps:
        attack_vector += " → Ransomware Deployment (T1486)"

    return CertInReport(
        report_id=f"CERT-IN-{incident_id.upper()}-{now.strftime('%Y%m%d')}",
        generated_at=now.isoformat(),
        organization_name=config.CERT_IN_ORGANIZATION,
        nic_contact=config.CERT_IN_CONTACT_EMAIL,
        incident_type="Advanced Persistent Threat (APT) — Lateral Movement",
        affected_systems=incident.get("affected_entities", []),
        date_time_discovered=incident.get("created_at", now.isoformat()),
        date_time_reported=now.isoformat(),
        attack_vector=attack_vector,
        impact_description=(
            f"Unauthorized access to internal systems via compromised user credentials. "
            f"Attacker achieved lateral movement across {len(incident.get('affected_entities', []))} systems. "
            f"Severity: {incident.get('severity', 'high').upper()}. "
            f"Attribution: {incident.get('attribution', 'Unknown')}."
        ),
        initial_response_actions=actions_taken or ["No automated actions taken yet. Manual investigation in progress."],
        requested_assistance=(
            "Request CERT-In technical assistance for forensic analysis. "
            "Please share threat intelligence on APT41 India-targeting campaigns."
        ),
        mandatory_fields_complete=True,
        reporting_deadline=report_deadline,
    )


def _simulate_action_result(action_type: str, target: str) -> str:
    """Simulate realistic action results from SOAR integrations."""
    results = {
        "firewall_block_ip":      f"IP {target} blocked at perimeter firewall. ACL rule DENY-{uuid.uuid4().hex[:4].upper()} applied. Traffic dropped.",
        "firewall_block_egress":  f"Egress rule applied. All outbound traffic from {target} to external IPs blocked. 0 packets will pass.",
        "endpoint_isolate":       f"{target} moved to quarantine VLAN (VLAN-999). Network access suspended. Management plane retained for forensics.",
        "vm_snapshot":            f"Immutable snapshot of {target} created: snap-{uuid.uuid4().hex[:8]}. Stored in evidence vault S3 bucket.",
        "revoke_sessions":        f"All active sessions for {target} terminated. SSO tokens, VPN sessions, and cloud app sessions revoked.",
        "force_password_reset":   f"Password reset triggered for {target}. User notified via backup contact. Temporary token issued to IT helpdesk.",
        "disable_ad_account":     f"AD account {target} disabled in Active Directory. Account GUID logged. Cannot authenticate until re-enabled.",
        "revoke_mfa":             f"MFA enrollment revoked for {target}. User must re-enroll at next login. Backup codes invalidated.",
        "enable_packet_capture":  f"Full packet capture enabled on interface connected to {target}. Storing to evidence vault (10GB limit).",
        "edr_scan_segment":       f"EDR scan triggered on all 23 endpoints in segment containing {target}. Estimated completion: 4 minutes.",
        "notify_dpo_cert_in":     f"CERT-In preliminary report submitted. DPO notified via secure channel. Report ID: CERT-IN-{uuid.uuid4().hex[:6].upper()}",
        "legal_hold_evidence":    f"Legal hold applied to all logs for {target}. Evidence transferred to WORM S3 bucket. Chain of custody preserved.",
        "quarantine_email":       f"Phishing email quarantined from 847 mailboxes. Subject: 'Urgent: Salary Revision'. Sender domain blocked.",
        "block_email_domain":     f"Sender domain blocked at email gateway. 0 emails will be delivered from this domain.",
        "block_url_proxy":        f"Phishing URL added to web proxy block list. 2,341 devices protected.",
        "notify_exposed_users":   f"Security alert sent to 847 users who received the phishing email. 2 users already clicked — marked for credential reset.",
        "reset_clicked_user_credentials": f"Credentials reset for {target}. Sessions revoked. Enrolled in mandatory security awareness training.",
        "revoke_privileges":      f"Elevated privileges revoked for {target}. Removed from Domain Admins. Group membership changes logged.",
        "kill_processes":         f"Suspicious processes terminated on {target}: cmd.exe (PID 4821), powershell.exe (PID 3942).",
        "audit_privilege_changes":f"72-hour privilege change audit completed. 3 unexpected changes found. Report in evidence vault.",
        "hunt_persistence":       f"Persistence hunt completed on {target}. 1 malicious scheduled task found and removed: WindowsUpdateHelper.",
        "reset_privileged_credentials": f"Credentials reset for 12 privileged accounts. Service account passwords rotated. DC replication triggered.",
        "firewall_block_ip":      f"Block rule applied. {target} unreachable.",
        "asset_software_query":   f"Query complete. 127 systems running affected software version found. Report generated.",
        "rollback_deployment":    f"Deployment rolled back to v2.1.4 (last known good) across 127 systems. Zero downtime achieved.",
        "audit_dependencies":     f"Dependency audit complete. 3 transitive dependencies flagged. SBOM updated.",
        "notify_cert_in":         f"CERT-In notified. Report ID: CERT-IN-{uuid.uuid4().hex[:6].upper()}. 6-hour deadline: Met.",
        "activate_ot_airgap":     f"OT/IT air gap activated. Waterfall FLIP data diode in blocking mode. All OT traffic halted.",
        "alert_facility_manager": f"Facility manager notified via pager and phone. On-site response team alerted.",
        "switch_to_manual_control":f"HVAC/Power control switched to manual mode. Operators have direct physical control.",
        "preserve_ot_evidence":   f"OT historian data captured. Network traffic archived. Chain of custody document generated.",
        "legal_hold_evidence":    f"Legal hold applied. Evidence immutably stored in WORM bucket.",
    }
    return results.get(action_type, f"Action {action_type} executed on {target}. Operation completed successfully.")
