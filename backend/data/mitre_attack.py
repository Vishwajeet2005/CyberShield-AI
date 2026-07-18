"""
CyberShield AI — Embedded MITRE ATT&CK Data
Threat actor profiles + technique definitions for AAPA module.
APT groups known to target India's Critical National Infrastructure.
"""

# ─────────────────────────────────────────────
# MITRE ATT&CK Technique Definitions
# ─────────────────────────────────────────────

ATTACK_TECHNIQUES = {
    "T1566.001": {
        "id": "T1566.001", "name": "Spearphishing Attachment",
        "tactic": "Initial Access",
        "description": "Adversaries send spearphishing emails with malicious attachments to gain initial access."
    },
    "T1566.002": {
        "id": "T1566.002", "name": "Spearphishing Link",
        "tactic": "Initial Access",
        "description": "Emails with malicious links to credential harvesting or drive-by download sites."
    },
    "T1059.001": {
        "id": "T1059.001", "name": "PowerShell",
        "tactic": "Execution",
        "description": "Adversaries abuse PowerShell commands and scripts for execution."
    },
    "T1059.003": {
        "id": "T1059.003", "name": "Windows Command Shell",
        "tactic": "Execution",
        "description": "Adversaries abuse the Windows command shell (cmd.exe) for execution."
    },
    "T1059.005": {
        "id": "T1059.005", "name": "Visual Basic",
        "tactic": "Execution",
        "description": "VBScript execution via phishing or malicious documents."
    },
    "T1055": {
        "id": "T1055", "name": "Process Injection",
        "tactic": "Defense Evasion",
        "description": "Adversaries inject code into processes to evade process-based defenses."
    },
    "T1070.004": {
        "id": "T1070.004", "name": "File Deletion",
        "tactic": "Defense Evasion",
        "description": "Adversaries delete files to conceal malicious activity."
    },
    "T1070.003": {
        "id": "T1070.003", "name": "Clear Command History",
        "tactic": "Defense Evasion",
        "description": "Clear command history to remove indicators of activity."
    },
    "T1021.002": {
        "id": "T1021.002", "name": "SMB/Windows Admin Shares",
        "tactic": "Lateral Movement",
        "description": "Adversaries use SMB and Windows admin shares to move laterally."
    },
    "T1021.001": {
        "id": "T1021.001", "name": "Remote Desktop Protocol",
        "tactic": "Lateral Movement",
        "description": "Adversaries use RDP for lateral movement."
    },
    "T1486": {
        "id": "T1486", "name": "Data Encrypted for Impact",
        "tactic": "Impact",
        "description": "Adversaries encrypt data on target systems to interrupt availability (ransomware)."
    },
    "T1041": {
        "id": "T1041", "name": "Exfiltration Over C2 Channel",
        "tactic": "Exfiltration",
        "description": "Adversaries steal data by exfiltrating it over an existing command and control channel."
    },
    "T1078": {
        "id": "T1078", "name": "Valid Accounts",
        "tactic": "Defense Evasion",
        "description": "Adversaries obtain and abuse credentials of existing accounts to maintain access."
    },
    "T1547.001": {
        "id": "T1547.001", "name": "Registry Run Keys / Startup Folder",
        "tactic": "Persistence",
        "description": "Adversaries add programs to startup keys in the Registry or startup folder."
    },
    "T1053.005": {
        "id": "T1053.005", "name": "Scheduled Task",
        "tactic": "Persistence",
        "description": "Adversaries abuse the Windows task scheduler to execute malicious code."
    },
    "T1053.002": {
        "id": "T1053.002", "name": "At",
        "tactic": "Persistence",
        "description": "Adversaries use the at utility to schedule malicious tasks."
    },
    "T1083": {
        "id": "T1083", "name": "File and Directory Discovery",
        "tactic": "Discovery",
        "description": "Adversaries enumerate files and directories to locate valuable data."
    },
    "T1005": {
        "id": "T1005", "name": "Data from Local System",
        "tactic": "Collection",
        "description": "Adversaries search for and collect data from the local system prior to exfiltration."
    },
    "T1027": {
        "id": "T1027", "name": "Obfuscated Files or Information",
        "tactic": "Defense Evasion",
        "description": "Adversaries obfuscate files or information to avoid detection."
    },
    "T1497": {
        "id": "T1497", "name": "Virtualization/Sandbox Evasion",
        "tactic": "Defense Evasion",
        "description": "Adversaries employ various means to detect and avoid virtualization and analysis environments."
    },
    "T1204.002": {
        "id": "T1204.002", "name": "Malicious File",
        "tactic": "Execution",
        "description": "Adversaries rely on a user opening a malicious file for execution."
    },
    "T1204.001": {
        "id": "T1204.001", "name": "Malicious Link",
        "tactic": "Execution",
        "description": "Adversaries rely on a user clicking a malicious link for execution."
    },
    "T1082": {
        "id": "T1082", "name": "System Information Discovery",
        "tactic": "Discovery",
        "description": "Adversaries gather detailed information about the operating system and hardware."
    },
    "T1016": {
        "id": "T1016", "name": "System Network Configuration Discovery",
        "tactic": "Discovery",
        "description": "Adversaries look for details about the network configuration and settings."
    },
    "T1071.001": {
        "id": "T1071.001", "name": "Web Protocols",
        "tactic": "Command and Control",
        "description": "Adversaries use standard web protocols (HTTP/HTTPS) for C2 communications."
    },
    "T1105": {
        "id": "T1105", "name": "Ingress Tool Transfer",
        "tactic": "Command and Control",
        "description": "Adversaries transfer tools or files from external systems into compromised environments."
    },
    "T1036.005": {
        "id": "T1036.005", "name": "Match Legitimate Name or Location",
        "tactic": "Defense Evasion",
        "description": "Adversaries masquerade malicious files as legitimate ones."
    },
    "T1036": {
        "id": "T1036", "name": "Masquerading",
        "tactic": "Defense Evasion",
        "description": "Adversaries rename or manipulate artifacts to match legitimate ones."
    },
    "T1547": {
        "id": "T1547", "name": "Boot or Logon Autostart Execution",
        "tactic": "Persistence",
        "description": "Adversaries configure system settings to automatically execute a program during system boot or logon."
    },
    "T1070": {
        "id": "T1070", "name": "Indicator Removal",
        "tactic": "Defense Evasion",
        "description": "Adversaries delete or alter artifacts to remove evidence of their presence."
    },
    "T1003": {
        "id": "T1003", "name": "OS Credential Dumping",
        "tactic": "Credential Access",
        "description": "Adversaries attempt to dump credentials to obtain account login information."
    },
    "T1110": {
        "id": "T1110", "name": "Brute Force",
        "tactic": "Credential Access",
        "description": "Adversaries may use brute force techniques to gain access to accounts."
    },
    "T1190": {
        "id": "T1190", "name": "Exploit Public-Facing Application",
        "tactic": "Initial Access",
        "description": "Adversaries exploit weakness in an Internet-facing computer or program."
    },
    "T1133": {
        "id": "T1133", "name": "External Remote Services",
        "tactic": "Initial Access",
        "description": "Adversaries leverage external remote services like VPNs to gain access."
    },
    "T1098": {
        "id": "T1098", "name": "Account Manipulation",
        "tactic": "Persistence",
        "description": "Adversaries manipulate accounts to maintain access."
    },
    "T1560": {
        "id": "T1560", "name": "Archive Collected Data",
        "tactic": "Collection",
        "description": "Adversaries may compress or encrypt data before exfiltration."
    },
    "T1071": {
        "id": "T1071", "name": "Application Layer Protocol",
        "tactic": "Command and Control",
        "description": "Adversaries communicate using application layer protocols to blend in with normal traffic."
    },
    "T1046": {
        "id": "T1046", "name": "Network Service Discovery",
        "tactic": "Discovery",
        "description": "Adversaries scan target networks to identify active services."
    },
    "T1018": {
        "id": "T1018", "name": "Remote System Discovery",
        "tactic": "Discovery",
        "description": "Adversaries enumerate remote systems on the network."
    },
    "T1074": {
        "id": "T1074", "name": "Data Staged",
        "tactic": "Collection",
        "description": "Adversaries collect and stage data to prepare for exfiltration."
    },
}


# ─────────────────────────────────────────────
# Threat Actor Profiles — India-Targeting APTs
# ─────────────────────────────────────────────

THREAT_ACTORS = [
    {
        "id": "apt41",
        "name": "APT41",
        "aliases": ["Double Dragon", "Winnti Group", "BARIUM", "Wicked Panda"],
        "origin": "China",
        "motivation": "Espionage + Financial gain",
        "targets": ["Healthcare", "Telecom", "Finance", "Government", "Defence"],
        "ttps": [
            "T1566.001", "T1059.003", "T1055", "T1070.004",
            "T1021.002", "T1486", "T1041", "T1078", "T1547.001", "T1053.005"
        ],
        "campaigns": [
            "Operation CuckooBees (2022)",
            "Cobalt Strike Campaign India (2023)",
            "ShadowPad India Healthcare (2024)"
        ],
        "last_seen": "2026-06-15",
        "description": (
            "APT41 is a China-nexus threat group known for both state-sponsored espionage and "
            "financially motivated cybercrime. It has repeatedly targeted Indian healthcare institutions, "
            "including AIIMS Delhi, and financial sector entities. APT41 uses ShadowPad malware and "
            "Cobalt Strike beacons delivered via spearphishing and supply chain compromise."
        ),
        "iocs": [
            "185.220.101.47", "45.142.212.100", "shadowpad.dll", "winnti_dropper.exe",
            "c2.healthcheck-update[.]com", "update.microsoft-patch[.]net"
        ],
        "markov_transitions": {
            "T1566.001": {"T1059.003": 0.55, "T1204.002": 0.30, "T1190": 0.15},
            "T1059.003": {"T1055": 0.50, "T1078": 0.30, "T1547.001": 0.20},
            "T1055":     {"T1021.002": 0.45, "T1070.004": 0.30, "T1041": 0.25},
            "T1021.002": {"T1486": 0.40, "T1003": 0.35, "T1083": 0.25},
            "T1486":     {"T1041": 0.60, "T1070.004": 0.40},
            "T1078":     {"T1021.002": 0.50, "T1053.005": 0.30, "T1098": 0.20},
            "T1070.004": {"T1041": 0.70, "T1486": 0.30},
            "T1041":     {"T1070.004": 0.80, "T1486": 0.20},
            "T1547.001": {"T1055": 0.60, "T1078": 0.40},
            "T1053.005": {"T1059.003": 0.55, "T1078": 0.45},
        },
        "confidence": 91.0,
    },
    {
        "id": "lazarus",
        "name": "Lazarus Group",
        "aliases": ["Hidden Cobra", "ZINC", "Guardians of Peace", "APT38"],
        "origin": "North Korea (DPRK)",
        "motivation": "Financial gain + Espionage",
        "targets": ["Banking", "Cryptocurrency", "Defence", "Government"],
        "ttps": [
            "T1566.001", "T1059.001", "T1055", "T1083",
            "T1005", "T1041", "T1486", "T1070.003", "T1027", "T1497"
        ],
        "campaigns": [
            "AppleJeus India (2023)",
            "DreamJob Operation (2023)",
            "TraderTraitor Banking Campaign (2024)"
        ],
        "last_seen": "2026-05-20",
        "description": (
            "Lazarus Group is a DPRK state-sponsored APT focused on financial theft to fund the regime. "
            "It has targeted Indian banks, cryptocurrency exchanges, and defence contractors. "
            "Known for the $81M Bangladesh Bank heist and multiple Indian crypto thefts. "
            "Uses custom malware including BLINDINGCAN, COPPERHEDGE, and TAINTEDSCRIBE."
        ),
        "iocs": [
            "103.76.228.10", "cryptocoin-update[.]com", "blindingcan.dll",
            "taintedscribe.exe", "47.242.181.198", "update-security[.]org"
        ],
        "markov_transitions": {
            "T1566.001": {"T1059.001": 0.60, "T1204.001": 0.40},
            "T1059.001": {"T1055": 0.50, "T1027": 0.30, "T1497": 0.20},
            "T1055":     {"T1083": 0.45, "T1005": 0.35, "T1041": 0.20},
            "T1083":     {"T1005": 0.60, "T1560": 0.40},
            "T1005":     {"T1041": 0.55, "T1486": 0.45},
            "T1041":     {"T1070.003": 0.70, "T1027": 0.30},
            "T1486":     {"T1041": 1.0},
            "T1070.003": {"T1055": 0.50, "T1083": 0.50},
            "T1027":     {"T1055": 0.60, "T1497": 0.40},
            "T1497":     {"T1059.001": 0.60, "T1027": 0.40},
        },
        "confidence": 67.0,
    },
    {
        "id": "sidewinder",
        "name": "SideWinder",
        "aliases": ["Rattlesnake", "T-APT-04", "APT-C-17"],
        "origin": "Unknown (India-focused)",
        "motivation": "Espionage",
        "targets": ["Military", "Government", "Law Enforcement", "Education"],
        "ttps": [
            "T1566.001", "T1204.002", "T1059.005", "T1082",
            "T1016", "T1071.001", "T1105", "T1547.001", "T1036.005", "T1053.002"
        ],
        "campaigns": [
            "Operation Sidewind 2023",
            "CERT-In Advisory AA23-290",
            "CBSE Board Exam Data Exfil (2026)"
        ],
        "last_seen": "2026-03-10",
        "description": (
            "SideWinder (also known as Rattlesnake) is an APT group that has been active since at least 2012. "
            "It predominantly targets government entities, military, and law enforcement in South Asia, "
            "with a specific focus on India. The group was responsible for the 2026 CBSE data breach "
            "ahead of board examinations, compromising student PII across multiple states. "
            "Uses RTF exploits and LNK files for initial access."
        ),
        "iocs": [
            "cbse-results.indiagovt[.]net", "army-update[.]in",
            "sidewinder_loader.dll", "94.158.244.15",
            "docs-viewer[.]in", "gov-portal-update[.]com"
        ],
        "markov_transitions": {
            "T1566.001": {"T1204.002": 0.65, "T1566.002": 0.35},
            "T1204.002": {"T1059.005": 0.55, "T1059.003": 0.45},
            "T1059.005": {"T1082": 0.45, "T1547.001": 0.35, "T1016": 0.20},
            "T1082":     {"T1016": 0.55, "T1071.001": 0.45},
            "T1016":     {"T1071.001": 0.60, "T1105": 0.40},
            "T1071.001": {"T1105": 0.50, "T1041": 0.50},
            "T1105":     {"T1036.005": 0.50, "T1547.001": 0.50},
            "T1547.001": {"T1053.002": 0.55, "T1082": 0.45},
            "T1036.005": {"T1041": 0.60, "T1059.005": 0.40},
            "T1053.002": {"T1059.005": 0.60, "T1082": 0.40},
        },
        "confidence": 43.0,
    },
    {
        "id": "transparent_tribe",
        "name": "Transparent Tribe",
        "aliases": ["APT36", "ProjectM", "Mythic Leopard", "TEMP.Lapis"],
        "origin": "Pakistan",
        "motivation": "Espionage",
        "targets": ["Defence", "Education", "Government", "Diplomatic"],
        "ttps": [
            "T1566.001", "T1204.001", "T1059.003", "T1082",
            "T1016", "T1041", "T1105", "T1036", "T1547", "T1070"
        ],
        "campaigns": [
            "Operation Crimson (2024)",
            "Education Sector Attack (2026)",
            "Defence Targeting Campaign (2025)"
        ],
        "last_seen": "2026-01-22",
        "description": (
            "Transparent Tribe (APT36) is a Pakistan-based APT group primarily targeting Indian defence, "
            "education, and government entities. Known for using CrimsonRAT and ObliqueRAT malware, "
            "delivered via spearphishing and fake government portals. Has specifically targeted "
            "Indian military personnel, diplomatic staff, and recently education institutions "
            "including NDA candidates and UPSC aspirants."
        ),
        "iocs": [
            "ministry-defence[.]in", "crimsonrat.exe", "obliquerat.dll",
            "202.59.10.100", "india-army-portal[.]com", "upsc-results[.]org"
        ],
        "markov_transitions": {
            "T1566.001": {"T1204.001": 0.60, "T1204.002": 0.40},
            "T1204.001": {"T1059.003": 0.55, "T1059.005": 0.45},
            "T1059.003": {"T1082": 0.45, "T1036": 0.35, "T1016": 0.20},
            "T1082":     {"T1016": 0.50, "T1041": 0.50},
            "T1016":     {"T1105": 0.55, "T1041": 0.45},
            "T1041":     {"T1070": 0.60, "T1547": 0.40},
            "T1105":     {"T1059.003": 0.55, "T1547": 0.45},
            "T1036":     {"T1059.003": 0.60, "T1082": 0.40},
            "T1547":     {"T1059.003": 0.55, "T1082": 0.45},
            "T1070":     {"T1041": 0.70, "T1105": 0.30},
        },
        "confidence": 34.0,
    },
]

# Build a lookup dict by actor ID
THREAT_ACTORS_BY_ID = {a["id"]: a for a in THREAT_ACTORS}

# ─────────────────────────────────────────────
# Demo lateral movement chain
# ─────────────────────────────────────────────

LATERAL_MOVEMENT_CHAIN = [
    "WORKSTATION-HR-01",
    "FILE-SERVER-02",
    "DOMAIN-CONTROLLER-01",
    "AIIMS-EMR-SERVER",
]
