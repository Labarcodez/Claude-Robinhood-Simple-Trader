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
