import { useState } from 'react'

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

const API = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

export default function AAPAView() {
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
    <div className="flex flex-col h-full bg-surface-dim relative">
      {/* Header */}
      <div className="p-sm border-b border-outline-variant bg-background flex justify-between items-center sticky top-0 z-10">
        <h1 className="font-headline-sm text-headline-sm text-primary uppercase">Advanced Persistent Threat Attribution [AAPA]</h1>
        {loading && <div className="font-code-table text-code-table text-error animate-pulse">[!! ANALYZING !!]</div>}
        {attr && !loading && <div className="font-code-table text-code-table text-error">[!! CAMPAIGN IDENTIFIED !!]</div>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 flex-1 auto-rows-min md:auto-rows-fr gap-gutter bg-[#333333]">
        {/* Left: Input Payload */}
        <div className="md:col-span-7 bg-background flex flex-col h-full">
          <div className="p-xs border-b border-outline-variant bg-surface-container-low font-label-caps text-label-caps text-on-surface-variant flex justify-between">
            <span>// ENTITY PAYLOAD (JSON)</span>
            <button className="hover:text-primary" onClick={analyze} disabled={loading}>
              {loading ? '[ ANALYZING... ]' : '[ RUN ATTRIBUTION ]'}
            </button>
          </div>
          <div className="p-md flex-1 flex flex-col">
            <div className="mb-sm">
              <h2 className="font-headline-md text-headline-md mb-xs text-primary">Input Telemetry</h2>
              <p className="font-body-sm text-on-surface-variant mb-sm">Provide anomalous entity JSON payload for MITRE ATT&CK attribution.</p>
              {error && <div className="inline-block border border-error px-sm py-xs text-error text-code-table font-code-table">ERROR: {error}</div>}
            </div>
            
            <textarea
              className="flex-1 bg-[#0d0d0d] border border-[#1a1a1a] text-[#7a9a7a] font-code-table text-code-table p-md outline-none resize-none focus:border-outline-variant"
              value={input}
              onChange={e => setInput(e.target.value)}
              spellCheck={false}
            />
          </div>
        </div>

        {/* Right: MITRE ATT&CK Block */}
        <div className="md:col-span-5 bg-background flex flex-col h-full">
          <div className="p-xs border-b border-outline-variant bg-primary text-on-primary font-label-caps text-label-caps font-bold flex justify-between">
            <span>// ATTRIBUTION ANALYSIS</span>
            <span>[ OUTPUT ]</span>
          </div>
          
          <div className="p-md flex-1 flex flex-col overflow-auto">
            {!attr && !loading ? (
              <div className="text-outline text-center mt-xl font-code-table">AWAITING PAYLOAD ANALYSIS</div>
            ) : loading ? (
              <div className="text-on-surface-variant text-center mt-xl font-code-table">
                <span className="blink-cursor">_</span> QUERYING CHROMA DB...
              </div>
            ) : attr ? (
              <>
                <div className="flex justify-between items-end mb-md border-b border-outline-variant pb-sm">
                  <div>
                    <div className="font-label-caps text-label-caps text-on-surface-variant">PRIMARY SUSPECT</div>
                    <div className="font-display-lg text-display-lg text-primary">{attr.threat_actor ?? 'UNKNOWN'}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-label-caps text-label-caps text-on-surface-variant">CONFIDENCE LEVEL</div>
                    <div className="font-headline-md text-headline-md text-primary">
                      {attr.confidence != null ? `${(attr.confidence * 100).toFixed(1)}%` : '--'}
                    </div>
                  </div>
                </div>

                <div className="flex-1">
                  <div className="font-label-caps text-label-caps text-on-surface-variant mb-xs">// OBSERVED TTPs (MITRE ATT&CK)</div>
                  <div className="grid grid-cols-2 gap-gutter bg-[#333333] mb-md">
                    {(attr.techniques || []).length === 0 && (
                      <div className="bg-background p-xs col-span-2 text-outline font-code-table">NO TTPs IDENTIFIED</div>
                    )}
                    {(attr.techniques || []).map((t, i) => (
                      <div key={i} className="bg-background p-xs border border-transparent hover:border-primary">
                        <div className="font-code-table text-code-table text-on-surface-variant">{t.id}</div>
                        <div className="font-body-sm">{t.name}</div>
                        <div className="font-label-caps text-outline mt-xs">{t.tactic}</div>
                      </div>
                    ))}
                  </div>

                  {attr.next_stage && attr.next_stage.length > 0 && (
                    <>
                      <div className="font-label-caps text-label-caps text-on-surface-variant mb-xs mt-md">
                        // PREDICTED ADVERSARY TRAJECTORY
                      </div>
                      <div className="bg-surface-dim p-sm border border-outline-variant">
                        <ul className="font-code-table text-code-table space-y-xs">
                          {attr.next_stage.map((s, i) => (
                            <li key={i} className="flex items-start gap-sm">
                              <span className="text-error mt-[2px]">&gt;</span>
                              <div className="text-on-surface">{s}</div>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </>
                  )}

                  {attr.justification && (
                    <>
                      <div className="font-label-caps text-label-caps text-on-surface-variant mb-xs mt-md">
                        // JUSTIFICATION
                      </div>
                      <div className="font-code-table text-code-table text-on-surface-variant whitespace-pre-wrap leading-relaxed">
                        {attr.justification}
                      </div>
                    </>
                  )}
                </div>
              </>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  )
}
