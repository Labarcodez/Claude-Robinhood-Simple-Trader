from risk import data_is_fresh, validate_order


def test_valid_buy():
    assert validate_order(
        action="BUY", quantity=1, notional=5,
        buying_power=10, tradable=True
    ).allowed


def test_buy_cannot_exceed_buying_power():
    assert not validate_order(
        action="BUY", quantity=1, notional=11,
        buying_power=10, tradable=True
    ).allowed


def test_sell_can_execute_with_zero_buying_power():
    assert validate_order(
        action="SELL", quantity=1, notional=5,
        buying_power=0, tradable=True
    ).allowed


def test_kill_switch():
    assert not validate_order(
        action="BUY", quantity=1, notional=5,
        buying_power=10, tradable=True, kill_switch=True
    ).allowed


def test_non_tradable():
    assert not validate_order(
        action="BUY", quantity=1, notional=5,
        buying_power=10, tradable=False
    ).allowed


def test_data_freshness_rejects_future_timestamp():
    from datetime import datetime, timedelta, timezone
    future = datetime.now(timezone.utc) + timedelta(seconds=2)
    assert not data_is_fresh(future, 5)
