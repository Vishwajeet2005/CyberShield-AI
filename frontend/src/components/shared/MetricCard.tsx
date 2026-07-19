import { ReactNode } from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  unit?: string;
  change?: number; // positive for up, negative for down
  icon: ReactNode;
}

export default function MetricCard({ title, value, unit, change, icon }: MetricCardProps) {
  return (
    <div className="glass p-4 rounded-xl relative overflow-hidden group hover:glow-cyan transition-all duration-300">
      <div className="flex justify-between items-start mb-2">
        <div className="text-text-secondary text-sm font-medium">{title}</div>
        <div className="text-accent-cyan opacity-80 group-hover:scale-110 transition-transform">{icon}</div>
      </div>
      <div className="flex items-baseline gap-1">
        <div className="text-2xl font-bold text-text-primary">{value}</div>
        {unit && <div className="text-sm text-text-secondary">{unit}</div>}
      </div>
      {change !== undefined && (
        <div className={`text-xs mt-2 font-medium flex items-center gap-1 ${change >= 0 ? 'text-success' : 'text-danger'}`}>
          {change >= 0 ? '↑' : '↓'} {Math.abs(change)}% vs last hr
        </div>
      )}
      <div className="absolute -bottom-4 -right-4 w-16 h-16 bg-accent-cyan/10 rounded-full blur-xl group-hover:bg-accent-cyan/20 transition-colors" />
    </div>
  );
}
