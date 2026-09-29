import json
from pathlib import Path

from execution_guard import reserve, mark_status, unresolved
from fomo import score, chase_state
from risk import validate_order

def test_account_aware_guard_has_no_portfolio_caps():
    ok = validate_order(
        action="BUY", quantity=10, notional=50, buying_power=100,
        tradable=True, kill_switch=False
    )
    assert ok.allowed

def test_buy_cannot_exceed_broker_buying_power():
    result = validate_order(
        action="BUY", quantity=10, notional=101, buying_power=100,
        tradable=True
    )
    assert not result.allowed

def test_fomo_score_is_bounded():
    assert 0 <= score({k: 100 for k in load_weights()}) <= 100

def load_weights():
    return list(json.loads(Path("config/fomo.json").read_text())["weights"])

def test_chase_detector():
    state, reasons = chase_state(
        vwap_distance_pct=10,
        breakout_distance_pct=7,
        upper_wick_pct=20,
        volume_acceleration=-1,
        seconds_since_breakout=500,
    )
    assert state == "CHASING"
    assert reasons

def test_fomo_config_exists():
    data = json.loads(Path("config/fomo.json").read_text())
    assert sum(data["weights"].values()) == 92
