export default function TTpHeatmap() {
  const tactics = ['Initial Access', 'Execution', 'Persistence', 'Privilege Escalation', 'Defense Evasion', 'Discovery', 'Lateral Movement', 'Collection', 'Exfiltration', 'Impact'];
  
  // Mock data
  const grid = tactics.map(tactic => ({
    name: tactic,
    techniques: Array.from({ length: 5 }).map((_, i) => ({
      id: `T1${Math.floor(Math.random() * 900) + 100}`,
      observed: Math.random() > 0.8,
      actorMatch: Math.random() > 0.6
    }))
  }));

  return (
    <div className="glass rounded-xl p-4 h-full flex flex-col overflow-hidden">
      <h3 className="font-bold text-lg mb-4">MITRE ATT&CK Mapping</h3>
      <div className="flex-1 overflow-auto scrollbar-thin">
        <div className="flex gap-2 min-w-max">
          {grid.map(tactic => (
            <div key={tactic.name} className="flex-1 min-w-[120px]">
              <div className="text-[10px] font-bold text-text-secondary uppercase tracking-wider mb-2 pb-1 border-b border-border-subtle truncate" title={tactic.name}>
                {tactic.name}
              </div>
              <div className="space-y-2">
                {tactic.techniques.map((tech, i) => (
                  <div 
                    key={i} 
                    className={`text-xs font-mono p-1.5 rounded text-center border cursor-help transition-colors
                      ${tech.observed && tech.actorMatch ? 'bg-danger/20 border-danger/50 text-danger' : 
                        tech.observed ? 'bg-accent-cyan/20 border-accent-cyan/50 text-accent-cyan' : 
                        tech.actorMatch ? 'bg-white/5 border-white/10 text-text-secondary' : 
                        'bg-transparent border-transparent text-text-secondary/30'}`}
                    title={tech.id}
                  >
                    {tech.id}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="mt-4 pt-4 border-t border-border-subtle flex gap-4 text-xs">
        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-accent-cyan/20 border border-accent-cyan/50 rounded" /> Observed</div>
        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-white/5 border border-white/10 rounded" /> Actor TTP</div>
        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-danger/20 border border-danger/50 rounded" /> Overlap</div>
      </div>
    </div>
  );
}
