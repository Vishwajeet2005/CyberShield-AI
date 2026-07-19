import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

const data = Array.from({ length: 24 }).map((_, i) => ({
  time: `${i}:00`,
  'WORKSTATION-HR-01': 30 + Math.random() * 20 + (i > 18 ? 40 : 0),
  'DOMAIN-CONTROLLER-01': 40 + Math.random() * 15,
  'AIIMS-EMR-SERVER': 20 + Math.random() * 10,
}));

export default function AnomalyScoreChart() {
  return (
    <div className="glass rounded-xl p-4 h-full flex flex-col">
      <h3 className="font-bold text-lg mb-4">Anomaly Score Timeline (24h)</h3>
      <div className="flex-1 w-full min-h-[200px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e2d42" vertical={false} />
            <XAxis dataKey="time" stroke="#8899aa" fontSize={10} tickLine={false} />
            <YAxis stroke="#8899aa" fontSize={10} tickLine={false} axisLine={false} domain={[0, 100]} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#111827', borderColor: '#1e2d42', borderRadius: '8px', fontSize: '12px' }}
              itemStyle={{ fontSize: '12px', fontWeight: 'bold' }}
            />
            <ReferenceLine y={70} stroke="#ff3366" strokeDasharray="3 3" label={{ position: 'top', value: 'Threshold', fill: '#ff3366', fontSize: 10 }} />
            <Line type="monotone" dataKey="WORKSTATION-HR-01" stroke="#ff3366" strokeWidth={2} dot={false} activeDot={{ r: 4 }} />
            <Line type="monotone" dataKey="DOMAIN-CONTROLLER-01" stroke="#ff9900" strokeWidth={2} dot={false} activeDot={{ r: 4 }} />
            <Line type="monotone" dataKey="AIIMS-EMR-SERVER" stroke="#00d4ff" strokeWidth={2} dot={false} activeDot={{ r: 4 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
