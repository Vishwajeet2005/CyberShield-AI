"""
CyberShield AI — Application Configuration
"""

APP_NAME = "CyberShield AI"
VERSION = "1.0.0"
DESCRIPTION = "AI-Powered Cyber Resilience Platform for India's Critical National Infrastructure"

FRONTEND_URL = "http://localhost:5173"
FRONTEND_URL_ALT = "http://localhost:3000"

# Live threat intelligence feed URLs
NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
MITRE_ATTACK_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

# Demo mode — uses simulated data for ML models, live data for CVE/KEV feeds
DEMO_MODE = True

# SQLite audit log path (production: replace with PostgreSQL)
AUDIT_DB_PATH = "audit_log.db"

# Simulation settings
ALERT_GENERATION_INTERVAL_MIN = 5   # seconds
ALERT_GENERATION_INTERVAL_MAX = 10  # seconds
MAX_ALERTS_IN_MEMORY = 100

# CERT-In compliance
CERT_IN_ORGANIZATION = "AIIMS Delhi"
CERT_IN_CONTACT_EMAIL = "cert@aiims.edu"
CERT_IN_REPORTING_HOURS = 6   # mandatory reporting within 6 hours

# Performance SLAs
ALERT_LATENCY_P99_SECONDS = 5
CONTAINMENT_SLA_SECONDS = 30
INCIDENT_REPORT_SLA_MINUTES = 10
