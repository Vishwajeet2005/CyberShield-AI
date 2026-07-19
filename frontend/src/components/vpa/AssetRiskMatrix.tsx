import { AssetItem } from '../../types';

export default function AssetRiskMatrix({ assets }: { assets: AssetItem[] }) {
  // Mock data for matrix
  const severities = ['Critical', 'High', 'Medium', 'Low'];
  
  return (
    <div className="glass rounded-xl p-4 flex flex-col h-full overflow-hidden">
      <h3 className="font-bold text-lg mb-4">Asset Risk Matrix</h3>
      <div className="flex-1 overflow-auto scrollbar-thin">
        <table className="w-full text-xs text-center border-collapse">
          <thead>
            <tr>
              <th className="p-2 border border-border-subtle bg-bg-secondary text-left w-1/3">Asset</th>
              {severities.map(s => <th key={s} className="p-2 border border-border-subtle bg-bg-secondary">{s}</th>)}
            </tr>
          </thead>
          <tbody>
            {assets.map(asset => (
              <tr key={asset.id} className="hover:bg-white/5 transition-colors">
                <td className="p-2 border border-border-subtle text-left truncate max-w-[120px]" title={asset.name}>{asset.name}</td>
                {severities.map(s => {
                  const val = Math.floor(Math.random() * (s === 'Critical' ? 3 : s === 'High' ? 8 : 15));
                  let colorClass = '';
                  if (val > 0) {
                    if (s === 'Critical') colorClass = 'bg-danger/80 text-white font-bold';
                    else if (s === 'High') colorClass = 'bg-warning/80 text-white font-bold';
                    else if (s === 'Medium') colorClass = 'bg-yellow-500/80 text-white font-bold';
                    else colorClass = 'bg-success/80 text-black font-bold';
                  } else {
                    colorClass = 'text-text-secondary/30';
                  }
                  
                  return (
                    <td key={s} className={`p-2 border border-border-subtle ${colorClass} cursor-pointer hover:opacity-80`}>
                      {val}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
