import { useState, useEffect } from 'react';
import { Alert } from '../../types';
import RiskBadge from '../shared/RiskBadge';
import { api } from '../../api/client';
import LoadingSpinner from '../shared/LoadingSpinner';

export default function AlertFeed() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const data = await api.getAlerts();
        setAlerts(data.slice(0, 15));
      } finally {
        setLoading(false);
      }
    };
    
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="glass rounded-xl h-[600px] flex flex-col overflow-hidden">
      <div className="p-4 border-b border-border-subtle bg-bg-secondary/50 flex justify-between items-center">
        <h3 className="font-bold text-lg flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-danger animate-pulse" />
          Live Alert Feed
        </h3>
        <span className="text-xs bg-bg-primary px-2 py-1 rounded text-text-secondary border border-border-subtle">
          {alerts.length} Active
        </span>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-3 scrollbar-thin">
        {alerts.map((alert, i) => (
          <div 
            key={alert.id} 
            className="bg-bg-secondary/50 border border-border-subtle rounded-lg p-3 hover:border-accent-cyan/30 transition-all group animate-[slideIn_0.3s_ease-out_forwards]"
            style={{ animationDelay: `${i * 0.05}s` }}
          >
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center gap-2">
                <RiskBadge severity={alert.severity} />
                <span className="text-xs font-mono text-accent-blue bg-accent-blue/10 px-1.5 py-0.5 rounded">{alert.module}</span>
              </div>
              <span className="text-[10px] text-text-secondary font-mono">
                {new Date(alert.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <h4 className="font-medium text-sm text-text-primary mb-1">{alert.title}</h4>
            <p className="text-xs text-text-secondary mb-3">{alert.description}</p>
            <div className="flex justify-between items-center text-xs">
              <div className="font-mono text-text-secondary bg-bg-primary px-2 py-1 rounded border border-border-subtle">
                {alert.entityName} <span className="opacity-50">|</span> {alert.ipAddress}
              </div>
              <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button className="text-text-secondary hover:text-white px-2 py-1">Dismiss</button>
                <button className="text-accent-cyan hover:bg-accent-cyan/10 px-2 py-1 rounded border border-accent-cyan/30 transition-colors">Investigate</button>
              </div>
            </div>
          </div>
        ))}
        {alerts.length === 0 && (
          <div className="h-full flex items-center justify-center text-text-secondary text-sm">
            No active alerts
          </div>
        )}
      </div>
    </div>
  );
}
