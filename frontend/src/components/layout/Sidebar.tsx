import { Link, useLocation } from 'react-router-dom';
import { 
  ShieldAlert, Activity, Target, Zap, 
  ShieldCheck, Network, ClipboardList, TrendingUp,
  Shield
} from 'lucide-react';

const NAV_ITEMS = [
  { path: '/', label: 'SOC Dashboard', icon: ShieldAlert },
  { path: '/anomaly', label: 'Anomaly Detection', icon: Activity },
  { path: '/attribution', label: 'APT Attribution', icon: Target },
  { path: '/incidents', label: 'Incident Response', icon: Zap },
  { path: '/vulnerabilities', label: 'Vulnerability Manager', icon: ShieldCheck },
  { path: '/digital-twin', label: 'Digital Twin', icon: Network },
  { path: '/audit', label: 'Audit Log', icon: ClipboardList },
  { path: '/executive', label: 'Executive View', icon: TrendingUp },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-64 bg-bg-secondary border-r border-border-subtle flex flex-col h-full">
      <div className="p-6 flex items-center gap-3 border-b border-border-subtle">
        <Shield className="w-8 h-8 text-accent-cyan animate-pulse-slow" />
        <div>
          <h1 className="font-bold text-lg text-text-primary leading-tight">CyberShield</h1>
          <span className="text-xs text-accent-cyan tracking-wider font-semibold">AI PLATFORM</span>
        </div>
      </div>
      
      <nav className="flex-1 py-4">
        <ul className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-3 px-6 py-3 transition-colors duration-200 ${
                    isActive 
                      ? 'bg-accent-cyan/10 border-l-4 border-accent-cyan text-accent-cyan' 
                      : 'border-l-4 border-transparent text-text-secondary hover:bg-white/5 hover:text-text-primary'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium text-sm">{item.label}</span>
                  {item.path === '/incidents' && (
                    <span className="ml-auto bg-danger/20 text-danger text-[10px] font-bold px-2 py-0.5 rounded-full animate-pulse">2</span>
                  )}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="p-4 border-t border-border-subtle text-center text-xs text-text-secondary">
        v2.4.0 (Live Demo)
      </div>
    </aside>
  );
}
