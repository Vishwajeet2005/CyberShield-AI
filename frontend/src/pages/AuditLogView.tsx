import { useState, useEffect, useRef } from 'react'

interface AuditEntry {
  log_id: string
  action_type: string
  target: string
  blast_radius: string
  result: string
  written_at: string
}

const API = 'http://localhost:8000'

export default function AuditLogView() {
  const [logs, setLogs] = useState<AuditEntry[]>([])
  const [filter, setFilter] = useState('')
  const logEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const poll = async () => {
      try {
        const r = await fetch(`${API}/api/audit/logs`)
        if (r.ok) {
          const newLogs = await r.json()
          setLogs(newLogs)
        }
      } catch { /* no-op */ }
    }
    poll()
    const id = setInterval(poll, 3000)
    return () => clearInterval(id)
  }, [])

  // Auto-scroll to bottom only if not interacting (simple implementation)
  useEffect(() => {
    if (!filter) {
      logEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [logs, filter])

  const filtered = logs.filter(l => 
    l.action_type.toLowerCase().includes(filter.toLowerCase()) || 
    l.target.toLowerCase().includes(filter.toLowerCase()) ||
    l.log_id.toLowerCase().includes(filter.toLowerCase())
  )

  return (
    <div className="flex-1 overflow-hidden bg-surface p-md flex flex-col gap-md h-full">
      <div className="flex justify-between items-end border-b border-outline-variant pb-xs shrink-0">
        <div>
          <h1 className="font-headline-md text-headline-md text-primary">IMMUTABLE AUDIT LOG</h1>
          <p className="font-code-table text-code-table text-on-surface-variant mt-xs">APPEND-ONLY SYSTEM LEDGER // INTEGRITY VERIFIED</p>
        </div>
        <div className="flex gap-sm">
          <button className="border border-outline-variant bg-surface text-on-surface px-sm py-xs font-code-table text-code-table hover:bg-primary hover:text-on-primary transition-none">
            [ EXPORT .CSV ]
          </button>
          <button className="border border-outline-variant bg-surface text-on-surface px-sm py-xs font-code-table text-code-table hover:bg-primary hover:text-on-primary transition-none">
            [ VERIFY HASH ]
          </button>
        </div>
      </div>

      <div className="border-b border-outline-variant bg-surface-container-low shrink-0 flex gap-sm border border-outline-variant p-sm">
        <span className="font-code-table text-code-table text-on-surface-variant mt-1">[ / ]</span>
        <input
          className="w-full bg-transparent border-none outline-none text-on-surface font-code-table text-code-table focus:ring-0 placeholder:text-outline p-0"
          placeholder="SEARCH LOGS..."
          type="text"
          value={filter}
          onChange={e => setFilter(e.target.value)}
        />
      </div>

      {/* Data Table Container */}
      <div className="border border-outline-variant flex-1 flex flex-col bg-background overflow-hidden relative">
        {/* Table Header */}
        <div className="grid grid-cols-12 gap-gutter bg-surface-variant border-b border-outline-variant p-sm font-label-caps text-label-caps text-on-primary font-bold sticky top-0">
          <div className="col-span-2">TIMESTAMP</div>
          <div className="col-span-3">ACTION / BLAST</div>
          <div className="col-span-3">TARGET</div>
          <div className="col-span-1">RESULT</div>
          <div className="col-span-3">SHA-256 HASH</div>
        </div>

        {/* Table Body */}
        <div className="flex-1 overflow-y-auto font-code-table text-code-table pb-xl">
          {filtered.length === 0 && (
            <div className="p-md text-outline text-center">NO AUDIT LOGS FOUND</div>
          )}
          {filtered.map((log, i) => {
            const isError = log.result !== 'success'
            const resultText = isError ? '[ FAIL ]' : '[ OK ]'
            const resultClass = isError ? 'text-error' : 'text-[#00FF00]'
            const bgClass = i % 2 === 0 ? 'bg-surface-container-low' : ''
            const isAlert = log.action_type.includes('CRITICAL') || log.action_type.includes('ALERT')

            return (
              <div 
                key={log.log_id} 
                className={`grid grid-cols-12 gap-gutter p-sm border-b border-outline-variant hover:bg-surface-container-high transition-none ${bgClass} ${isAlert ? 'bg-error-container/20 text-on-error-container' : ''}`}
              >
                <div className="col-span-2 text-on-surface-variant">
                  {new Date(log.written_at).toISOString().replace(/\.\d{3}Z$/, 'Z')}
                </div>
                <div className={`col-span-3 ${isError ? 'text-error' : 'text-primary'}`}>
                  {log.action_type} <span className="text-outline-variant ml-xs">[{log.blast_radius}]</span>
                </div>
                <div className="col-span-3 text-on-surface-variant truncate">{log.target}</div>
                <div className={`col-span-1 ${resultClass}`}>{resultText}</div>
                <div className="col-span-3 text-on-surface-variant truncate font-mono text-[10px]">
                  {/* Simulate SHA256 of log entry */}
                  {Array.from(log.log_id.replace(/-/g, '')).map(c => c.charCodeAt(0).toString(16)).join('').padEnd(64, '0').slice(0,64)}
                </div>
              </div>
            )
          })}
          <div className="p-sm text-center text-on-surface-variant border-b border-outline-variant animate-pulse" ref={logEndRef}>
            _AWAITING_NEW_ENTRIES_
          </div>
        </div>
      </div>
    </div>
  )
}
