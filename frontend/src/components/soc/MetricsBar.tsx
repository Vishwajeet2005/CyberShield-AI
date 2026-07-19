import { SystemMetrics } from '../../types';
import MetricCard from '../shared/MetricCard';
import { Clock, ShieldAlert, Activity, CheckCircle, ShieldX, Target } from 'lucide-react';

export default function MetricsBar({ metrics }: { metrics: SystemMetrics }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      <MetricCard title="MTTD" value={metrics.mttd} icon={<Clock className="w-5 h-5" />} change={-12} />
      <MetricCard title="MTTR" value={metrics.mttr} icon={<Activity className="w-5 h-5" />} change={-8} />
      <MetricCard title="True Positives" value={metrics.tpr} icon={<Target className="w-5 h-5" />} change={2} />
      <MetricCard title="False Positives" value={metrics.fpr} icon={<ShieldX className="w-5 h-5" />} change={-15} />
      <MetricCard title="Alerts Today" value={metrics.alertsToday} icon={<ShieldAlert className="w-5 h-5" />} change={5} />
      <MetricCard title="Auto-Contained" value={metrics.containments} icon={<CheckCircle className="w-5 h-5" />} change={24} />
    </div>
  );
}
