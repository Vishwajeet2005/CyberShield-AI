import AttributionPanel from '../components/aapa/AttributionPanel';
import TTpHeatmap from '../components/aapa/TTpHeatmap';
import NextMovePredictor from '../components/aapa/NextMovePredictor';

export default function APTAttribution() {
  const mockActors = [
    { id: '1', name: 'Lazarus Group', country: 'KP', confidence: 85, matchedTtps: ['T1486', 'T1059', 'T1543'], evidenceSummary: 'Observed usage of unique DTrack malware variant and fast-flux DNS infrastructure matching previous campaigns targeting healthcare.', isPrimary: true },
    { id: '2', name: 'APT41', country: 'CN', confidence: 45, matchedTtps: ['T1059', 'T1105'], evidenceSummary: 'Overlap in initial access vectors, but lacking signature post-exploitation tooling.', isPrimary: false },
    { id: '3', name: 'FIN7', country: 'RU', confidence: 20, matchedTtps: ['T1566'], evidenceSummary: 'Generic phishing techniques used, low confidence overall match.', isPrimary: false }
  ];

  return (
    <div className="flex flex-col gap-4 h-full">
      <h1 className="text-2xl font-bold text-text-primary mb-2">APT Attribution & Prediction Agent (AAPA)</h1>
      
      <div className="glass p-4 rounded-xl flex items-center gap-4 shrink-0 overflow-x-auto">
        <span className="text-sm text-text-secondary font-bold uppercase shrink-0">Current Campaign TTPs:</span>
        {['T1566.001', 'T1059.001', 'T1078', 'T1105', 'T1486', 'T1098'].map(ttp => (
          <span key={ttp} className="px-2 py-1 bg-accent-cyan/20 border border-accent-cyan/50 text-accent-cyan text-xs font-mono rounded shrink-0">
            {ttp}
          </span>
        ))}
      </div>

      <div className="flex gap-4 flex-1 min-h-0">
        <div className="w-1/3 overflow-y-auto pr-2 scrollbar-thin">
          <AttributionPanel actors={mockActors} />
        </div>
        <div className="w-1/3 flex flex-col h-full">
          <TTpHeatmap />
        </div>
        <div className="w-1/3 flex flex-col h-full">
          <NextMovePredictor />
        </div>
      </div>
    </div>
  );
}
