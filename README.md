# Claude Robinhood Simple Trader

A small LIVE-only Robinhood equity trader where Claude is the trading brain, Robinhood MCP is the broker/data interface, and Python provides scheduling, persistent state, duplicate-order protection, charting, logging and recovery.

## What changed

- Claude reads the live Robinhood account/wallet and decides position sizing.
- Removed arbitrary portfolio percentage, position-count, daily-loss, order-size, confidence, reward/risk and daily-trade hard limits.
- Kept only operational safeguards: kill switch, valid broker state, broker buying power, tradability, fresh data, duplicate-order protection, order review and post-order reconciliation.
- Added an always-on supervisor.py that launches Claude repeatedly, prevents overlapping cycles, records failures/timeouts and lets the next cycle reconcile broker state before acting.
- scheduler.py remains as a backward-compatible entry point to the supervisor.
- Added transparent FOMO/chase scoring configuration.
- Improved charts with timestamps, EMA 9, EMA 20, VWAP and volume.
- Added deterministic tests for the local execution guards.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Connect the official Robinhood Trading MCP in Claude: https://agent.robinhood.com/mcp/trading

## Run

```bash
python run.py --status
python run.py --kill
python run.py --unkill
python supervisor.py
pytest
```

Optional environment variables:

```bash
TRADING_INTERVAL_SECONDS=60
CLAUDE_CYCLE_TIMEOUT_SECONDS=600
CLAUDE_COMMAND="claude -p"
```

The exact Claude Code command and MCP connection must be configured on the machine. A Python scheduler cannot create a Robinhood MCP connection by itself. Do not consider the system autonomous until a real Claude cycle successfully reads the Robinhood account through the connected MCP.

## Trading universe

Discovery covers ALL tradable long U.S. equities with a current price strictly below $8.00 and above $0. The $8 ceiling is the discovery universe, not a signal to buy cheap stocks.

No arbitrary market-cap, sector, exchange, minimum-volume, watchlist, popularity, momentum, gap or FOMO restriction is applied at discovery. Scanner filters rank candidates; they do not define the universe.

No options, shorting, margin borrowing, crypto, OTC or leveraged products.

## Architecture

supervisor.py -> Claude -> Robinhood account -> broad sub-$8 discovery -> candle/volume/FOMO/Level 2 research -> Claude decision -> operational execution guard -> Robinhood order review/place/verify -> journal -> next cycle reconciliation.

The supervisor does not contain a fake trading strategy. Claude remains responsible for market research and trade decisions.

## Live trading warning

Orders are real-money trades. The project does not guarantee profit. Fast momentum trading can lose money rapidly. Keep the kill switch available and verify the Robinhood MCP connection, account state and order workflow before running unattended.