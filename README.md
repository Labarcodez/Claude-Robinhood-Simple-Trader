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

Start with long U.S. equities only. Orders are real-money trades. Keep the kill switch available and verify the Robinhood account, risk limits, and order-review flow before running unattended.

## Architecture

Claude -> research/reasoning/decision -> local hard-risk check -> Robinhood MCP -> verify -> journal

Keep this project intentionally small so it can be fairly compared with the complex trader.
