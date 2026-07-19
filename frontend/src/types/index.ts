export type Severity = 'critical' | 'high' | 'medium' | 'low';
export type AlertStatus = 'new' | 'investigating' | 'resolved' | 'dismissed';
export type IncidentStatus = 'open' | 'contained' | 'resolved' | 'closed';
export type ActionStatus = 'pending' | 'executing' | 'completed' | 'failed' | 'awaiting_approval';

export interface Alert {
  id: string;
  title: string;
  description: string;
  severity: Severity;
  module: string;
  entityId: string;
  entityName: string;
  ipAddress?: string;
  timestamp: string;
  status: AlertStatus;
}

export interface Entity {
  id: string;
  name: string;
  type: string;
  ipAddress: string;
  department: string;
  baselineScore: number;
  currentScore: number;
  deviation: number;
  riskLevel: Severity;
  lastSeen: string;
}

export interface Incident {
  id: string;
  title: string;
  severity: Severity;
  status: IncidentStatus;
  affectedEntities: string[];
  currentStep: string;
  timeline: { timestamp: string; action: string }[];
}

export interface PlaybookAction {
  id: string;
  stepNumber: number;
  name: string;
  blastRadius: Severity;
  status: ActionStatus;
  executionTimeMs?: number;
}

export interface AuditEntry {
  id: string;
  timestamp: string;
  module: string;
  action: string;
  actor: string;
  target: string;
  result: string;
  hash: string;
}

export interface CVEItem {
  id: string;
  cveId: string;
  description: string;
  cvssScore: number;
  severity: Severity;
  contextScore: number;
  isKev: boolean;
  actorTargeted: boolean;
  affectedAssetsCount: number;
  remediationPriority: number;
}

export interface AssetItem {
  id: string;
  name: string;
  type: string;
  criticality: Severity;
  cveCount: number;
}

export interface ThreatActor {
  id: string;
  name: string;
  country: string;
  confidence: number;
  matchedTtps: string[];
  evidenceSummary: string;
  isPrimary: boolean;
}

export interface Attribution {
  id: string;
  actors: ThreatActor[];
}

export interface NetworkNode {
  id: string;
  label: string;
  type: 'server' | 'workstation' | 'ot' | 'external';
  criticality: number;
  status: 'protected' | 'weak' | 'unprotected' | 'compromised';
  isChokepoint: boolean;
}

export interface NetworkEdge {
  source: string;
  target: string;
  status: 'protected' | 'weak' | 'unprotected';
}

export interface AttackPath {
  nodes: NetworkNode[];
  edges: NetworkEdge[];
}

export interface SystemMetrics {
  mttd: string;
  mttr: string;
  tpr: string;
  fpr: string;
  alertsToday: number;
  containments: number;
}
