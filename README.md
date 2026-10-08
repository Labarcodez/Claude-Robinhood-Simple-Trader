# Claude Robinhood Simple Trader

A small **LIVE-only** Robinhood day-trading equity trader where Claude is the trading brain,
Robinhood MCP is the broker/data interface, and Python provides scheduling,
persistent state, duplicate-order protection, charting, logging and recovery.

## What changed

- Claude reads the live Robinhood account/wallet and decides position sizing.
- Removed arbitrary portfolio percentage, position-count, daily-loss, order-size,
  confidence, reward/risk and daily-trade hard limits.
- Kept only operational safeguards: kill switch, valid broker state, broker
  buying power, tradability, fresh data, duplicate-order protection, order review
  and post-order reconciliation.
- Added an always-on supervisor.py that launches Claude repeatedly, prevents
  overlapping cycles, records failures/timeouts and lets the next cycle reconcile
  broker state before acting.
- scheduler.py remains as a backward-compatible entry point to the supervisor.
- Added transparent FOMO/chase scoring configuration.
- Improved charts with timestamps, EMA 9, EMA 20, VWAP and volume.
- Added deterministic tests for the local execution guards.

## Setup

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env

Use the Robinhood Trading MCP and any other MCP/data connectors that are already
available in Claude. The project does not require or request additional MCP
connections; do not invoke connect/install/authorize flows.

## Run

    python run.py --status
    python run.py --kill
    python run.py --unkill
    python run.py
    python run.py --start
    python supervisor.py
    pytest

Optional environment variables:

    TRADING_INTERVAL_SECONDS=60
    CLAUDE_CYCLE_TIMEOUT_SECONDS=600
    CLAUDE_COMMAND="claude -p"
    TRADER_DB=data/trader.db

The supervisor loads .env when python-dotenv is installed. `python run.py` now
starts the always-on supervisor by default; `python run.py --start` is an explicit
alias. The exact Claude Code command and Robinhood MCP connection must still exist
in the runtime environment because a Python process cannot manufacture a broker
connection. Once that environment is configured, no manual symbol selection,
trade entry, or cycle management is required.

## Trading universe

Discovery covers **all tradable long U.S. equities with a current price above $0**. This includes sub-$2 stocks, low-market-cap stocks, and stocks already up more than 30% on the day. There is no discovery price ceiling, market-cap floor, or daily percentage-gain ceiling. Every BUY is sized from actual Robinhood buying power and broker-reported tradability/fractional-share support.

No arbitrary price, market-cap, percentage-gain, sector, exchange, minimum-volume, watchlist, popularity, momentum, gap or FOMO restriction is applied at discovery.
Scanner filters rank candidates; they do not define the universe.

No options, shorting, margin borrowing, crypto, OTC or leveraged products.

## Automatic scan and decision pipeline

Each cycle is a complete loop: reconcile account/orders -> manage existing
positions -> classify market regime -> run multiple discovery passes -> dedupe ->
deep-research the strongest candidates -> validate execution -> place/verify if
justified -> journal. The trader does not need to manually pick symbols or enter
trades.

The scanner deliberately stays broad at discovery. It then becomes selective
using structure, VWAP, volume quality, relative strength, catalyst evidence,
Level 2, liquidity and execution conditions. This improves signal quality without
hardcoding a tiny watchlist.

## Architecture

supervisor.py -> Claude -> Robinhood account -> broad all-equity discovery ->
open-position management -> candle/volume/FOMO/Level 2 research -> Claude
decision -> operational execution guard -> Robinhood order review/place/verify ->
journal -> next cycle reconciliation.

The supervisor does not contain a fake trading strategy. Claude remains
responsible for market research and trade decisions. Every cycle manages
existing positions before new entries.

## Trading strategy

The live trader follows STRATEGY.md: adaptive intraday entries across breakouts, pullbacks, reclaims, momentum continuation, reversals and catalyst-driven setups, with dynamic position management, peak protection and pressure-based exits. The system is designed for day trades rather than rapid-fire scalps. This is an
evidence-based adaptation of published intraday-momentum research, not a
guarantee of profitability and not independently validated on this repo's
broad all-equity universe.

## Extended-hours trading

The trader is allowed to operate during **pre-market and after-hours**, not only
the regular 9:30 AM-4:00 PM ET session, when the security and order mechanics
permit execution.

Extended-hours execution is not identical to regular-hours execution. The agent
must verify session eligibility and supported order types from the live Robinhood
response. Do not assume market, stop, or trailing-stop orders work outside
regular hours; use an executable limit-order workflow when required.
Extended-hours liquidity can be lower and spreads/volatility can be higher, so
execution quality matters without creating a blanket ban.

## Live trading warning

Orders are real-money trades. The project does not guarantee profit. Intraday trading can lose money rapidly. Keep the kill switch available and
verify the Robinhood MCP connection, account state and order workflow before
running unattended.
