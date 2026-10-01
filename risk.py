"""Broker-state-aware execution guards.

This module intentionally does not impose portfolio percentage, position-count,
daily-loss, reward/risk, or trade-frequency limits. Sizing and trade selection
belong to Claude using the live Robinhood account state.

The guards here are operational protections only.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config" / "risk.json"


@dataclass
class ExecutionDecision:
    allowed: bool
    reason: str


def load_config():
    configured = os.getenv("TRADER_RISK_CONFIG")
    path = Path(configured) if configured else CONFIG_PATH
    return json.loads(path.read_text())


def validate_order(
    *,
    action: str,
    quantity: float,
    notional: float,
    buying_power: float,
    tradable: bool,
    kill_switch: bool = False,
):
    if kill_switch:
        return ExecutionDecision(False, "kill switch active")
    if action not in {"BUY", "SELL"}:
        return ExecutionDecision(False, "invalid equity action")
    if quantity <= 0:
        return ExecutionDecision(False, "non-positive quantity")
    if notional <= 0:
        return ExecutionDecision(False, "non-positive notional")
    if buying_power < 0:
        return ExecutionDecision(False, "invalid broker buying power")
    if action == "BUY" and notional > buying_power:
        return ExecutionDecision(False, "order exceeds broker-reported buying power")
    if not tradable:
        return ExecutionDecision(False, "broker reports security is not tradable")
    return ExecutionDecision(True, "operational execution checks passed")


def data_is_fresh(observed_at, max_age_seconds: float) -> bool:
    if max_age_seconds < 0:
        return False
    if isinstance(observed_at, str):
        observed_at = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    if observed_at.tzinfo is None:
        observed_at = observed_at.replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - observed_at).total_seconds()
    return 0 <= age <= max_age_seconds
