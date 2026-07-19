import { Incident } from '../../types';
import RiskBadge from '../shared/RiskBadge';

export default function IncidentPanel({ incident }: { incident: Incident }) {
  if (!incident) return null;

  return (
    <div className="glass rounded-xl p-5 flex flex-col h-full border-t-4 border-t-danger">
      <div className="flex justify-between items-start mb-6">
        <div>
          <RiskBadge severity={incident.severity} />
          <h2 className="text-2xl font-bold mt-2 text-text-primary">{incident.title}</h2>
          <div className="text-xs font-mono text-text-secondary mt-1">INC-{incident.id}</div>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${
          incident.status === 'open' ? 'bg-danger/20 text-danger border border-danger/50' :
          incident.status === 'contained' ? 'bg-warning/20 text-warning border border-warning/50' :
          'bg-success/20 text-success border border-success/50'
        }`}>
          {incident.status}
        </div>
      </div>

      <div className="mb-6">
        <h4 className="text-sm font-bold text-text-secondary mb-2 uppercase tracking-wider">Affected Entities</h4>
        <div className="flex flex-wrap gap-2">
          {incident.affectedEntities.map(entity => (
            <span key={entity} className="px-2 py-1 bg-white/5 border border-white/10 rounded text-sm font-mono">
              {entity}
            </span>
          ))}
        </div>
      </div>

      <div className="flex-1">
        <h4 className="text-sm font-bold text-text-secondary mb-3 uppercase tracking-wider">Incident Timeline</h4>
        <div className="space-y-4 relative before:absolute before:inset-0 before:ml-2 before:-translate-x-px before:h-full before:w-0.5 before:bg-border-subtle">
          {incident.timeline.map((item, idx) => (
            <div key={idx} className="relative flex items-start gap-4">
              <div className="w-4 h-4 rounded-full bg-bg-secondary border-2 border-accent-cyan shrink-0 z-10 mt-0.5" />
              <div>
                <div className="text-xs font-mono text-accent-cyan mb-0.5">{new Date(item.timestamp).toLocaleTimeString()}</div>
                <div className="text-sm text-text-primary">{item.action}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <button className="w-full mt-6 py-3 bg-accent-blue hover:bg-accent-blue/80 text-white font-bold rounded-lg transition-colors shadow-[0_0_15px_rgba(0,102,255,0.3)]">
        Run Containment Playbook
      </button>
    </div>
  );
}
