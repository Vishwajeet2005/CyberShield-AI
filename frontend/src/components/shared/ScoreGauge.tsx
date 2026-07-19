export default function ScoreGauge({ score, size = 120, label = "Risk Score" }: { score: number, size?: number, label?: string }) {
  const radius = (size - 20) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDashoffset = circumference - (score / 100) * circumference;
  
  let color = '#00ff88'; // green
  if (score >= 80) color = '#ff3366'; // red
  else if (score >= 60) color = '#ff9900'; // orange
  else if (score >= 30) color = '#eab308'; // yellow

  return (
    <div className="relative flex flex-col items-center justify-center" style={{ width: size, height: size }}>
      <svg className="transform -rotate-90 w-full h-full">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(255,255,255,0.1)"
          strokeWidth="8"
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth="8"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          className="transition-all duration-1000 ease-out"
          style={{ filter: `drop-shadow(0 0 4px ${color})` }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-bold" style={{ color }}>{score}</span>
        {label && <span className="text-[10px] text-text-secondary uppercase tracking-wider mt-1">{label}</span>}
      </div>
    </div>
  );
}
