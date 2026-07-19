import { Severity } from '../../types';

export default function RiskBadge({ severity }: { severity: Severity }) {
  const styles = {
    critical: 'bg-danger/20 text-danger border-danger/50 animate-pulse-slow glow-red',
    high: 'bg-warning/20 text-warning border-warning/50',
    medium: 'bg-yellow-500/20 text-yellow-500 border-yellow-500/50',
    low: 'bg-success/20 text-success border-success/50',
  };

  return (
    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${styles[severity]}`}>
      {severity}
    </span>
  );
}
