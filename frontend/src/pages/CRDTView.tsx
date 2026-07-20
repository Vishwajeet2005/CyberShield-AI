import { useState, useEffect, useRef } from 'react'

interface TopoNode {
  id: string
  label: string
  type: string
  criticality: string
  department: string
  cves: string[]
}

interface TopoEdge {
  source: string
  target: string
  protocol: string
  port: number
  encrypted: boolean
}

const API = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

export default function CRDTView() {
  const [nodes, setNodes] = useState<TopoNode[]>([])
  const [edges, setEdges] = useState<TopoEdge[]>([])
  const [selected, setSelected] = useState<TopoNode | null>(null)
  const svgRef = useRef<SVGSVGElement>(null)
  const scrollRef = useRef<HTMLDivElement>(null)

  const [refreshing, setRefreshing] = useState(false)

  // Scroll Pan state
  const [isDragging, setIsDragging] = useState(false)
  const [dragStart, setDragStart] = useState({ x: 0, y: 0, scrollLeft: 0, scrollTop: 0 })

  const fetchTopo = async () => {
    setRefreshing(true)
    try {
      const d = await fetch(`${API}/api/crdt/topology`).then(r => r.json())
      setNodes(d.nodes ?? [])
      setEdges(d.edges ?? [])
    } catch {}
    setRefreshing(false)
  }

  useEffect(() => { fetchTopo() }, [])

  // Minimal force-free layout — group by department, stack vertically
  const departments = [...new Set(nodes.map(n => n.department))].filter(Boolean)
  const W = Math.max(1200, departments.length * 160)
  
  const currentSegCount: Record<string, number> = {}
  const segCount: Record<string, number> = {}
  nodes.forEach(n => { segCount[n.department] = (segCount[n.department] ?? 0) + 1 })
  const maxNodesInSeg = Math.max(0, ...Object.values(segCount))
  const H = Math.max(700, maxNodesInSeg * 100 + 100)

  const segW = departments.length > 0 ? W / departments.length : W

  const pos: Record<string, { x: number; y: number }> = {}
  nodes.forEach(n => {
    const si = departments.indexOf(n.department)
    const idx = currentSegCount[n.department] ?? 0
    currentSegCount[n.department] = idx + 1
    pos[n.id] = { x: (si + 0.5) * segW, y: 80 + idx * 100 }
  })

  const CRIT_COLOR: Record<string, string> = { CRITICAL: '#ffb4ab', HIGH: '#FFA500', MEDIUM: '#fdfdfc', LOW: '#3a7d44' }
  const nodeColor = (n: TopoNode) => CRIT_COLOR[n.criticality] ?? '#2a2a2a'

  return (
    <div className="flex-1 relative overflow-hidden flex flex-col bg-surface-container-lowest grid-bg h-full w-full">
      {/* Canvas Header */}
      <div className="h-10 border-b border-outline-variant flex items-center px-md justify-between bg-black z-20 shrink-0 w-full">
        <div className="font-code-table text-code-table text-on-surface font-bold">
          [ VIEW: DIGITAL TWIN TOPOLOGY ] ({nodes.length} NODES / {edges.length} EDGES)
        </div>
        <div className="flex gap-sm items-center">
          <button
            onClick={fetchTopo}
            disabled={refreshing}
            className="px-sm py-xs text-code-table font-code-table bg-black border border-outline-variant hover:bg-primary hover:text-black transition-none disabled:opacity-50"
          >
            {refreshing ? '[ LOADING... ]' : '[ REFRESH ]'}
          </button>
        </div>
      </div>

      <div className="flex-1 relative overflow-hidden flex w-full">
        {/* Network Topology SVG Area */}
        <div 
          ref={scrollRef}
          className={`flex-1 relative overflow-auto z-10 w-full h-full ${isDragging ? 'cursor-grabbing' : 'cursor-grab'}`}
          onPointerDown={(e) => {
            if (e.button !== 0) return // Only left click drag
            setIsDragging(true)
            if (scrollRef.current) {
              setDragStart({ 
                x: e.clientX, 
                y: e.clientY, 
                scrollLeft: scrollRef.current.scrollLeft, 
                scrollTop: scrollRef.current.scrollTop 
              })
            }
            e.currentTarget.setPointerCapture(e.pointerId)
          }}
          onPointerMove={(e) => {
            if (isDragging && scrollRef.current) {
              scrollRef.current.scrollLeft = dragStart.scrollLeft - (e.clientX - dragStart.x)
              scrollRef.current.scrollTop = dragStart.scrollTop - (e.clientY - dragStart.y)
            }
          }}
          onPointerUp={(e) => {
            setIsDragging(false)
            e.currentTarget.releasePointerCapture(e.pointerId)
          }}
          onPointerLeave={() => {
            setIsDragging(false)
          }}
        >
          {/* Centering Wrapper */}
          <div className="min-w-full min-h-full flex items-center justify-center p-xl">
            <div 
              className="relative shadow-2xl transition-all duration-75 ease-out"
              style={{ width: W, height: H }}
            >
              <div 
                className="relative border border-[#333] bg-black bg-opacity-80"
                style={{ width: W, height: H }}
              >
              {nodes.length === 0 ? (
                <div className="absolute inset-0 flex items-center justify-center font-code-table text-outline">LOADING TOPOLOGY...</div>
              ) : (
                <svg ref={svgRef} width="100%" height="100%" viewBox={`0 0 ${W} ${H}`}>
                  {/* Edges */}
                {edges.map((e, i) => {
                  const s = pos[e.source], t = pos[e.target]
                  if (!s || !t) return null
                  return (
                    <line key={i} x1={s.x} y1={s.y} x2={t.x} y2={t.y}
                      stroke={e.encrypted ? '#1a2a1a' : '#333'}
                      strokeWidth={1}
                      strokeDasharray={e.encrypted ? undefined : '3 3'}
                    />
                  )
                })}
                {/* Department labels */}
                {departments.map((dept, i) => (
                  <text key={dept} x={(i + 0.5) * segW} y={30} textAnchor="middle"
                    fontSize={12} fill="#777" fontFamily="JetBrains Mono, monospace" fontWeight="bold"
                    letterSpacing="0.1em">
                    {dept}
                  </text>
                ))}
                {/* Nodes */}
                {nodes.map(n => {
                  const p = pos[n.id]
                  if (!p) return null
                  const isCrit = n.criticality === 'CRITICAL'
                  const isSelected = selected?.id === n.id
                  return (
                    <g key={n.id} onClick={() => setSelected(n)} onPointerDown={(e) => e.stopPropagation()} style={{ cursor: 'pointer' }}>
                      <rect x={p.x - 40} y={p.y - 20} width={80} height={40}
                        fill={isCrit ? 'rgba(255, 180, 171, 0.1)' : '#111'} 
                        stroke={isSelected ? '#fdfdfc' : isCrit ? '#ffb4ab' : '#333'}
                        strokeWidth={isSelected ? 2 : 1}
                      />
                      <text x={p.x} y={p.y + 4} textAnchor="middle"
                        fontSize={10} fill={nodeColor(n)} fontFamily="JetBrains Mono, monospace" fontWeight="bold">
                        {n.label?.slice(0, 10)}
                      </text>
                      {isCrit && (
                         <circle cx={p.x + 40} cy={p.y - 20} r={4} fill="#ffb4ab" className="animate-pulse" />
                      )}
                    </g>
                  )
                })}
              </svg>
            )}
              </div>
            </div>
          </div>
        </div>

        {/* Side Panel: Node Details (Overlay-style) */}
        <div className="w-80 bg-black border-l border-outline-variant z-30 flex flex-col shrink-0">
          <div className={`h-10 border-b border-outline-variant flex items-center px-md ${selected?.criticality === 'CRITICAL' ? 'bg-error-container/20' : 'bg-surface-container-high'}`}>
            <span className={`font-code-table text-code-table font-bold ${selected?.criticality === 'CRITICAL' ? 'text-error' : 'text-primary'}`}>
              {selected ? '[ NODE ACQUIRED ]' : '[ AWAITING SELECTION ]'}
            </span>
          </div>
          
          <div className="p-md flex-1 overflow-y-auto">
            {!selected ? (
              <div className="text-outline font-code-table text-center mt-xl">CLICK NODE IN GRAPH</div>
            ) : (
              <div className="font-code-table text-code-table flex flex-col gap-md">
                <div className="bg-surface-container-low border border-outline-variant p-sm">
                  <div className="flex justify-between mb-xs">
                    <span className="text-outline">NODE ID:</span>
                    <span className="text-on-surface font-bold">{selected.id}</span>
                  </div>
                  <div className="flex justify-between mb-xs">
                    <span className="text-outline">LABEL:</span>
                    <span className="text-on-surface">{selected.label}</span>
                  </div>
                  <div className="flex justify-between mb-xs">
                    <span className="text-outline">TYPE:</span>
                    <span className="text-on-surface">{selected.type}</span>
                  </div>
                  <div className="flex justify-between mb-xs">
                    <span className="text-outline">DEPARTMENT:</span>
                    <span className="text-on-surface">{selected.department}</span>
                  </div>
                  <div className="flex justify-between mt-sm pt-sm border-t border-outline-variant">
                    <span className="text-outline">CRITICALITY:</span>
                    <span className={selected.criticality === 'CRITICAL' ? 'text-error font-bold' : 'text-primary font-bold'}>
                      {selected.criticality}
                    </span>
                  </div>
                </div>

                {selected.cves && selected.cves.length > 0 && (
                  <div>
                    <div className="text-on-surface-variant mb-xs">// VULNERABILITIES</div>
                    <div className="bg-surface-container-low border border-outline-variant p-sm space-y-xs">
                      {selected.cves.map(c => (
                        <div key={c} className="text-error hover:underline cursor-pointer">{c}</div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
          
          {selected && (
            <div className="p-md border-t border-outline-variant mt-auto space-y-xs">
              <button
                onClick={() => { window.dispatchEvent(new CustomEvent('navigate-view', { detail: 'bade' })) }}
                className="w-full h-8 bg-black text-on-surface border border-outline-variant hover:bg-primary hover:text-black hover:border-primary font-code-table text-code-table transition-none"
              >
                [ INVESTIGATE ASSET ]
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
