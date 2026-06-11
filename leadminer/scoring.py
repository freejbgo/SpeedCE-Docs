"""Lead scoring heuristics for CDN sales outreach."""

from __future__ import annotations

from dataclasses import dataclass

from .cdn_fingerprints import MAJOR_VENDORS
from .http_probe import ProbeResult

# Tranco rank buckets (lower rank = more traffic)
RANK_TIERS = [
    (10_000, 25),
    (100_000, 18),
    (500_000, 12),
    (1_000_000, 8),
    (5_000_000, 4),
]


@dataclass
class LeadScore:
    score: int
    tier: str
    reasons: list[str]


def score_lead(
    probe: ProbeResult,
    *,
    dns_vendors: list[str],
    tranco_rank: int | None = None,
    target_regions_slow: bool = False,
) -> LeadScore:
    """Higher score = better outreach candidate for overseas CDN PoC."""
    score = 0
    reasons: list[str] = []
    all_vendors = list(dict.fromkeys(probe.cdn_vendors + dns_vendors))

    if tranco_rank is not None:
        for threshold, points in RANK_TIERS:
            if tranco_rank <= threshold:
                score += points
                reasons.append(f"tranco_rank={tranco_rank} (+{points})")
                break

    if not probe.ok:
        return LeadScore(score=0, tier="skip", reasons=["unreachable"])

    if not all_vendors:
        score += 20
        reasons.append("no_cdn_detected (+20)")
    elif any(v in MAJOR_VENDORS for v in all_vendors):
        score += 12
        reasons.append(f"major_cdn={','.join(all_vendors)} (+12)")
    else:
        score += 6
        reasons.append(f"niche_cdn={','.join(all_vendors)} (+6)")

    if probe.ttfb_ms is not None:
        if probe.ttfb_ms >= 800:
            score += 15
            reasons.append(f"slow_ttfb={probe.ttfb_ms}ms (+15)")
        elif probe.ttfb_ms >= 400:
            score += 8
            reasons.append(f"moderate_ttfb={probe.ttfb_ms}ms (+8)")

    if probe.asset_count_hint >= 8:
        score += 10
        reasons.append(f"many_third_party_assets={probe.asset_count_hint} (+10)")
    elif probe.asset_count_hint >= 3:
        score += 5
        reasons.append(f"some_third_party_assets={probe.asset_count_hint} (+5)")

    if not probe.uses_https:
        score += 5
        reasons.append("no_https (+5)")

    if target_regions_slow:
        score += 10
        reasons.append("slow_in_target_region (+10)")

    if score >= 45:
        tier = "hot"
    elif score >= 28:
        tier = "warm"
    elif score >= 15:
        tier = "cool"
    else:
        tier = "low"

    return LeadScore(score=score, tier=tier, reasons=reasons)
