import { useState } from 'react';
import { PlaybookAction } from '../../types';
import { CheckCircle2, Circle, Loader2, AlertTriangle } from 'lucide-react';

export default function PlaybookRunner({ actions, onExecute, onApprove }: { actions: PlaybookAction[], onExecute: (id: string) => void, onApprove: (id: string) => void }) {
  return (
    <div className="glass rounded-xl p-5 h-full flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <h3 className="font-bold text-xl">Execution Pipeline</h3>
        <span className="text-xs text-text-secondary">Playbook: PB-RANSOM-01</span>
      </div>

      <div className="flex-1 overflow-auto space-y-4 relative before:absolute before:inset-0 before:ml-6 before:-translate-x-px before:h-full before:w-1 before:bg-border-subtle">
        {actions.map((action, idx) => {
          const isPending = action.status === 'pending';
          const isExecuting = action.status === 'executing';
          const isCompleted = action.status === 'completed';
          const needsApproval = action.status === 'awaiting_approval';

          return (
            <div key={action.id} className={`relative flex items-center gap-4 p-4 rounded-lg border transition-all ${
              isExecuting ? 'bg-accent-cyan/10 border-accent-cyan shadow-[0_0_15px_rgba(0,212,255,0.2)]' :
              needsApproval ? 'bg-warning/10 border-warning shadow-[0_0_15px_rgba(255,153,0,0.2)]' :
              'bg-bg-primary/50 border-border-subtle'
            }`}>
              {/* Status Icon */}
              <div className="shrink-0 z-10 bg-bg-primary rounded-full">
                {isCompleted ? <CheckCircle2 className="w-8 h-8 text-success" /> :
                 isExecuting ? <Loader2 className="w-8 h-8 text-accent-cyan animate-spin" /> :
                 needsApproval ? <AlertTriangle className="w-8 h-8 text-warning animate-pulse" /> :
                 <Circle className="w-8 h-8 text-text-secondary" />}
              </div>

              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-mono text-text-secondary">STEP {action.stepNumber}</span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                    action.blastRadius === 'critical' || action.blastRadius === 'high' ? 'bg-danger/20 text-danger' : 
                    action.blastRadius === 'medium' ? 'bg-warning/20 text-warning' : 'bg-success/20 text-success'
                  }`}>
                    {action.blastRadius} Radius
                  </span>
                </div>
                <div className={`font-semibold ${isCompleted ? 'text-text-secondary line-through' : 'text-text-primary'}`}>
                  {action.name}
                </div>
              </div>

              {/* Action Buttons / Execution Time */}
              <div className="shrink-0 text-right">
                {isCompleted && action.executionTimeMs && (
                  <span className="text-xs text-text-secondary font-mono">{action.executionTimeMs}ms</span>
                )}
                {isPending && (action.blastRadius === 'low' || action.blastRadius === 'medium') && (
                  <button 
                    onClick={() => onExecute(action.id)}
                    className="px-4 py-1.5 bg-accent-cyan/20 text-accent-cyan hover:bg-accent-cyan hover:text-bg-primary rounded font-medium text-sm transition-colors"
                  >
                    Execute
                  </button>
                )}
                {needsApproval && (
                  <button 
                    onClick={() => onApprove(action.id)}
                    className="px-4 py-1.5 bg-warning text-bg-primary hover:bg-warning/80 rounded font-bold text-sm transition-colors animate-pulse"
                  >
                    Approve Action
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
