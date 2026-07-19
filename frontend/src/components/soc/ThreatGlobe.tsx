export default function ThreatGlobe() {
  const cities = [
    { x: '35%', y: '35%', name: 'Delhi' },
    { x: '25%', y: '60%', name: 'Mumbai' },
    { x: '35%', y: '75%', name: 'Bangalore' },
    { x: '45%', y: '70%', name: 'Chennai' },
    { x: '40%', y: '65%', name: 'Hyderabad' },
    { x: '65%', y: '45%', name: 'Kolkata' },
  ];

  return (
    <div className="glass rounded-xl h-[400px] relative overflow-hidden flex items-center justify-center bg-[url('https://upload.wikimedia.org/wikipedia/commons/e/eb/Blank_map_of_India.svg')] bg-contain bg-no-repeat bg-center">
      <div className="absolute inset-0 bg-bg-primary/80" /> {/* Darken map */}
      <div className="absolute inset-0 border-[1px] border-accent-cyan/10 rounded-xl pointer-events-none" />
      
      {/* Decorative grid */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(0,212,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(0,212,255,0.05)_1px,transparent_1px)] bg-[size:20px_20px]" />
      
      {/* Scanning line */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-accent-cyan/30 shadow-[0_0_15px_rgba(0,212,255,0.5)] animate-scan" />

      {cities.map((city, i) => (
        <div 
          key={city.name}
          className="absolute"
          style={{ left: city.x, top: city.y }}
        >
          {/* Pulsing rings */}
          <div className="absolute -inset-4 border border-danger/30 rounded-full animate-ping" style={{ animationDelay: `${i * 0.5}s`, animationDuration: '3s' }} />
          <div className="absolute -inset-2 border border-danger/50 rounded-full animate-ping" style={{ animationDelay: `${i * 0.5 + 0.2}s`, animationDuration: '3s' }} />
          
          {/* Core dot */}
          <div className="w-2 h-2 bg-danger rounded-full relative z-10 glow-red" />
          
          {/* Label */}
          <div className="absolute left-3 top-1/2 -translate-y-1/2 text-[10px] font-mono text-accent-cyan bg-bg-primary/80 px-1 rounded border border-accent-cyan/30 whitespace-nowrap hidden md:block">
            {city.name}
          </div>
        </div>
      ))}
      
      {/* Connecting lines between some nodes */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-30">
        <path d="M 35% 35% L 25% 60%" stroke="#ff3366" strokeWidth="1" strokeDasharray="4 4" className="animate-pulse" />
        <path d="M 35% 35% L 40% 65%" stroke="#00d4ff" strokeWidth="1" />
        <path d="M 40% 65% L 45% 70%" stroke="#00d4ff" strokeWidth="1" />
        <path d="M 35% 75% L 25% 60%" stroke="#ff3366" strokeWidth="1" strokeDasharray="4 4" className="animate-pulse" />
      </svg>
    </div>
  );
}
