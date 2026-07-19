import { ThreatActor } from '../../types';

export default function AttributionPanel({ actors }: { actors: ThreatActor[] }) {
  if (!actors.length) return null;

  return (
    <div className="flex flex-col gap-4">
      {actors.map((actor, idx) => (
        <div key={actor.id} className={`glass rounded-xl p-5 relative overflow-hidden transition-all ${actor.isPrimary ? 'border-accent-cyan/50 glow-cyan' : 'opacity-80'}`}>
          {actor.isPrimary && (
            <div className="absolute top-0 right-0 bg-accent-cyan/20 text-accent-cyan text-[10px] font-bold px-3 py-1 rounded-bl-lg">
              PRIMARY SUSPECT
            </div>
          )}
          
          <div className="flex justify-between items-start mb-4">
            <div>
              <h3 className="text-xl font-bold text-text-primary flex items-center gap-2">
                {actor.name} <span className="text-2xl">{actor.country === 'CN' ? '🇨🇳' : actor.country === 'RU' ? '🇷🇺' : actor.country === 'KP' ? '🇰🇵' : '🏴‍☠️'}</span>
              </h3>
            </div>
            <div className="text-right">
              <div className={`text-3xl font-bold ${actor.confidence >= 80 ? 'text-danger' : 'text-warning'}`}>
                {actor.confidence}%
              </div>
              <div className="text-[10px] text-text-secondary uppercase">Confidence</div>
            </div>
          </div>

          <div className="w-full h-2 bg-bg-primary rounded-full mb-4 overflow-hidden">
            <div 
              className={`h-full ${actor.confidence >= 80 ? 'bg-danger' : 'bg-warning'}`} 
              style={{ width: `${actor.confidence}%` }} 
            />
          </div>

          <div className="mb-4">
            <div className="text-xs text-text-secondary mb-2">Matched TTPs:</div>
            <div className="flex flex-wrap gap-2">
              {actor.matchedTtps.map(ttp => (
                <span key={ttp} className="px-2 py-1 bg-white/5 border border-white/10 rounded text-xs font-mono text-accent-cyan">
                  {ttp}
                </span>
              ))}
            </div>
          </div>

          <p className="text-sm text-text-secondary mb-4 line-clamp-2">
            {actor.evidenceSummary}
          </p>

          <button className="w-full py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-sm transition-colors text-text-primary">
            View Actor Profile
          </button>
        </div>
      ))}
    </div>
  );
}
