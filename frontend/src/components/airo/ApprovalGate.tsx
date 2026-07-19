import { useState, useEffect } from 'react';
import { AlertOctagon } from 'lucide-react';

export default function ApprovalGate({ actionName, impact, onApprove, onReject }: { actionName: string, impact: string, onApprove: (name: string) => void, onReject: () => void }) {
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutes
  const [approverName, setApproverName] = useState('SOC Analyst (Current User)');

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="fixed inset-0 bg-bg-primary/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-bg-secondary border-2 border-danger rounded-xl max-w-lg w-full overflow-hidden shadow-[0_0_50px_rgba(255,51,102,0.3)]">
        <div className="bg-danger/20 p-4 flex items-center justify-center gap-3 border-b border-danger/50">
          <AlertOctagon className="text-danger w-8 h-8 animate-pulse" />
          <h2 className="text-danger font-bold text-lg tracking-wider">HIGH BLAST RADIUS ACTION</h2>
        </div>
        
        <div className="p-6">
          <div className="text-center mb-6">
            <div className="text-sm text-text-secondary uppercase tracking-wider mb-1">Human Approval Required For</div>
            <div className="text-xl font-bold text-text-primary font-mono">{actionName}</div>
          </div>

          <div className="bg-bg-primary p-4 rounded-lg border border-border-subtle mb-6">
            <div className="text-xs text-text-secondary uppercase mb-2">Impact Assessment</div>
            <p className="text-sm text-warning font-medium">{impact}</p>
          </div>

          <div className="flex flex-col gap-4 mb-8">
            <div>
              <label className="block text-xs text-text-secondary uppercase mb-1">Approver Identity</label>
              <input 
                type="text" 
                value={approverName}
                onChange={(e) => setApproverName(e.target.value)}
                className="w-full bg-bg-primary border border-border-subtle rounded p-2 text-sm text-text-primary focus:border-accent-cyan outline-none transition-colors" 
              />
            </div>
            <div>
              <label className="block text-xs text-text-secondary uppercase mb-1">Timeout In</label>
              <div className="text-2xl font-mono font-bold text-danger animate-pulse">
                {formatTime(timeLeft)}
              </div>
            </div>
          </div>

          <div className="flex gap-4">
            <button onClick={onReject} className="flex-1 py-3 bg-bg-primary border border-border-subtle hover:bg-white/5 rounded-lg text-text-primary font-medium transition-colors">
              Reject
            </button>
            <button 
              onClick={() => onApprove(approverName)} 
              className="flex-1 py-3 bg-danger hover:bg-danger/80 text-white font-bold rounded-lg transition-colors shadow-[0_0_15px_rgba(255,51,102,0.5)]"
            >
              APPROVE ACTION
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
