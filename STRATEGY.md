# Day-Trading Strategy — Intraday Momentum, Trend Capture & Pressure-Based Exits

This is the primary executable strategy for the live Simple Trader. It is adapted
from published intraday-momentum research and is not a guarantee of profitability
or independently validated on this repository's broad all-equity universe.

## Research basis

Zarattini, Aziz and Barbon, "Beat the Market: An Effective Intraday Momentum
Strategy for S&P500 ETF (SPY)" (Swiss Finance Institute Research Paper 24-97)
describes trend-following entries when abnormal intraday demand/supply imbalance
appears and dynamic trailing stops that protect downside while allowing upside.
The paper's results are for SPY and do not establish the same results for broad all-equity
stocks.

## Core setup — day trade, not scalping

Find a stock at any price that is proving demand, then participate in a meaningful intraday move without chasing an exhausted spike. This is a day-trading system, not a high-frequency/scalping system: the goal is to capture the useful portion of an intraday trend, manage it continuously, and exit when the trend tops, pressure turns down, or the thesis fails.

Normally require fresh broker data, a coherent price/volume structure, a reason the stock is likely to move, an executable quote, a clear invalidation or exit reference, and acceptable execution conditions. VWAP, relative volume, opening-range levels, market cap, price, daily gain, catalysts and other indicators are evidence inputs—not mandatory gates. The strongest setup depends on current market conditions.

A real catalyst is useful confirmation when available; never invent one.

## Session handling

Treat regular hours, pre-market and after-hours as valid trading sessions when
Robinhood says the security and proposed order are executable. Recalculate
session structure and VWAP from the relevant session data rather than blindly
carrying regular-session levels into extended hours. Give greater weight to
fresh news, actual extended-hours volume, spread/depth and the current executable
order type outside regular hours.

## Market-regime and candidate ranking

Before a new BUY, classify the broad market and relevant sector/index as
TRENDING_UP, MIXED, or RISK_OFF/WEAK using current available index data.
Prefer candidates with clear relative strength when the broader regime is mixed
or weak. Do not automatically reject every trade in a weak regime; require a
specific stock-level reason for strength.

Rank surviving candidates using a weighted evidence stack:
- structure quality and proximity to a valid trigger;
- relative volume and volume acceleration;
- VWAP alignment;
- relative strength versus market/sector;
- catalyst/event quality when verifiable;
- spread/depth and expected execution quality;
- extension/rejection/chase risk;
- data freshness.

A high composite score is a research priority, not an automatic BUY. The final
decision still requires a coherent thesis and defined invalidation.

## Entry A — Breakout continuation

BUY when current evidence shows a favorable intraday setup—not only an opening-range breakout when applicable. Valid entries may include confirmed breakouts, first pullbacks, VWAP reclaims, support reclaims, momentum continuation, consolidation breaks, failed-breakdown reversals, catalyst-driven moves, relative-strength continuation, and other structures supported by current price/volume/order-book evidence. Do not require a specific clock window, opening range, VWAP relationship, minimum price, market cap, daily percentage-gain ceiling, or bar-close-only trigger. The entry must still have a coherent thesis, current tradability, executable pricing, and a defined invalidation/exit plan.

## Entry B — First pullback / bull flag

After an upward impulse, require price to remain above session VWAP, an orderly
pullback with contracting volume when volume is informative, support at the
breakout/VWAP/structure, and a bullish reclaim of the pullback trigger with
renewed participation.

## Do not enter

Do not enter when the broker state is unclear, data is stale or contradictory, the security/order is not tradable, execution is materially impaired, or the thesis has no credible trigger and invalidation. A stock being under $2, having a small market cap, or already being up more than 30% is not by itself a rejection reason. A highly extended move can still be traded when current evidence supports continuation or reversal, but do not buy solely because a percentage move is large.

## Scanner workflow

Run multiple complementary discovery passes rather than trusting one scanner:
momentum/acceleration, breakout/reclaim, pullback continuation, catalyst/event,
and relative-strength scans when the corresponding scanner filters are available.
Deduplicate the results, then deep-research only the strongest candidates.

Scanner results are intentionally broad. Do not add arbitrary market-cap, minimum
volume, gap, momentum, or popularity restrictions merely to make the list smaller.
Liquidity, spread, stale data and tradability are execution-quality filters after
discovery. If a scanner cannot express a desired filter, do not invent one; use
another available data source or state the limitation.

## Position management

Every cycle manages open positions first.

### HOLD

Hold while the thesis remains intact: support/trigger holds, VWAP relationship
is constructive, higher highs/higher lows continue, participation supports the
move, and no thesis-breaking event appears. Do not sell solely because the trade
is green.

### REDUCE / TAKE PROFIT — protect the top of the move

The system cannot know the exact future high, so "sell at the top" means sell
near the end of a confirmed intraday advance rather than waiting for a complete
collapse. When a position makes a new high, continuously reassess whether buying
pressure is still expanding. Consider a full or partial exit into resistance,
large extension from VWAP, repeated upper-wick rejection, a failed new high,
climactic volume with weak price follow-through, or a lower high after the peak.
For a tiny account, a full exit is acceptable when partial execution is
impractical.

Pressure reversal is an active exit signal. Stronger evidence includes several
of these appearing together: bids weakening or stepping down, asks remaining
heavy, lower highs/lower lows, bearish candle closes, loss of the breakout level,
loss of session VWAP, rising sell volume, and failure to reclaim the recent high.
Do not wait for a fixed percentage loss or a distant stop when the original
intraday pressure has clearly reversed. A single noisy tick is not enough by
itself; seek confirmation from price structure, volume, VWAP and/or the order
book when available.

### SELL — topping, pressure reversal, or thesis invalidation

Exit proactively when the advance is topping or selling pressure is taking
control. The preferred sequence is to protect a strong winner as soon as the
market stops confirming the highs, rather than giving the whole move back.

### Sell-the-top / pressure checklist

When a position is extended or has just printed a new high, check:
- Did the latest high fail to hold?
- Did price make a lower high after the peak?
- Are consecutive candles closing weaker or below the prior candle lows?
- Is volume increasing while price stops advancing or starts falling?
- Is the bid weakening, stepping down, or losing depth while offers remain firm?
- Did price lose the breakout/retest level or session VWAP?
- Is the stock unable to reclaim the recent high after rejection?

If multiple independent signals confirm pressure has turned down, SELL/REDUCE
without waiting for a fixed target. Do not claim to have sold the exact high;
the objective is to exit near the top while evidence is still favorable enough
to obtain an executable fill.

Exit when evidence shows:
1. structural failure below the defined swing/pullback low or breakout level
   without quick reclaim;
2. confirmed VWAP loss with buyers losing control;
3. failure of higher highs/higher lows followed by a lower high/lower low;
4. breakout failure with rejection back below the trigger;
5. volume/participation failure with increasing selling pressure;
6. materially deteriorated spread/depth;
7. fresh information that invalidates the original thesis; or
8. the expected intraday move fails and the stock becomes persistent chop.

Being down money alone is not the reason to sell; thesis invalidation is.

## Dynamic trailing exit and peak protection

Do not use one arbitrary percentage stop for every stock. Initial invalidation
comes from the setup's swing low or failed-breakout level. Once a position is
profitable, the exit reference should move with the trade: record the most
recent meaningful high, identify the first confirmed signs of exhaustion, and
protect the remaining gain behind the newest confirmed higher low, VWAP or
other current intraday support. As price advances,
trail behind newly confirmed higher lows. VWAP may become a trailing reference
when appropriate. After strong extension, protect gains behind current intraday
support instead of giving the whole move back. Every trailing reference must be
explainable from current market structure.

## End of executable session

This is an intraday day trader, not an overnight holder. The executable trading
window runs from eligible pre-market through eligible regular hours and
after-hours. Before the end of the after-hours session, explicitly reassess and
normally close every day-trade position so no position is intentionally carried
overnight. If an exit is required during extended hours, use an order type that
Robinhood actually accepts for that session and verify the fill. Never claim an
exit without broker confirmation.

## Re-entry

A failed setup can be traded again only after a genuinely new setup forms. Do not
repeatedly rebuy the same failed level without new evidence.

## Decision hierarchy

Broker/account/order state > execution/tradability > price structure/invalidation
> VWAP > volume/momentum > relative strength/regime > catalyst/news/fundamentals
> FOMO.

FOMO is research priority, never an automatic BUY or an excuse to delay an exit.

## Required decision record

For every position record:
- entry thesis;
- thesis state: INTACT, WEAKENING or INVALIDATED;
- trigger/structure;
- VWAP relationship;
- volume/participation state;
- trailing invalidation;
- target/resistance;
- action: HOLD, REDUCE or SELL;
- exact evidence.

Record the same fields before every new BUY.

## Order mechanics

Do not assume regular-session order types work in extended hours. Verify the
current Robinhood order response, session eligibility and supported quantity
before submission. During extended hours, use an executable limit-order workflow
when required; do not place a market order expecting it to execute immediately.
Stop and trailing-stop orders should not be treated as active extended-hours
protection unless Robinhood explicitly reports that the current session supports
them.

All orders still require fresh broker/account state, tradability, review where
supported, local order-intent protection, broker submission and post-order
reconciliation.
