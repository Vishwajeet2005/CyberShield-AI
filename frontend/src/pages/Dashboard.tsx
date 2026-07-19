import { useState, useEffect } from 'react';
import MetricsBar from '../components/soc/MetricsBar';
import AlertFeed from '../components/soc/AlertFeed';
import ThreatGlobe from '../components/soc/ThreatGlobe';
import ThreatSummary from '../components/soc/ThreatSummary';
import { api } from '../api/client';
import { SystemMetrics } from '../types';

export default function Dashboard() {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      const data = await api.getMetrics();
      setMetrics(data);
    };
    fetchMetrics();
    const int = setInterval(fetchMetrics, 5000);
    return () => clearInterval(int);
  }, []);

  return (
    <div className="flex flex-col gap-4 h-full animate-fadeIn">
      {metrics && <MetricsBar metrics={metrics} />}
      
      <div className="flex flex-col lg:flex-row gap-4 flex-1 min-h-0">
        <div className="w-full lg:w-2/3 flex flex-col gap-4">
          <div className="h-[400px]">
            <ThreatGlobe />
          </div>
          <div className="flex-1 min-h-[300px]">
            <AlertFeed />
          </div>
        </div>
        
        <div className="w-full lg:w-1/3 flex flex-col gap-4">
          <ThreatSummary />
          
          <div className="glass rounded-xl p-4 flex-1">
            <h3 className="font-bold text-lg mb-4">Module Status</h3>
            <div className="space-y-3">
              {['BADE', 'AAPA', 'AIRO', 'VPA', 'CRDT'].map(mod => (
                <div key={mod} className="flex justify-between items-center p-2 bg-white/5 rounded border border-white/10">
                  <span className="font-mono text-sm">{mod} Engine</span>
                  <div className="flex items-center gap-2 text-xs">
                    <span className="text-success">ONLINE</span>
                    <div className="w-2 h-2 bg-success rounded-full animate-pulse" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
