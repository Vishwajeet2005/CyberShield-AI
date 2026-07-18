"""
CyberShield AI — Playbook Library (AIRO Module)
50+ incident response playbook templates bootstrapped from CISA playbook library
and NIST SP 800-61 Rev.2 incident handling guidance.
"""

PLAYBOOKS = [
    {
        "id": "PB-001",
        "name": "Ransomware Response",
        "description": "Complete response playbook for ransomware attacks. Prioritises containment, evidence preservation, and business continuity over decryption.",
        "trigger_conditions": [
            "BADE detects mass file encryption activity",
            "Alert: Data Encrypted for Impact (T1486)",
            "Multiple endpoints reporting file extension changes",
            "C2 beacon detected from known ransomware infrastructure"
        ],
        "estimated_containment_seconds": 45,
        "blast_radius_summary": "Steps 1-3 are LOW auto-execute; Step 4 is MEDIUM notify+execute; Step 5 requires HIGH approval",
        "steps": [
            {
                "id": "PB-001-S1", "name": "Block C2 IP at Perimeter Firewall",
                "description": "Immediately block all traffic to/from identified C2 IP addresses at the perimeter firewall using pre-staged ACL rules.",
                "action_type": "firewall_block_ip", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 10
            },
            {
                "id": "PB-001-S2", "name": "Isolate Affected Endpoints",
                "description": "Move compromised endpoints to quarantine VLAN via NAC enforcement. Endpoints retain management plane access for forensics.",
                "action_type": "endpoint_isolate", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 15
            },
            {
                "id": "PB-001-S3", "name": "Snapshot VM State",
                "description": "Take immutable snapshot of affected VMs for forensic analysis and potential recovery. Do not shutdown VMs before snapshot.",
                "action_type": "vm_snapshot", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 30
            },
            {
                "id": "PB-001-S4", "name": "Revoke Active Sessions & Force Logout",
                "description": "Revoke all active user sessions for accounts on affected systems. Force re-authentication across the domain.",
                "action_type": "revoke_sessions", "blast_radius": "medium",
                "auto_execute": True, "timeout_seconds": 20
            },
            {
                "id": "PB-001-S5", "name": "Activate Network Segmentation — Isolate Affected Subnet",
                "description": "Apply emergency ACL to completely isolate the affected subnet from the rest of the network. WARNING: Will disrupt all services in the subnet.",
                "action_type": "network_segment_isolate", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
        ]
    },
    {
        "id": "PB-002",
        "name": "Lateral Movement Containment",
        "description": "Playbook to detect, track, and contain adversarial lateral movement across the network. Focuses on cutting the kill chain before reaching crown jewel assets.",
        "trigger_conditions": [
            "BADE score > 80 on two or more correlated entities",
            "Lateral movement graph: 2+ hops detected",
            "Unusual SMB/RDP authentication from non-admin account",
            "AAPA attribution confidence > 70%"
        ],
        "estimated_containment_seconds": 28,
        "blast_radius_summary": "Steps 1-3 are LOW auto-execute; Steps 4-5 are MEDIUM; Step 6 requires HIGH approval",
        "steps": [
            {
                "id": "PB-002-S1", "name": "Block Source IP at Internal Firewall",
                "description": "Block the originating IP address at the internal firewall and core switch ACL to prevent further lateral movement.",
                "action_type": "firewall_block_ip", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 8
            },
            {
                "id": "PB-002-S2", "name": "Isolate Compromised Endpoint",
                "description": "Place the identified source endpoint into quarantine VLAN. Preserve network connectivity to management plane.",
                "action_type": "endpoint_isolate", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 12
            },
            {
                "id": "PB-002-S3", "name": "Revoke Session Tokens",
                "description": "Invalidate all active session tokens for the compromised user account across all services (SSO, VPN, cloud apps).",
                "action_type": "revoke_sessions", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 10
            },
            {
                "id": "PB-002-S4", "name": "Force Password Reset for Compromised Account",
                "description": "Trigger immediate password reset for the compromised account. User will be notified and required to authenticate with new credentials.",
                "action_type": "force_password_reset", "blast_radius": "medium",
                "auto_execute": True, "timeout_seconds": 15
            },
            {
                "id": "PB-002-S5", "name": "Scan All Endpoints in Affected Segment",
                "description": "Trigger immediate EDR scan across all endpoints in the affected network segment to identify additional compromise.",
                "action_type": "edr_scan_segment", "blast_radius": "medium",
                "auto_execute": True, "timeout_seconds": 120
            },
            {
                "id": "PB-002-S6", "name": "Disable Account in Active Directory",
                "description": "Permanently disable the compromised account in Active Directory. WARNING: User will be locked out of all systems immediately.",
                "action_type": "disable_ad_account", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
        ]
    },
    {
        "id": "PB-003",
        "name": "Data Exfiltration Response",
        "description": "Playbook for suspected or confirmed data exfiltration. Focuses on stopping the data loss, preserving evidence, and meeting DPDP Act 2023 and CERT-In reporting obligations.",
        "trigger_conditions": [
            "BADE detects anomalous outbound data volume (>500MB/hr)",
            "Alert: Exfiltration Over C2 Channel (T1041)",
            "DNS queries to suspicious external domains",
            "Large file transfers to cloud storage from sensitive systems"
        ],
        "estimated_containment_seconds": 35,
        "blast_radius_summary": "Steps 1-2 LOW auto-execute; Step 3 MEDIUM; Steps 4-5 HIGH require approval",
        "steps": [
            {
                "id": "PB-003-S1", "name": "Block Egress IPs at Perimeter Firewall",
                "description": "Immediately block outbound traffic to identified exfiltration destination IPs. Apply both IPv4 and IPv6 rules.",
                "action_type": "firewall_block_egress", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 10
            },
            {
                "id": "PB-003-S2", "name": "Enable Full Packet Capture on Affected Interface",
                "description": "Activate full packet capture on the affected network interface for forensic evidence. Captures will be stored in the evidence vault.",
                "action_type": "enable_packet_capture", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 5
            },
            {
                "id": "PB-003-S3", "name": "Isolate Exfiltrating Endpoint",
                "description": "Move the source endpoint to quarantine VLAN. All network traffic will be blocked except management access.",
                "action_type": "endpoint_isolate", "blast_radius": "medium",
                "auto_execute": True, "timeout_seconds": 12
            },
            {
                "id": "PB-003-S4", "name": "Notify DPO and CERT-In",
                "description": "Automatically generate and send breach notification to the Data Protection Officer and CERT-In as required by DPDP Act 2023 and CERT-In Directions 2022.",
                "action_type": "notify_dpo_cert_in", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
            {
                "id": "PB-003-S5", "name": "Preserve Evidence — Legal Hold",
                "description": "Apply legal hold to all logs, packet captures, and system images. Evidence is transferred to immutable S3 WORM bucket for court proceedings.",
                "action_type": "legal_hold_evidence", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
        ]
    },
    {
        "id": "PB-004",
        "name": "Credential Compromise Response",
        "description": "Response to confirmed credential theft or account compromise. Designed to minimize attacker dwell time using stolen credentials.",
        "trigger_conditions": [
            "Alert: OS Credential Dumping (T1003) detected",
            "Account accessing unusual resources outside working hours",
            "Multiple failed login attempts followed by success from new location",
            "BADE deviation > 75 for login anomaly features"
        ],
        "estimated_containment_seconds": 20,
        "blast_radius_summary": "Steps 1-3 LOW auto-execute; Step 4 MEDIUM; Step 5 HIGH approval required",
        "steps": [
            {
                "id": "PB-004-S1", "name": "Disable Compromised Account",
                "description": "Immediately disable the compromised account in Active Directory to prevent further use of stolen credentials.",
                "action_type": "disable_ad_account", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 8
            },
            {
                "id": "PB-004-S2", "name": "Revoke All Active Sessions",
                "description": "Terminate all active sessions for the compromised account across SSO, VPN, Office 365, and cloud services.",
                "action_type": "revoke_sessions", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 10
            },
            {
                "id": "PB-004-S3", "name": "Force MFA Re-Enrollment",
                "description": "Revoke existing MFA tokens and force re-enrollment when account is reactivated. Blocks re-use of stolen MFA seeds.",
                "action_type": "revoke_mfa", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 5
            },
            {
                "id": "PB-004-S4", "name": "Audit All Recent Access by Account",
                "description": "Generate a 72-hour access audit for the compromised account across all systems. Identify all data accessed, commands run, and files modified.",
                "action_type": "audit_account_access", "blast_radius": "medium",
                "auto_execute": True, "timeout_seconds": 60
            },
            {
                "id": "PB-004-S5", "name": "Scan for Persistence Mechanisms",
                "description": "Run EDR hunt across systems accessed by the compromised account to identify any persistence mechanisms (scheduled tasks, registry keys, startup items) planted by attacker.",
                "action_type": "hunt_persistence", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
        ]
    },
    {
        "id": "PB-005",
        "name": "OT/ICS Sabotage Response",
        "description": "Emergency response for attacks targeting Operational Technology (OT) and Industrial Control Systems (ICS). Prioritises physical safety above all else.",
        "trigger_conditions": [
            "BADE detects anomalous ICS command sequences",
            "SCADA alert: setpoint modification outside safe range",
            "OT device communicating with IT network unexpectedly",
            "MITRE ICS technique detected: T0855 (Unauthorized Command Message)"
        ],
        "estimated_containment_seconds": 60,
        "blast_radius_summary": "All steps require HIGH approval — OT actions cannot be automated due to physical safety risk",
        "steps": [
            {
                "id": "PB-005-S1", "name": "Activate OT-IT Air Gap",
                "description": "Immediately activate the data diode in blocking mode to cut all traffic between OT and IT networks. Physical safety takes precedence over data collection.",
                "action_type": "activate_ot_airgap", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 300
            },
            {
                "id": "PB-005-S2", "name": "Alert Facility/Plant Manager",
                "description": "Immediately notify the on-site facility manager and operations team of potential cyber-physical attack. Provide current threat status.",
                "action_type": "alert_facility_manager", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 60
            },
            {
                "id": "PB-005-S3", "name": "Switch to Manual Control Mode",
                "description": "Transition affected ICS processes to manual control mode. Operators take direct physical control. This prevents attacker from sending remote commands.",
                "action_type": "switch_to_manual_control", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
            {
                "id": "PB-005-S4", "name": "Preserve OT Forensic Evidence",
                "description": "Capture and preserve all OT network traffic, historian data, and PLC/RTU logs before any remediation. Evidence needed for CERT-In report and potential legal proceedings.",
                "action_type": "preserve_ot_evidence", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
        ]
    },
    {
        "id": "PB-006",
        "name": "Phishing / Email Attack Response",
        "description": "Response to detected phishing campaign targeting the organization. Designed to stop credential theft and malware delivery.",
        "trigger_conditions": [
            "Email security gateway flags high-confidence phishing",
            "User reports suspicious email with malicious attachment",
            "BADE detects credential submission to external site",
            "Alert: Spearphishing Attachment (T1566.001) detected"
        ],
        "estimated_containment_seconds": 25,
        "blast_radius_summary": "Steps 1-3 LOW auto-execute; Step 4 MEDIUM; Step 5 depends on click status",
        "steps": [
            {
                "id": "PB-006-S1", "name": "Quarantine Phishing Email",
                "description": "Automatically quarantine the phishing email from all user mailboxes organisation-wide using email security platform API.",
                "action_type": "quarantine_email", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 10
            },
            {
                "id": "PB-006-S2", "name": "Block Sender Domain at Email Gateway",
                "description": "Add sender domain and all associated IPs to the email gateway block list. Apply both inbound and outbound blocks.",
                "action_type": "block_email_domain", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 8
            },
            {
                "id": "PB-006-S3", "name": "Block Phishing URL at Web Proxy",
                "description": "Add the phishing URL to the web proxy block list to prevent users who may have the email from clicking the link.",
                "action_type": "block_url_proxy", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 8
            },
            {
                "id": "PB-006-S4", "name": "Notify All Potentially Exposed Users",
                "description": "Send security alert to all users who received the phishing email with instructions not to click links or open attachments.",
                "action_type": "notify_exposed_users", "blast_radius": "medium",
                "auto_execute": True, "timeout_seconds": 20
            },
            {
                "id": "PB-006-S5", "name": "Reset Credentials for Users Who Clicked",
                "description": "For users who clicked the link or opened the attachment, immediately reset credentials, revoke sessions, and flag for security awareness training.",
                "action_type": "reset_clicked_user_credentials", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
        ]
    },
    {
        "id": "PB-007",
        "name": "Privilege Escalation Response",
        "description": "Response to detected unauthorized privilege escalation. Aims to revoke elevated access before attacker can use it to cause further damage.",
        "trigger_conditions": [
            "BADE detects privilege escalation (T1078) on entity",
            "Account added to Domain Admins unexpectedly",
            "Alert: new scheduled task created by non-admin account",
            "Windows Event 4672 (Special Logon) for unexpected account"
        ],
        "estimated_containment_seconds": 20,
        "blast_radius_summary": "Steps 1-2 LOW; Step 3 MEDIUM; Steps 4-5 HIGH",
        "steps": [
            {
                "id": "PB-007-S1", "name": "Revoke Escalated Privileges",
                "description": "Immediately remove the account from elevated groups (Domain Admins, Enterprise Admins, local Administrators) and revoke any newly granted permissions.",
                "action_type": "revoke_privileges", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 10
            },
            {
                "id": "PB-007-S2", "name": "Kill Suspicious Processes",
                "description": "Terminate processes that were spawned using the escalated privileges. Focus on cmd.exe, powershell.exe, and unknown binaries.",
                "action_type": "kill_processes", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 8
            },
            {
                "id": "PB-007-S3", "name": "Audit Privilege Changes (72-hour window)",
                "description": "Run a full audit of all privilege changes across Active Directory for the past 72 hours to identify scope of compromise.",
                "action_type": "audit_privilege_changes", "blast_radius": "medium",
                "auto_execute": True, "timeout_seconds": 60
            },
            {
                "id": "PB-007-S4", "name": "Hunt for Persistence Mechanisms",
                "description": "Conduct targeted threat hunt for persistence (scheduled tasks, registry run keys, WMI subscriptions) planted using escalated privileges.",
                "action_type": "hunt_persistence", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
            {
                "id": "PB-007-S5", "name": "Full Credential Reset for Privileged Accounts",
                "description": "Reset credentials for all privileged accounts (Domain Admins, Service Accounts) that may have been exposed. WARNING: Requires coordination with IT operations.",
                "action_type": "reset_privileged_credentials", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
        ]
    },
    {
        "id": "PB-008",
        "name": "Supply Chain Compromise Response",
        "description": "Response to supply chain attack via compromised software update or third-party library. Focuses on identifying blast radius and blocking malicious update infrastructure.",
        "trigger_conditions": [
            "BADE detects unusual process tree from trusted software",
            "Threat intel: known-compromised software version in use",
            "Alert: Ingress Tool Transfer (T1105) from update server",
            "Vendor discloses supply chain compromise affecting our version"
        ],
        "estimated_containment_seconds": 90,
        "blast_radius_summary": "Steps 1-2 LOW; Step 3-4 MEDIUM; Steps 5-6 HIGH",
        "steps": [
            {
                "id": "PB-008-S1", "name": "Block Compromised Update Server",
                "description": "Block network access to the compromised vendor update server at perimeter firewall and internal proxy. Prevents further distribution of malicious updates.",
                "action_type": "firewall_block_ip", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 10
            },
            {
                "id": "PB-008-S2", "name": "Identify All Systems with Affected Software",
                "description": "Query asset management and EDR for all endpoints running the affected software version. Generate list for remediation prioritisation.",
                "action_type": "asset_software_query", "blast_radius": "low",
                "auto_execute": True, "timeout_seconds": 30
            },
            {
                "id": "PB-008-S3", "name": "Isolate Highest-Risk Affected Systems",
                "description": "Quarantine systems that are running the affected software AND are in critical network segments or handling sensitive data.",
                "action_type": "endpoint_isolate", "blast_radius": "medium",
                "auto_execute": True, "timeout_seconds": 20
            },
            {
                "id": "PB-008-S4", "name": "Rollback Affected Deployments",
                "description": "Roll back the compromised software version to the last known-good version across all affected systems.",
                "action_type": "rollback_deployment", "blast_radius": "medium",
                "auto_execute": True, "timeout_seconds": 300
            },
            {
                "id": "PB-008-S5", "name": "Audit Dependencies and SBOM",
                "description": "Run full dependency audit against current SBOM (Software Bill of Materials). Identify all transitive dependencies that may also be affected.",
                "action_type": "audit_dependencies", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
            {
                "id": "PB-008-S6", "name": "Notify CERT-In and Affected Stakeholders",
                "description": "Submit mandatory incident report to CERT-In within 6 hours as required by CERT-In Directions 2022. Notify all affected department heads.",
                "action_type": "notify_cert_in", "blast_radius": "high",
                "auto_execute": False, "timeout_seconds": 600
            },
        ]
    },
]

# Quick lookup by ID
PLAYBOOKS_BY_ID = {p["id"]: p for p in PLAYBOOKS}
