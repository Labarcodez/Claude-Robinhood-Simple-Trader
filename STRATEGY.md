# Intraday Momentum Strategy — VWAP Breakout / Pullback

This is the primary executable strategy for the live Simple Trader. It is adapted from published intraday-momentum research and is not a guarantee of profitability or independently validated on this repository's sub-$10 universe.

## Research basis
Zarattini, Aziz and Barbon, "Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)" (Swiss Finance Institute Research Paper 24-97) describes trend-following entries when abnormal intraday demand/supply imbalance appears and dynamic trailing stops that protect downside while allowing upside. The paper's results are for SPY and do not establish the same results for sub-$10 stocks. Practitioner research also emphasizes relative volume, breakout/pullback structure, VWAP and volume confirmation.

## Core setup
Find a stock below $10 that is proving demand, then enter continuation rather than chase a completed vertical move.

Normally require:
- fresh intraday OHLCV and a confirmed tradable quote;
- higher highs/higher lows or a clear breakout/reclaim structure;
- price at/above VWAP for a long;
- meaningfully elevated relative volume/volume acceleration (2x is a useful reference, not a blind guarantee);
- a nearby trigger such as opening-range high, prior intraday high, flat-top resistance or pullback/retest high;
- a clear invalidation level before entry;
- acceptable spread, depth and data freshness.

A real catalyst is useful confirmation when available; never invent one.

## Entry A — Breakout continuation
BUY only after a fresh candle breaks a defined resistance/trigger while price is above VWAP and breakout volume expands. Prefer confirmation/retest over chasing a single extended candle.

## Entry B — First pullback / bull flag
After an upward impulse, require price to remain above VWAP, an orderly pullback with contracting volume, support at the breakout/VWAP/structure, and a bullish reclaim of the pullback trigger with renewed volume.

## Do not enter
Avoid vertical extension far above VWAP with no nearby invalidation, repeated upper-wick rejection, immediate breakout failure, collapsing volume, materially poor spread/depth, stale/contradictory data, or an entry justified only because price already rose sharply.

## Position management
Every cycle manages open positions first.

### HOLD
Hold while the thesis remains intact: support/trigger holds, VWAP relationship is constructive, higher highs/higher lows continue, volume supports the move, and no thesis-breaking event appears. Do not sell solely because the trade is green.

### REDUCE / TAKE PROFIT
When execution mechanics allow, consider reducing into clearly identified resistance/extension, repeated upper wicks, climactic volume with weak follow-through, or a new high that cannot hold. For a tiny account, a full exit is acceptable when partial execution is impractical.

### SELL — thesis invalidation
Exit when evidence shows:
1. structural failure below the defined swing/pullback low or breakout level without quick reclaim;
2. confirmed VWAP loss with buyers losing control;
3. failure of higher highs/higher lows followed by a lower high/lower low;
4. breakout failure with rejection back below the trigger;
5. volume/momentum failure with increasing selling pressure;
6. materially deteriorated spread/depth;
7. fresh information that invalidates the original thesis; or
8. the expected intraday move fails and the stock becomes persistent chop.

Being down money alone is not the reason to sell; thesis invalidation is.

## Dynamic trailing exit
Do not use one arbitrary percentage stop for every stock. Initial invalidation comes from the setup's swing low or failed-breakout level. As price advances, trail behind newly confirmed higher lows. VWAP may become a trailing reference when appropriate. After strong extension, protect gains behind current intraday support instead of giving the whole move back. Every trailing reference must be explainable from current market structure.

## End of session
This is an intraday trader. In the final part of regular hours, explicitly reassess every open position. Do not intentionally carry a momentum day trade overnight. If still open, either exit because the intraday thesis has ended or document a specific current reason it remains open and continue monitoring broker state.

## Re-entry
A failed setup can be traded again only after a genuinely new setup forms. Do not repeatedly rebuy the same failed level without new evidence.

## Decision hierarchy
Broker/account/order state > execution/tradability > price structure/invalidation > VWAP > volume/momentum > relative strength/regime > catalyst/news/fundamentals > FOMO.

FOMO is research priority, never an automatic BUY or an excuse to delay an exit.

## Required decision record
For every position: entry thesis, thesis state (INTACT/WEAKENING/INVALIDATED), trigger/structure, VWAP relationship, volume state, trailing invalidation, target/resistance, action (HOLD/REDUCE/SELL), and exact evidence. Record the same fields before every new BUY.
