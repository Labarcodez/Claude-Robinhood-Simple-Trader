# Robinhood Agentic Tool Matrix

Verified against Robinhood's current "Trading with your agent" support page on 2026-09-29.

The project is intentionally **long U.S. equities only**. Therefore every tool relevant to equity discovery, research, portfolio state, risk, and execution is used or explicitly considered. Options and crypto tools are available at the broker level but are intentionally excluded from this project's scope.

## Equity-relevant tools

### Account / portfolio
| Tool | Use |
|---|---|
| get_accounts | Confirm account context |
| get_portfolio | Buying power, total value, exposure |
| get_realized_pnl | Broker-verified performance |
| get_pnl_trade_history | Trade-by-trade performance |
| search | Resolve company/ticker |

### Watchlists
| Tool | Use |
|---|---|
| get_watchlists | Load saved watchlists |
| get_watchlist_items | Read candidate lists |
| get_popular_watchlists | Discover popular symbols |
| create_watchlist | Create momentum watchlist |
| update_watchlist | Maintain it |
| follow_watchlist | Follow relevant Robinhood lists |
| unfollow_watchlist | Remove irrelevant followed lists |
| add_to_watchlist | Preserve strong candidates |
| remove_from_watchlist | Remove stale candidates |

The option-watchlist tools are intentionally excluded because this project does not trade options.

### Market data
| Tool | Use |
|---|---|
| get_equity_historicals | Intraday OHLCV candles and volume |
| get_equity_fundamentals | Market cap, valuation, 52-week context and today's OHLCV |
| get_financials | Company financial history |
| get_equity_price_book | Level 2 spread/depth/liquidity |
| get_equity_technical_indicators | RSI, MACD, Bollinger, moving averages, VWAP and more |
| get_earnings_results | Earnings history and next report |
| get_earnings_calendar | Scheduled market earnings |
| get_indexes | Resolve market/sector indexes |
| get_index_quotes | Current market regime |

### Equities
| Tool | Use |
|---|---|
| get_equity_positions | Current holdings |
| get_equity_tax_lots | Cost basis/tax-lot context |
| get_equity_quotes | Current price/bid/ask and prior close |
| get_equity_orders | Order status/history |
| get_equity_tradability | Tradability/fractional eligibility |
| review_equity_order | Pre-trade simulation/warnings |
| place_equity_order | Live order placement when explicitly enabled |
| cancel_equity_order | Cancel open orders |

### Scanner
| Tool | Use |
|---|---|
| get_scans | Existing saved scans |
| get_scanner_filter_specs | Discover valid scanner filters before use |
| create_scan | Build momentum scan |
| run_scan | Live candidate discovery |
| update_scan_filters | Tune scan |
| update_scan_config | Control ranking/sorting |

## FOMO is not a single filter

The trader should combine scanner results with:
- short-term price acceleration
- relative volume
- volume acceleration
- OHLCV candle structure
- breakout/retest behavior
- VWAP and technical alignment
- market/sector relative strength
- earnings/event context
- Level 2 spread and depth
- liquidity and tradability
- extension/rejection penalties

A stock being up 10% is not enough. The system should distinguish an **active, continuing momentum move** from a **late vertical spike that is already fading**.

## Candle visualization

Robinhood's historical tool supplies OHLCV data. This repo includes chart.py to turn those bars into a real candlestick chart with a separate volume panel.

Example:

    python chart.py --input data/example.json --symbol AAPL --output data/charts/AAPL.png

Claude should use the generated image for visual confirmation when image inspection is available and otherwise fall back to exact OHLCV analysis.

## Important current limitation

The current Robinhood support page does not list a dedicated equity-news tool. Do not invent get_equity_news. Use the listed earnings tools for Robinhood event data and use an external news source separately when the environment provides one.

Options and crypto tools are deliberately not called by this project because the project's trading universe is long U.S. equities only.
