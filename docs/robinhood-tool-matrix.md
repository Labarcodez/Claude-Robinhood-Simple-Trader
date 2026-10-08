# Robinhood Agentic Tool Matrix

Verified against Robinhood's current "Trading with your agent" support page on 2026-10-08.

Robinhood currently lists **92 tools for external agents** on that page. One additional market-data tool, `get_earnings_transcript`, is listed for built-in agents only. The project is intentionally **long U.S. equities only**, so the trader should use every applicable account, market-data, equity, scanner, alert, advanced-order, and Legend tool when it materially improves a decision, while leaving options/crypto execution outside this project's scope.

Source: https://robinhood.com/us/en/support/articles/trading-with-your-agent/

## Operating rule

Do not blindly call every tool every cycle. Use the tool that answers the current decision:

- **State first:** account, portfolio, positions, orders, approvals.
- **Discover broadly:** scanner specs, multiple scans, datapoints, watchlists.
- **Validate deeply:** quotes, OHLCV, technicals, Level 2, fundamentals, financials, news, filings, earnings, analyst context.
- **Execute carefully:** tradability -> review -> appropriate order -> verify -> reconcile.
- **Monitor:** alerts, alert log, open orders, positions, P&L.
- Never invent a tool. If the connected MCP exposes fewer tools than this page, use only what is actually exposed and report the missing capability rather than substituting a fake call.

## Account / portfolio / approvals — external agent

| Tool | Primary use |
|---|---|
| get_accounts | Identify available Robinhood accounts and trading context |
| get_portfolio | Current portfolio value, asset-class values, real-time buying power |
| get_realized_pnl | Broker-verified realized performance over a time window |
| get_pnl_trade_history | Trade-by-trade realized P&L and outcome review |
| search | Resolve company names/partial names to symbols |
| get_limited_margin_upgrade_info | Understand available limited-margin eligibility; do not enable margin borrowing for this project |
| get_trade_approvals | Detect pending/past agent trade approvals |
| decline_trade_approval | Decline an approval request when a proposed trade is invalid or no longer wanted |
| get_trade_approval_setting | Detect whether approval is ON/OFF before attempting autonomous execution |

If trade approvals are ON, the agent may be prevented from placing eligible orders without manual approval. Do not pretend an order was placed.

## Watchlists — external agent

| Tool | Primary use |
|---|---|
| get_watchlists | Read existing watchlists |
| get_watchlist_items | Read symbols from a specific list |
| get_option_watchlist | Options-only; out of project scope |
| get_popular_watchlists | Discover broad Robinhood lists for supplementary discovery |
| create_watchlist | Maintain a focused research list when useful |
| update_watchlist | Rename/update a project research list |
| follow_watchlist | Follow a useful Robinhood list |
| unfollow_watchlist | Remove an obsolete followed list |
| add_to_watchlist | Preserve strong candidates for later research |
| remove_from_watchlist | Remove stale candidates |
| add_option_to_watchlist | Options-only; out of project scope |
| remove_option_from_watchlist | Options-only; out of project scope |

Watchlists supplement broad scanner discovery; they never replace it.

## Market data — external agent

| Tool | Primary use |
|---|---|
| get_equity_historicals | Intraday OHLCV, candle sequence, volume and session structure |
| get_equity_fundamentals | Market cap, valuation, 52-week range and current OHLCV context |
| get_financials | Revenue/profitability and reported financial history |
| get_equity_price_book | Real-time Level 2 bid/ask depth and spread |
| get_equity_technical_indicators | RSI, MACD, Bollinger Bands, moving averages and other technical indicators |
| get_earnings_results | Past earnings and next report context |
| get_earnings_calendar | Scheduled earnings across the market |
| get_indexes | Resolve market and sector indexes |
| get_index_quotes | Current market/sector regime and relative strength baseline |
| get_equity_news | Current equity-related news/catalyst context |
| get_sec_filing_index | Find available SEC filings |
| get_sec_filing | Read a specific SEC filing |
| get_sec_filing_facts | Read structured facts extracted from filings |
| get_sec_filing_facts_catalog | Discover available SEC fact types |
| get_index_historicals | Historical market/sector index context |
| get_politician_trades | Supplementary disclosed-trading context; never treat it as an entry signal |
| get_equity_analyst_ratings | Analyst ratings and price-target context |

`get_earnings_transcript` is listed by Robinhood for built-in agents only, so an external agent must not assume it exists.

## Equity trading — external agent

| Tool | Primary use |
|---|---|
| get_equity_positions | Current open equity positions |
| get_equity_tax_lots | Cost basis, acquisition dates and tax-lot context |
| get_equity_quotes | Fresh quote, bid/ask and prior close |
| get_equity_orders | Order status/history and reconciliation |
| get_equity_tradability | Security tradability and fractional-share support |
| review_equity_order | Pre-trade simulation and broker warnings |
| place_equity_order | Real equity order submission |
| cancel_equity_order | Cancel an open equity order |

For every order: fresh state -> tradability -> review -> place -> verify order -> verify position.

## Scanner — external agent

| Tool | Primary use |
|---|---|
| get_scans | Inspect saved scans |
| get_scanner_filter_specs | Discover valid scanner filters before creating/changing scans |
| create_scan | Build complementary discovery scans |
| run_scan | Get live scanner results |
| update_scan_filters | Tune a saved scan |
| update_scan_config | Change result sorting |
| get_scanner_datapoints | Inspect the actual data fields returned by a scanner |
| preview_scan | Test scan results before saving/changing a persistent scan |

The trader should use multiple complementary scans: momentum/acceleration, breakout/reclaim, pullback continuation, catalyst/event, and relative strength. Deduplicate results and report coverage honestly when scanner limits prevent exhaustive discovery.

## Alerts — external agent

| Tool | Primary use |
|---|---|
| get_alerts | Inspect configured alerts |
| get_alert_log | Review fired alerts |
| create_alert | Create useful price/indicator monitoring for active positions/candidates |
| update_alert | Modify/pause an alert |
| delete_alert | Remove stale alerts |
| mark_alerts_read | Maintain alert state |

Alerts are supplementary monitoring, not a substitute for active position polling.

## Advanced orders — external agent

| Tool | Primary use |
|---|---|
| get_advanced_orders | Inspect advanced-order types/history |
| place_advanced_order | Submit an advanced order when its supported mechanics fit the current equity trade |
| cancel_advanced_order | Cancel an open advanced order |
| review_advanced_order | Validate/preview an advanced order |

Use advanced orders only when the live Robinhood response confirms they are appropriate for the security/session. Never assume an advanced order provides extended-hours protection.

## Legend — external agent

| Tool | Primary use |
|---|---|
| get_legend_charts | Retrieve Legend charting data for candidate validation |
| get_legend_indicators | Inspect indicators applied to a Legend chart |
| get_legend_indicator_catalog | Discover available Legend indicators |
| get_legend_layouts | Inspect saved chart layouts |
| set_legend_chart_settings | Configure chart display when useful |
| add_legend_indicator | Add an indicator to a chart |
| update_legend_indicator | Change an applied indicator |
| remove_legend_indicator | Remove an applied indicator |

Legend tools are optional analytical depth. Do not waste cycles configuring charts when exact market data already answers the question.

## Options and crypto

Robinhood also exposes options and crypto tools to external agents. They are deliberately **out of scope** for this repository:

- Options: get_option_level_upgrade_info, get_option_chains, get_option_historicals, get_option_instruments, get_option_quotes, get_option_positions, get_option_orders, review_option_order, cancel_option_order, place_option_order, exercise_option, cancel_option_exercise.
- Crypto: get_currency_pairs, get_crypto_quotes, get_crypto_positions, get_crypto_orders, preview_crypto_order, place_crypto_order, cancel_crypto_order, get_crypto_account_onboarding_info, get_crypto_tax_lots.

Do not use those execution surfaces unless the project scope is explicitly changed.

## How the trader should exploit the tool set

1. **Before every cycle:** get_accounts, get_portfolio, get_equity_positions, get_equity_orders, get_trade_approval_setting, get_trade_approvals.
2. **Before discovery:** get_scanner_filter_specs, inspect get_scans, then use multiple scan/preview/run paths and get_scanner_datapoints where useful.
3. **For candidates:** get_equity_quotes -> get_equity_tradability -> get_equity_historicals -> get_equity_technical_indicators -> get_equity_price_book -> fundamentals/financials/news/SEC/earnings/analyst context as appropriate.
4. **For regime:** get_indexes, get_index_quotes, get_index_historicals and compare candidate relative strength.
5. **Before BUY/SELL:** refresh quote/position/order state, confirm tradability, review the exact order, then place only if broker state still matches the thesis.
6. **After an order:** get_equity_orders and get_equity_positions until the outcome is known; reconcile local order-guard state.
7. **After closed trades:** get_realized_pnl and get_pnl_trade_history to update the journal from broker truth.
8. **During active positions:** use price book, quotes, historical bars, alerts/alert log and order state to detect topping, pressure reversal, thesis failure and execution deterioration.
9. **Extended hours:** verify security/session eligibility and current supported order mechanics every time. Do not assume regular-session order types work after hours.

## Strategy principle

Tools provide evidence; they do not override the strategy. A high scanner score, FOMO score, analyst target, news headline, or Level 2 imbalance is never by itself a BUY. The primary setup remains VWAP breakout / first pullback continuation with active peak protection and pressure-based exits.
