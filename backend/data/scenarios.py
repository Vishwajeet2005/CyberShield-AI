"""
CyberShield AI — Demo Scenarios & Seed Data
Alert templates, entity profiles, and the active incident for demo.
"""

from datetime import datetime, timezone, timedelta
import uuid

def _ts(minutes_ago: int = 0) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat()

# ─────────────────────────────────────────────
# Entity Profiles (25 entities for BADE)
# ─────────────────────────────────────────────

ENTITY_PROFILES = [
    # HR Users
    {"id": "USR-HR-001", "name": "rajesh.kumar",    "type": "user",        "ip_address": "10.1.10.101", "os": "Windows 11", "department": "Human Resources", "baseline_score": 15.0},
    {"id": "USR-HR-002", "name": "priya.sharma",    "type": "user",        "ip_address": "10.1.10.102", "os": "Windows 11", "department": "Human Resources", "baseline_score": 12.0},
    {"id": "USR-HR-003", "name": "amit.verma",      "type": "user",        "ip_address": "10.1.10.103", "os": "Windows 10", "department": "Human Resources", "baseline_score": 18.0},
    # Finance Users
    {"id": "USR-FIN-001", "name": "deepika.nair",   "type": "user",        "ip_address": "10.1.20.101", "os": "Windows 11", "department": "Finance",         "baseline_score": 14.0},
    {"id": "USR-FIN-002", "name": "rohit.agarwal",  "type": "user",        "ip_address": "10.1.20.102", "os": "Windows 11", "department": "Finance",         "baseline_score": 16.0},
    # Admin Users
    {"id": "USR-ADM-001", "name": "sanjay.mishra",  "type": "user",        "ip_address": "10.1.30.101", "os": "Windows 11", "department": "IT Admin",        "baseline_score": 22.0},
    {"id": "USR-ADM-002", "name": "kavita.singh",   "type": "user",        "ip_address": "10.1.30.102", "os": "Windows 11", "department": "IT Admin",        "baseline_score": 24.0},
    # Clinical Users
    {"id": "USR-CLI-001", "name": "dr.anand.patel", "type": "user",        "ip_address": "10.1.40.101", "os": "Windows 11", "department": "Clinical",        "baseline_score": 11.0},
    {"id": "USR-CLI-002", "name": "nurse.meera",    "type": "user",        "ip_address": "10.1.40.102", "os": "Windows 10", "department": "Clinical",        "baseline_score": 9.0},
    # Servers
    {"id": "SRV-DC-001",  "name": "DOMAIN-CONTROLLER-01", "type": "server","ip_address": "10.2.20.10", "os": "Windows Server 2022", "department": "IT Infrastructure", "baseline_score": 8.0},
    {"id": "SRV-DC-002",  "name": "DOMAIN-CONTROLLER-02", "type": "server","ip_address": "10.2.20.11", "os": "Windows Server 2022", "department": "IT Infrastructure", "baseline_score": 7.5},
    {"id": "SRV-FS-001",  "name": "FILE-SERVER-01",  "type": "server",     "ip_address": "10.2.10.11", "os": "Windows Server 2019", "department": "IT Infrastructure", "baseline_score": 10.0},
    {"id": "SRV-FS-002",  "name": "FILE-SERVER-02",  "type": "server",     "ip_address": "10.2.10.12", "os": "Windows Server 2016", "department": "IT Infrastructure", "baseline_score": 11.0},
    {"id": "SRV-EMR-001", "name": "AIIMS-EMR-SERVER","type": "server",     "ip_address": "10.2.30.10", "os": "Oracle Linux 8.8",   "department": "Clinical",          "baseline_score": 5.0},
    {"id": "SRV-HIS-001", "name": "HIS-SERVER",      "type": "server",     "ip_address": "10.2.30.11", "os": "RHEL 9",             "department": "Clinical",          "baseline_score": 5.5},
    {"id": "SRV-BAK-001", "name": "BACKUP-SERVER",   "type": "server",     "ip_address": "10.2.40.10", "os": "Windows Server 2022","department": "IT Infrastructure", "baseline_score": 6.0},
    {"id": "SRV-SIEM-001","name": "SIEM-SERVER",     "type": "server",     "ip_address": "10.2.50.10", "os": "Ubuntu 22.04",       "department": "Security",          "baseline_score": 4.0},
    # Service Accounts
    {"id": "SA-BACKUP",   "name": "svc_backup",     "type": "service_account","ip_address": "10.2.40.10","os": "Windows", "department": "IT Infrastructure", "baseline_score": 3.0},
    {"id": "SA-AV",       "name": "svc_antivirus",  "type": "service_account","ip_address": "10.2.50.10","os": "Windows", "department": "Security",          "baseline_score": 2.0},
    {"id": "SA-DEPLOY",   "name": "svc_deploy",     "type": "service_account","ip_address": "10.2.50.20","os": "Ubuntu",  "department": "IT Operations",     "baseline_score": 4.0},
    # OT Devices
    {"id": "OT-SCADA",    "name": "SCADA-SERVER",   "type": "ot_device",   "ip_address": "10.100.1.10","os": "Win Server 2012R2","department": "Facilities",   "baseline_score": 2.0},
    {"id": "OT-PLC-HVAC", "name": "PLC-HVAC",       "type": "ot_device",   "ip_address": "10.100.2.10","os": "Siemens S7",      "department": "Facilities",   "baseline_score": 1.5},
    {"id": "OT-PLC-PWR",  "name": "PLC-POWER",      "type": "ot_device",   "ip_address": "10.100.2.11","os": "Allen Bradley",   "department": "Facilities",   "baseline_score": 1.5},
    # Network Devices
    {"id": "NET-FW-01",   "name": "FW-PERIMETER",   "type": "network_device","ip_address": "203.0.113.1","os": "PAN-OS 11.1",   "department": "IT Infrastructure","baseline_score": 3.0},
    {"id": "NET-FW-02",   "name": "FW-INTERNAL",    "type": "network_device","ip_address": "10.0.0.2",   "os": "PAN-OS 11.1",  "department": "IT Infrastructure","baseline_score": 3.0},
]

# ─────────────────────────────────────────────
# Alert Templates (20 templates)
# ─────────────────────────────────────────────

ALERT_TEMPLATES = [
    {
        "severity": "critical", "entity_type": "user", "module": "BADE",
        "description": "Anomalous PowerShell execution detected: encoded command with AMSI bypass attempt. Score deviation +68 from 30-day baseline.",
        "ttps": ["T1059.001", "T1027"], "mitre_tactics": ["Execution", "Defense Evasion"]
    },
    {
        "severity": "critical", "entity_type": "user", "module": "BADE",
        "description": "Lateral movement detected: SMB authentication to 4 new hosts in 90 seconds. Atypical for this user's 30-day baseline.",
        "ttps": ["T1021.002", "T1078"], "mitre_tactics": ["Lateral Movement"]
    },
    {
        "severity": "high", "entity_type": "server", "module": "BADE",
        "description": "Unusual process creation burst: 127 processes in 60 seconds (baseline: 8±2). Possible malware execution.",
        "ttps": ["T1059.003", "T1055"], "mitre_tactics": ["Execution", "Defense Evasion"]
    },
    {
        "severity": "high", "entity_type": "user", "module": "BADE",
        "description": "Off-hours login detected at 02:34 IST from new IP 45.142.212.100 (GeoIP: Netherlands). User baseline: 09:00-19:00 IST, India only.",
        "ttps": ["T1078", "T1133"], "mitre_tactics": ["Defense Evasion", "Initial Access"]
    },
    {
        "severity": "critical", "entity_type": "server", "module": "BADE",
        "description": "Mass file extension change detected: 2,847 files modified in 3 minutes with .lockbit extension. Ransomware activity confirmed.",
        "ttps": ["T1486"], "mitre_tactics": ["Impact"]
    },
    {
        "severity": "high", "entity_type": "user", "module": "BADE",
        "description": "Credential dumping attempt: LSASS memory access by non-security process (python.exe). MITRE T1003.001 indicator.",
        "ttps": ["T1003.001", "T1055"], "mitre_tactics": ["Credential Access"]
    },
    {
        "severity": "medium", "entity_type": "server", "module": "BADE",
        "description": "Anomalous DNS query volume: 4,200 queries/hour to new external domains (baseline: 45±10/hour). Possible DNS tunnelling.",
        "ttps": ["T1071.004", "T1041"], "mitre_tactics": ["Command and Control", "Exfiltration"]
    },
    {
        "severity": "high", "entity_type": "server", "module": "BADE",
        "description": "Scheduled task created by non-admin account: 'WindowsUpdateHelper' running encoded PowerShell every 15 minutes.",
        "ttps": ["T1053.005", "T1059.001"], "mitre_tactics": ["Persistence", "Execution"]
    },
    {
        "severity": "medium", "entity_type": "user", "module": "BADE",
        "description": "Anomalous outbound data volume: 4.7GB transferred to cloud storage in 2 hours (baseline: 0.2GB/day). Possible exfiltration.",
        "ttps": ["T1041", "T1005"], "mitre_tactics": ["Exfiltration", "Collection"]
    },
    {
        "severity": "high", "entity_type": "service_account", "module": "BADE",
        "description": "Service account used interactively: svc_backup logged into HR workstation. Service accounts should never log in interactively.",
        "ttps": ["T1078", "T1021.001"], "mitre_tactics": ["Defense Evasion", "Lateral Movement"]
    },
    {
        "severity": "critical", "entity_type": "ot_device", "module": "BADE",
        "description": "OT anomaly: Modbus write command to HVAC setpoint register outside safe range (received: 95°C, safe: 20-28°C). Possible sabotage.",
        "ttps": ["T0855"], "mitre_tactics": ["Impair Process Control"]
    },
    {
        "severity": "medium", "entity_type": "server", "module": "BADE",
        "description": "Network port scan detected from internal host: 8,432 ports probed in 60 seconds. Possible reconnaissance.",
        "ttps": ["T1046", "T1018"], "mitre_tactics": ["Discovery"]
    },
    {
        "severity": "high", "entity_type": "user", "module": "BADE",
        "description": "Registry Run key added by user process: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\svchost32 → suspicious path.",
        "ttps": ["T1547.001"], "mitre_tactics": ["Persistence"]
    },
    {
        "severity": "medium", "entity_type": "server", "module": "AAPA",
        "description": "TTP sequence matches APT41 campaign pattern with 91% confidence. Observed: Initial Access → Execution → Defense Evasion → Lateral Movement.",
        "ttps": ["T1566.001", "T1059.003", "T1055", "T1021.002"], "mitre_tactics": ["Multiple"]
    },
    {
        "severity": "high", "entity_type": "network_device", "module": "BADE",
        "description": "Firewall configuration change detected outside change window: New allow rule for port 4444 inbound added by unknown process.",
        "ttps": ["T1562.004"], "mitre_tactics": ["Defense Evasion"]
    },
    {
        "severity": "low", "entity_type": "user", "module": "BADE",
        "description": "Anomalous login time: 47 minutes earlier than 30-day average (07:13 vs 07:59 baseline). Low priority — monitoring.",
        "ttps": [], "mitre_tactics": []
    },
    {
        "severity": "high", "entity_type": "server", "module": "BADE",
        "description": "WMI subscription created: EventFilter + EventConsumer pair targeting logon events. Classic WMI persistence mechanism.",
        "ttps": ["T1546.003"], "mitre_tactics": ["Persistence", "Privilege Escalation"]
    },
    {
        "severity": "critical", "entity_type": "server", "module": "BADE",
        "description": "Domain Controller: New admin account 'supportdesk99' created outside HR process at 03:47 IST. Not present in AD approved list.",
        "ttps": ["T1136.002", "T1098"], "mitre_tactics": ["Persistence"]
    },
    {
        "severity": "medium", "entity_type": "user", "module": "BADE",
        "description": "Privilege escalation: User added themselves to local Administrators group using net.exe. Windows Event 4732 triggered.",
        "ttps": ["T1078.003", "T1098"], "mitre_tactics": ["Privilege Escalation"]
    },
    {
        "severity": "high", "entity_type": "server", "module": "BADE",
        "description": "Outbound C2 beacon detected: Regular 60-second interval HTTPS callbacks to 185.220.101.47 (known APT41 C2 infrastructure).",
        "ttps": ["T1071.001", "T1041"], "mitre_tactics": ["Command and Control"]
    },
]

# ─────────────────────────────────────────────
# Active Demo Incident
# ─────────────────────────────────────────────

CURRENT_INCIDENT = {
    "id": "incident-001",
    "title": "APT41 Lateral Movement Detected — AIIMS Delhi Network",
    "severity": "critical",
    "status": "investigating",
    "created_at": _ts(minutes_ago=118),
    "updated_at": _ts(minutes_ago=2),
    "affected_entities": ["WORKSTATION-HR-01", "FILE-SERVER-02", "DOMAIN-CONTROLLER-01"],
    "ttps": ["T1566.001", "T1059.003", "T1055", "T1021.002", "T1070.004"],
    "playbook_id": "PB-002",
    "blast_radius": "medium",
    "attribution": "APT41 (confidence: 91%)",
    "cert_in_reported": False,
    "mttd_minutes": 47.0,
    "actions_taken": [
        {
            "id": "act-001", "incident_id": "incident-001", "playbook_id": "PB-002",
            "action_type": "firewall_block_ip", "target": "185.220.101.47",
            "status": "completed", "blast_radius": "low",
            "executed_at": _ts(minutes_ago=68),
            "execution_time_ms": 847, "result": "IP 185.220.101.47 blocked at perimeter firewall. Rule ID: ACL-DENY-4821",
            "rollback_available": True, "approved_by": None
        },
        {
            "id": "act-002", "incident_id": "incident-001", "playbook_id": "PB-002",
            "action_type": "endpoint_isolate", "target": "WORKSTATION-HR-01",
            "status": "completed", "blast_radius": "low",
            "executed_at": _ts(minutes_ago=67),
            "execution_time_ms": 1243, "result": "WORKSTATION-HR-01 moved to quarantine VLAN (VLAN-999). User session preserved for forensics.",
            "rollback_available": True, "approved_by": None
        },
        {
            "id": "act-003", "incident_id": "incident-001", "playbook_id": "PB-002",
            "action_type": "revoke_sessions", "target": "rajesh.kumar@aiims.edu",
            "status": "completed", "blast_radius": "low",
            "executed_at": _ts(minutes_ago=66),
            "execution_time_ms": 512, "result": "All active sessions revoked for rajesh.kumar. 3 SSO tokens, 1 VPN session, 2 cloud app sessions terminated.",
            "rollback_available": False, "approved_by": None
        },
        {
            "id": "act-004", "incident_id": "incident-001", "playbook_id": "PB-002",
            "action_type": "force_password_reset", "target": "rajesh.kumar@aiims.edu",
            "status": "completed", "blast_radius": "medium",
            "executed_at": _ts(minutes_ago=60),
            "execution_time_ms": 2100, "result": "Password reset triggered. User notified via backup email. Temporary password issued to IT helpdesk.",
            "rollback_available": False, "approved_by": None
        },
        {
            "id": "act-005", "incident_id": "incident-001", "playbook_id": "PB-002",
            "action_type": "disable_ad_account", "target": "rajesh.kumar@aiims.edu",
            "status": "awaiting_approval", "blast_radius": "high",
            "executed_at": None,
            "execution_time_ms": None, "result": None,
            "rollback_available": True, "approved_by": None
        },
    ]
}

SECOND_INCIDENT = {
    "id": "incident-002",
    "title": "Anomalous Data Exfiltration — Finance Workstation FIN-02",
    "severity": "high",
    "status": "open",
    "created_at": _ts(minutes_ago=23),
    "updated_at": _ts(minutes_ago=5),
    "affected_entities": ["WORKSTATION-FIN-02"],
    "ttps": ["T1005", "T1041"],
    "playbook_id": None,
    "blast_radius": "low",
    "attribution": None,
    "cert_in_reported": False,
    "mttd_minutes": 18.0,
    "actions_taken": []
}
