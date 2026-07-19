import RiskBadge from './RiskBadge';
import { Severity } from '../../types';

interface Event {
  id: string;
  timestamp: string;
  severity: Severity;
  description: string;
}

export default function ThreatTimeline({ events }: { events: Event[] }) {
  return (
    <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border-subtle before:to-transparent">
      {events.map((event) => (
        <div key={event.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
          <div className="flex items-center justify-center w-10 h-10 rounded-full border border-border-subtle bg-bg-secondary shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 shadow-[0_0_10px_rgba(0,0,0,0.5)]">
            <div className={`w-3 h-3 rounded-full ${event.severity === 'critical' ? 'bg-danger animate-pulse glow-red' : event.severity === 'high' ? 'bg-warning' : event.severity === 'medium' ? 'bg-yellow-500' : 'bg-success'}`} />
          </div>
          <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] glass p-4 rounded-xl shadow-lg group-hover:border-accent-cyan/30 transition-colors">
            <div className="flex items-center justify-between mb-2">
              <time className="text-xs text-accent-cyan font-mono">{new Date(event.timestamp).toLocaleTimeString()}</time>
              <RiskBadge severity={event.severity} />
            </div>
            <p className="text-sm text-text-primary">{event.description}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
