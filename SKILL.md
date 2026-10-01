# Simple Trading Skill

Operate the Simple Claude Robinhood Trader as a LIVE-only autonomous equity
trader.

Claude is the trading brain. The local Python supervisor provides scheduling,
persistent state, duplicate-order protection, logging and recovery. Robinhood
MCP is the source of broker/account/market data and the execution interface.

There are NO arbitrary portfolio percentage, position-count, daily-loss,
order-size, confidence, reward/risk or daily-trade hard limits. Claude reads
the actual Robinhood wallet/account state and decides sizing. Operational
checks remain mandatory.

Before any new order:
1. Read account/buying power.
2. Read positions and open orders.
3. Reconcile unresolved local order intents.
4. Confirm tradability and fresh market data.
5. Decide size from live account state and thesis.
6. Run execution_guard.
7. Review the order.
8. Reserve the order intent.
9. Place through Robinhood MCP.
10. Verify broker status/fill/position state.

Never blindly retry an order with unknown status.

## Intraday behavior

Each cycle manages existing positions before looking for new entries. Claude may BUY, SELL, or HOLD based on fresh evidence. It should seek intraday opportunities without manufacturing trades. Near the end of the regular session, explicitly review whether open positions should be exited for the day.

Use all already-available MCP/data connectors when useful, but never invoke or request connect/install/authorization flows for another MCP. Never invent unavailable tools.

## Autonomous supervisor

Run:
python supervisor.py

The supervisor repeatedly launches Claude headlessly, prevents overlapping
cycles, honors the kill switch, logs failures/timeouts and lets the next cycle
reconcile broker state before acting again.

Configure:
TRADING_INTERVAL_SECONDS (default 60)
CLAUDE_CYCLE_TIMEOUT_SECONDS (default 600)
CLAUDE_COMMAND (default "claude -p")

The exact Claude Code/MCP environment must be configured on the machine. A
scheduler process alone cannot manufacture a Robinhood MCP connection.

## Universe

Discover ALL tradable long U.S. equities with 0 < current price < $10.00. The $10 ceiling is only a discovery ceiling. BUY sizing must come from actual Robinhood buying power and current broker rules.
Scanner filters only rank/prioritize. Use multiple passes when capped.

No options, shorting, margin borrowing, crypto, OTC or leveraged products.

## Momentum/FOMO

Use account, scanner, quotes, historical candles/volume, technicals,
fundamentals, earnings/events, Level 2, tradability and order tools available
from Robinhood.

FOMO score 0-100:
reward acceleration, RVOL, volume acceleration, breakout/retest, persistence,
relative strength, catalyst, liquidity/depth;
penalize extension, rejection, volume fade, spread, thin depth and stale data.

High score is research priority, not an automatic buy.

## Candles

Use get_equity_historicals for serious candidates. Inspect bodies, wicks,
higher highs/lows, breakout/retest structure and per-bar volume. Render with
chart.py when visual inspection is available.

## Kill switch

Stop new trading activity with:
python run.py --kill

Clear it with:
python run.py --unkill

Inspect status with:
python run.py --status


## Executable trading strategy
Read and follow STRATEGY.md on every cycle. Do not substitute vague "momentum" judgment for the documented setup.

Primary setup: VWAP Breakout / First Pullback continuation. Long only when fresh intraday structure, VWAP, volume and a nearby trigger align. Prefer a confirmed breakout/retest or first orderly bull-flag pullback over a vertical chase. Define invalidation BEFORE buying. Manage open positions before new entries. HOLD while structure, VWAP and volume remain constructive. SELL/REDUCE when structural failure, confirmed VWAP loss, breakout failure, momentum/volume deterioration, materially worse execution, thesis-breaking information, or persistent intraday chop invalidates the setup. Trail invalidation behind confirmed higher lows/current intraday support instead of using one arbitrary percentage stop. Use resistance/extension and failed follow-through to protect gains. A losing position is not automatically a SELL, and a winning position is not automatically a HOLD. Every BUY and position-management decision must state thesis, trigger, invalidation/trailing reference, VWAP state, volume state and exact evidence.

Research basis: Zarattini, Aziz and Barbon, Swiss Finance Institute Research Paper 24-97 on intraday momentum in SPY, using abnormal intraday demand/supply signals and dynamic trailing stops. Its SPY results are not a guarantee and do not validate this sub-$10 adaptation.

## Extended-hours trading
The trader is allowed to operate during **pre-market and after-hours**, not only the regular 9:30 AM–4:00 PM ET session. Treat pre-market and after-hours as valid trading sessions when the Robinhood account, symbol and order mechanics permit execution.

- Pre-market: prioritize fresh news/catalysts, relative volume, VWAP/session structure, breakouts and pullbacks using extended-hours data.
- After-hours: actively manage existing positions and evaluate fresh setups using after-hours price/volume structure and new information.
- Do not assume regular-session order mechanics apply. Robinhood currently requires limit-order behavior for extended-hours execution; market orders do not execute in extended hours, and stop/trailing-stop orders do not execute there. Use the actual Robinhood tool/account response to determine what order is currently executable.
- Verify that the individual security is eligible for extended-hours trading and that the proposed quantity/order type is supported before submitting it.
- Because extended-hours liquidity can be lower and volatility/spreads can be higher, execution quality and current Level 2/quote conditions become especially important, but do not impose an arbitrary blanket ban on extended-hours trades.
- The strategy's thesis, invalidation, VWAP/session structure, volume and fresh evidence still govern BUY/HOLD/REDUCE/SELL decisions.
- If an existing position needs an exit during extended hours, actively attempt an executable limit-order exit when supported rather than simply waiting for the next regular session.
