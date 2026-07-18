"""
CyberShield AI — Network Topology for Digital Twin (CRDT Module)
Simulates an AIIMS Delhi / Indian government hybrid network with OT.
30 nodes, 45 edges, 5 pre-built attack scenarios.
"""

# ─────────────────────────────────────────────
# Network Nodes
# ─────────────────────────────────────────────

NODES = [
    # External
    {
        "id": "INTERNET", "label": "Internet", "type": "external",
        "ip": "0.0.0.0/0", "vulnerabilities": [], "controls": [],
        "criticality": 1, "os": None, "department": "External"
    },
    # Perimeter
    {
        "id": "FW-PERIMETER", "label": "Perimeter Firewall", "type": "perimeter",
        "ip": "203.0.113.1", "vulnerabilities": ["CVE-2024-3400"], "controls": ["IPS", "DPI", "GeoIP"],
        "criticality": 9, "os": "PAN-OS 11.1", "department": "IT Infrastructure"
    },
    {
        "id": "DMZ-WEBSERVER", "label": "DMZ Web Server", "type": "server",
        "ip": "203.0.113.10", "vulnerabilities": ["CVE-2021-44228", "CVE-2022-0778"], "controls": ["WAF"],
        "criticality": 6, "os": "Ubuntu 20.04 LTS", "department": "IT Infrastructure"
    },
    {
        "id": "MAIL-GW", "label": "Mail Gateway", "type": "server",
        "ip": "203.0.113.11", "vulnerabilities": ["CVE-2023-23397"], "controls": ["AntiSpam", "TLS"],
        "criticality": 7, "os": "Windows Server 2019", "department": "IT Infrastructure"
    },
    {
        "id": "VPN-GW", "label": "VPN Gateway", "type": "perimeter",
        "ip": "203.0.113.15", "vulnerabilities": ["CVE-2024-21887"], "controls": ["MFA", "IPS"],
        "criticality": 8, "os": "Fortinet FortiOS 7.4", "department": "IT Infrastructure"
    },
    # Core Network
    {
        "id": "CORE-SWITCH", "label": "Core Switch", "type": "network",
        "ip": "10.0.0.1", "vulnerabilities": [], "controls": ["VLAN", "Port-Security"],
        "criticality": 9, "os": "Cisco IOS XE 17.9", "department": "IT Infrastructure"
    },
    {
        "id": "FW-INTERNAL", "label": "Internal Firewall", "type": "perimeter",
        "ip": "10.0.0.2", "vulnerabilities": [], "controls": ["IPS", "AppID", "URL-Filter"],
        "criticality": 9, "os": "PAN-OS 11.1", "department": "IT Infrastructure"
    },
    # HR Workstations
    {
        "id": "WORKSTATION-HR-01", "label": "HR Workstation 01", "type": "workstation",
        "ip": "10.1.10.101", "vulnerabilities": ["CVE-2022-30190", "CVE-2023-36884"], "controls": ["EDR", "AV"],
        "criticality": 4, "os": "Windows 11 22H2", "department": "Human Resources"
    },
    {
        "id": "WORKSTATION-HR-02", "label": "HR Workstation 02", "type": "workstation",
        "ip": "10.1.10.102", "vulnerabilities": ["CVE-2022-30190"], "controls": ["EDR", "AV"],
        "criticality": 3, "os": "Windows 10 21H2", "department": "Human Resources"
    },
    {
        "id": "WORKSTATION-HR-03", "label": "HR Workstation 03", "type": "workstation",
        "ip": "10.1.10.103", "vulnerabilities": ["CVE-2021-34527"], "controls": ["AV"],
        "criticality": 3, "os": "Windows 10 21H2 (EOL)", "department": "Human Resources"
    },
    # Finance Workstations
    {
        "id": "WORKSTATION-FIN-01", "label": "Finance Workstation 01", "type": "workstation",
        "ip": "10.1.20.101", "vulnerabilities": ["CVE-2023-28252"], "controls": ["EDR", "AV", "DLP"],
        "criticality": 7, "os": "Windows 11 23H2", "department": "Finance"
    },
    {
        "id": "WORKSTATION-FIN-02", "label": "Finance Workstation 02", "type": "workstation",
        "ip": "10.1.20.102", "vulnerabilities": [], "controls": ["EDR", "AV", "DLP"],
        "criticality": 7, "os": "Windows 11 23H2", "department": "Finance"
    },
    # Admin Workstations
    {
        "id": "WORKSTATION-ADMIN-01", "label": "Admin Workstation 01", "type": "workstation",
        "ip": "10.1.30.101", "vulnerabilities": [], "controls": ["EDR", "AV", "PAM"],
        "criticality": 8, "os": "Windows 11 23H2", "department": "IT Administration"
    },
    {
        "id": "WORKSTATION-ADMIN-02", "label": "Admin Workstation 02", "type": "workstation",
        "ip": "10.1.30.102", "vulnerabilities": ["CVE-2024-21338"], "controls": ["EDR", "AV"],
        "criticality": 7, "os": "Windows 11 22H2", "department": "IT Administration"
    },
    # File Servers
    {
        "id": "FILE-SERVER-01", "label": "File Server 01 (HR Data)", "type": "server",
        "ip": "10.2.10.11", "vulnerabilities": ["CVE-2020-0796"], "controls": ["AV", "DLP", "Access-Control"],
        "criticality": 7, "os": "Windows Server 2019", "department": "Human Resources"
    },
    {
        "id": "FILE-SERVER-02", "label": "File Server 02 (Clinical)", "type": "server",
        "ip": "10.2.10.12", "vulnerabilities": ["CVE-2021-34527", "CVE-2020-0796"], "controls": ["AV"],
        "criticality": 8, "os": "Windows Server 2016 (EOL Risk)", "department": "Clinical"
    },
    # Domain Controllers
    {
        "id": "DOMAIN-CONTROLLER-01", "label": "Domain Controller Primary", "type": "server",
        "ip": "10.2.20.10", "vulnerabilities": ["CVE-2020-1472"], "controls": ["EDR", "AV", "NDR"],
        "criticality": 10, "os": "Windows Server 2022", "department": "IT Infrastructure"
    },
    {
        "id": "DOMAIN-CONTROLLER-02", "label": "Domain Controller Backup", "type": "server",
        "ip": "10.2.20.11", "vulnerabilities": [], "controls": ["EDR", "AV"],
        "criticality": 9, "os": "Windows Server 2022", "department": "IT Infrastructure"
    },
    # Database Servers
    {
        "id": "AIIMS-EMR-SERVER", "label": "AIIMS EMR Database", "type": "server",
        "ip": "10.2.30.10", "vulnerabilities": ["CVE-2022-21500"], "controls": ["DB-Firewall", "Encryption", "Audit"],
        "criticality": 10, "os": "Oracle Linux 8.8", "department": "Clinical"
    },
    {
        "id": "HIS-SERVER", "label": "Hospital Information System", "type": "server",
        "ip": "10.2.30.11", "vulnerabilities": ["CVE-2023-23504"], "controls": ["Access-Control", "Audit"],
        "criticality": 9, "os": "Red Hat Enterprise Linux 9", "department": "Clinical"
    },
    # Backup Server
    {
        "id": "BACKUP-SERVER", "label": "Backup Server", "type": "server",
        "ip": "10.2.40.10", "vulnerabilities": ["CVE-2023-27532"], "controls": ["AV", "Encryption"],
        "criticality": 8, "os": "Windows Server 2022", "department": "IT Infrastructure"
    },
    # SIEM / Security
    {
        "id": "SIEM-SERVER", "label": "SIEM / Log Aggregator", "type": "server",
        "ip": "10.2.50.10", "vulnerabilities": [], "controls": ["Access-Control", "Encryption", "MFA"],
        "criticality": 9, "os": "Ubuntu 22.04 LTS", "department": "Security"
    },
    # OT Network
    {
        "id": "OT-GATEWAY", "label": "OT/IT Gateway (Data Diode)", "type": "ot",
        "ip": "10.100.0.1", "vulnerabilities": [], "controls": ["DataDiode", "Unidirectional", "IDS"],
        "criticality": 10, "os": "Waterfall FLIP v5.1", "department": "Facilities"
    },
    {
        "id": "SCADA-SERVER", "label": "SCADA Server (HVAC/Power)", "type": "ot",
        "ip": "10.100.1.10", "vulnerabilities": ["CVE-2023-1709"], "controls": ["ICS-IDS", "Air-Gap"],
        "criticality": 10, "os": "Windows Server 2012 R2 (EOL)", "department": "Facilities"
    },
    {
        "id": "PLC-HVAC", "label": "PLC — HVAC Control", "type": "ot",
        "ip": "10.100.2.10", "vulnerabilities": ["CVE-2022-34151"], "controls": ["Physical-Lock"],
        "criticality": 8, "os": "Siemens S7-1500 FW 2.9", "department": "Facilities"
    },
    {
        "id": "PLC-POWER", "label": "PLC — Power Distribution", "type": "ot",
        "ip": "10.100.2.11", "vulnerabilities": [], "controls": ["Physical-Lock", "ICS-IDS"],
        "criticality": 9, "os": "Allen Bradley ControlLogix", "department": "Facilities"
    },
    {
        "id": "PLC-MEDICAL-GAS", "label": "PLC — Medical Gas Control", "type": "ot",
        "ip": "10.100.2.12", "vulnerabilities": ["CVE-2022-34152"], "controls": ["Physical-Lock"],
        "criticality": 10, "os": "Schneider Electric M340", "department": "Facilities"
    },
    # Cloud
    {
        "id": "CLOUD-CONNECTOR", "label": "Cloud Connector (NIC/MeitY)", "type": "cloud",
        "ip": "10.50.0.1", "vulnerabilities": ["CVE-2024-1709"], "controls": ["TLS", "API-Gateway"],
        "criticality": 7, "os": "NIC Cloud Gateway", "department": "IT Infrastructure"
    },
    {
        "id": "MGMT-CONSOLE", "label": "Management Console", "type": "server",
        "ip": "10.2.50.20", "vulnerabilities": [], "controls": ["MFA", "PAM", "IP-Whitelist"],
        "criticality": 9, "os": "Ubuntu 22.04 LTS", "department": "IT Administration"
    },
    {
        "id": "MEDICAL-DEVICES", "label": "Medical Devices Subnet", "type": "ot",
        "ip": "10.150.0.0/24", "vulnerabilities": ["CVE-2022-45459", "CVE-2023-23590"], "controls": ["VLAN"],
        "criticality": 10, "os": "Various (FDA-regulated)", "department": "Clinical"
    },
]

# Build lookup
NODES_BY_ID = {n["id"]: n for n in NODES}

# ─────────────────────────────────────────────
# Network Edges (directed graph)
# ─────────────────────────────────────────────

EDGES = [
    # Internet → Perimeter
    {"source": "INTERNET",           "target": "FW-PERIMETER",        "protocol": "Any",   "port": 0,   "encrypted": False, "firewall_protected": True},
    {"source": "FW-PERIMETER",       "target": "DMZ-WEBSERVER",       "protocol": "HTTPS", "port": 443, "encrypted": True,  "firewall_protected": True},
    {"source": "FW-PERIMETER",       "target": "MAIL-GW",             "protocol": "SMTP",  "port": 25,  "encrypted": True,  "firewall_protected": True},
    {"source": "FW-PERIMETER",       "target": "VPN-GW",              "protocol": "SSL",   "port": 443, "encrypted": True,  "firewall_protected": True},
    # DMZ → Internal
    {"source": "DMZ-WEBSERVER",      "target": "CORE-SWITCH",         "protocol": "HTTP",  "port": 8080,"encrypted": False, "firewall_protected": True},
    {"source": "MAIL-GW",            "target": "CORE-SWITCH",         "protocol": "SMTP",  "port": 25,  "encrypted": True,  "firewall_protected": True},
    {"source": "VPN-GW",             "target": "CORE-SWITCH",         "protocol": "IPSec", "port": 500, "encrypted": True,  "firewall_protected": True},
    # Core switch → Internal firewall → Segments
    {"source": "CORE-SWITCH",        "target": "FW-INTERNAL",         "protocol": "Any",   "port": 0,   "encrypted": False, "firewall_protected": True},
    # HR Segment
    {"source": "FW-INTERNAL",        "target": "WORKSTATION-HR-01",   "protocol": "Any",   "port": 0,   "encrypted": False, "firewall_protected": True},
    {"source": "FW-INTERNAL",        "target": "WORKSTATION-HR-02",   "protocol": "Any",   "port": 0,   "encrypted": False, "firewall_protected": True},
    {"source": "FW-INTERNAL",        "target": "WORKSTATION-HR-03",   "protocol": "Any",   "port": 0,   "encrypted": False, "firewall_protected": True},
    # Finance Segment
    {"source": "FW-INTERNAL",        "target": "WORKSTATION-FIN-01",  "protocol": "Any",   "port": 0,   "encrypted": False, "firewall_protected": True},
    {"source": "FW-INTERNAL",        "target": "WORKSTATION-FIN-02",  "protocol": "Any",   "port": 0,   "encrypted": False, "firewall_protected": True},
    # Admin Segment
    {"source": "FW-INTERNAL",        "target": "WORKSTATION-ADMIN-01","protocol": "Any",   "port": 0,   "encrypted": False, "firewall_protected": True},
    {"source": "FW-INTERNAL",        "target": "WORKSTATION-ADMIN-02","protocol": "Any",   "port": 0,   "encrypted": False, "firewall_protected": True},
    # Workstations → File Servers (SMB)
    {"source": "WORKSTATION-HR-01",  "target": "FILE-SERVER-01",      "protocol": "SMB",   "port": 445, "encrypted": False, "firewall_protected": False},
    {"source": "WORKSTATION-HR-02",  "target": "FILE-SERVER-01",      "protocol": "SMB",   "port": 445, "encrypted": False, "firewall_protected": False},
    {"source": "WORKSTATION-HR-03",  "target": "FILE-SERVER-01",      "protocol": "SMB",   "port": 445, "encrypted": False, "firewall_protected": False},
    {"source": "WORKSTATION-HR-01",  "target": "FILE-SERVER-02",      "protocol": "SMB",   "port": 445, "encrypted": False, "firewall_protected": False},
    # File Servers → Domain Controllers
    {"source": "FILE-SERVER-01",     "target": "DOMAIN-CONTROLLER-01","protocol": "LDAP",  "port": 389, "encrypted": False, "firewall_protected": False},
    {"source": "FILE-SERVER-02",     "target": "DOMAIN-CONTROLLER-01","protocol": "LDAP",  "port": 389, "encrypted": False, "firewall_protected": False},
    # Domain Controllers → Critical Servers
    {"source": "DOMAIN-CONTROLLER-01","target": "DOMAIN-CONTROLLER-02","protocol": "RPC",  "port": 135, "encrypted": False, "firewall_protected": False},
    {"source": "DOMAIN-CONTROLLER-01","target": "AIIMS-EMR-SERVER",   "protocol": "Kerberos","port": 88,"encrypted": True,  "firewall_protected": True},
    {"source": "DOMAIN-CONTROLLER-01","target": "HIS-SERVER",         "protocol": "Kerberos","port": 88,"encrypted": True,  "firewall_protected": True},
    {"source": "DOMAIN-CONTROLLER-01","target": "BACKUP-SERVER",      "protocol": "RPC",   "port": 135, "encrypted": False, "firewall_protected": False},
    # Admin workstations → Domain Controllers (RDP)
    {"source": "WORKSTATION-ADMIN-01","target": "DOMAIN-CONTROLLER-01","protocol": "RDP",  "port": 3389,"encrypted": True,  "firewall_protected": True},
    {"source": "WORKSTATION-ADMIN-01","target": "MGMT-CONSOLE",       "protocol": "SSH",   "port": 22,  "encrypted": True,  "firewall_protected": True},
    # Finance → HIS
    {"source": "WORKSTATION-FIN-01", "target": "HIS-SERVER",          "protocol": "HTTPS", "port": 443, "encrypted": True,  "firewall_protected": True},
    {"source": "WORKSTATION-FIN-02", "target": "AIIMS-EMR-SERVER",    "protocol": "HTTPS", "port": 443, "encrypted": True,  "firewall_protected": True},
    # OT segment
    {"source": "CORE-SWITCH",        "target": "OT-GATEWAY",          "protocol": "Any",   "port": 0,   "encrypted": False, "firewall_protected": True},
    {"source": "OT-GATEWAY",         "target": "SCADA-SERVER",        "protocol": "Modbus","port": 502, "encrypted": False, "firewall_protected": False},
    {"source": "SCADA-SERVER",       "target": "PLC-HVAC",            "protocol": "Modbus","port": 502, "encrypted": False, "firewall_protected": False},
    {"source": "SCADA-SERVER",       "target": "PLC-POWER",           "protocol": "DNP3",  "port": 20000,"encrypted": False,"firewall_protected": False},
    {"source": "SCADA-SERVER",       "target": "PLC-MEDICAL-GAS",     "protocol": "Modbus","port": 502, "encrypted": False, "firewall_protected": False},
    {"source": "SCADA-SERVER",       "target": "MEDICAL-DEVICES",     "protocol": "HL7",   "port": 2575,"encrypted": False, "firewall_protected": False},
    # Cloud connector
    {"source": "CORE-SWITCH",        "target": "CLOUD-CONNECTOR",     "protocol": "HTTPS", "port": 443, "encrypted": True,  "firewall_protected": True},
    {"source": "CLOUD-CONNECTOR",    "target": "AIIMS-EMR-SERVER",    "protocol": "API",   "port": 8443,"encrypted": True,  "firewall_protected": True},
    # SIEM collects from everything
    {"source": "FW-PERIMETER",       "target": "SIEM-SERVER",         "protocol": "Syslog","port": 514, "encrypted": True,  "firewall_protected": True},
    {"source": "DOMAIN-CONTROLLER-01","target": "SIEM-SERVER",        "protocol": "WEF",   "port": 5985,"encrypted": True,  "firewall_protected": True},
    {"source": "SCADA-SERVER",       "target": "SIEM-SERVER",         "protocol": "Syslog","port": 514, "encrypted": True,  "firewall_protected": True},
    # Backup
    {"source": "AIIMS-EMR-SERVER",   "target": "BACKUP-SERVER",       "protocol": "Backup","port": 9000,"encrypted": True,  "firewall_protected": True},
    {"source": "HIS-SERVER",         "target": "BACKUP-SERVER",       "protocol": "Backup","port": 9000,"encrypted": True,  "firewall_protected": True},
    {"source": "FILE-SERVER-01",     "target": "BACKUP-SERVER",       "protocol": "Backup","port": 9000,"encrypted": True,  "firewall_protected": True},
    {"source": "FILE-SERVER-02",     "target": "BACKUP-SERVER",       "protocol": "SMB",   "port": 445, "encrypted": False, "firewall_protected": False},
    # Lateral movement path (unencrypted SMB)
    {"source": "WORKSTATION-HR-01",  "target": "DOMAIN-CONTROLLER-01","protocol": "SMB",   "port": 445, "encrypted": False, "firewall_protected": False},
]

# ─────────────────────────────────────────────
# Pre-Built Attack Scenarios
# ─────────────────────────────────────────────

PRE_BUILT_SCENARIOS = {
    "ransomware": {
        "name": "Ransomware Attack",
        "description": "APT41 deploys ransomware via phishing → lateral movement → encrypt backup server to maximise impact.",
        "entry_point": "DMZ-WEBSERVER",
        "target": "BACKUP-SERVER",
        "ttp_chain": ["T1566.001", "T1059.003", "T1055", "T1021.002", "T1486"],
        "risk_level": "critical",
        "recommended_mitigations": [
            "Patch CVE-2021-44228 on DMZ Web Server",
            "Enable SMB signing on all servers",
            "Isolate backup server network segment",
            "Enforce Privileged Access Workstations for admin tasks",
        ]
    },
    "lateral_movement": {
        "name": "APT Lateral Movement",
        "description": "SideWinder gains foothold via spearphish on HR workstation, moves laterally to Domain Controller.",
        "entry_point": "WORKSTATION-HR-01",
        "target": "DOMAIN-CONTROLLER-01",
        "ttp_chain": ["T1566.001", "T1059.003", "T1021.002", "T1078", "T1547.001"],
        "risk_level": "critical",
        "recommended_mitigations": [
            "Deploy EDR on all workstations",
            "Segment HR VLAN from server VLAN with internal firewall",
            "Enforce SMB signing and disable NTLM",
            "Enable Credential Guard on workstations",
        ]
    },
    "ot_pivot": {
        "name": "OT/ICS Pivot Attack",
        "description": "Attacker pivots from corporate IT through OT gateway to SCADA server, threatening HVAC and medical gas controls.",
        "entry_point": "WORKSTATION-ADMIN-01",
        "target": "SCADA-SERVER",
        "ttp_chain": ["T1133", "T1078", "T1021.001", "T1190", "T1059.003"],
        "risk_level": "critical",
        "recommended_mitigations": [
            "Deploy true unidirectional data diode (enforce hardware, not software)",
            "Network air-gap OT from IT entirely",
            "Upgrade SCADA server from Windows Server 2012 R2",
            "Implement ICS-specific IDS (Claroty/Nozomi)",
        ]
    },
    "supply_chain": {
        "name": "Supply Chain Compromise",
        "description": "Backdoored software update from NIC cloud reaches cloud connector and propagates to EMR database.",
        "entry_point": "CLOUD-CONNECTOR",
        "target": "AIIMS-EMR-SERVER",
        "ttp_chain": ["T1195.002", "T1105", "T1059.003", "T1078", "T1005"],
        "risk_level": "high",
        "recommended_mitigations": [
            "Verify software integrity with code signing certificates",
            "Maintain SBOM and alert on new dependency versions",
            "Segment cloud connector from EMR server with application-layer firewall",
            "Implement zero-trust access to EMR API",
        ]
    },
    "insider_threat": {
        "name": "Insider Data Exfiltration",
        "description": "Malicious finance employee with legitimate access exfiltrates patient financial data from EMR database.",
        "entry_point": "WORKSTATION-FIN-02",
        "target": "AIIMS-EMR-SERVER",
        "ttp_chain": ["T1078", "T1005", "T1560", "T1041"],
        "risk_level": "high",
        "recommended_mitigations": [
            "Implement DLP on all finance workstations",
            "Enable user behaviour analytics (UEBA) for finance segment",
            "Enforce data-level RBAC in EMR — finance staff get billing fields only",
            "Monitor and alert on bulk data queries from any user",
        ]
    },
}
