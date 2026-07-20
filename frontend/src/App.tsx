import { useState, useEffect } from 'react'
import BADEView from './pages/BADEView'
import AAPAView from './pages/AAPAView'
import AIROView from './pages/AIROView'
import VPAView from './pages/VPAView'
import CRDTView from './pages/CRDTView'
import AuditLogView from './pages/AuditLogView'

const API = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

interface Metrics {
  tpr?: string | number
  fpr?: string | number
  mttd_hours?: number
  mttr_hours?: number
  true_positive_rate?: number
  false_positive_rate?: number
  alerts_today?: number
  containments?: number
}

const VIEWS = [
  { id: 'bade',  label: 'BADE', icon: 'security' },
  { id: 'aapa',  label: 'AAPA', icon: 'shield' },
  { id: 'airo',  label: 'AIRO', icon: 'memory' },
  { id: 'vpa',   label: 'VPA', icon: 'visibility' },
  { id: 'crdt',  label: 'CRDT', icon: 'analytics' },
  { id: 'audit', label: 'AUDIT LOG', icon: 'terminal' },
]

export default function App() {
  const [view, setView] = useState('bade')
  const [metrics, setMetrics] = useState<Metrics>({})
  const [alive, setAlive] = useState(false)
  const [clock, setClock] = useState(new Date().toISOString().replace('T', ' ').slice(0, 19))

  useEffect(() => {
    const t = setInterval(() => setClock(new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC'), 1000)
    return () => clearInterval(t)
  }, [])

  useEffect(() => {
    const poll = async () => {
      try {
        const r = await fetch(`${API}/api/system/metrics`)
        if (r.ok) {
          setMetrics(await r.json())
          setAlive(true)
        } else {
          setAlive(false)
        }
      } catch {
        setAlive(false)
      }
    }
    poll()
    const id = setInterval(poll, 10000)
    return () => clearInterval(id)
  }, [])

  return (
    <div className="bg-background text-on-surface font-body-lg min-h-screen w-full flex overflow-hidden">
      {/* SideNavBar */}
      <nav className="w-64 shrink-0 h-screen bg-background dark:bg-background border-r border-outline-variant flex flex-col z-20">
        <div className="p-md border-b border-outline-variant flex flex-col gap-xs">
          <h1 className="font-headline-sm text-headline-sm font-bold text-primary dark:text-primary tracking-tighter">SOC-PRIME</h1>
          <p className="font-code-table text-code-table text-on-surface-variant">NODE-01.SYSTEM.RESILIENCE</p>
        </div>
        <div className="flex-1 overflow-y-auto py-sm">
          <ul className="flex flex-col">
            {VIEWS.map(v => (
              <li key={v.id}>
                <button
                  onClick={() => setView(v.id)}
                  className={`w-full flex items-center gap-md px-md py-sm ${
                    view === v.id
                      ? 'bg-primary text-on-primary font-bold border-y border-outline'
                      : 'text-on-surface hover:bg-surface-container-high transition-none'
                  }`}
                >
                  <span className="material-symbols-outlined font-code-table text-code-table">{v.icon}</span>
                  <span className="font-code-table text-code-table">{v.label}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      </nav>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-screen min-w-0">
        {/* TopAppBar */}
        <header className="flex justify-between items-center h-12 px-md border-b border-outline-variant w-full bg-background dark:bg-background z-10 shrink-0 overflow-x-auto whitespace-nowrap">
          <div className="font-label-caps text-label-caps font-bold text-primary dark:text-primary flex items-center gap-2">
            SOC-PRIME // RESILIENCE PLATFORM
            <span style={{ color: alive ? '#3a7d44' : '#ffb4ab', fontSize: 10, marginLeft: 16 }}>
              <span className={alive ? 'blink-cursor' : ''}>■</span> {alive ? 'SYSTEM ONLINE' : 'SYSTEM OFFLINE'}
            </span>
          </div>
          <div className="flex items-center gap-lg">
            <div className="flex items-center gap-md font-code-table text-code-table text-on-surface-variant">
              <span className="hover:text-primary cursor-pointer" title="Mean Time To Detect">MTTD: {metrics.mttd_hours !== undefined ? `${metrics.mttd_hours.toFixed(1)}h` : '--'}</span>
              <span className="hover:text-primary cursor-pointer" title="Mean Time To Respond">MTTR: {metrics.mttr_hours !== undefined ? `${metrics.mttr_hours.toFixed(1)}h` : '--'}</span>
              <span className="hover:text-primary cursor-pointer" title="True Positive Rate">TPR: {metrics.true_positive_rate !== undefined ? `${(metrics.true_positive_rate * 100).toFixed(1)}%` : '--'}</span>
              <span className="hover:text-primary cursor-pointer text-error" title="False Positive Rate">FPR: {metrics.false_positive_rate !== undefined ? `${(metrics.false_positive_rate * 100).toFixed(1)}%` : '--'}</span>
            </div>
            <div className="flex items-center gap-sm text-on-surface-variant border-l border-outline-variant pl-md ml-sm h-12">
              <span className="font-code-table text-code-table mr-4">{clock}</span>

            </div>
          </div>
        </header>

        {/* Canvas */}
        <main className="flex-1 overflow-auto p-md grid-bg flex flex-col gap-md">
          {view === 'bade' && <BADEView />}
          {view === 'aapa' && <AAPAView />}
          {view === 'airo' && <AIROView />}
          {view === 'vpa' && <VPAView />}
          {view === 'crdt' && <CRDTView />}
          {view === 'audit' && <AuditLogView />}
        </main>
      </div>
    </div>
  )
}
