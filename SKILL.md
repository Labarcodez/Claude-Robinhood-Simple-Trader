# Simple Trading Skill

Operate the Simple Claude Robinhood Trader.

Inspect the currently connected Robinhood MCP tools before trading. Prefer account, buying power, positions, open orders, quotes, historical data, fundamentals, news, order review, order placement, and order status.

Before a new position, inspect local state with:

```bash
python run.py --status
```

The local safety layer is authoritative.

PAPER: do not place a real broker order; journal the decision.

LIVE: only use Robinhood MCP, review before submission when supported, and verify broker state afterward. If state is ambiguous, reconcile instead of blindly retrying.

If account, positions, buying power, required market data, or order state cannot be verified, do not open a new position.
