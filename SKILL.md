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

## Fast momentum / FOMO skill

When scanning for fast-moving equities, use the full equity research chain rather than a single scanner result.

Required Robinhood workflow:
- Account/performance: get_accounts, get_portfolio, get_realized_pnl, get_pnl_trade_history
- Discovery: search, get_scans, get_scanner_filter_specs, create_scan, run_scan, update_scan_filters, update_scan_config
- Watchlists: get_watchlists, get_watchlist_items, get_popular_watchlists, create_watchlist, update_watchlist, follow_watchlist, unfollow_watchlist, add_to_watchlist, remove_from_watchlist
- Market: get_equity_quotes, get_equity_historicals, get_equity_technical_indicators, get_equity_price_book, get_equity_fundamentals, get_financials, get_earnings_results, get_earnings_calendar, get_indexes, get_index_quotes
- Portfolio/execution: get_equity_positions, get_equity_tax_lots, get_equity_orders, get_equity_tradability, review_equity_order, place_equity_order, cancel_equity_order

Do not call options or crypto tools unless the project scope is explicitly changed.

### Candle + volume requirement

A candidate is not fully researched until its intraday OHLCV has been examined. Use get_equity_historicals and inspect:
- candle bodies and wicks
- higher highs/lows
- breakout/retest structure
- volume per bar
- volume expansion versus prior bars
- volume collapse after a spike

When visual confirmation is useful, save the returned bars as JSON and run:
python chart.py --input <json> --symbol <SYMBOL> --output data/charts/<SYMBOL>.png

The chart contains both candlesticks and a separate volume panel. Never claim to have visually inspected a chart unless the generated image was actually available for inspection.

### FOMO score

Score 0-100 using configurable weights. Reward acceleration, relative volume, volume acceleration, breakout quality, persistence, relative strength, catalyst/event context and liquidity. Penalize spread, thin Level 2 depth, volume fade, excessive VWAP extension, rejection wicks, and stale data.

A high score identifies a candidate for deeper research. It does not override the entry trigger or deterministic risk layer.

Always record why the candidate is early enough to enter rather than simply being the stock that already made the move.

