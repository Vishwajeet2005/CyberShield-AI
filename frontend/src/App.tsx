import { useState, useEffect, useRef, useCallback } from 'react'

// ─── Types ─────────────────────────────────────────────────────────────────────
interface Alert {
  alert_id: string
  entity_id: string
  entity_type: string
  anomaly_score: number
  severity: string
  top_features: string[]
  timestamp: string
  status: string
}

interface AuditEntry {
  log_id: string
  action_type: string
  target: string
  blast_radius: string
  result: string
  written_at: string
}

interface Incident {
  incident_id: string
  title?: string
  severity?: string
  status: string
  actions?: IncidentAction[]
  entity_id?: string
}

interface IncidentAction {
  action_id: string
  name: string
  blast_radius: string
  status: string
  executed: boolean
}

interface CVEEntry {
  cve_id: string
  cvss_base: number
  cvss_adjusted: number
  is_kev: boolean
  severity: string
  description: string
  affected_assets: string[]
  remediation: string
  priority_rank: number
}

interface TopoNode {
  id: string
  label: string
  type: string
  criticality: string
  segment: string
  cves: string[]
}

interface TopoEdge {
  source: string
  target: string
  protocol: string
  port: number
  encrypted: boolean
}

interface Attribution {
  threat_actor?: string
  actor_type?: string
  origin_country?: string
  confidence?: number
  campaign_name?: string
  techniques?: { id: string; name: string; tactic: string }[]
  next_stage?: string[]
  justification?: string
}

interface Metrics {
  mttd?: string
  mttr?: string
  tpr?: string
  fpr?: string
  alerts_today?: number
  containments?: number
}

const API = 'http://localhost:8000'

function tsRelative(ts: string) {
  const diff = Date.now() - new Date(ts).getTime()
  const s = Math.floor(diff / 1000)
  if (s < 60) return `${s}s ago`
  if (s < 3600) return `${Math.floor(s / 60)}m ago`
  return `${Math.floor(s / 3600)}h ago`
}

function tsShort(ts: string) {
  try {
    const d = new Date(ts)
    return d.toISOString().replace('T', ' ').slice(0, 19)
  } catch { return ts }
}

function scoreClass(score: number) {
  if (score >= 80) return 'crit'
  if (score >= 60) return 'high'
  return 'med'
}

// ─── Top Status Bar ─────────────────────────────────────────────────────────
function TopBar({ metrics, alive }: { metrics: Metrics; alive: boolean }) {
  const [clock, setClock] = useState(new Date().toISOString().replace('T', ' ').slice(0, 19))
  useEffect(() => {
    const t = setInterval(() => setClock(new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC'), 1000)
    return () => clearInterval(t)
  }, [])

  return (
    <div className="topbar">
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span className="brand">CYBERSHIELD//AI</span>
        <span style={{ color: '#222' }}>|</span>
        <span style={{ color: alive ? '#3a7d44' : '#8b1a1a', fontSize: 9 }}>
          <span className={alive ? 'blink' : ''}>■</span>&nbsp;{alive ? 'BACKEND ONLINE' : 'BACKEND UNREACHABLE'}
        </span>
      </div>
      <div className="metrics">
        <div className="metric"><span className="metric-label">MTTD</span><span className="metric-value ok">{metrics.mttd ?? '--'}</span></div>
        <div className="metric"><span className="metric-label">MTTR</span><span className="metric-value ok">{metrics.mttr ?? '--'}</span></div>
        <div className="metric"><span className="metric-label">TPR</span><span className="metric-value ok">{metrics.tpr ?? '--'}</span></div>
        <div className="metric"><span className="metric-label">FPR</span><span className="metric-value warn">{metrics.fpr ?? '--'}</span></div>
        <div className="metric"><span className="metric-label">ALERTS/24H</span><span className="metric-value crit">{metrics.alerts_today ?? '--'}</span></div>
        <div className="metric"><span className="metric-label">CONTAINED</span><span className="metric-value ok">{metrics.containments ?? '--'}</span></div>
        <div style={{ color: '#2a2a2a', marginLeft: 8 }}>{clock}</div>
      </div>
    </div>
  )
}

// ─── Sidebar ────────────────────────────────────────────────────────────────
const VIEWS = [
  { id: 'bade',  label: 'BADE — Anomaly Feed' },
  { id: 'aapa',  label: 'AAPA — Attribution' },
  { id: 'airo',  label: 'AIRO — Orchestrator' },
  { id: 'vpa',   label: 'VPA  — Vulnerabilities' },
  { id: 'crdt',  label: 'CRDT — Digital Twin' },
  { id: 'audit', label: 'Audit Log' },
]

function Sidebar({ view, setView }: { view: string; setView: (v: string) => void }) {
  return (
    <div className="sidebar">
      <div className="sidebar-section">
        <div className="sidebar-heading">Modules</div>
        {VIEWS.map(v => (
          <div key={v.id} className={`nav-item ${view === v.id ? 'active' : ''}`} onClick={() => setView(v.id)}>
            <span className="nav-dot" />
            {v.label}
          </div>
        ))}
      </div>
      <div style={{ marginTop: 'auto', padding: '10px 12px', borderTop: '1px solid #1a1a1a' }}>
        <div style={{ fontSize: 9, color: '#2a2a2a', lineHeight: 1.8 }}>
          PHASE 1.5 MODELS<br />
          NSL-KDD: P=97.6% R=63.4%<br />
          UNSW-NB15: P=85.8% R=19.7%<br />
          CICIDS2017: ACTIVE
        </div>
      </div>
    </div>
  )
}

// ─── BADE: Anomaly Feed ──────────────────────────────────────────────────────
function BADEView() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [selected, setSelected] = useState<Alert | null>(null)
  const [threshold, setThreshold] = useState(50)
  const [tick, setTick] = useState(0)

  useEffect(() => {
    const poll = async () => {
      try {
        const r = await fetch(`${API}/api/bade/alerts`)
        if (r.ok) setAlerts(await r.json())
      } catch { /* backend unreachable, keep last state */ }
      setTick(t => t + 1)
    }
    poll()
    const id = setInterval(poll, 3000)
    return () => clearInterval(id)
  }, [])

  const filtered = alerts.filter(a => a.anomaly_score >= threshold)

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', height: '100%', gap: 1 }}>
      <div className="panel" style={{ height: '100%' }}>
        <div className="panel-header">
          <span className="panel-title">BADE — Behavioural Anomaly Detection &nbsp;<span className="blink" style={{ color: '#3a7d44' }}>◆</span></span>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 10, color: '#555' }}>
            <label>SCORE THRESHOLD: <span style={{ color: '#999' }}>{threshold}</span></label>
            <input
              type="range" min={0} max={100} value={threshold}
              onChange={e => setThreshold(+e.target.value)}
              style={{ width: 80, accentColor: '#555', cursor: 'pointer' }}
            />
            <span style={{ color: '#3a3a3a' }}>SHOWING {filtered.length}/{alerts.length}</span>
          </div>
        </div>
        <div className="panel-body">
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ width: 70 }}>SCORE</th>
                <th style={{ width: 70 }}>SEV</th>
                <th>ENTITY</th>
                <th>TYPE</th>
                <th>TOP FEATURES</th>
                <th style={{ width: 80 }}>STATUS</th>
                <th style={{ width: 70 }}>AGE</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr><td colSpan={7} style={{ textAlign: 'center', color: '#2a2a2a', padding: 20 }}>NO EVENTS ABOVE THRESHOLD</td></tr>
              )}
              {filtered.map(a => (
                <tr key={a.alert_id} onClick={() => setSelected(a)}
                  style={{ cursor: 'pointer', background: selected?.alert_id === a.alert_id ? '#141414' : undefined }}>
                  <td>
                    <div className="score-bar">
                      <div className="score-track"><div className={`score-fill ${scoreClass(a.anomaly_score)}`} style={{ width: `${a.anomaly_score}%` }} /></div>
                      <span style={{ color: '#777' }}>{Math.round(a.anomaly_score)}</span>
                    </div>
                  </td>
                  <td><span className={`sev sev-${a.severity}`}>{a.severity}</span></td>
                  <td style={{ color: '#aaa', fontFamily: 'inherit' }}>{a.entity_id}</td>
                  <td style={{ color: '#555' }}>{a.entity_type}</td>
                  <td style={{ color: '#555', maxWidth: 240, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {(a.top_features || []).slice(0, 3).join(' · ')}
                  </td>
                  <td style={{ color: '#444', textTransform: 'uppercase', fontSize: 10 }}>{a.status}</td>
                  <td style={{ color: '#3a3a3a' }}>{tsRelative(a.timestamp)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="footer-bar">
          <span>ISOLATION FOREST ENSEMBLE — 3 NATIVE MODELS ACTIVE</span>
          <span>POLLED {tick}x — INTERVAL 3s</span>
        </div>
      </div>

      {/* Detail Panel */}
      <div className="panel" style={{ height: '100%' }}>
        <div className="panel-header">
          <span className="panel-title">ALERT DETAIL</span>
        </div>
        <div className="panel-body">
          {!selected ? (
            <div style={{ padding: 20, color: '#2a2a2a', fontSize: 11 }}>SELECT ROW TO INSPECT</div>
          ) : (
            <div className="attr-block">
              <div className="attr-field"><span className="attr-key">Alert ID</span><span className="attr-val accent">{selected.alert_id}</span></div>
              <div className="attr-field"><span className="attr-key">Entity</span><span className="attr-val accent">{selected.entity_id}</span></div>
              <div className="attr-field"><span className="attr-key">Type</span><span className="attr-val">{selected.entity_type}</span></div>
              <div className="attr-field"><span className="attr-key">Severity</span><span className={`attr-val sev sev-${selected.severity}`}>{selected.severity}</span></div>
              <div className="attr-field"><span className="attr-key">Score</span><span className="attr-val warn">{selected.anomaly_score.toFixed(2)}</span></div>
              <div className="attr-field"><span className="attr-key">Status</span><span className="attr-val">{selected.status}</span></div>
              <div className="attr-field"><span className="attr-key">Timestamp</span><span className="attr-val" style={{ fontSize: 10 }}>{tsShort(selected.timestamp)}</span></div>
              <div style={{ borderTop: '1px solid #1a1a1a', paddingTop: 8, marginTop: 4 }}>
                <div className="attr-key" style={{ marginBottom: 6 }}>TOP ANOMALOUS FEATURES</div>
                {(selected.top_features || []).map((f, i) => (
                  <div key={i} style={{ padding: '3px 0', color: '#666', fontSize: 11 }}>
                    <span style={{ color: '#3a3a3a', marginRight: 8 }}>{String(i + 1).padStart(2, '0')}</span>{f}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ─── AAPA: Attribution View ──────────────────────────────────────────────────
function AAPAView() {
  const [attr, setAttr] = useState<Attribution | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [input, setInput] = useState(`{
  "id": "SRV-PROD-042",
  "type": "server",
  "features": {
    "duration": 12.5,
    "src_bytes": 98400,
    "dst_bytes": 512,
    "protocol_type": "tcp",
    "flag": "SF"
  }
}`)

  const analyze = async () => {
    setLoading(true)
    setError('')
    try {
      const entity = JSON.parse(input)
      const r = await fetch(`${API}/api/aapa/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entity)
      })
      if (!r.ok) throw new Error(`HTTP ${r.status}`)
      setAttr(await r.json())
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', height: '100%', gap: 1 }}>
      {/* Input */}
      <div className="panel" style={{ height: '100%' }}>
        <div className="panel-header">
          <span className="panel-title">AAPA — ATT&CK ATTRIBUTION INPUT</span>
          <button className="btn btn-neutral" onClick={analyze} disabled={loading}>
            {loading ? 'ANALYZING...' : '► RUN ATTRIBUTION'}
          </button>
        </div>
        <div style={{ padding: 10, display: 'flex', flexDirection: 'column', height: '100%', gap: 8 }}>
          <div style={{ fontSize: 9, color: '#3a3a3a', letterSpacing: '0.1em' }}>
            ENTITY PAYLOAD (JSON) — WILL BE ATTRIBUTED AGAINST MITRE ATT&CK VIA RAG + CLAUDE
          </div>
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            spellCheck={false}
            style={{
              flex: 1,
              background: '#0d0d0d',
              border: '1px solid #1a1a1a',
              color: '#7a9a7a',
              fontFamily: 'JetBrains Mono, monospace',
              fontSize: 11,
              padding: 10,
              resize: 'none',
              outline: 'none',
              lineHeight: 1.6
            }}
          />
          {error && <div style={{ color: '#8b1a1a', fontSize: 10, padding: '4px 0' }}>ERROR: {error}</div>}
        </div>
      </div>

      {/* Attribution Output */}
      <div className="panel" style={{ height: '100%' }}>
        <div className="panel-header">
          <span className="panel-title">RAG OUTPUT — MITRE ATT&CK ATTRIBUTION</span>
          {attr && <span style={{ fontSize: 9, color: '#3a7d44' }}>ATTRIBUTED</span>}
        </div>
        <div className="panel-body">
          {!attr && !loading ? (
            <div style={{ padding: 20, color: '#2a2a2a', fontSize: 11 }}>AWAITING ANALYSIS RUN</div>
          ) : loading ? (
            <div style={{ padding: 20, color: '#555', fontSize: 11 }}>
              <span className="blink">_</span>&nbsp;QUERYING CHROMA DB + CLAUDE...
            </div>
          ) : attr ? (
            <div className="attr-block">
              <div className="attr-field">
                <span className="attr-key">Attributed Actor</span>
                <span className={`attr-val ${attr.threat_actor && attr.threat_actor !== 'Unknown' ? 'danger' : ''}`}>
                  {attr.threat_actor ?? 'Unknown'}
                </span>
              </div>
              <div className="attr-field">
                <span className="attr-key">Actor Type</span>
                <span className="attr-val">{attr.actor_type ?? '--'}</span>
              </div>
              <div className="attr-field">
                <span className="attr-key">Origin Country</span>
                <span className="attr-val warn">{attr.origin_country ?? '--'}</span>
              </div>
              <div className="attr-field">
                <span className="attr-key">Confidence</span>
                <span className="attr-val warn">
                  {attr.confidence != null ? `${(attr.confidence * 100).toFixed(0)}%` : '--'}
                </span>
              </div>
              <div className="attr-field">
                <span className="attr-key">Campaign</span>
                <span className="attr-val">{attr.campaign_name ?? '--'}</span>
              </div>

              {attr.techniques && attr.techniques.length > 0 && (
                <div style={{ marginTop: 8 }}>
                  <div className="attr-key" style={{ marginBottom: 6 }}>MATCHED TECHNIQUES</div>
                  {attr.techniques.map((t, i) => (
                    <div key={i} style={{
                      borderBottom: '1px solid #131313',
                      padding: '4px 0',
                      display: 'grid',
                      gridTemplateColumns: '80px 1fr 80px',
                      gap: 8,
                      fontSize: 11
                    }}>
                      <span style={{ color: '#b8860b', fontWeight: 700 }}>{t.id}</span>
                      <span style={{ color: '#777' }}>{t.name}</span>
                      <span style={{ color: '#444', fontSize: 10 }}>{t.tactic}</span>
                    </div>
                  ))}
                </div>
              )}

              {attr.next_stage && attr.next_stage.length > 0 && (
                <div style={{ marginTop: 8 }}>
                  <div className="attr-key" style={{ marginBottom: 6 }}>PREDICTED NEXT STAGE</div>
                  {attr.next_stage.map((s, i) => (
                    <div key={i} style={{ color: '#8b1a1a', padding: '2px 0', fontSize: 11 }}>
                      <span style={{ color: '#3a3a3a', marginRight: 8 }}>→</span>{s}
                    </div>
                  ))}
                </div>
              )}

              {attr.justification && (
                <div style={{ marginTop: 8 }}>
                  <div className="attr-key" style={{ marginBottom: 6 }}>JUSTIFICATION</div>
                  <div style={{ color: '#555', fontSize: 11, lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>
                    {attr.justification}
                  </div>
                </div>
              )}
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}

// ─── AIRO: Orchestrator ──────────────────────────────────────────────────────
function AIROView() {
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [selected, setSelected] = useState<Incident | null>(null)
  const [approving, setApproving] = useState<string | null>(null)

  useEffect(() => {
    const poll = async () => {
      try {
        const r = await fetch(`${API}/api/airo/incidents`)
        if (r.ok) setIncidents(await r.json())
      } catch { /* keep state */ }
    }
    poll()
    const id = setInterval(poll, 4000)
    return () => clearInterval(id)
  }, [])

  const handleApproval = async (actionId: string, decision: 'approve' | 'deny') => {
    setApproving(actionId)
    try {
      await fetch(`${API}/api/airo/incidents/${selected?.incident_id}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action_id: actionId, decision, approver: 'SOC-ANALYST-01' })
      })
    } catch { /* no-op */ }
    setApproving(null)
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '260px 1fr', height: '100%', gap: 1 }}>
      {/* Incident List */}
      <div className="panel" style={{ height: '100%' }}>
        <div className="panel-header">
          <span className="panel-title">ACTIVE INCIDENTS</span>
          <span style={{ fontSize: 9, color: '#3a7d44' }}>{incidents.length} OPEN</span>
        </div>
        <div className="panel-body">
          {incidents.length === 0 && (
            <div style={{ padding: 16, color: '#2a2a2a', fontSize: 11 }}>NO ACTIVE INCIDENTS</div>
          )}
          {incidents.map(inc => (
            <div key={inc.incident_id}
              onClick={() => setSelected(inc)}
              style={{
                padding: '7px 10px',
                borderBottom: '1px solid #131313',
                cursor: 'pointer',
                background: selected?.incident_id === inc.incident_id ? '#141414' : undefined
              }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className={`sev sev-${inc.severity ?? 'info'}`}>{inc.severity ?? 'INFO'}</span>
                <span style={{ fontSize: 9, color: '#2a2a2a', textTransform: 'uppercase' }}>{inc.status}</span>
              </div>
              <div style={{ color: '#777', marginTop: 4, fontSize: 11, fontFamily: 'inherit' }}>
                {inc.entity_id ?? inc.incident_id}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Incident Detail + Approval Gate */}
      <div className="panel" style={{ height: '100%' }}>
        <div className="panel-header">
          <span className="panel-title">BLAST-RADIUS APPROVAL GATE</span>
          {selected && <span style={{ fontSize: 10, color: '#555' }}>{selected.incident_id}</span>}
        </div>
        <div className="panel-body">
          {!selected ? (
            <div style={{ padding: 20, color: '#2a2a2a', fontSize: 11 }}>SELECT INCIDENT TO REVIEW ACTIONS</div>
          ) : (
            <div style={{ padding: 10, display: 'flex', flexDirection: 'column', gap: 1 }}>
              {(selected.actions ?? []).length === 0 && (
                <div style={{ color: '#2a2a2a', fontSize: 11, padding: 10 }}>NO PENDING ACTIONS FOR THIS INCIDENT</div>
              )}
              {(selected.actions ?? []).map((action, _ai) => (
                <div key={action.action_id ?? _ai} style={{
                  border: '1px solid #1a1a1a',
                  padding: '8px 10px',
                  display: 'grid',
                  gridTemplateColumns: '1fr auto auto auto',
                  alignItems: 'center',
                  gap: 12,
                  background: action.status === 'awaiting_approval' ? '#0f0a0a' : '#0a0a0a'
                }}>
                  <div>
                    <div style={{ color: '#888', fontFamily: 'inherit', fontSize: 11 }}>{action.name}</div>
                    <div style={{ marginTop: 3, fontSize: 9, color: '#2a2a2a' }}>
                      STATUS: <span style={{ color: '#444', textTransform: 'uppercase' }}>{action.status}</span>
                      &nbsp;&nbsp;ACTION: {action.action_id}
                    </div>
                  </div>
                  <span className={`blast-${action.blast_radius}`} style={{ fontSize: 10 }}>
                    {action.blast_radius}-BLAST
                  </span>
                  {action.status === 'awaiting_approval' ? (
                    <>
                      <button
                        className="btn btn-approve"
                        disabled={approving === action.action_id}
                        onClick={() => handleApproval(action.action_id, 'approve')}
                      >
                        {approving === action.action_id ? '...' : 'APPROVE'}
                      </button>
                      <button
                        className="btn btn-deny"
                        disabled={approving === action.action_id}
                        onClick={() => handleApproval(action.action_id, 'deny')}
                      >
                        DENY
                      </button>
                    </>
                  ) : (
                    <span style={{ fontSize: 9, color: action.executed ? '#3a7d44' : '#444', gridColumn: 'span 2', textTransform: 'uppercase' }}>
                      {action.executed ? 'EXECUTED' : 'PENDING'}
                    </span>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ─── VPA: Vulnerabilities ────────────────────────────────────────────────────
function VPAView() {
  const [cves, setCves] = useState<CVEEntry[]>([])
  const [selected, setSelected] = useState<CVEEntry | null>(null)
  const [refreshing, setRefreshing] = useState(false)

  useEffect(() => {
    fetch(`${API}/api/vpa/vulnerabilities`)
      .then(r => r.json())
      .then(d => setCves(Array.isArray(d) ? d : d?.items ?? d?.vulnerabilities ?? []))
      .catch(() => {})
  }, [])

  const refresh = async () => {
    setRefreshing(true)
    try {
      await fetch(`${API}/api/vpa/refresh`, { method: 'POST' })
      const r = await fetch(`${API}/api/vpa/vulnerabilities`)
      if (r.ok) {
        const d = await r.json()
        setCves(Array.isArray(d) ? d : d?.items ?? d?.vulnerabilities ?? [])
      }
    } catch { /* no-op */ }
    setRefreshing(false)
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', height: '100%', gap: 1 }}>
      <div className="panel" style={{ height: '100%' }}>
        <div className="panel-header">
          <span className="panel-title">VPA — VULNERABILITY PRIORITY AGENT &nbsp;(NVD + CISA KEV)</span>
          <button className="btn btn-neutral" onClick={refresh} disabled={refreshing}>
            {refreshing ? 'REFRESHING...' : '⟳ REFRESH FEEDS'}
          </button>
        </div>
        <div className="panel-body">
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ width: 30 }}>#</th>
                <th style={{ width: 120 }}>CVE ID</th>
                <th style={{ width: 55 }}>CVSS</th>
                <th style={{ width: 55 }}>ADJ</th>
                <th style={{ width: 60 }}>SEV</th>
                <th style={{ width: 35 }}>KEV</th>
                <th>DESCRIPTION</th>
              </tr>
            </thead>
            <tbody>
              {cves.length === 0 && (
                <tr><td colSpan={7} style={{ textAlign: 'center', color: '#2a2a2a', padding: 20 }}>
                  NO CVE DATA — CLICK REFRESH FEEDS
                </td></tr>
              )}
              {cves.map((c, i) => (
                <tr key={c.cve_id} onClick={() => setSelected(c)} style={{ cursor: 'pointer', background: selected?.cve_id === c.cve_id ? '#141414' : undefined }}>
                  <td style={{ color: '#2a2a2a' }}>{String(i + 1).padStart(2, '0')}</td>
                  <td style={{ color: '#b8860b', fontWeight: 700 }}>{c.cve_id}</td>
                  <td style={{ color: '#777' }}>{c.cvss_base?.toFixed(1) ?? '--'}</td>
                  <td style={{ color: c.cvss_adjusted > c.cvss_base ? '#cc3333' : '#777' }}>
                    {c.cvss_adjusted?.toFixed(1) ?? '--'}
                  </td>
                  <td><span className={`sev sev-${c.severity}`}>{c.severity}</span></td>
                  <td style={{ color: c.is_kev ? '#cc3333' : '#2a2a2a', fontWeight: c.is_kev ? 700 : 400 }}>
                    {c.is_kev ? 'KEV' : '---'}
                  </td>
                  <td style={{ color: '#555', maxWidth: 300 }}>{c.description?.slice(0, 80)}...</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="footer-bar">
          <span>SOURCE: NVD API v2 + CISA KEV FEED</span>
          <span>{cves.length} CVEs LOADED</span>
        </div>
      </div>

      <div className="panel" style={{ height: '100%' }}>
        <div className="panel-header"><span className="panel-title">CVE DETAIL</span></div>
        <div className="panel-body">
          {!selected ? (
            <div style={{ padding: 20, color: '#2a2a2a', fontSize: 11 }}>SELECT CVE TO INSPECT</div>
          ) : (
            <div className="attr-block">
              <div className="attr-field"><span className="attr-key">CVE ID</span><span className="attr-val accent">{selected.cve_id}</span></div>
              <div className="attr-field"><span className="attr-key">Severity</span><span className={`sev sev-${selected.severity}`}>{selected.severity}</span></div>
              <div className="attr-field"><span className="attr-key">CVSS Base</span><span className="attr-val warn">{selected.cvss_base?.toFixed(1)}</span></div>
              <div className="attr-field"><span className="attr-key">CVSS Adjusted</span><span className={`attr-val ${selected.cvss_adjusted > selected.cvss_base ? 'danger' : 'warn'}`}>{selected.cvss_adjusted?.toFixed(1)}</span></div>
              <div className="attr-field"><span className="attr-key">CISA KEV</span><span className={`attr-val ${selected.is_kev ? 'danger' : ''}`}>{selected.is_kev ? 'YES — ACTIVELY EXPLOITED' : 'NO'}</span></div>
              <div className="attr-field"><span className="attr-key">Priority Rank</span><span className="attr-val">{selected.priority_rank}</span></div>
              <div style={{ marginTop: 8 }}>
                <div className="attr-key" style={{ marginBottom: 6 }}>DESCRIPTION</div>
                <div style={{ color: '#555', fontSize: 11, lineHeight: 1.7 }}>{selected.description}</div>
              </div>
              {selected.affected_assets?.length > 0 && (
                <div style={{ marginTop: 8 }}>
                  <div className="attr-key" style={{ marginBottom: 6 }}>AFFECTED ASSETS</div>
                  {selected.affected_assets.map((a, i) => (
                    <div key={i} style={{ color: '#666', padding: '2px 0', fontSize: 11 }}>
                      <span style={{ color: '#2a2a2a', marginRight: 6 }}>{String(i + 1).padStart(2, '0')}</span>{a}
                    </div>
                  ))}
                </div>
              )}
              {selected.remediation && (
                <div style={{ marginTop: 8 }}>
                  <div className="attr-key" style={{ marginBottom: 6 }}>REMEDIATION</div>
                  <div style={{ color: '#3a7d44', fontSize: 11, lineHeight: 1.7 }}>{selected.remediation}</div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ─── CRDT: Digital Twin ──────────────────────────────────────────────────────
function CRDTView() {
  const [nodes, setNodes] = useState<TopoNode[]>([])
  const [edges, setEdges] = useState<TopoEdge[]>([])
  const [selected, setSelected] = useState<TopoNode | null>(null)
  const svgRef = useRef<SVGSVGElement>(null)

  useEffect(() => {
    fetch(`${API}/api/crdt/topology`)
      .then(r => r.json())
      .then(d => { setNodes(d.nodes ?? []); setEdges(d.edges ?? []) })
      .catch(() => {})
  }, [])

  // Minimal force-free layout — group by segment, stack vertically
  const W = 700, H = 400
  const segments = [...new Set(nodes.map(n => n.segment))].filter(Boolean)
  const segW = segments.length > 0 ? W / segments.length : W

  const pos: Record<string, { x: number; y: number }> = {}
  const segCount: Record<string, number> = {}
  nodes.forEach(n => {
    const si = segments.indexOf(n.segment)
    const idx = segCount[n.segment] ?? 0
    segCount[n.segment] = idx + 1
    pos[n.id] = { x: (si + 0.5) * segW, y: 60 + idx * 60 }
  })

  const CRIT_COLOR: Record<string, string> = { CRITICAL: '#8b1a1a', HIGH: '#6b3a00', MEDIUM: '#5a4a00', LOW: '#3a7d44' }
  const nodeColor = (n: TopoNode) => CRIT_COLOR[n.criticality] ?? '#2a2a2a'

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 280px', height: '100%', gap: 1 }}>
      <div className="panel" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div className="panel-header">
          <span className="panel-title">CRDT — CYBER RESILIENCE DIGITAL TWIN &nbsp;({nodes.length} NODES / {edges.length} EDGES)</span>
        </div>
        <div style={{ flex: 1, overflow: 'hidden', padding: 10 }}>
          {nodes.length === 0 ? (
            <div style={{ color: '#2a2a2a', fontSize: 11 }}>LOADING TOPOLOGY...</div>
          ) : (
            <svg ref={svgRef} width="100%" height="100%" viewBox={`0 0 ${W} ${H}`}
              style={{ background: '#0a0a0a', border: '1px solid #1a1a1a', cursor: 'default' }}>
              {/* Edges */}
              {edges.map((e, i) => {
                const s = pos[e.source], t = pos[e.target]
                if (!s || !t) return null
                return (
                  <line key={i} x1={s.x} y1={s.y} x2={t.x} y2={t.y}
                    stroke={e.encrypted ? '#1a2a1a' : '#2a1a1a'}
                    strokeWidth={1}
                    strokeDasharray={e.encrypted ? undefined : '3 3'}
                  />
                )
              })}
              {/* Segment labels */}
              {segments.map((seg, i) => (
                <text key={seg} x={(i + 0.5) * segW} y={20} textAnchor="middle"
                  fontSize={8} fill="#2a2a2a" fontFamily="JetBrains Mono, monospace"
                  letterSpacing="0.1em">
                  {seg}
                </text>
              ))}
              {/* Nodes */}
              {nodes.map(n => {
                const p = pos[n.id]
                if (!p) return null
                return (
                  <g key={n.id} onClick={() => setSelected(n)} style={{ cursor: 'pointer' }}>
                    <rect x={p.x - 28} y={p.y - 10} width={56} height={20}
                      fill={nodeColor(n)} stroke={selected?.id === n.id ? '#c8c8c8' : 'transparent'}
                      strokeWidth={1}
                    />
                    <text x={p.x} y={p.y + 4} textAnchor="middle"
                      fontSize={8} fill="#aaa" fontFamily="JetBrains Mono, monospace">
                      {n.label?.slice(0, 9)}
                    </text>
                  </g>
                )
              })}
            </svg>
          )}
        </div>
        <div className="footer-bar">
          <span>SOLID LINE = ENCRYPTED &nbsp;|&nbsp; DASHED = UNENCRYPTED</span>
          <span>RED = CRITICAL &nbsp; ORANGE = HIGH &nbsp; YELLOW = MEDIUM &nbsp; GREEN = LOW</span>
        </div>
      </div>

      <div className="panel" style={{ height: '100%' }}>
        <div className="panel-header"><span className="panel-title">NODE DETAIL</span></div>
        <div className="panel-body">
          {!selected ? (
            <div style={{ padding: 20, color: '#2a2a2a', fontSize: 11 }}>CLICK NODE IN GRAPH</div>
          ) : (
            <div className="attr-block">
              <div className="attr-field"><span className="attr-key">Node ID</span><span className="attr-val accent">{selected.id}</span></div>
              <div className="attr-field"><span className="attr-key">Label</span><span className="attr-val">{selected.label}</span></div>
              <div className="attr-field"><span className="attr-key">Type</span><span className="attr-val">{selected.type}</span></div>
              <div className="attr-field"><span className="attr-key">Segment</span><span className="attr-val">{selected.segment}</span></div>
              <div className="attr-field">
                <span className="attr-key">Criticality</span>
                <span className={`sev sev-${selected.criticality}`}>{selected.criticality}</span>
              </div>
              {selected.cves?.length > 0 && (
                <div style={{ marginTop: 8 }}>
                  <div className="attr-key" style={{ marginBottom: 6 }}>LINKED CVEs ({selected.cves.length})</div>
                  {selected.cves.map((c, i) => (
                    <div key={i} style={{ color: '#b8860b', padding: '2px 0', fontSize: 11 }}>{c}</div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ─── Audit Log ───────────────────────────────────────────────────────────────
function AuditView() {
  const [logs, setLogs] = useState<AuditEntry[]>([])
  const [page, setPage] = useState(0)
  const PAGE = 50

  const load = useCallback(async (p: number) => {
    try {
      const r = await fetch(`${API}/api/airo/audit?limit=${PAGE}&offset=${p * PAGE}`)
      if (r.ok) setLogs(await r.json())
    } catch { /* no-op */ }
  }, [])

  useEffect(() => { load(page) }, [page, load])

  const RESULT_COLOR: Record<string, string> = { success: '#3a7d44', failed: '#8b1a1a', queued: '#b8860b', rejected: '#555' }

  return (
    <div className="panel" style={{ height: '100%' }}>
      <div className="panel-header">
        <span className="panel-title">IMMUTABLE AUDIT LOG — AIRO ACTION HISTORY</span>
        <div style={{ display: 'flex', gap: 6 }}>
          <button className="btn btn-neutral" disabled={page === 0} onClick={() => setPage(p => Math.max(0, p - 1))}>PREV</button>
          <span style={{ fontSize: 10, color: '#444', padding: '3px 6px' }}>PAGE {page + 1}</span>
          <button className="btn btn-neutral" onClick={() => setPage(p => p + 1)}>NEXT</button>
        </div>
      </div>
      <div className="panel-body">
        <table className="data-table">
          <thead>
            <tr>
              <th style={{ width: 60 }}>LOG ID</th>
              <th style={{ width: 160 }}>TIMESTAMP (UTC)</th>
              <th>ACTION TYPE</th>
              <th>TARGET</th>
              <th style={{ width: 70 }}>BLAST</th>
              <th style={{ width: 70 }}>RESULT</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 && (
              <tr><td colSpan={6} style={{ textAlign: 'center', color: '#2a2a2a', padding: 20 }}>NO AUDIT RECORDS FOUND</td></tr>
            )}
            {logs.map(l => (
              <tr key={l.log_id}>
                <td style={{ color: '#3a3a3a', fontFamily: 'inherit' }}>{l.log_id?.slice(-6)}</td>
                <td style={{ color: '#3a3a3a', fontFamily: 'inherit', fontSize: 10 }}>{tsShort(l.written_at)}</td>
                <td style={{ color: '#777', textTransform: 'uppercase', fontSize: 10 }}>{l.action_type}</td>
                <td style={{ color: '#555' }}>{l.target}</td>
                <td><span className={`blast-${l.blast_radius}`}>{l.blast_radius}</span></td>
                <td style={{ color: RESULT_COLOR[l.result?.toLowerCase()] ?? '#444', fontWeight: 700, textTransform: 'uppercase', fontSize: 10 }}>
                  {l.result}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="footer-bar">
        <span>WRITE-ONCE SQLITE LOG — FORENSIC CHAIN OF CUSTODY</span>
        <span>SHOWING {logs.length} ENTRIES — OFFSET {page * PAGE}</span>
      </div>
    </div>
  )
}

// ─── Root App ────────────────────────────────────────────────────────────────
export default function App() {
  const [view, setView] = useState('bade')
  const [metrics, setMetrics] = useState<Metrics>({})
  const [alive, setAlive] = useState(false)

  useEffect(() => {
    const poll = async () => {
      try {
        const r = await fetch(`${API}/api/system/metrics`, { signal: AbortSignal.timeout(2000) })
        if (r.ok) { setMetrics(await r.json()); setAlive(true) }
        else setAlive(false)
      } catch { setAlive(false) }
    }
    poll()
    const id = setInterval(poll, 5000)
    return () => clearInterval(id)
  }, [])

  const PANELS: Record<string, JSX.Element> = {
    bade:  <BADEView />,
    aapa:  <AAPAView />,
    airo:  <AIROView />,
    vpa:   <VPAView />,
    crdt:  <CRDTView />,
    audit: <AuditView />,
  }

  return (
    <div className="shell">
      <TopBar metrics={metrics} alive={alive} />
      <Sidebar view={view} setView={setView} />
      <div className="main" style={{ gap: 0 }}>
        {PANELS[view] ?? null}
      </div>
    </div>
  )
}
