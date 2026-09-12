import json
from pathlib import Path
from dataclasses import dataclass

CONFIG_PATH = Path(__file__).parent / "config" / "risk.json"

@dataclass
class RiskDecision:
    allowed: bool
    reason: str

def load_config():
    return json.loads(CONFIG_PATH.read_text())

def evaluate_new_position(equity, current_exposure, proposed_notional,
                          open_positions, daily_pnl_pct, new_positions_today,
                          symbol_exposure_after=0.0, kill_switch=False):
    c = load_config()
    if kill_switch:
        return RiskDecision(False, "kill switch active")
    if equity <= 0:
        return RiskDecision(False, "invalid equity")
    if proposed_notional <= 0:
        return RiskDecision(False, "non-positive proposed notional")
    if proposed_notional > equity * c["max_order_pct"]:
        return RiskDecision(False, "order exceeds maximum order size")
    if symbol_exposure_after > equity * c["max_position_pct"]:
        return RiskDecision(False, "post-trade symbol exposure exceeds position limit")
    if current_exposure + proposed_notional > equity * c["max_total_exposure_pct"]:
        return RiskDecision(False, "post-trade total exposure exceeds total limit")
    if open_positions >= c["max_open_positions"]:
        return RiskDecision(False, "maximum open positions reached")
    if new_positions_today >= c["max_new_positions_per_day"]:
        return RiskDecision(False, "daily new-position limit reached")
    if daily_pnl_pct <= -c["max_daily_loss_pct"]:
        return RiskDecision(False, "daily loss limit reached")
    return RiskDecision(True, "all hard risk checks passed")
