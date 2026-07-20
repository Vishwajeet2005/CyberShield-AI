"""
CyberShield AI — Pydantic Data Models
All request/response schemas for the 5 modules.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ─────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class AlertStatus(str, Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

class IncidentStatus(str, Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RESOLVED = "resolved"

class ActionStatus(str, Enum):
    PENDING = "pending"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"

class BlastRadius(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class EntityType(str, Enum):
    USER = "user"
    SERVER = "server"
    WORKSTATION = "workstation"
    OT_DEVICE = "ot_device"
    SERVICE_ACCOUNT = "service_account"
    NETWORK_DEVICE = "network_device"

class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NORMAL = "normal"

class RemediationPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ─────────────────────────────────────────────
# BADE — Behavioural Anomaly Detection Engine
# ─────────────────────────────────────────────

class Alert(BaseModel):
    id: str
    timestamp: str
    severity: Severity
    entity_id: str
    entity_name: str
    entity_type: str
    score: float = Field(ge=0, le=100, description="Anomaly score 0-100")
    description: str
    module: str = "BADE"
    ttps: List[str] = []
    status: AlertStatus = AlertStatus.OPEN
    mitre_tactics: List[str] = []
    raw_features: Optional[Dict[str, float]] = None

class Entity(BaseModel):
    id: str
    name: str
    type: EntityType
    ip_address: str
    os: str
    department: str
    baseline_score: float = Field(ge=0, le=100)
    current_score: float = Field(ge=0, le=100)
    deviation: float
    risk_level: RiskLevel
    last_seen: str
    alert_count: int = 0
    features: Optional[Dict[str, float]] = None

class TimelineEvent(BaseModel):
    id: str
    timestamp: str
    event_type: str
    entity_id: str
    entity_name: str
    severity: Severity
    description: str
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    process: Optional[str] = None

class FeedbackRequest(BaseModel):
    alert_id: str
    feedback_type: str  # "true_positive" | "false_positive"
    analyst_notes: Optional[str] = None

class IsolateRequest(BaseModel):
    alert_id: str
    entity_id: str

class FeedbackResponse(BaseModel):
    success: bool
    message: str
    alert_id: str
    new_score: Optional[float] = None


# ─────────────────────────────────────────────
# AAPA — APT Attribution & Prediction Agent
# ─────────────────────────────────────────────

class ThreatActor(BaseModel):
    id: str
    name: str
    aliases: List[str] = []
    origin: str
    motivation: str
    targets: List[str]
    ttps: List[str]
    campaigns: List[str]
    confidence: float = Field(ge=0, le=100)
    last_seen: str
    description: str
    iocs: List[str] = []

class Attribution(BaseModel):
    actor_id: str
    actor_name: str
    origin: str
    confidence: float = Field(ge=0, le=100)
    matched_ttps: List[str]
    unmatched_ttps: List[str] = []
    predicted_next_moves: List[Dict[str, Any]] = []
    evidence: str
    rank: int = 1

class NextMove(BaseModel):
    ttp_id: str
    ttp_name: str
    tactic: str
    probability: float = Field(ge=0, le=1)
    description: str
    recommendation: str
    urgency: str  # "immediate" | "high" | "medium"

class TTpAnalysisRequest(BaseModel):
    ttps: List[str]
    context: Optional[str] = None

class TTpAnalysisResponse(BaseModel):
    observed_ttps: List[str]
    attributions: List[Attribution]
    next_moves: List[NextMove]
    confidence_summary: str
    analysis_timestamp: str


# ─────────────────────────────────────────────
# AIRO — Autonomous Incident Response Orchestrator
# ─────────────────────────────────────────────

class PlaybookStep(BaseModel):
    id: str
    name: str
    description: str
    action_type: str
    blast_radius: BlastRadius
    auto_execute: bool
    timeout_seconds: int
    status: ActionStatus = ActionStatus.PENDING
    executed_at: Optional[str] = None
    execution_time_ms: Optional[int] = None
    result: Optional[str] = None

class Playbook(BaseModel):
    id: str
    name: str
    description: str
    trigger_conditions: List[str]
    steps: List[PlaybookStep]
    estimated_containment_seconds: int
    blast_radius_summary: str

class PlaybookAction(BaseModel):
    id: str
    incident_id: str
    playbook_id: str
    action_type: str
    target: str
    status: ActionStatus
    blast_radius: BlastRadius
    executed_at: Optional[str] = None
    approved_by: Optional[str] = None
    execution_time_ms: Optional[int] = None
    result: Optional[str] = None
    rollback_available: bool = True

class Incident(BaseModel):
    id: str
    title: str
    severity: Severity
    status: IncidentStatus
    created_at: str
    updated_at: str
    affected_entities: List[str]
    ttps: List[str]
    playbook_id: Optional[str] = None
    actions_taken: List[PlaybookAction] = []
    blast_radius: BlastRadius
    attribution: Optional[str] = None
    cert_in_reported: bool = False
    mttd_minutes: Optional[float] = None

class ExecuteActionRequest(BaseModel):
    incident_id: str
    action_id: str
    actor: str = "system"

class ApproveActionRequest(BaseModel):
    action_id: str
    approver: str
    decision: str  # "approve" | "reject"
    notes: Optional[str] = None

class AuditEntry(BaseModel):
    id: int
    timestamp: str
    action: str
    actor: str
    target: str
    result: str
    hash: str
    previous_hash: str
    module: str

class CertInReport(BaseModel):
    report_id: str
    generated_at: str
    organization_name: str
    nic_contact: str
    incident_type: str
    affected_systems: List[str]
    date_time_discovered: str
    date_time_reported: str
    attack_vector: str
    impact_description: str
    initial_response_actions: List[str]
    requested_assistance: str
    mandatory_fields_complete: bool
    reporting_deadline: str


# ─────────────────────────────────────────────
# VPA — Vulnerability Prioritisation Agent
# ─────────────────────────────────────────────

class CVEItem(BaseModel):
    cve_id: str
    description: str
    cvss_score: float = Field(ge=0, le=10)
    cvss_vector: Optional[str] = None
    severity: Severity
    affected_assets: List[str] = []
    published_date: str
    is_kev: bool = False
    kev_date_added: Optional[str] = None
    exploit_exists: bool = False
    actor_targeted: bool = False
    context_score: float = Field(ge=0, le=100)
    remediation_priority: RemediationPriority
    patch_available: bool = True
    patch_url: Optional[str] = None
    network_exposed: bool = False
    has_compensating_control: bool = False

class AssetItem(BaseModel):
    id: str
    hostname: str
    ip: str
    os: str
    department: str
    criticality: int = Field(ge=1, le=10)
    vulnerabilities_count: int = 0
    critical_vuln_count: int = 0
    patch_level: str  # "current" | "1-month" | "3-month" | "6-month+" | "eol"
    network_segment: str
    last_scanned: str
    business_function: str

class KEVMatch(BaseModel):
    cve_id: str
    vulnerability_name: str
    affected_assets: List[str]
    date_added_to_kev: str
    required_action: str
    action_deadline: str
    context_score: float


# ─────────────────────────────────────────────
# CRDT — Cyber Resilience Digital Twin
# ─────────────────────────────────────────────

class NetworkNode(BaseModel):
    id: str
    label: str
    type: str  # external | perimeter | server | workstation | ot | cloud
    ip: str
    vulnerabilities: List[str] = []
    controls: List[str] = []
    criticality: int = Field(ge=1, le=10)
    os: Optional[str] = None
    department: Optional[str] = None
    is_chokepoint: bool = False

class NetworkEdge(BaseModel):
    source: str
    target: str
    protocol: str
    port: int
    encrypted: bool
    firewall_protected: bool
    bandwidth: Optional[str] = None

class AttackPath(BaseModel):
    path_nodes: List[str]
    path_edges: List[Dict[str, str]]
    risk_score: float
    effort: str  # "low" | "medium" | "high"
    description: str
    step_count: int
    weakest_control: Optional[str] = None

class Chokepoint(BaseModel):
    node_id: str
    node_label: str
    betweenness_centrality: float
    paths_through: int
    controls: List[str]
    recommendation: str

class ScenarioRequest(BaseModel):
    scenario_name: str

class ScenarioResult(BaseModel):
    scenario_name: str
    description: str
    entry_point: str
    target: str
    attack_paths: List[AttackPath]
    chokepoints: List[Chokepoint]
    ttp_chain: List[str]
    risk_level: str
    recommended_mitigations: List[str]


# ─────────────────────────────────────────────
# System / Metrics
# ─────────────────────────────────────────────

class SystemMetrics(BaseModel):
    mttd_hours: float
    mttr_hours: float
    true_positive_rate: float  # 0-1
    false_positive_rate: float  # 0-1
    alerts_today: int
    incidents_today: int
    automated_containments: int
    endpoints_monitored: int
    events_per_second: int
    uptime_hours: float
    last_updated: str

class ModuleStatus(BaseModel):
    name: str
    status: str  # "operational" | "degraded" | "offline"
    last_heartbeat: str
    processed_events: int
    error_count: int

class SystemStatus(BaseModel):
    platform: str
    version: str
    overall_status: str
    uptime_hours: float
    modules: List[ModuleStatus]
    timestamp: str
