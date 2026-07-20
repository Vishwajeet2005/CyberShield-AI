import { useState, useEffect } from 'react'

interface Incident {
  id: string
  title?: string
  severity?: string
  status: string
  actions_taken?: IncidentAction[]
  affected_entities?: string[]
}

interface IncidentAction {
  id: string
  action_type: string
  target: string
  blast_radius: string
  status: string
  executed_at?: string
  result?: string
}

const API = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

export default function AIROView() {
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [selected, setSelected] = useState<Incident | null>(null)
  const [approving, setApproving] = useState<string | null>(null)
  const [filter, setFilter] = useState('')

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
      await fetch(`${API}/api/airo/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action_id: actionId, decision, approver: 'SOC-ANALYST-01' })
      })
      // Immediately re-fetch incidents so the UI reflects the new status
      const r = await fetch(`${API}/api/airo/incidents`)
      if (r.ok) {
        const fresh = await r.json()
        setIncidents(fresh)
        // Update selected to reflect fresh state
        const freshSelected = fresh.find((i: Incident) => i.id === selected?.id)
        if (freshSelected) setSelected(freshSelected)
      }
    } catch { /* no-op */ }
    setApproving(null)
  }

  const filtered = incidents.filter(i => (i.id + i.title + (i.affected_entities?.[0]||'')).toLowerCase().includes(filter.toLowerCase()))

  return (
    <div className="flex-1 flex flex-col lg:flex-row overflow-hidden bg-background h-full">
      {/* LEFT: Active Incidents Queue */}
      <section className="flex-1 flex flex-col border-r border-outline-variant h-full overflow-hidden min-w-[320px]">
        {/* Header */}
        <div className="p-sm border-b border-outline-variant bg-surface-container-high flex justify-between items-center shrink-0">
          <h2 className="font-label-caps text-label-caps text-primary tracking-widest">ACTIVE_INCIDENTS_QUEUE</h2>
          <span className="font-code-table text-code-table text-on-surface-variant">[ {filtered.length} ITEMS ]</span>
        </div>
        {/* Search/Filter */}
        <div className="p-sm border-b border-outline-variant bg-surface-container-low shrink-0 flex gap-sm focus-within:border-primary">
          <span className="font-code-table text-code-table text-on-surface-variant mt-1">[ / ]</span>
          <input
            className="w-full bg-transparent border-none text-on-surface font-code-table text-code-table focus:ring-0 placeholder:text-outline p-0 outline-none"
            placeholder="FILTER QUEUE..."
            type="text"
            value={filter}
            onChange={e => setFilter(e.target.value)}
          />
        </div>
        {/* Queue List */}
        <div className="flex-1 overflow-y-auto">
          {filtered.length === 0 && (
            <div className="p-md text-outline font-code-table">NO ACTIVE INCIDENTS</div>
          )}
          {filtered.map(inc => {
            const isCrit = inc.severity === 'CRITICAL'
            const isHigh = inc.severity === 'HIGH'
            return (
              <div
                key={inc.id}
                onClick={() => setSelected(inc)}
                className={`p-md border-b border-outline-variant cursor-pointer relative ${
                  selected?.id === inc.id ? 'bg-surface-container-low' : 'hover:bg-surface-container-low'
                } ${isCrit ? 'border-l-4 border-l-error' : ''}`}
              >
                <div className="flex justify-between items-start mb-sm">
                  <div className={`font-code-table text-code-table px-xs py-0.5 border ${
                    isCrit ? 'text-error bg-error-container/20 border-error-container' :
                    isHigh ? 'text-[#FFA500] border-[#FFA500]/50' :
                    'text-primary border-outline-variant'
                  }`}>
                    {isCrit ? '[!! CRITICAL !!]' : `[ ${inc.severity || 'INFO'} ]`}
                  </div>
                  <div className="font-code-table text-code-table text-on-surface-variant">{inc.status}</div>
                </div>
                <h3 className="font-headline-sm text-headline-sm text-primary mb-xs">{inc.title || inc.id}</h3>
                <div className="font-code-table text-code-table text-on-surface-variant mb-md">
                  TARGET: <span className="text-on-surface">{inc.affected_entities?.[0] || 'UNKNOWN'}</span>
                </div>
              </div>
            )
          })}
        </div>
      </section>

      {/* RIGHT: Playbook Execution */}
      <section className="flex-[1.5] flex flex-col h-full overflow-hidden bg-surface-dim relative min-w-[400px]">
        {/* Header */}
        <div className="p-sm border-b border-outline-variant bg-surface-container-highest flex justify-between items-center shrink-0 z-10">
          <div className="flex items-center gap-sm">
            <span className="material-symbols-outlined text-primary text-sm">memory</span>
            <h2 className="font-label-caps text-label-caps text-primary tracking-widest">
              PLAYBOOK_EXECUTION: {selected ? selected.id : 'AWAITING SELECTION'}
            </h2>
          </div>
          {selected && (
            <span className="font-code-table text-code-table text-[#00FF00] border border-[#00FF00]/30 px-xs py-0.5 bg-[#00FF00]/10">
              STATUS: {selected.status}
            </span>
          )}
        </div>
        
        {/* Playbook Steps Terminal */}
        <div className="flex-1 p-md overflow-y-auto font-code-table text-code-table z-10 space-y-md">
          {!selected ? (
            <div className="text-outline">SELECT AN INCIDENT TO VIEW PLAYBOOK STATUS</div>
          ) : (selected.actions_taken || []).length === 0 ? (
            <div className="text-outline">NO PLAYBOOK ACTIONS PENDING OR EXECUTED</div>
          ) : (
            (selected.actions_taken || []).map((action, idx) => (
              <div key={idx} className={`border p-sm ${action.status === 'awaiting_approval' ? 'border-outline bg-surface-container-high' : 'border-outline-variant bg-background'}`}>
                <div className="flex justify-between items-center mb-xs">
                  <span className={action.status === 'awaiting_approval' ? 'text-primary font-bold' : 'text-on-surface-variant'}>
                    &gt; {action.status === 'awaiting_approval' ? 'REQ' : 'EXEC'}: {action.action_type} - {action.target}
                  </span>
                  <span className="text-on-surface-variant text-[10px] uppercase">BLAST: {action.blast_radius}</span>
                </div>
                {action.status === 'awaiting_approval' ? (
                  <div className="text-[#FFA500] flex items-center gap-xs">
                    <span className="material-symbols-outlined text-[14px] animate-pulse">hourglass_empty</span>
                    [ PENDING ] AWAITING HUMAN AUTHORIZATION...<span className="blink-cursor bg-primary w-2 h-[14px] inline-block ml-1 align-middle"></span>
                  </div>
                ) : (
                  <div className="text-[#00FF00] flex items-center gap-xs">
                    <span className="material-symbols-outlined text-[14px]">check_box</span>
                    [ {action.status.toUpperCase()} ] ACTION STATUS LOGGED.
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Human-in-the-loop Approval Gate */}
        {selected && (selected.actions_taken || []).some(a => a.status === 'awaiting_approval') && (
          <div className="shrink-0 p-lg border-t-2 border-error bg-error-container/10 relative z-10 m-md">
            <div className="absolute -top-3 left-4 bg-background px-xs font-label-caps text-label-caps text-error border border-error">
              APPROVAL GATE: REQUIRED ACTION
            </div>
            
            {/* Find the pending action */}
            {(() => {
              const pendingAction = (selected.actions_taken || []).find(a => a.status === 'awaiting_approval')!
              return (
                <>
                  <div className="mb-md mt-sm">
                    <h3 className="font-headline-sm text-headline-sm text-error mb-xs flex items-center gap-sm">
                      <span className="material-symbols-outlined">warning</span>
                      {pendingAction.action_type} - {pendingAction.target} ({pendingAction.blast_radius} RADIUS)
                    </h3>
                    <p className="font-code-table text-code-table text-on-surface max-w-2xl">
                      WARNING: Autonomous execution halted due to policy constraints on {pendingAction.blast_radius}-BLAST actions. Please authorize.
                    </p>
                  </div>
                  <div className="flex gap-md">
                    <button 
                      onClick={() => handleApproval(pendingAction.id, 'approve')}
                      disabled={approving === pendingAction.id}
                      className="flex-1 bg-[#00FF00]/10 text-[#00FF00] border border-[#00FF00] p-md font-label-caps text-label-caps tracking-widest hover:bg-[#00FF00] hover:text-black transition-none flex justify-center items-center gap-sm"
                    >
                      <span className="material-symbols-outlined text-sm">check</span>
                      [ {approving === pendingAction.id ? 'PROCESSING...' : 'APPROVE'} ]
                    </button>
                    <button 
                      onClick={() => handleApproval(pendingAction.id, 'deny')}
                      disabled={approving === pendingAction.id}
                      className="flex-1 bg-error/10 text-error border border-error p-md font-label-caps text-label-caps tracking-widest hover:bg-error hover:text-black transition-none flex justify-center items-center gap-sm"
                    >
                      <span className="material-symbols-outlined text-sm">close</span>
                      [ REJECT ]
                    </button>
                  </div>
                </>
              )
            })()}
          </div>
        )}
      </section>
    </div>
  )
}
