import { useState, useEffect } from 'react';
import { Bell, User } from 'lucide-react';

export default function Header() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="h-16 bg-bg-primary border-b border-border-subtle flex items-center justify-between px-6 shrink-0">
      <div className="flex items-center gap-6">
        <h2 className="font-semibold text-text-primary">AIIMS Delhi — Cyber Operations Center</h2>
        <div className="flex items-center gap-2 px-3 py-1 bg-danger/10 border border-danger/30 rounded-full">
          <div className="w-2 h-2 rounded-full bg-danger animate-pulse-slow glow-red" />
          <span className="text-xs font-bold text-danger tracking-wider">THREAT LEVEL: CRITICAL</span>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="text-sm text-text-secondary font-mono bg-bg-secondary px-3 py-1 rounded border border-border-subtle">
          {time.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata' })} IST
        </div>
        
        <button className="relative p-2 text-text-secondary hover:text-accent-cyan transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-danger rounded-full animate-pulse" />
        </button>

        <div className="flex items-center gap-3 pl-4 border-l border-border-subtle">
          <div className="text-right hidden md:block">
            <div className="text-sm font-medium text-text-primary">SOC Analyst</div>
            <div className="text-xs text-text-secondary">L3 Responder</div>
          </div>
          <div className="w-8 h-8 rounded-full bg-accent-blue/20 border border-accent-blue/50 flex items-center justify-center text-accent-cyan">
            <User className="w-4 h-4" />
          </div>
        </div>
      </div>
    </header>
  );
}
