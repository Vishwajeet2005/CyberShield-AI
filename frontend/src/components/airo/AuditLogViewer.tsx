import { AuditEntry } from '../../types';
import { ShieldCheck } from 'lucide-react';

export default function AuditLogViewer({ logs }: { logs: AuditEntry[] }) {
  return (
    <div className="glass rounded-xl overflow-hidden flex flex-col h-full">
      <div className="p-4 border-b border-border-subtle bg-bg-secondary/50 flex justify-between items-center">
        <h3 className="font-bold text-lg">Immutable Audit Log</h3>
        <div className="flex items-center gap-2 text-success text-sm bg-success/10 px-3 py-1 rounded border border-success/30">
          <ShieldCheck className="w-4 h-4" />
          <span className="font-medium">Hash Chain Valid</span>
        </div>
      </div>
      <div className="overflow-x-auto flex-1">
        <table className="w-full text-left text-sm whitespace-nowrap">
          <thead className="bg-bg-primary/50 text-text-secondary sticky top-0">
            <tr>
              <th className="px-4 py-3 font-medium">Timestamp</th>
              <th className="px-4 py-3 font-medium">Module</th>
              <th className="px-4 py-3 font-medium">Action</th>
              <th className="px-4 py-3 font-medium">Actor</th>
              <th className="px-4 py-3 font-medium">Target</th>
              <th className="px-4 py-3 font-medium">Result</th>
              <th className="px-4 py-3 font-medium">Hash Integrity</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {logs.map(log => (
              <tr key={log.id} className="hover:bg-white/5 transition-colors font-mono text-xs">
                <td className="px-4 py-3 text-text-secondary">{new Date(log.timestamp).toISOString()}</td>
                <td className="px-4 py-3 text-accent-blue">{log.module}</td>
                <td className="px-4 py-3 text-text-primary">{log.action}</td>
                <td className="px-4 py-3 text-text-secondary">{log.actor}</td>
                <td className="px-4 py-3 text-text-secondary">{log.target}</td>
                <td className="px-4 py-3 text-success">{log.result}</td>
                <td className="px-4 py-3 text-text-secondary/50 truncate max-w-[150px]">{log.hash}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
