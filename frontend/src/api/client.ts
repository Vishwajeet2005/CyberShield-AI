import axios from 'axios';
import { 
  Alert, Entity, Incident, PlaybookAction, AuditEntry, CVEItem, 
  AssetItem, ThreatActor, Attribution, AttackPath, SystemMetrics 
} from '../types';

const API_BASE = 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 5000,
});

// Mock Data Generators (Fallbacks)
const getMockAlerts = (): Alert[] => ([
  { id: '1', title: 'Suspicious Lateral Movement', description: 'Multiple RDP sessions initiated from HR desktop.', severity: 'critical', module: 'BADE', entityId: 'e1', entityName: 'WORKSTATION-HR-01', ipAddress: '10.0.1.45', timestamp: new Date().toISOString(), status: 'new' },
  { id: '2', title: 'Failed Login Anomalies', description: '50+ failed logins for Admin account.', severity: 'high', module: 'BADE', entityId: 'e2', entityName: 'DOMAIN-CONTROLLER-01', ipAddress: '10.0.0.5', timestamp: new Date(Date.now() - 300000).toISOString(), status: 'investigating' }
]);

export const api = {
  // System
  getStatus: async () => client.get('/system/status').catch(() => ({ data: { status: 'mock' } })),
  getMetrics: async (): Promise<SystemMetrics> => client.get('/system/metrics').then(r => r.data).catch(() => ({
    mttd: '4m 12s', mttr: '12m 45s', tpr: '98.2%', fpr: '1.4%', alertsToday: 142, containments: 12
  })),

  // BADE
  getAlerts: async (): Promise<Alert[]> => client.get('/bade/alerts').then(r => r.data).catch(() => getMockAlerts()),
  getEntities: async (): Promise<Entity[]> => client.get('/bade/entities').then(r => r.data).catch(() => []),
  getTimeline: async () => client.get('/bade/timeline').catch(() => ({ data: [] })),
  submitFeedback: async (alertId: string, feedbackType: string) => client.post(`/bade/feedback`, { alertId, feedbackType }),

  // AAPA
  getAttribution: async (): Promise<Attribution> => client.get('/aapa/attribution').then(r => r.data).catch(() => ({ id: '1', actors: [] })),
  getActors: async (): Promise<ThreatActor[]> => client.get('/aapa/actors').then(r => r.data).catch(() => []),
  getNextMoves: async (actorId: string) => client.get(`/aapa/actors/${actorId}/next-moves`).then(r => r.data).catch(() => []),
  analyzeTTPs: async (ttps: string[]) => client.post('/aapa/analyze', { ttps }).then(r => r.data).catch(() => ({})),

  // AIRO
  getIncidents: async (): Promise<Incident[]> => client.get('/airo/incidents').then(r => r.data).catch(() => []),
  getPlaybooks: async () => client.get('/airo/playbooks').then(r => r.data).catch(() => []),
  executeAction: async (incidentId: string, actionId: string) => client.post(`/airo/incidents/${incidentId}/execute`, { actionId }),
  approveAction: async (actionId: string, approver: string) => client.post(`/airo/actions/${actionId}/approve`, { approver }),
  getAuditLog: async (limit: number, offset: number): Promise<AuditEntry[]> => client.get(`/airo/audit?limit=${limit}&offset=${offset}`).then(r => r.data).catch(() => []),
  getCertInReport: async (incidentId: string) => client.get(`/airo/incidents/${incidentId}/report`).then(r => r.data).catch(() => ({})),

  // VPA
  getVulnerabilities: async (): Promise<CVEItem[]> => client.get('/vpa/vulnerabilities').then(r => r.data).catch(() => []),
  getAssets: async (): Promise<AssetItem[]> => client.get('/vpa/assets').then(r => r.data).catch(() => []),
  getKevStatus: async () => client.get('/vpa/kev-status').then(r => r.data).catch(() => ({ hasKev: false, count: 0 })),
  refreshFeeds: async () => client.post('/vpa/refresh-feeds').then(r => r.data),

  // CRDT
  getTopology: async (): Promise<AttackPath> => client.get('/crdt/topology').then(r => r.data).catch(() => ({ nodes: [], edges: [] })),
  getAttackPaths: async (source: string, target: string) => client.get(`/crdt/paths?source=${source}&target=${target}`).then(r => r.data).catch(() => []),
  getChokepoints: async () => client.get('/crdt/chokepoints').then(r => r.data).catch(() => []),
  runScenario: async (name: string) => client.post('/crdt/scenario', { name }).then(r => r.data).catch(() => ({}))
};
