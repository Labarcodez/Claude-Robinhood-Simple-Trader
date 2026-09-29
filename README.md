# Claude Robinhood Simple Trader

Simple architecture: Claude is the trading brain, Robinhood MCP is the broker, and a tiny Python layer provides hard risk controls, persistence, scheduling, and a kill switch.

This is a live-trading project. Claude uses the Robinhood MCP to place real broker orders; the local Python layer provides hard risk controls, persistence, scheduling, and a kill switch.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Connect the official Robinhood Trading MCP in Claude:
`https://agent.robinhood.com/mcp/trading`

Run:

```bash
python run.py
python run.py --status
python run.py --kill
python run.py --unkill
python scheduler.py
pytest
```

## Trading universe

Discovery covers ALL tradable long U.S. equities with a current price strictly below $8.00 and above $0. No arbitrary market-cap, sector, exchange, minimum-volume, watchlist, popularity, or momentum restriction is applied at discovery.

Scanner filters rank candidates; they do not define the universe. Liquidity, tradability, stale-data, spread, Level 2, and deterministic risk checks can still reject a candidate before a real order.

Orders are real-money trades. Keep the kill switch available and verify the Robinhood account, risk limits, and order-review flow before running unattended.

## Architecture

Claude -> broad discovery -> research/reasoning/decision -> local hard-risk check -> Robinhood MCP -> verify -> journal

Keep this project intentionally small so it can be fairly compared with the complex trader.
