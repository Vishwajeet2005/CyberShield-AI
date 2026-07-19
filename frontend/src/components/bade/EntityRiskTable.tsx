import { Entity } from '../../types';
import RiskBadge from '../shared/RiskBadge';

export default function EntityRiskTable({ entities }: { entities: Entity[] }) {
  return (
    <div className="glass rounded-xl overflow-hidden flex flex-col h-full">
      <div className="p-4 border-b border-border-subtle bg-bg-secondary/50">
        <h3 className="font-bold text-lg">Monitored Entities</h3>
      </div>
      <div className="overflow-x-auto flex-1">
        <table className="w-full text-left text-sm whitespace-nowrap">
          <thead className="bg-bg-primary/50 text-text-secondary sticky top-0">
            <tr>
              <th className="px-4 py-3 font-medium">Entity</th>
              <th className="px-4 py-3 font-medium">Type</th>
              <th className="px-4 py-3 font-medium">IP Address</th>
              <th className="px-4 py-3 font-medium">Risk Score</th>
              <th className="px-4 py-3 font-medium">Deviation</th>
              <th className="px-4 py-3 font-medium">Risk Level</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {entities.map(entity => (
              <tr key={entity.id} className={`hover:bg-white/5 transition-colors cursor-pointer ${entity.riskLevel === 'critical' ? 'bg-danger/5' : ''}`}>
                <td className="px-4 py-3 font-medium">{entity.name}</td>
                <td className="px-4 py-3 text-text-secondary">{entity.type}</td>
                <td className="px-4 py-3 font-mono text-xs">{entity.ipAddress}</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <span className="w-8 text-right font-mono">{entity.currentScore}</span>
                    <div className="w-24 h-1.5 bg-bg-primary rounded-full overflow-hidden">
                      <div 
                        className={`h-full ${entity.currentScore > 80 ? 'bg-danger' : entity.currentScore > 60 ? 'bg-warning' : 'bg-success'}`} 
                        style={{ width: `${entity.currentScore}%` }} 
                      />
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3">
                  <span className={`text-xs font-bold ${entity.deviation > 20 ? 'text-danger' : 'text-text-secondary'}`}>
                    +{entity.deviation}
                  </span>
                </td>
                <td className="px-4 py-3"><RiskBadge severity={entity.riskLevel} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
