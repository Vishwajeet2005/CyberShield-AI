import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const data = [
  { name: 'Critical', value: 12, color: '#ff3366' },
  { name: 'High', value: 45, color: '#ff9900' },
  { name: 'Medium', value: 85, color: '#eab308' },
  { name: 'Low', value: 130, color: '#00ff88' },
];

export default function ThreatSummary() {
  return (
    <div className="glass rounded-xl p-4 h-[300px] flex flex-col">
      <h3 className="font-bold text-lg mb-2">Alert Distribution</h3>
      <div className="flex-1 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
              stroke="none"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} style={{ filter: `drop-shadow(0 0 4px ${entry.color}80)` }} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ backgroundColor: '#111827', borderColor: '#1e2d42', borderRadius: '8px' }}
              itemStyle={{ color: '#f0f4ff' }}
            />
            <Legend 
              verticalAlign="bottom" 
              height={36}
              iconType="circle"
              formatter={(value, entry: any) => <span style={{ color: '#8899aa', fontSize: '12px' }}>{value}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
