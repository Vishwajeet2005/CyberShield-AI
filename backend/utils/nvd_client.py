"""
CyberShield AI — NVD + CISA KEV API Client (VPA Module)
Live threat intelligence feeds with in-memory caching and realistic fallback data.
"""

import requests
import time
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Cache
# ─────────────────────────────────────────────
_cache: Dict[str, Any] = {}
CACHE_TTL_SECONDS = 3600  # 1 hour


def _cache_get(key: str) -> Optional[Any]:
    entry = _cache.get(key)
    if entry and (time.time() - entry["ts"]) < CACHE_TTL_SECONDS:
        return entry["data"]
    return None


def _cache_set(key: str, data: Any) -> None:
    _cache[key] = {"data": data, "ts": time.time()}


# ─────────────────────────────────────────────
# Fallback CVE Data (used when NVD is unavailable)
# ─────────────────────────────────────────────

FALLBACK_CVES = [
    {
        "cve_id": "CVE-2021-44228", "description": "Apache Log4j2 JNDI injection vulnerability (Log4Shell). Remote code execution via JNDI lookup in log messages.",
        "cvss_score": 10.0, "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
        "severity": "critical", "published_date": "2021-12-10T00:00:00+00:00", "patch_url": "https://logging.apache.org/log4j/2.x/security.html"
    },
    {
        "cve_id": "CVE-2020-1472", "description": "Zerologon: Netlogon elevation of privilege vulnerability. Allows attacker to establish a vulnerable Netlogon secure channel connection to a domain controller.",
        "cvss_score": 10.0, "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
        "severity": "critical", "published_date": "2020-08-17T00:00:00+00:00", "patch_url": "https://portal.msrc.microsoft.com/security-guidance/advisory/CVE-2020-1472"
    },
    {
        "cve_id": "CVE-2024-3400", "description": "PAN-OS GlobalProtect gateway command injection. Unauthenticated RCE in Palo Alto Networks PAN-OS.",
        "cvss_score": 10.0, "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
        "severity": "critical", "published_date": "2024-04-12T00:00:00+00:00", "patch_url": "https://security.paloaltonetworks.com/CVE-2024-3400"
    },
    {
        "cve_id": "CVE-2022-30190", "description": "Microsoft Windows Support Diagnostic Tool (MSDT) remote code execution vulnerability (Follina). Triggered by opening malicious Office documents.",
        "cvss_score": 7.8, "cvss_vector": "CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H",
        "severity": "high", "published_date": "2022-05-30T00:00:00+00:00", "patch_url": "https://msrc.microsoft.com/update-guide/vulnerability/CVE-2022-30190"
    },
    {
        "cve_id": "CVE-2021-34527", "description": "Windows Print Spooler remote code execution vulnerability (PrintNightmare). Allows domain user to gain SYSTEM privileges.",
        "cvss_score": 8.8, "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H",
        "severity": "high", "published_date": "2021-07-01T00:00:00+00:00", "patch_url": "https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34527"
    },
    {
        "cve_id": "CVE-2020-0796", "description": "SMBGhost: Windows SMBv3 client/server remote code execution. Wormable vulnerability in SMBv3 compression.",
        "cvss_score": 10.0, "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
        "severity": "critical", "published_date": "2020-03-12T00:00:00+00:00", "patch_url": "https://msrc.microsoft.com/update-guide/vulnerability/CVE-2020-0796"
    },
    {
        "cve_id": "CVE-2023-36884", "description": "Windows HTML remote code execution vulnerability. Exploitation via specially crafted Office/HTML documents, exploited by Storm-0978.",
        "cvss_score": 8.3, "cvss_vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H",
        "severity": "high", "published_date": "2023-07-11T00:00:00+00:00", "patch_url": "https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-36884"
    },
    {
        "cve_id": "CVE-2024-21887", "description": "Ivanti Connect Secure command injection. Pre-auth RCE in Ivanti VPN appliances. Actively exploited by nation-state actors.",
        "cvss_score": 9.1, "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H",
        "severity": "critical", "published_date": "2024-01-10T00:00:00+00:00", "patch_url": "https://forums.ivanti.com/s/article/CVE-2024-21887"
    },
    {
        "cve_id": "CVE-2023-23397", "description": "Microsoft Outlook privilege escalation. Zero-click exploit triggers when email is received; leaks NTLM hash. Exploited by APT28.",
        "cvss_score": 9.8, "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "severity": "critical", "published_date": "2023-03-14T00:00:00+00:00", "patch_url": "https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-23397"
    },
    {
        "cve_id": "CVE-2022-0778", "description": "OpenSSL infinite loop vulnerability. Remote DoS attack against services using OpenSSL certificate parsing.",
        "cvss_score": 7.5, "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
        "severity": "high", "published_date": "2022-03-15T00:00:00+00:00", "patch_url": "https://openssl.org/news/secadv/20220315.txt"
    },
    {
        "cve_id": "CVE-2022-34151", "description": "Siemens SIMATIC S7 PLC authentication bypass. Allows unauthenticated access to PLC memory areas, enabling process manipulation.",
        "cvss_score": 8.1, "cvss_vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "severity": "high", "published_date": "2022-07-12T00:00:00+00:00", "patch_url": "https://cert-portal.siemens.com/productcert/html/ssa-382653.html"
    },
    {
        "cve_id": "CVE-2023-27532", "description": "Veeam Backup & Replication authentication bypass. Allows unauthenticated remote access to encrypted credentials stored in configuration database.",
        "cvss_score": 7.5, "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
        "severity": "high", "published_date": "2023-03-07T00:00:00+00:00", "patch_url": "https://www.veeam.com/kb4424"
    },
    {
        "cve_id": "CVE-2022-21500", "description": "Oracle E-Business Suite authentication bypass. Unauthenticated access to sensitive data in Oracle EBS.",
        "cvss_score": 7.5, "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
        "severity": "high", "published_date": "2022-04-19T00:00:00+00:00", "patch_url": "https://www.oracle.com/security-alerts/cpuapr2022.html"
    },
    {
        "cve_id": "CVE-2024-1709", "description": "ConnectWise ScreenConnect authentication bypass (SlashAndGrab). Critical auth bypass enabling mass exploitation of remote access software.",
        "cvss_score": 10.0, "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
        "severity": "critical", "published_date": "2024-02-19T00:00:00+00:00", "patch_url": "https://www.connectwise.com/company/trust/security-bulletins/connectwise-screenconnect-23.9.8"
    },
    {
        "cve_id": "CVE-2023-28252", "description": "Windows Common Log File System driver privilege escalation. Exploited in ransomware campaigns to gain SYSTEM privileges.",
        "cvss_score": 7.8, "cvss_vector": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H",
        "severity": "high", "published_date": "2023-04-11T00:00:00+00:00", "patch_url": "https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-28252"
    },
]

# CVEs known to be actively targeted by India-targeting APT groups
ACTOR_TARGETED_CVES = {
    "CVE-2022-30190", "CVE-2023-36884", "CVE-2024-3400",
    "CVE-2023-23397", "CVE-2021-44228", "CVE-2020-1472",
    "CVE-2024-21887", "CVE-2022-34151",
}

# AIIMS-specific affected asset mappings
ASSET_CVE_MAP = {
    "CVE-2021-44228": ["DMZ-WEBSERVER", "HIS-SERVER"],
    "CVE-2020-1472":  ["DOMAIN-CONTROLLER-01", "DOMAIN-CONTROLLER-02"],
    "CVE-2024-3400":  ["FW-PERIMETER"],
    "CVE-2022-30190": ["WORKSTATION-HR-01", "WORKSTATION-HR-02", "WORKSTATION-HR-03"],
    "CVE-2021-34527": ["FILE-SERVER-02", "WORKSTATION-HR-03"],
    "CVE-2020-0796":  ["FILE-SERVER-01", "FILE-SERVER-02"],
    "CVE-2023-36884": ["WORKSTATION-HR-01", "WORKSTATION-ADMIN-02"],
    "CVE-2024-21887": ["VPN-GW"],
    "CVE-2023-23397": ["MAIL-GW"],
    "CVE-0022-0778":  ["DMZ-WEBSERVER"],
    "CVE-2022-34151": ["PLC-HVAC"],
    "CVE-2023-27532": ["BACKUP-SERVER"],
    "CVE-2022-21500": ["AIIMS-EMR-SERVER"],
    "CVE-2024-1709":  ["CLOUD-CONNECTOR"],
    "CVE-2023-28252": ["WORKSTATION-FIN-01"],
}

# ─────────────────────────────────────────────
# Context Scoring
# ─────────────────────────────────────────────

def calculate_context_score(
    cvss: float,
    is_kev: bool,
    actor_targeted: bool,
    network_exposed: bool,
    has_compensating_control: bool,
) -> float:
    score = cvss * 10
    if is_kev:
        score = min(100.0, score + 25.0)
    if actor_targeted:
        score = min(100.0, score + 20.0)
    if network_exposed:
        score = min(100.0, score + 15.0)
    if has_compensating_control:
        score = max(0.0, score - 15.0)
    return round(score, 1)


# ─────────────────────────────────────────────
# CISA KEV Feed
# ─────────────────────────────────────────────

def fetch_cisa_kev() -> List[Dict]:
    cached = _cache_get("cisa_kev")
    if cached:
        return cached

    try:
        resp = requests.get(
            "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
            timeout=15
        )
        resp.raise_for_status()
        data = resp.json()
        vulns = data.get("vulnerabilities", [])
        result = [
            {
                "cveID": v.get("cveID", ""),
                "vulnerabilityName": v.get("vulnerabilityName", ""),
                "dateAdded": v.get("dateAdded", ""),
                "shortDescription": v.get("shortDescription", ""),
                "product": v.get("product", ""),
                "vendorProject": v.get("vendorProject", ""),
                "requiredAction": v.get("requiredAction", ""),
                "dueDate": v.get("dueDate", ""),
            }
            for v in vulns
        ]
        _cache_set("cisa_kev", result)
        logger.info(f"CISA KEV: fetched {len(result)} entries")
        return result
    except Exception as e:
        logger.warning(f"CISA KEV fetch failed ({e}), using fallback set")
        fallback = [
            {"cveID": c["cve_id"], "vulnerabilityName": c["description"][:60],
             "dateAdded": "2024-01-01", "shortDescription": c["description"],
             "product": "Various", "vendorProject": "Multiple",
             "requiredAction": "Apply vendor patch immediately.", "dueDate": "2024-01-21"}
            for c in FALLBACK_CVES if c["cvss_score"] >= 9.0
        ]
        return fallback


# ─────────────────────────────────────────────
# NVD CVE Feed
# ─────────────────────────────────────────────

def fetch_nvd_cves(keyword: str = "windows server", results_per_page: int = 20) -> List[Dict]:
    cache_key = f"nvd_{keyword}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    try:
        params = {
            "keywordSearch": keyword,
            "resultsPerPage": results_per_page,
            "startIndex": 0,
        }
        resp = requests.get(
            "https://services.nvd.nist.gov/rest/json/cves/2.0",
            params=params,
            timeout=20,
            headers={"User-Agent": "CyberShieldAI/1.0 (hackathon demo)"}
        )
        resp.raise_for_status()
        data = resp.json()
        vulns = data.get("vulnerabilities", [])

        result = []
        for item in vulns:
            cve = item.get("cve", {})
            cve_id = cve.get("id", "")
            descriptions = cve.get("descriptions", [])
            desc = next((d["value"] for d in descriptions if d["lang"] == "en"), "No description")
            metrics = cve.get("metrics", {})
            cvss_score = 0.0
            cvss_vector = ""

            # Try CVSSv3.1 first, then v3.0, then v2.0
            for metric_key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
                m = metrics.get(metric_key, [])
                if m:
                    cvss_data = m[0].get("cvssData", {})
                    cvss_score = cvss_data.get("baseScore", 0.0)
                    cvss_vector = cvss_data.get("vectorString", "")
                    break

            published = cve.get("published", "")
            result.append({
                "cve_id": cve_id,
                "description": desc[:300],
                "cvss_score": float(cvss_score),
                "cvss_vector": cvss_vector,
                "published_date": published,
            })

        _cache_set(cache_key, result)
        logger.info(f"NVD: fetched {len(result)} CVEs for keyword '{keyword}'")
        return result

    except Exception as e:
        logger.warning(f"NVD fetch failed ({e}), using fallback CVE list")
        return [
            {
                "cve_id": c["cve_id"], "description": c["description"],
                "cvss_score": c["cvss_score"], "cvss_vector": c.get("cvss_vector", ""),
                "published_date": c["published_date"],
            }
            for c in FALLBACK_CVES
        ]
