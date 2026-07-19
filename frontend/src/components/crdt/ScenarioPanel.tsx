import { Play } from 'lucide-react';

export default function ScenarioPanel({ onSimulate, isSimulating }: { onSimulate: (name: string) => void, isSimulating: boolean }) {
  const scenarios = [
    { name: 'Ransomware Outbreak', desc: 'Simulates rapid propagation via SMB.', risk: 95, from: 'WORKSTATION', to: 'EMR-SERVER' },
    { name: 'Supply Chain Compromise', desc: 'Vendor portal to internal DB.', risk: 85, from: 'VENDOR-VPN', to: 'CORE-DB' },
    { name: 'Insider Threat Data Exfil', desc: 'Admin accessing sensitive records.', risk: 70, from: 'ADMIN-PC', to: 'INTERNET' },
    { name: 'OT Pivot', desc: 'IT network to OT control systems.', risk: 98, from: 'IT-MGMT', to: 'SCADA-CTRL' }
  ];

  return (
    <div className="glass rounded-xl p-4 h-full flex flex-col">
      <h3 className="font-bold text-lg mb-4">Attack Scenarios</h3>
      <div className="flex-1 overflow-auto space-y-3 scrollbar-thin">
        {scenarios.map(s => (
          <div key={s.name} className="bg-bg-secondary/50 border border-border-subtle rounded-lg p-3 hover:border-accent-cyan/50 transition-colors">
            <div className="flex justify-between items-start mb-2">
              <h4 className="font-bold text-sm text-text-primary">{s.name}</h4>
              <span className={`text-xs font-bold px-2 py-0.5 rounded ${s.risk >= 90 ? 'bg-danger/20 text-danger' : 'bg-warning/20 text-warning'}`}>
                Risk: {s.risk}
              </span>
            </div>
            <p className="text-xs text-text-secondary mb-3">{s.desc}</p>
            <div className="flex items-center justify-between">
              <div className="text-[10px] font-mono text-text-secondary">
                {s.from} → {s.to}
              </div>
              <button 
                onClick={() => onSimulate(s.name)}
                disabled={isSimulating}
                className="flex items-center gap-1 text-xs bg-accent-cyan/20 hover:bg-accent-cyan hover:text-bg-primary text-accent-cyan px-3 py-1.5 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Play className="w-3 h-3" /> {isSimulating ? 'Running...' : 'Simulate'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
