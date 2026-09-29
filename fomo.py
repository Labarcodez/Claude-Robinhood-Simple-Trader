"""Transparent momentum/FOMO scoring helpers.

This is a ranking aid, not an automatic trading strategy. Inputs are expected
to be normalized to 0..100 before scoring.
"""
import json
from pathlib import Path

CONFIG = Path(__file__).parent / "config" / "fomo.json"

def load_config():
    return json.loads(CONFIG.read_text())

def score(features):
    c = load_config()
    total = 0.0
    for name, weight in c["weights"].items():
        total += float(features.get(name, 0)) * float(weight) / 100.0
    for name, penalty in c["penalties"].items():
        total -= float(features.get(name, 0)) * float(penalty) / 100.0
    return round(max(0.0, min(100.0, total)), 2)

def chase_state(*, vwap_distance_pct, breakout_distance_pct,
                upper_wick_pct, volume_acceleration,
                seconds_since_breakout=None):
    """Classify entry timing without turning FOMO into a buy signal."""
    reasons = []
    extension = abs(float(vwap_distance_pct))
    if extension > 8:
        reasons.append("far_from_vwap")
    if abs(float(breakout_distance_pct)) > 5:
        reasons.append("far_from_breakout")
    if float(upper_wick_pct) > 45:
        reasons.append("rejection_wick")
    if float(volume_acceleration) < 0:
        reasons.append("volume_fading")
    if seconds_since_breakout is not None and seconds_since_breakout > 300:
        reasons.append("breakout_is_aging")
    if len(reasons) >= 2:
        return "CHASING", reasons
    if reasons:
        return "EXTENDED", reasons
    return "EARLY_OR_CONTROLLED", reasons
