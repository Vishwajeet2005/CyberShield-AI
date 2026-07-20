import { useState, useEffect } from 'react'

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

const API = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

function tsRelative(ts: string) {
  if (!ts) return 'UNKNOWN'
  const diff = Date.now() - new Date(ts).getTime()
  if (Number.isNaN(diff)) return 'UNKNOWN'
  const s = Math.floor(diff / 1000)
  if (s < 60) return `${s}s ago`
  if (s < 3600) return `${Math.floor(s / 60)}m ago`
  return `${Math.floor(s / 3600)}h ago`
}

export default function BADEView() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [selected, setSelected] = useState<Alert | null>(null)
  const [filter, setFilter] = useState('')

  useEffect(() => {
    const poll = async () => {
      try {
        const r = await fetch(`${API}/api/bade/alerts`)
        if (r.ok) setAlerts(await r.json())
      } catch { /* backend unreachable, keep last state */ }
    }
    poll()
    const id = setInterval(poll, 3000)
    return () => clearInterval(id)
  }, [])

  const safeAlerts = Array.isArray(alerts) ? alerts : []
  const filtered = safeAlerts.filter(a => 
    (a.entity_id || '').includes(filter) || (a.entity_type || '').includes(filter)
  )
  const criticalCount = safeAlerts.filter(a => (a.anomaly_score || 0) >= 80).length
  const warningCount = safeAlerts.filter(a => (a.anomaly_score || 0) >= 60 && (a.anomaly_score || 0) < 80).length

  return (
    <>
      {/* Page Header */}
      <div className="flex justify-between items-end border-b border-outline-variant pb-sm">
        <div>
          <h2 className="font-display-lg text-display-lg text-primary">BEHAVIOURAL ANOMALY DETECTION ENGINE</h2>
          <p className="font-code-table text-code-table text-on-surface-variant mt-xs">&gt; MONITORING NETWORK ENTITIES [ACTIVE]</p>
        </div>
        <div className="flex gap-sm">
          <div className="border border-outline-variant px-sm py-xs font-code-table text-code-table flex items-center gap-xs">
            <span className="text-error">●</span> CRITICAL: {criticalCount}
          </div>
          <div className="border border-outline-variant px-sm py-xs font-code-table text-code-table flex items-center gap-xs">
            <span className="text-surface-tint">●</span> WARNING: {warningCount}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-md flex-1 overflow-hidden">
        {/* Main Data Table Container */}
        <div className="col-span-12 xl:col-span-8 border border-outline-variant bg-surface-container flex flex-col h-full">
          <div className="border-b border-outline-variant p-sm bg-surface-container-high flex justify-between items-center">
            <span className="font-label-caps text-label-caps text-primary">[ ENTITY RISK MATRIX ]</span>
            <div className="flex gap-sm">
              <input
                className="bg-surface text-on-surface border border-outline-variant font-code-table text-code-table px-sm py-xs w-48 focus:border-primary focus:outline-none focus:ring-0 placeholder:text-outline"
                placeholder="[ / FILTER ]"
                type="text"
                value={filter}
                onChange={e => setFilter(e.target.value)}
              />
            </div>
          </div>
          <div className="flex-1 overflow-auto">
            <table className="w-full text-left border-collapse">
              <thead className="bg-surface-container-high font-code-table text-code-table text-on-surface border-b border-outline-variant sticky top-0">
                <tr>
                  <th className="p-sm font-normal">ENTITY ID</th>
                  <th className="p-sm font-normal">TYPE</th>
                  <th className="p-sm font-normal">CURRENT</th>
                  <th className="p-sm font-normal">AGE</th>
                  <th className="p-sm font-normal">RISK LVL</th>
                </tr>
              </thead>
              <tbody className="font-code-table text-code-table">
                {filtered.length === 0 && (
                  <tr>
                    <td colSpan={5} className="p-md text-center text-outline">NO EVENTS FOUND</td>
                  </tr>
                )}
                {filtered.map(a => {
                  const isCrit = a.anomaly_score >= 80
                  const isHigh = a.anomaly_score >= 60 && !isCrit
                  return (
                    <tr
                      key={a.alert_id}
                      onClick={() => setSelected(a)}
                      className={`border-b border-outline-variant cursor-pointer ${
                        selected?.alert_id === a.alert_id ? 'bg-surface-container-highest' :
                        isCrit ? 'bg-error-container/20 hover:bg-surface-container-high' : 'hover:bg-surface-container-high'
                      }`}
                    >
                      <td className={`p-sm font-bold ${isCrit ? 'text-error' : 'text-on-surface'}`}>
                        {a.entity_id || 'UNKNOWN'} {selected?.alert_id === a.alert_id && <span className="blink-cursor">_</span>}
                      </td>
                      <td className="p-sm">{a.entity_type || 'UNKNOWN'}</td>
                      <td className={`p-sm ${isCrit ? 'text-error' : isHigh ? 'text-surface-tint' : ''}`}>
                        {(a.anomaly_score || 0).toFixed(1)}
                      </td>
                      <td className="p-sm">{tsRelative(a.timestamp || '')}</td>
                      <td className="p-sm">
                        {isCrit ? (
                          <span className="bg-error text-on-error px-xs py-[2px]">[ CRITICAL ]</span>
                        ) : isHigh ? (
                          <span>[ HIGH ]</span>
                        ) : (
                          <span className="text-outline">[ NOMINAL ]</span>
                        )}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Side Panel (Charts & Details) */}
        <div className="col-span-12 xl:col-span-4 flex flex-col gap-md h-full">
          {/* Trend Chart Module (Simplified) */}
          <div className="border border-outline-variant bg-surface-container flex flex-col flex-1 min-h-0">
            <div className="border-b border-outline-variant p-sm bg-surface-container-high flex justify-between items-center">
              <span className="font-label-caps text-label-caps text-primary">[ GLOBAL ANOMALY TREND ]</span>
              <span className="font-code-table text-code-table text-outline">T-1H</span>
            </div>
            <div className="flex-1 p-sm relative">
              <svg className="w-full h-full" preserveAspectRatio="none" viewBox="0 0 100 100">
                <line stroke="#353434" strokeDasharray="2,2" strokeWidth="0.5" x1="0" x2="100" y1="25" y2="25"></line>
                <line stroke="#353434" strokeDasharray="2,2" strokeWidth="0.5" x1="0" x2="100" y1="50" y2="50"></line>
                <line stroke="#353434" strokeDasharray="2,2" strokeWidth="0.5" x1="0" x2="100" y1="75" y2="75"></line>
                <polyline fill="none" points="0,70 10,65 20,68 30,50 40,55 50,30 60,35 70,15 80,40 90,20 100,5" stroke="#c6c6c6" strokeWidth="1"></polyline>
                <line stroke="#ffb4ab" strokeDasharray="4,2" strokeWidth="1" x1="0" x2="100" y1="20" y2="20"></line>
              </svg>
              {criticalCount > 0 && (
                <div className="absolute top-sm right-sm font-code-table text-code-table text-error bg-surface border border-error px-xs py-[2px]">
                  SPIKE DETECTED
                </div>
              )}
            </div>
          </div>

          {/* Selected Entity Details */}
          <div className="border border-outline-variant bg-surface-container flex flex-col flex-1 min-h-0">
            <div className="border-b border-outline-variant p-sm bg-primary text-on-primary flex justify-between items-center">
              <span className="font-label-caps text-label-caps font-bold">[ TARGET ACQUIRED ]</span>
              <span className="font-code-table text-code-table">{selected ? `ID: ${selected.entity_id}` : 'WAITING'}</span>
            </div>
            <div className="p-md font-code-table text-code-table flex flex-col gap-sm overflow-auto">
              {!selected ? (
                <div className="text-outline text-center mt-md">SELECT TARGET TO INVESTIGATE</div>
              ) : (
                <>
                  <div className="grid grid-cols-2 border-b border-outline-variant pb-xs">
                    <span className="text-outline">ALERT ID:</span>
                    <span className="text-right">{selected.alert_id.split('-')[0]}...</span>
                  </div>
                  <div className="grid grid-cols-2 border-b border-outline-variant pb-xs">
                    <span className="text-outline">TYPE:</span>
                    <span className="text-right">{selected.entity_type}</span>
                  </div>
                  <div className="grid grid-cols-2 border-b border-outline-variant pb-xs">
                    <span className="text-outline">STATUS:</span>
                    <span className="text-right">{selected.status}</span>
                  </div>
                  <div className="mt-sm">
                    <span className="text-outline block mb-xs">ANOMALY VECTORS:</span>
                    <ul className="list-none space-y-xs">
                      {(selected.top_features || []).map((f, i) => (
                        <li key={i} className="text-error">&gt; {f.toUpperCase()}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="mt-auto pt-sm flex gap-sm">
                    <button className="flex-1 py-xs border border-error text-error hover:bg-error hover:text-on-error transition-none uppercase">
                      [ ISOLATE HOST ]
                    </button>
                    <button className="flex-1 py-xs border border-outline-variant hover:bg-surface-tint hover:text-on-surface transition-none uppercase">
                      [ INVESTIGATE ]
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
