export default function NextMovePredictor() {
  const moves = [
    { id: 'T1486', name: 'Data Encrypted for Impact', tactic: 'Impact', probability: 85, recommendation: 'Isolate compromised segment immediately. Enable ransomware protection on EMR servers.' },
    { id: 'T1567', name: 'Exfiltration Over Web Service', tactic: 'Exfiltration', probability: 65, recommendation: 'Block mega.io and common file sharing domains on firewall.' },
    { id: 'T1098', name: 'Account Manipulation', tactic: 'Persistence', probability: 40, recommendation: 'Audit recent Active Directory group changes.' }
  ];

  return (
    <div className="glass rounded-xl p-4 flex flex-col gap-4">
      <h3 className="font-bold text-lg mb-2 flex items-center gap-2">
        <span className="animate-pulse text-danger">⚠️</span> Predicted Next Moves
      </h3>
      {moves.map((move, idx) => (
        <div key={idx} className={`p-4 rounded-lg border ${move.probability >= 80 ? 'bg-danger/10 border-danger/30' : move.probability >= 60 ? 'bg-warning/10 border-warning/30' : 'bg-white/5 border-white/10'}`}>
          <div className="flex justify-between items-center mb-2">
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono bg-bg-primary px-1.5 py-0.5 rounded text-text-secondary">{move.id}</span>
              <span className="font-medium text-sm text-text-primary">{move.name}</span>
            </div>
            <span className={`text-lg font-bold ${move.probability >= 80 ? 'text-danger' : move.probability >= 60 ? 'text-warning' : 'text-text-secondary'}`}>
              {move.probability}%
            </span>
          </div>
          
          <div className="w-full h-1.5 bg-bg-primary rounded-full mb-3 overflow-hidden">
            <div 
              className={`h-full ${move.probability >= 80 ? 'bg-danger' : move.probability >= 60 ? 'bg-warning' : 'bg-white/20'}`} 
              style={{ width: `${move.probability}%` }} 
            />
          </div>

          <div className="text-xs text-text-secondary mb-2">
            <span className="uppercase text-[10px] tracking-wider opacity-70">Tactic:</span> {move.tactic}
          </div>

          <div className="bg-bg-primary p-2 rounded text-xs text-accent-cyan border border-accent-cyan/10">
            <span className="font-bold">Recommendation:</span> {move.recommendation}
          </div>
        </div>
      ))}
    </div>
  );
}
