# Simple Trading Skill

Operate the Simple Claude Robinhood Trader as a LIVE-only autonomous equity
trader.

Claude is the trading brain. The local Python supervisor provides scheduling,
persistent state, duplicate-order protection, logging and recovery. Robinhood
MCP is the source of broker/account/market data and the execution interface.

There are NO arbitrary portfolio percentage, position-count, daily-loss, order-size, confidence, reward/risk or daily-trade hard limits. The trader may take as many trades as current opportunities justify. Claude reads
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

## Day-trading behavior

Each cycle manages existing positions before looking for new entries. Claude may BUY, SELL, or HOLD based on fresh evidence. It should seek meaningful intraday opportunities without manufacturing trades. This is day trading, not rapid-fire scalping. Near the end of the regular session, explicitly review whether open positions should be exited for the day.

Use all already-available MCP/data connectors when useful, but never invoke or request connect/install/authorization flows for another MCP. Never invent unavailable tools.

## Autonomous day-trading supervisor

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

Discover ALL tradable long U.S. equities with current price > $0, including sub-$2 stocks, low-market-cap stocks, and stocks already up more than 30% on the day. There is no discovery price ceiling, market-cap floor, or daily percentage-gain ceiling. BUY sizing must come from actual Robinhood buying power and current broker rules.
Scanner filters only rank/prioritize. Use multiple passes when capped.

No options, shorting, margin borrowing, crypto, OTC or leveraged products.

## Current Robinhood MCP tool utilization

Robinhood's current support page lists 93 tools for external agents. Use the
complete applicable catalog in `docs/robinhood-tool-matrix.md`. Do not call
everything blindly; use the tool that answers the current decision and never
invent an unavailable tool.

At cycle start use account/portfolio/position/order/approval state. For discovery
use scanner filter specs plus multiple scans, previews, scanner datapoints and
watchlists as supplementary sources. For serious candidates use fresh quotes,
tradability, OHLCV, technical indicators, Level 2, fundamentals, financials,
equity news, earnings, SEC filings/facts, analyst ratings and index/relative-
strength data when relevant. Use realized P&L/trade history for broker-verified
performance review. Use alerts/alert logs and advanced-order tools when they
materially improve active monitoring or execution and the live broker response
supports them. Legend chart/indicator tools may be used for deeper chart
validation when available.

Options and crypto execution remain outside this project's scope. Never claim a
tool was used unless it was actually exposed and called.

If trade approvals are enabled, respect the broker's approval workflow and never
claim an order was placed without broker confirmation.

## Discovery quality

Use multiple complementary scan families when available: momentum/acceleration,
breakout/reclaim, pullback continuation, catalyst/event and relative strength.
Deduplicate results and report actual/approximate coverage. Read scanner filter
specifications before creating or changing scans.

Before a new entry, classify broad market/sector regime from current index data
as TRENDING_UP, MIXED, or RISK_OFF/WEAK. Favor strong relative strength and clean
structure in mixed/weak regimes rather than automatically buying losers.

Deep research only the strongest candidates: quote/tradability -> OHLCV -> VWAP/
technicals -> volume -> relative strength -> catalyst -> Level 2/liquidity ->
order mechanics -> thesis/invalidation -> sizing -> review.

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

Primary setup: adaptive intraday opportunity selection. Use breakout/continuation, pullback/reclaim, momentum, reversal, catalyst and other evidence-backed setups when current market conditions support them. Prefer a confirmed breakout/retest or first orderly bull-flag pullback over a vertical chase. Define invalidation BEFORE buying. Manage open positions before new entries. HOLD while structure, VWAP and volume remain constructive. SELL/REDUCE when structural failure, confirmed VWAP loss, breakout failure, momentum/volume deterioration, materially worse execution, thesis-breaking information, or persistent intraday chop invalidates the setup. Trail invalidation behind confirmed higher lows/current intraday support instead of using one arbitrary percentage stop. Use resistance/extension and failed follow-through to protect gains. A losing position is not automatically a SELL, and a winning position is not automatically a HOLD. Every BUY and position-management decision must state thesis, trigger, invalidation/trailing reference, VWAP state, volume state and exact evidence.

Research basis: Zarattini, Aziz and Barbon, Swiss Finance Institute Research Paper 24-97 on intraday momentum in SPY, using abnormal intraday demand/supply signals and dynamic trailing stops. Its SPY results are not a guarantee and do not validate this broad all-equity adaptation.

## Extended-hours trading
The trader is allowed to operate during **pre-market and after-hours**, not only the regular 9:30 AM–4:00 PM ET session. Treat pre-market and after-hours as valid trading sessions when the Robinhood account, symbol and order mechanics permit execution.

- Pre-market: prioritize fresh news/catalysts, relative volume, VWAP/session structure, breakouts and pullbacks using extended-hours data.
- After-hours: actively manage existing positions and evaluate fresh setups using after-hours price/volume structure and new information.
- Do not assume regular-session order mechanics apply. Robinhood currently requires limit-order behavior for extended-hours execution; market orders do not execute in extended hours, and stop/trailing-stop orders do not execute there. Use the actual Robinhood tool/account response to determine what order is currently executable.
- Verify that the individual security is eligible for extended-hours trading and that the proposed quantity/order type is supported before submitting it.
- Because extended-hours liquidity can be lower and volatility/spreads can be higher, execution quality and current Level 2/quote conditions become especially important, but do not impose an arbitrary blanket ban on extended-hours trades.
- The strategy's thesis, invalidation, VWAP/session structure, volume and fresh evidence still govern BUY/HOLD/REDUCE/SELL decisions.
- If an existing position needs an exit during extended hours, actively attempt an executable limit-order exit when supported rather than simply waiting for the next regular session.
