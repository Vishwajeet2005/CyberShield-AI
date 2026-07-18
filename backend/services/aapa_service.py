"""
CyberShield AI — AAPA Service
APT attribution via cosine similarity + Markov chain next-move prediction.
"""

import numpy as np
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from data.mitre_attack import THREAT_ACTORS, ATTACK_TECHNIQUES, THREAT_ACTORS_BY_ID
from models import ThreatActor, Attribution, NextMove, TTpAnalysisResponse

# Default observed TTPs for demo (the active APT41 incident)
DEFAULT_OBSERVED_TTPS = ["T1566.001", "T1059.003", "T1055", "T1021.002", "T1070.004"]

# Full TTP universe for vector building
ALL_TTPS = sorted(ATTACK_TECHNIQUES.keys())


def _build_ttp_vector(ttps: List[str]) -> np.ndarray:
    """Convert a list of TTP IDs into a binary indicator vector over ALL_TTPS."""
    vec = np.zeros(len(ALL_TTPS))
    for i, t in enumerate(ALL_TTPS):
        if t in ttps:
            vec[i] = 1.0
    return vec


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def get_threat_actors() -> List[ThreatActor]:
    return [
        ThreatActor(
            id=actor["id"],
            name=actor["name"],
            aliases=actor["aliases"],
            origin=actor["origin"],
            motivation=actor["motivation"],
            targets=actor["targets"],
            ttps=actor["ttps"],
            campaigns=actor["campaigns"],
            confidence=actor["confidence"],
            last_seen=actor["last_seen"],
            description=actor["description"],
            iocs=actor.get("iocs", []),
        )
        for actor in THREAT_ACTORS
    ]


def get_attribution_hypotheses(observed_ttps: Optional[List[str]] = None) -> List[Attribution]:
    if not observed_ttps:
        observed_ttps = DEFAULT_OBSERVED_TTPS

    obs_vec = _build_ttp_vector(observed_ttps)
    results = []

    for actor in THREAT_ACTORS:
        actor_vec = _build_ttp_vector(actor["ttps"])
        raw_sim = _cosine_similarity(obs_vec, actor_vec)

        # Apply context multiplier: higher if actor is known to target India CNI
        context_bonus = 1.15 if "Healthcare" in actor["targets"] or "Government" in actor["targets"] else 1.0
        confidence = round(min(100.0, raw_sim * 100 * context_bonus), 1)

        matched = [t for t in observed_ttps if t in actor["ttps"]]
        unmatched = [t for t in observed_ttps if t not in actor["ttps"]]

        # Generate next moves
        next_moves = _get_next_moves_for_actor(actor, observed_ttps)

        evidence = (
            f"Matched {len(matched)}/{len(observed_ttps)} observed TTPs against {actor['name']} profile. "
            f"Strongest matches: {', '.join(matched[:3])}. "
            f"Known campaigns targeting Indian CNI: {', '.join(actor['campaigns'][:2])}."
        )

        results.append(Attribution(
            actor_id=actor["id"],
            actor_name=actor["name"],
            origin=actor["origin"],
            confidence=confidence,
            matched_ttps=matched,
            unmatched_ttps=unmatched,
            predicted_next_moves=[nm.dict() for nm in next_moves],
            evidence=evidence,
        ))

    results.sort(key=lambda a: a.confidence, reverse=True)
    for i, r in enumerate(results):
        r.rank = i + 1
    return results


def _get_next_moves_for_actor(actor: Dict, observed_ttps: List[str]) -> List[NextMove]:
    """Use Markov chain to predict top 3 next moves."""
    transitions = actor.get("markov_transitions", {})
    next_prob: Dict[str, float] = {}

    # Aggregate transition probabilities from all observed TTPs
    for ttp in observed_ttps:
        if ttp in transitions:
            for next_ttp, prob in transitions[ttp].items():
                if next_ttp not in observed_ttps:  # Only predict TTPs not yet seen
                    next_prob[next_ttp] = max(next_prob.get(next_ttp, 0), prob)

    # Sort by probability and take top 3
    top3 = sorted(next_prob.items(), key=lambda x: x[1], reverse=True)[:3]

    moves = []
    for ttp_id, prob in top3:
        technique = ATTACK_TECHNIQUES.get(ttp_id, {})
        urgency = "immediate" if prob >= 0.6 else ("high" if prob >= 0.4 else "medium")
        moves.append(NextMove(
            ttp_id=ttp_id,
            ttp_name=technique.get("name", ttp_id),
            tactic=technique.get("tactic", "Unknown"),
            probability=round(prob, 2),
            description=technique.get("description", "Predicted next attacker action."),
            recommendation=_get_recommendation(ttp_id),
            urgency=urgency,
        ))
    return moves


def _get_recommendation(ttp_id: str) -> str:
    recs = {
        "T1486": "Immediately back up all critical data and verify offline backups are intact. Deploy ransomware honeypots.",
        "T1003.001": "Enable Credential Guard. Monitor LSASS access. Enforce Windows Defender Credential Guard.",
        "T1041": "Block egress to unknown IPs. Enable DLP. Capture outbound traffic for analysis.",
        "T1078": "Rotate all privileged credentials. Enable MFA for all accounts. Review recent logon events.",
        "T1055": "Block unsigned code injection. Enable kernel-level EDR. Review process injection alerts.",
        "T1547.001": "Audit startup locations. Monitor Run keys. Deploy application whitelisting.",
        "T1053.005": "Audit scheduled tasks. Block task creation by non-admin users.",
        "T1021.002": "Enforce SMB signing. Disable NTLM. Segment file servers from workstations.",
        "T1059.001": "Enable PowerShell Constrained Language Mode. Log all PowerShell activity to SIEM.",
        "T1059.003": "Enable command line auditing (Event 4688). Alert on cmd.exe spawned by Office apps.",
    }
    return recs.get(ttp_id, "Monitor for this technique. Enable relevant detections in your EDR/SIEM.")


def get_next_moves(actor_id: str) -> List[NextMove]:
    actor = THREAT_ACTORS_BY_ID.get(actor_id)
    if not actor:
        return []
    return _get_next_moves_for_actor(actor, DEFAULT_OBSERVED_TTPS)


def analyze_ttps(ttp_list: List[str]) -> TTpAnalysisResponse:
    attributions = get_attribution_hypotheses(ttp_list)
    top_actor = THREAT_ACTORS_BY_ID.get(attributions[0].actor_id) if attributions else None
    next_moves = _get_next_moves_for_actor(top_actor, ttp_list) if top_actor else []

    top_conf = attributions[0].confidence if attributions else 0
    summary = (
        f"Analysis of {len(ttp_list)} observed TTPs completed. "
        f"Primary attribution: {attributions[0].actor_name} ({top_conf}% confidence). "
        f"{'High confidence — immediate action recommended.' if top_conf >= 70 else 'Medium confidence — gather more indicators.'}"
    )

    return TTpAnalysisResponse(
        observed_ttps=ttp_list,
        attributions=attributions,
        next_moves=next_moves,
        confidence_summary=summary,
        analysis_timestamp=datetime.now(timezone.utc).isoformat(),
    )
