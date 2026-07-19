import { useState, useEffect } from 'react';
import MetricCard from '../components/shared/MetricCard';
import EntityRiskTable from '../components/bade/EntityRiskTable';
import AnomalyScoreChart from '../components/bade/AnomalyScoreChart';
import LateralMovementGraph from '../components/bade/LateralMovementGraph';
import { api } from '../api/client';
import { Entity } from '../types';
import { Activity, ShieldAlert, Target, ShieldCheck } from 'lucide-react';

export default function AnomalyDetection() {
  const [entities, setEntities] = useState<Entity[]>([]);

  useEffect(() => {
    // Generate mock entities
    const mock: Entity[] = [
      { id: '1', name: 'WORKSTATION-HR-01', type: 'Workstation', ipAddress: '10.0.1.45', department: 'HR', baselineScore: 10, currentScore: 85, deviation: 75, riskLevel: 'critical', lastSeen: new Date().toISOString() },
      { id: '2', name: 'DOMAIN-CONTROLLER-01', type: 'Server', ipAddress: '10.0.0.5', department: 'IT', baselineScore: 5, currentScore: 65, deviation: 60, riskLevel: 'high', lastSeen: new Date().toISOString() },
      { id: '3', name: 'FILE-SERVER-02', type: 'Server', ipAddress: '10.0.0.15', department: 'Finance', baselineScore: 12, currentScore: 45, deviation: 33, riskLevel: 'medium', lastSeen: new Date().toISOString() },
      { id: '4', name: 'AIIMS-EMR-SERVER', type: 'Server', ipAddress: '10.1.0.10', department: 'Clinical', baselineScore: 8, currentScore: 15, deviation: 7, riskLevel: 'low', lastSeen: new Date().toISOString() },
    ];
    setEntities(mock);
  }, []);

  return (
    <div className="flex flex-col gap-4 h-full">
      <div className="flex justify-between items-center mb-2">
        <h1 className="text-2xl font-bold text-text-primary">Behavioural Anomaly Detection Engine (BADE)</h1>
        <div className="flex items-center gap-2 px-3 py-1 bg-accent-cyan/10 border border-accent-cyan/30 rounded-full text-accent-cyan text-sm">
          <div className="w-2 h-2 bg-accent-cyan rounded-full animate-pulse" /> Live Analysis
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4 shrink-0">
        <MetricCard title="Entities Monitored" value="14,235" icon={<Activity />} />
        <MetricCard title="Anomalies Today" value="842" icon={<ShieldAlert />} change={12} />
        <MetricCard title="True Positive Rate" value="96.5%" icon={<Target />} change={0.5} />
        <MetricCard title="False Positive Rate" value="2.1%" icon={<ShieldCheck />} change={-0.3} />
      </div>

      <div className="flex gap-4 flex-1 min-h-0">
        <div className="w-3/5 flex flex-col h-full">
          <EntityRiskTable entities={entities} />
        </div>
        <div className="w-2/5 flex flex-col gap-4 h-full">
          <div className="h-1/2">
            <AnomalyScoreChart />
          </div>
          <div className="h-1/2">
            <LateralMovementGraph />
          </div>
        </div>
      </div>
    </div>
  );
}
