"""
CyberShield AI — VPA Service
Vulnerability prioritisation with live NVD + CISA KEV integration.
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import List, Optional

from utils.nvd_client import (
    fetch_cisa_kev, fetch_nvd_cves, calculate_context_score,
    FALLBACK_CVES, ACTOR_TARGETED_CVES, ASSET_CVE_MAP
)
from models import CVEItem, AssetItem, KEVMatch, Severity, RemediationPriority

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Asset Inventory (25 simulated CNI assets)
# ─────────────────────────────────────────────

ASSETS = [
    {"id": "AS-001", "hostname": "FW-PERIMETER",         "ip": "203.0.113.1",  "os": "PAN-OS 11.1",           "department": "IT Infrastructure", "criticality": 9,  "patch_level": "current",  "network_segment": "DMZ",        "business_function": "Perimeter Security"},
    {"id": "AS-002", "hostname": "DMZ-WEBSERVER",         "ip": "203.0.113.10", "os": "Ubuntu 20.04 LTS",      "department": "IT Infrastructure", "criticality": 6,  "patch_level": "1-month",  "network_segment": "DMZ",        "business_function": "Public Web Portal"},
    {"id": "AS-003", "hostname": "MAIL-GW",               "ip": "203.0.113.11", "os": "Windows Server 2019",   "department": "IT Infrastructure", "criticality": 7,  "patch_level": "current",  "network_segment": "DMZ",        "business_function": "Email Gateway"},
    {"id": "AS-004", "hostname": "VPN-GW",                "ip": "203.0.113.15", "os": "Fortinet FortiOS 7.4",  "department": "IT Infrastructure", "criticality": 8,  "patch_level": "current",  "network_segment": "DMZ",        "business_function": "Remote Access VPN"},
    {"id": "AS-005", "hostname": "WORKSTATION-HR-01",     "ip": "10.1.10.101",  "os": "Windows 11 22H2",       "department": "Human Resources",   "criticality": 4,  "patch_level": "3-month",  "network_segment": "HR-LAN",     "business_function": "HR Operations"},
    {"id": "AS-006", "hostname": "WORKSTATION-HR-02",     "ip": "10.1.10.102",  "os": "Windows 10 21H2",       "department": "Human Resources",   "criticality": 3,  "patch_level": "3-month",  "network_segment": "HR-LAN",     "business_function": "HR Operations"},
    {"id": "AS-007", "hostname": "WORKSTATION-HR-03",     "ip": "10.1.10.103",  "os": "Windows 10 21H2 (EOL)", "department": "Human Resources",   "criticality": 3,  "patch_level": "6-month+", "network_segment": "HR-LAN",     "business_function": "HR Operations"},
    {"id": "AS-008", "hostname": "WORKSTATION-FIN-01",    "ip": "10.1.20.101",  "os": "Windows 11 23H2",       "department": "Finance",           "criticality": 7,  "patch_level": "current",  "network_segment": "FIN-LAN",    "business_function": "Financial Management"},
    {"id": "AS-009", "hostname": "WORKSTATION-FIN-02",    "ip": "10.1.20.102",  "os": "Windows 11 23H2",       "department": "Finance",           "criticality": 7,  "patch_level": "current",  "network_segment": "FIN-LAN",    "business_function": "Financial Management"},
    {"id": "AS-010", "hostname": "WORKSTATION-ADMIN-01",  "ip": "10.1.30.101",  "os": "Windows 11 23H2",       "department": "IT Administration", "criticality": 8,  "patch_level": "current",  "network_segment": "ADMIN-LAN",  "business_function": "System Administration"},
    {"id": "AS-011", "hostname": "FILE-SERVER-01",        "ip": "10.2.10.11",   "os": "Windows Server 2019",   "department": "IT Infrastructure", "criticality": 7,  "patch_level": "1-month",  "network_segment": "SERVER-LAN", "business_function": "HR File Storage"},
    {"id": "AS-012", "hostname": "FILE-SERVER-02",        "ip": "10.2.10.12",   "os": "Windows Server 2016",   "department": "IT Infrastructure", "criticality": 8,  "patch_level": "6-month+", "network_segment": "SERVER-LAN", "business_function": "Clinical File Storage"},
    {"id": "AS-013", "hostname": "DOMAIN-CONTROLLER-01",  "ip": "10.2.20.10",   "os": "Windows Server 2022",   "department": "IT Infrastructure", "criticality": 10, "patch_level": "current",  "network_segment": "SERVER-LAN", "business_function": "Identity & Access"},
    {"id": "AS-014", "hostname": "DOMAIN-CONTROLLER-02",  "ip": "10.2.20.11",   "os": "Windows Server 2022",   "department": "IT Infrastructure", "criticality": 9,  "patch_level": "current",  "network_segment": "SERVER-LAN", "business_function": "Identity & Access (Backup)"},
    {"id": "AS-015", "hostname": "AIIMS-EMR-SERVER",      "ip": "10.2.30.10",   "os": "Oracle Linux 8.8",      "department": "Clinical",          "criticality": 10, "patch_level": "current",  "network_segment": "CLINICAL-LAN","business_function": "Patient Records (EMR)"},
    {"id": "AS-016", "hostname": "HIS-SERVER",            "ip": "10.2.30.11",   "os": "RHEL 9",                "department": "Clinical",          "criticality": 9,  "patch_level": "1-month",  "network_segment": "CLINICAL-LAN","business_function": "Hospital Information System"},
    {"id": "AS-017", "hostname": "BACKUP-SERVER",         "ip": "10.2.40.10",   "os": "Windows Server 2022",   "department": "IT Infrastructure", "criticality": 8,  "patch_level": "1-month",  "network_segment": "BACKUP-LAN", "business_function": "Data Backup & Recovery"},
    {"id": "AS-018", "hostname": "SIEM-SERVER",           "ip": "10.2.50.10",   "os": "Ubuntu 22.04 LTS",      "department": "Security",          "criticality": 9,  "patch_level": "current",  "network_segment": "MGMT-LAN",   "business_function": "Security Monitoring"},
    {"id": "AS-019", "hostname": "OT-GATEWAY",            "ip": "10.100.0.1",   "os": "Waterfall FLIP v5.1",   "department": "Facilities",        "criticality": 10, "patch_level": "current",  "network_segment": "OT-NET",     "business_function": "OT/IT Boundary"},
    {"id": "AS-020", "hostname": "SCADA-SERVER",          "ip": "10.100.1.10",  "os": "Windows Server 2012 R2","department": "Facilities",        "criticality": 10, "patch_level": "eol",       "network_segment": "OT-NET",     "business_function": "HVAC/Power Control (SCADA)"},
    {"id": "AS-021", "hostname": "PLC-HVAC",              "ip": "10.100.2.10",  "os": "Siemens S7-1500",       "department": "Facilities",        "criticality": 8,  "patch_level": "current",  "network_segment": "OT-NET",     "business_function": "HVAC Control"},
    {"id": "AS-022", "hostname": "PLC-POWER",             "ip": "10.100.2.11",  "os": "Allen Bradley",         "department": "Facilities",        "criticality": 9,  "patch_level": "current",  "network_segment": "OT-NET",     "business_function": "Power Distribution"},
    {"id": "AS-023", "hostname": "PLC-MEDICAL-GAS",       "ip": "10.100.2.12",  "os": "Schneider M340",        "department": "Facilities",        "criticality": 10, "patch_level": "1-month",  "network_segment": "OT-NET",     "business_function": "Medical Gas (O2/N2O)"},
    {"id": "AS-024", "hostname": "CLOUD-CONNECTOR",       "ip": "10.50.0.1",    "os": "NIC Cloud Gateway",     "department": "IT Infrastructure", "criticality": 7,  "patch_level": "current",  "network_segment": "CLOUD-LAN",  "business_function": "NIC/MeitY Cloud Bridge"},
    {"id": "AS-025", "hostname": "MGMT-CONSOLE",          "ip": "10.2.50.20",   "os": "Ubuntu 22.04 LTS",      "department": "IT Administration", "criticality": 9,  "patch_level": "current",  "network_segment": "MGMT-LAN",   "business_function": "Infrastructure Management"},
]

# Network-exposed assets (internet-facing or DMZ)
NETWORK_EXPOSED_HOSTS = {
    "DMZ-WEBSERVER", "MAIL-GW", "VPN-GW", "FW-PERIMETER",
    "CLOUD-CONNECTOR", "OT-GATEWAY"
}

# Assets with compensating controls
COMPENSATING_CONTROL_HOSTS = {
    "FW-PERIMETER", "AIIMS-EMR-SERVER", "DOMAIN-CONTROLLER-01",
    "DOMAIN-CONTROLLER-02", "SIEM-SERVER", "MGMT-CONSOLE"
}

# ─────────────────────────────────────────────
# State
# ─────────────────────────────────────────────

_cve_list: List[CVEItem] = []
_kev_ids: set = set()
_last_refreshed: str = ""


def _severity_from_cvss(cvss: float) -> Severity:
    if cvss >= 9.0: return Severity.CRITICAL
    if cvss >= 7.0: return Severity.HIGH
    if cvss >= 4.0: return Severity.MEDIUM
    return Severity.LOW


def _priority_from_score(score: float) -> RemediationPriority:
    if score >= 85: return RemediationPriority.CRITICAL
    if score >= 70: return RemediationPriority.HIGH
    if score >= 50: return RemediationPriority.MEDIUM
    return RemediationPriority.LOW


async def load_feeds():
    """Called at startup — fetch live CVE/KEV data."""
    global _cve_list, _kev_ids, _last_refreshed
    try:
        logger.info("VPA: Fetching CISA KEV feed...")
        kev_entries = fetch_cisa_kev()
        _kev_ids = {v["cveID"] for v in kev_entries}
        logger.info(f"VPA: {len(_kev_ids)} KEV entries loaded")

        logger.info("VPA: Fetching NVD CVE data...")
        nvd_raw = fetch_nvd_cves("windows server", 20)

        # Use our curated fallback list as the primary set, then append NVD results
        all_cves = {c["cve_id"]: c for c in FALLBACK_CVES}
        for nvd_cve in nvd_raw:
            if nvd_cve["cve_id"] not in all_cves:
                all_cves[nvd_cve["cve_id"]] = nvd_cve

        _cve_list = []
        for cve_data in all_cves.values():
            cve_id = cve_data["cve_id"]
            cvss = float(cve_data.get("cvss_score", 0))
            is_kev = cve_id in _kev_ids
            actor_targeted = cve_id in ACTOR_TARGETED_CVES
            affected = ASSET_CVE_MAP.get(cve_id, [])
            network_exposed = any(h in NETWORK_EXPOSED_HOSTS for h in affected)
            has_control = any(h in COMPENSATING_CONTROL_HOSTS for h in affected)

            context = calculate_context_score(cvss, is_kev, actor_targeted, network_exposed, has_control)

            _cve_list.append(CVEItem(
                cve_id=cve_id,
                description=cve_data.get("description", "")[:400],
                cvss_score=cvss,
                cvss_vector=cve_data.get("cvss_vector", ""),
                severity=_severity_from_cvss(cvss),
                affected_assets=affected,
                published_date=cve_data.get("published_date", ""),
                is_kev=is_kev,
                kev_date_added=None,
                exploit_exists=cvss >= 9.0 or is_kev,
                actor_targeted=actor_targeted,
                context_score=context,
                remediation_priority=_priority_from_score(context),
                patch_available=True,
                patch_url=cve_data.get("patch_url"),
                network_exposed=network_exposed,
                has_compensating_control=has_control,
            ))

        _cve_list.sort(key=lambda c: c.context_score, reverse=True)
        _last_refreshed = datetime.now(timezone.utc).isoformat()
        logger.info(f"VPA: {len(_cve_list)} CVEs loaded and scored.")
    except Exception as e:
        logger.error(f"VPA feed load error: {e}")


def get_prioritized_vulnerabilities() -> List[CVEItem]:
    if not _cve_list:
        # Return fallback if feeds not loaded yet
        return _build_fallback_cves()
    return _cve_list


def _build_fallback_cves() -> List[CVEItem]:
    items = []
    for cve_data in FALLBACK_CVES:
        cve_id = cve_data["cve_id"]
        cvss = float(cve_data.get("cvss_score", 0))
        is_kev = cve_id in {"CVE-2021-44228", "CVE-2020-1472", "CVE-2022-30190", "CVE-2024-3400", "CVE-2024-21887", "CVE-2023-23397"}
        actor_targeted = cve_id in ACTOR_TARGETED_CVES
        affected = ASSET_CVE_MAP.get(cve_id, [])
        network_exposed = any(h in NETWORK_EXPOSED_HOSTS for h in affected)
        has_control = any(h in COMPENSATING_CONTROL_HOSTS for h in affected)
        context = calculate_context_score(cvss, is_kev, actor_targeted, network_exposed, has_control)
        items.append(CVEItem(
            cve_id=cve_id, description=cve_data["description"][:400],
            cvss_score=cvss, cvss_vector=cve_data.get("cvss_vector", ""),
            severity=_severity_from_cvss(cvss), affected_assets=affected,
            published_date=cve_data.get("published_date", ""),
            is_kev=is_kev, exploit_exists=is_kev or cvss >= 9.0,
            actor_targeted=actor_targeted, context_score=context,
            remediation_priority=_priority_from_score(context),
            patch_available=True, patch_url=cve_data.get("patch_url"),
            network_exposed=network_exposed, has_compensating_control=has_control,
        ))
    return sorted(items, key=lambda c: c.context_score, reverse=True)


def get_assets() -> List[AssetItem]:
    vuln_count = {}
    critical_count = {}
    for cve in (_cve_list or _build_fallback_cves()):
        for asset_name in cve.affected_assets:
            vuln_count[asset_name] = vuln_count.get(asset_name, 0) + 1
            if cve.severity in (Severity.CRITICAL, Severity.HIGH):
                critical_count[asset_name] = critical_count.get(asset_name, 0) + 1

    items = []
    for a in ASSETS:
        hn = a["hostname"]
        items.append(AssetItem(
            id=a["id"], hostname=hn, ip=a["ip"], os=a["os"],
            department=a["department"], criticality=a["criticality"],
            vulnerabilities_count=vuln_count.get(hn, 0),
            critical_vuln_count=critical_count.get(hn, 0),
            patch_level=a["patch_level"], network_segment=a["network_segment"],
            last_scanned=datetime.now(timezone.utc).isoformat(),
            business_function=a["business_function"],
        ))
    return items


def get_kev_matches() -> List[KEVMatch]:
    cves = _cve_list or _build_fallback_cves()
    matches = []
    for cve in cves:
        if cve.is_kev and cve.affected_assets:
            matches.append(KEVMatch(
                cve_id=cve.cve_id,
                vulnerability_name=cve.description[:80],
                affected_assets=cve.affected_assets,
                date_added_to_kev=cve.kev_date_added or "2024-01-01",
                required_action="Apply patch immediately. CISA requires remediation within 14 days for federal systems.",
                action_deadline=(datetime.now(timezone.utc) + timedelta(days=14)).isoformat(),
                context_score=cve.context_score,
            ))
    return sorted(matches, key=lambda m: m.context_score, reverse=True)


async def refresh_feeds() -> dict:
    await load_feeds()
    return {"success": True, "cve_count": len(_cve_list), "kev_count": len(_kev_ids), "refreshed_at": _last_refreshed}
