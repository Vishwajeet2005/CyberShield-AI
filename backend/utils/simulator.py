"""
CyberShield AI — Background Event Simulator (BADE Module)
Generates realistic live data for the demo: alerts, entity scores, incidents, metrics.
Runs as a background asyncio task every 5-8 seconds.
"""

import asyncio
import random
import uuid
import copy
import numpy as np
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional

from data.scenarios import ALERT_TEMPLATES, ENTITY_PROFILES, CURRENT_INCIDENT, SECOND_INCIDENT
from models import (
    Alert, Entity, Incident, PlaybookAction, SystemMetrics,
    Severity, AlertStatus, IncidentStatus, ActionStatus, BlastRadius, EntityType, RiskLevel
)

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _mins_ago(n: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=n)).isoformat()

def _severity_from_score(score: float) -> Severity:
    if score >= 85: return Severity.CRITICAL
    if score >= 70: return Severity.HIGH
    if score >= 50: return Severity.MEDIUM
    return Severity.LOW

def _risk_from_score(score: float) -> RiskLevel:
    if score >= 85: return RiskLevel.CRITICAL
    if score >= 70: return RiskLevel.HIGH
    if score >= 50: return RiskLevel.MEDIUM
    if score >= 30: return RiskLevel.LOW
    return RiskLevel.NORMAL

# ─────────────────────────────────────────────
# Feature generation helpers
# ─────────────────────────────────────────────

ENTITY_TYPE_BASELINES = {
    "user":           {"login_count": (8,3), "failed_logins": (0.5,0.5), "bytes_sent": (50e6,20e6), "bytes_received": (200e6,80e6), "unique_destinations": (15,5), "port_scan_count": (0,0.1), "off_hours_logins": (0.2,0.3), "privilege_escalations": (0,0.05), "process_creations": (20,8), "dns_queries": (100,30), "lateral_connections": (0.5,0.5), "file_operations": (80,30)},
    "server":         {"login_count": (50,10), "failed_logins": (2,1), "bytes_sent": (500e6,200e6), "bytes_received": (1e9,400e6), "unique_destinations": (30,10), "port_scan_count": (0.1,0.1), "off_hours_logins": (5,2), "privilege_escalations": (0.1,0.1), "process_creations": (200,50), "dns_queries": (800,200), "lateral_connections": (5,3), "file_operations": (1000,300)},
    "workstation":    {"login_count": (5,2), "failed_logins": (0.3,0.3), "bytes_sent": (30e6,15e6), "bytes_received": (150e6,60e6), "unique_destinations": (10,4), "port_scan_count": (0,0.05), "off_hours_logins": (0.1,0.2), "privilege_escalations": (0,0.02), "process_creations": (15,5), "dns_queries": (80,25), "lateral_connections": (0.2,0.3), "file_operations": (60,20)},
    "ot_device":      {"login_count": (2,0.5), "failed_logins": (0,0.1), "bytes_sent": (1e6,0.5e6), "bytes_received": (2e6,1e6), "unique_destinations": (3,1), "port_scan_count": (0,0.01), "off_hours_logins": (0.5,0.2), "privilege_escalations": (0,0), "process_creations": (5,1), "dns_queries": (20,5), "lateral_connections": (1,0.5), "file_operations": (10,3)},
    "service_account":{"login_count": (200,50), "failed_logins": (0.1,0.1), "bytes_sent": (100e6,40e6), "bytes_received": (300e6,100e6), "unique_destinations": (5,2), "port_scan_count": (0,0.02), "off_hours_logins": (10,3), "privilege_escalations": (0.5,0.3), "process_creations": (50,15), "dns_queries": (200,60), "lateral_connections": (2,1), "file_operations": (500,150)},
    "network_device": {"login_count": (10,3), "failed_logins": (0.5,0.3), "bytes_sent": (1e9,500e6), "bytes_received": (2e9,1e9), "unique_destinations": (100,30), "port_scan_count": (0.2,0.1), "off_hours_logins": (2,1), "privilege_escalations": (0,0.02), "process_creations": (10,3), "dns_queries": (500,100), "lateral_connections": (50,20), "file_operations": (20,5)},
}

FEATURE_NAMES = ["login_count","failed_logins","bytes_sent","bytes_received","unique_destinations","port_scan_count","off_hours_logins","privilege_escalations","process_creations","dns_queries","lateral_connections","file_operations"]


def _generate_normal_features(entity_type: str) -> Dict[str, float]:
    baseline = ENTITY_TYPE_BASELINES.get(entity_type, ENTITY_TYPE_BASELINES["user"])
    return {
        feat: max(0.0, random.gauss(baseline[feat][0], baseline[feat][1]))
        for feat in FEATURE_NAMES
    }


def _generate_attack_features(entity_type: str, attack_type: str) -> Dict[str, float]:
    features = _generate_normal_features(entity_type)
    if attack_type == "lateral_movement":
        features["lateral_connections"] *= 15
        features["failed_logins"] *= 8
        features["unique_destinations"] *= 10
        features["off_hours_logins"] += 3
    elif attack_type == "exfiltration":
        features["bytes_sent"] *= 25
        features["dns_queries"] *= 12
        features["unique_destinations"] *= 5
    elif attack_type == "ransomware":
        features["file_operations"] *= 50
        features["process_creations"] *= 8
        features["bytes_sent"] *= 3
    elif attack_type == "credential_dump":
        features["privilege_escalations"] *= 20
        features["process_creations"] *= 4
        features["failed_logins"] *= 5
    return features


# ─────────────────────────────────────────────
# Isolation Forest scorer
# ─────────────────────────────────────────────

def _build_isolation_forest():
    """Build a simple Isolation Forest on synthetic normal training data."""
    try:
        from sklearn.ensemble import IsolationForest
        rng = np.random.RandomState(42)
        # Generate synthetic normal training data (500 samples × 12 features)
        X_train = np.abs(rng.randn(500, len(FEATURE_NAMES)))
        # Normalise each feature to 0-1 range
        X_train = (X_train - X_train.min(0)) / (X_train.max(0) - X_train.min(0) + 1e-9)
        model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        model.fit(X_train)
        return model
    except Exception:
        return None


def _score_features(model, features: Dict[str, float]) -> float:
    """Convert Isolation Forest decision function to 0-100 anomaly score."""
    if model is None:
        return round(random.uniform(10, 35), 1)
    try:
        X = np.array([[features.get(f, 0) for f in FEATURE_NAMES]], dtype=float)
        # Normalise (simple min-max based on expected ranges)
        X = np.clip(X / np.maximum(X, 1), 0, 1)
        decision = model.decision_function(X)[0]
        # decision_function returns negative for anomalies (more negative = more anomalous)
        # Map [-0.5, 0.1] → [100, 0]
        score = (0.1 - decision) / 0.6 * 100
        return round(float(np.clip(score, 0, 100)), 1)
    except Exception:
        return round(random.uniform(10, 35), 1)


# ─────────────────────────────────────────────
# EventSimulator
# ─────────────────────────────────────────────

class EventSimulator:
    def __init__(self):
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._if_model = None

        # In-memory state
        self._alerts: List[Dict] = []
        self._entities: List[Dict] = []
        self._incidents: List[Dict] = []
        self._alert_counter = 0
        self._start_time = datetime.now(timezone.utc)

        # Fixed KPIs for demo
        self._tpr = 87.0
        self._fpr = 3.2
        self._mttd = 0.8
        self._mttr = 2.1
        self._automated_containments = 3
        self._events_per_second = random.randint(80_000, 120_000)

        # Attack simulation state
        self._attack_active = True
        self._attack_step = 0
        self._attack_entities = ["USR-HR-001", "SRV-FS-002", "SRV-DC-001", "SRV-EMR-001"]

    def _initialise_entities(self):
        """Seed entity scores from profiles with slight random deviation."""
        self._if_model = _build_isolation_forest()

        for profile in ENTITY_PROFILES:
            etype = profile["type"]
            features = _generate_normal_features(etype)
            base = profile["baseline_score"]
            score = base + random.uniform(-3, 5)
            score = round(max(0, min(100, score)), 1)
            deviation = round(score - base, 1)

            self._entities.append({
                "id": profile["id"],
                "name": profile["name"],
                "type": etype,
                "ip_address": profile["ip_address"],
                "os": profile["os"],
                "department": profile["department"],
                "baseline_score": base,
                "current_score": score,
                "deviation": deviation,
                "risk_level": _risk_from_score(score).value,
                "last_seen": _now(),
                "alert_count": 0,
                "features": features,
            })

        # Set attack entities to high scores for demo
        attack_scores = {
            "USR-HR-001": 82.0,
            "SRV-FS-002": 76.0,
            "SRV-DC-001": 91.0,
        }
        for e in self._entities:
            if e["id"] in attack_scores:
                s = attack_scores[e["id"]]
                e["current_score"] = s
                e["deviation"] = round(s - e["baseline_score"], 1)
                e["risk_level"] = _risk_from_score(s).value
                e["alert_count"] = random.randint(2, 8)
                e["features"] = _generate_attack_features(e["type"], "lateral_movement")

    def _seed_initial_alerts(self):
        """Create 8 pre-seeded alerts in different states."""
        seeds = [
            ("USR-HR-001",  "user",   82.0, "critical", "BADE", 0,  "open"),
            ("SRV-FS-002",  "server", 76.0, "high",     "BADE", 5,  "investigating"),
            ("SRV-DC-001",  "server", 91.0, "critical", "BADE", 12, "investigating"),
            ("SRV-EMR-001", "server", 55.0, "medium",   "BADE", 18, "open"),
            ("USR-FIN-002", "user",   48.0, "medium",   "BADE", 25, "open"),
            ("USR-ADM-002", "user",   35.0, "low",      "BADE", 40, "resolved"),
            ("OT-SCADA",    "ot_device",70.0,"high",    "BADE", 55, "investigating"),
            ("USR-HR-001",  "user",   68.0, "high",     "AAPA", 60, "investigating"),
        ]
        for eid, etype, score, sev, module, mins, status in seeds:
            template = random.choice([t for t in ALERT_TEMPLATES if t["severity"] == sev] or ALERT_TEMPLATES)
            entity = next((e for e in self._entities if e["id"] == eid), None)
            ename = entity["name"] if entity else eid

            self._alerts.append({
                "id": f"alert-{uuid.uuid4().hex[:8]}",
                "timestamp": _mins_ago(mins),
                "severity": sev,
                "entity_id": eid,
                "entity_name": ename,
                "entity_type": etype,
                "score": score,
                "description": template["description"],
                "module": module,
                "ttps": template["ttps"],
                "status": status,
                "mitre_tactics": template.get("mitre_tactics", []),
                "raw_features": None,
            })

    def _seed_incidents(self):
        """Load the pre-built demo incidents."""
        self._incidents = [
            copy.deepcopy(CURRENT_INCIDENT),
            copy.deepcopy(SECOND_INCIDENT),
        ]

    def _random_walk_scores(self):
        """Apply small random walk to entity scores, with attack entities drifting higher."""
        for e in self._entities:
            drift = random.gauss(0, 0.8)
            if e["id"] in self._attack_entities[:self._attack_step + 1]:
                drift = abs(drift) + random.uniform(0.3, 1.2)  # Trend upward
            e["current_score"] = round(max(0, min(100, e["current_score"] + drift)), 1)
            e["deviation"] = round(e["current_score"] - e["baseline_score"], 1)
            e["risk_level"] = _risk_from_score(e["current_score"]).value
            e["last_seen"] = _now()

    def _generate_alert(self):
        """Generate a new realistic alert."""
        # Occasionally bias toward attack entities for drama
        if random.random() < 0.6 and self._attack_step < len(self._attack_entities):
            target_entity_id = self._attack_entities[self._attack_step]
            attack_entity = next((e for e in self._entities if e["id"] == target_entity_id), None)
            if attack_entity:
                sev = "critical" if attack_entity["current_score"] >= 80 else "high"
                template = random.choice([t for t in ALERT_TEMPLATES if t["severity"] == sev] or ALERT_TEMPLATES)
                self._attack_step = min(self._attack_step + 1, len(self._attack_entities) - 1)
                entity = attack_entity
            else:
                entity = random.choice(self._entities)
                template = random.choice(ALERT_TEMPLATES)
        else:
            entity = random.choice(self._entities)
            template = random.choice(ALERT_TEMPLATES)
            sev = template["severity"]

        self._alert_counter += 1
        alert = {
            "id": f"alert-{uuid.uuid4().hex[:8]}",
            "timestamp": _now(),
            "severity": template["severity"],
            "entity_id": entity["id"],
            "entity_name": entity["name"],
            "entity_type": entity["type"],
            "score": round(entity["current_score"], 1),
            "description": template["description"],
            "module": template["module"],
            "ttps": template["ttps"],
            "status": "open",
            "mitre_tactics": template.get("mitre_tactics", []),
            "raw_features": None,
        }

        # Update entity alert count
        entity["alert_count"] = entity.get("alert_count", 0) + 1

        self._alerts.insert(0, alert)
        if len(self._alerts) > 100:
            self._alerts = self._alerts[:100]

        return alert

    async def _run_loop(self):
        while self._running:
            interval = random.uniform(5, 10)
            await asyncio.sleep(interval)
            if not self._running:
                break
            self._random_walk_scores()
            self._generate_alert()
            # Slightly vary metrics
            self._events_per_second = max(70_000, min(150_000,
                self._events_per_second + random.randint(-2000, 2000)))

    async def start(self):
        self._initialise_entities()
        self._seed_initial_alerts()
        self._seed_incidents()
        self._running = True
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    # ─── Read-only accessors ───────────────────

    def get_alerts(self, limit: int = 50) -> List[Dict]:
        return self._alerts[:limit]

    def get_entities(self) -> List[Dict]:
        return sorted(self._entities, key=lambda e: e["current_score"], reverse=True)

    def get_incidents(self) -> List[Dict]:
        return self._incidents

    def get_incident_by_id(self, incident_id: str) -> Optional[Dict]:
        return next((i for i in self._incidents if i["id"] == incident_id), None)

    def get_metrics(self) -> Dict:
        uptime = (datetime.now(timezone.utc) - self._start_time).total_seconds() / 3600
        return {
            "mttd_hours": self._mttd,
            "mttr_hours": self._mttr,
            "true_positive_rate": self._tpr / 100,
            "false_positive_rate": self._fpr / 100,
            "alerts_today": len(self._alerts),
            "incidents_today": len(self._incidents),
            "automated_containments": self._automated_containments,
            "endpoints_monitored": len(self._entities),
            "events_per_second": self._events_per_second,
            "uptime_hours": round(uptime, 2),
            "last_updated": _now(),
        }

    def update_alert_status(self, alert_id: str, status: str) -> bool:
        for a in self._alerts:
            if a["id"] == alert_id:
                a["status"] = status
                return True
        return False

    def add_incident_action(self, incident_id: str, action: Dict) -> bool:
        for inc in self._incidents:
            if inc["id"] == incident_id:
                inc["actions_taken"].append(action)
                inc["updated_at"] = _now()
                return True
        return False

    def update_action_status(self, incident_id: str, action_id: str, status: str, result: str = "") -> bool:
        for inc in self._incidents:
            if inc["id"] == incident_id:
                for act in inc["actions_taken"]:
                    if act["id"] == action_id:
                        act["status"] = status
                        if result:
                            act["result"] = result
                        inc["updated_at"] = _now()
                        return True
        return False

    def increment_containments(self):
        self._automated_containments += 1


# Singleton
simulator = EventSimulator()
