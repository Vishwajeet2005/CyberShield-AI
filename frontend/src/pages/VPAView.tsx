import { useState, useEffect } from 'react'

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

const API = 'http://localhost:8000'

export default function VPAView() {
  const [cves, setCves] = useState<CVEEntry[]>([])
  const [selected, setSelected] = useState<CVEEntry | null>(null)
  const [refreshing, setRefreshing] = useState(false)
  const [filter, setFilter] = useState('')

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

  const filtered = cves.filter(c => c.cve_id.toLowerCase().includes(filter.toLowerCase()))

  return (
    <div className="flex-1 overflow-hidden bg-surface-container-lowest flex flex-col h-full relative">
      {/* Search / Filter Bar (Utilitarian) */}
      <div className="sticky top-0 bg-background border-b border-outline-variant flex items-center px-sm py-xs gap-md z-10 font-code-table text-code-table shrink-0">
        <div className="flex items-center gap-sm text-on-surface-variant border-r border-outline-variant pr-md">
          <span className="material-symbols-outlined text-[14px]">filter_alt</span>
          <span>FILTER: ACTIVE</span>
        </div>
        <div className="flex items-center gap-sm flex-1">
          <span className="text-primary font-bold">[ / ]</span>
          <input 
            className="bg-transparent border-none text-primary placeholder-on-surface-variant focus:ring-0 p-0 w-full font-code-table text-code-table uppercase outline-none" 
            placeholder="QUERY CVE ID..." 
            type="text"
            value={filter}
            onChange={e => setFilter(e.target.value)}
          />
        </div>
        <div className="flex items-center gap-sm text-on-surface-variant">
          <span>{filtered.length} RECORDS</span>
          <button 
            onClick={refresh}
            disabled={refreshing}
            className="border border-outline-variant px-xs hover:bg-primary hover:text-on-primary"
          >
            {refreshing ? '[ REFRESHING... ]' : '[ REFRESH NVD ]'}
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-auto">
        <table className="w-full border-collapse font-code-table text-code-table">
          <thead className="font-label-caps text-label-caps sticky top-0 z-10 bg-surface-container-highest text-primary">
            <tr>
              <th className="w-8 text-center border border-outline-variant p-1">[ ]</th>
              <th className="w-32 text-left border border-outline-variant p-1">CVE ID</th>
              <th className="w-16 text-right border border-outline-variant p-1">CVSS</th>
              <th className="w-16 text-right border border-outline-variant p-1">ADJ</th>
              <th className="w-24 text-center border border-outline-variant p-1">CISA KEV</th>
              <th className="w-48 text-left border border-outline-variant p-1">REMEDIATION PRIORITY</th>
              <th className="text-left border border-outline-variant p-1">DESCRIPTION</th>
            </tr>
          </thead>
          <tbody className="text-on-surface font-code-table text-code-table">
            {filtered.length === 0 && (
              <tr>
                <td colSpan={7} className="text-center p-md text-outline">NO CVE RECORDS FOUND</td>
              </tr>
            )}
            {filtered.map(c => {
              const isCrit = c.severity === 'CRITICAL'
              const isHigh = c.severity === 'HIGH'
              const isSelected = selected?.cve_id === c.cve_id
              return (
                <tr 
                  key={c.cve_id} 
                  onClick={() => setSelected(c)}
                  className={`cursor-pointer ${isSelected ? 'bg-surface-container-highest' : 'hover:bg-surface-container-high'}`}
                >
                  <td className="text-center border border-outline-variant p-1 text-outline-variant">
                    {isSelected ? '[X]' : '[ ]'}
                  </td>
                  <td className={`border border-outline-variant p-1 ${isSelected ? 'text-primary font-bold' : ''}`}>
                    {c.cve_id}
                  </td>
                  <td className={`text-right border border-outline-variant p-1 ${c.cvss_base >= 7 ? 'text-error font-bold' : 'text-on-surface'}`}>
                    {c.cvss_base?.toFixed(1)}
                  </td>
                  <td className={`text-right border border-outline-variant p-1 ${c.cvss_adjusted > c.cvss_base ? 'text-error font-bold' : 'text-on-surface-variant'}`}>
                    {c.cvss_adjusted?.toFixed(1)}
                  </td>
                  <td className={`text-center border border-outline-variant p-1 ${c.is_kev ? 'text-error font-bold bg-error-container/20' : 'text-on-surface-variant'}`}>
                    {c.is_kev ? 'TRUE' : 'FALSE'}
                  </td>
                  <td className="border border-outline-variant p-1">
                    {isCrit ? (
                      <span className="text-error font-bold bg-error-container/10 px-xs">[!! CRITICAL !!]</span>
                    ) : isHigh ? (
                      <span className="text-primary font-bold border border-primary px-xs">[ HIGH ]</span>
                    ) : (
                      <span className="text-on-surface border border-outline-variant px-xs">[ {c.severity || 'LOW'} ]</span>
                    )}
                  </td>
                  <td className="border border-outline-variant p-1 truncate max-w-xl text-on-surface-variant" title={c.description}>
                    {c.description}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
        
        {/* End of Data Indicator */}
        <div className="p-xs text-center border-t border-outline-variant text-on-surface-variant font-code-table text-code-table opacity-50">
          EOF_REACHED :: NO MORE RECORDS
        </div>
      </div>

      {/* Selected CVE Detail Panel */}
      {selected && (
        <div className="border-t border-outline-variant bg-surface-container-low shrink-0 h-64 flex flex-col font-code-table text-code-table">
          <div className="p-xs bg-primary text-on-primary font-bold flex justify-between items-center shrink-0">
            <span>[ CVE DETAIL: {selected.cve_id} ]</span>
            <button onClick={() => setSelected(null)} className="hover:text-background">[ CLOSE ]</button>
          </div>
          <div className="p-sm flex-1 overflow-auto grid grid-cols-2 gap-md">
            <div>
              <div className="mb-xs">
                <span className="text-outline">SEVERITY: </span>
                <span className={selected.severity === 'CRITICAL' ? 'text-error font-bold' : 'text-primary'}>{selected.severity}</span>
              </div>
              <div className="mb-xs">
                <span className="text-outline">CVSS BASE: </span>
                <span>{selected.cvss_base?.toFixed(1)}</span>
              </div>
              <div className="mb-xs">
                <span className="text-outline">CVSS ADJUSTED: </span>
                <span className={selected.cvss_adjusted > selected.cvss_base ? 'text-error font-bold' : ''}>{selected.cvss_adjusted?.toFixed(1)}</span>
              </div>
              <div className="mb-xs">
                <span className="text-outline">PRIORITY RANK: </span>
                <span>{selected.priority_rank}</span>
              </div>
              <div className="mb-sm">
                <span className="text-outline">AFFECTED ASSETS: </span>
                <span>{selected.affected_assets?.length > 0 ? selected.affected_assets.join(', ') : 'NONE IDENTIFIED'}</span>
              </div>
            </div>
            <div>
              <div className="mb-sm">
                <span className="text-outline block mb-xs">DESCRIPTION:</span>
                <div className="text-on-surface-variant whitespace-pre-wrap">{selected.description}</div>
              </div>
              {selected.remediation && (
                <div>
                  <span className="text-outline block mb-xs">REMEDIATION:</span>
                  <div className="text-[#3a7d44]">{selected.remediation}</div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
