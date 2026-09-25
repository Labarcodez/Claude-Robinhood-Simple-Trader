---
name: robinhood-trade-lessons-journal
description: "Running journal of what worked and failed in Claude's Robinhood day trades, kept because the user asked Claude to learn after every trade and keep getting better"
metadata:
  node_type: memory
  pinned: false
  originSessionId: b28dde51-ee23-43e1-aba8-925f0dd6c325
  modified: 2026-09-25T19:11:55.330Z
---

The user asked me to "learn after every trade" and "learn from your trade and keep getting better" when trading their Robinhood agentic account. This file is where those lessons persist between sessions. Read it before trading and append a short entry after each closed trade. Entries are my own observations from real fills, so treat them as working hypotheses to keep testing, not as proven rules.

## 2026-09-25 (small account, about $25, sub-$5 momentum stocks)

- **EVTL (Vertical Aerospace), +1.8%:** worked. It was a real company with higher lows on rising volume and no dilution or reverse-split news. I sold half at a resting +2.2% limit and the rest when volume died, instead of waiting for a bigger target.
- **SDEV (Stablecoin Development Corp), -1.2%:** failed. I bought right after a one-minute volume burst, which was the spike itself. Price made lower highs and volume collapsed immediately after I entered. Selling early on the fade, before the stop, saved about $0.15 versus letting the stop hit.
- **MRLN (Merlin, Inc.), -0.3%:** roughly flat, about -$0.07. It was a $180M-cap stock breaking out of a consolidation on volume, and I bought a small pullback (not the top), which avoided the SDEV mistake. But the breakout had no follow-through: it peaked 1.4% above my entry, then sat pinned at one price on tiny volume for 8 minutes. I set an explicit exit trigger (no new high or a break of support by the next check), and exited at breakeven when it hit. The cost was one spread, which was much cheaper than sitting for the stop or waiting for a target that was not coming.
- **SRFM (Surf Air Mobility), -1.8%:** failed, about -$0.44. Real NYSE company with a multi-day rally and a 40-minute base, and volume stayed elevated for four minutes after the breakout, so it met my rules. But after my entry at $1.09 it pinned at $1.08-$1.09 and volume collapsed from about 130k to a few thousand shares a minute. It never made a new high above $1.10 and broke $1.08 support 9 minutes later. I exited on my pre-set trigger, selling inside the spread at $1.07 (filled instantly) instead of hitting the bid or the stop.

## Pattern after 4 trades (1 win, 3 small losses or flat)

Three of four entries stalled within minutes of my buying. Each time I bought after the move had already run and the elevated volume faded right after my fill, so the +3% targets were never close to filling. Only EVTL worked, and it paid because I took a small +2.2% target. For future entries: aim for smaller targets (about +1.5% to +2.5%) that fit the stock's recent range, prefer entering at the base or first higher low instead of after the breakout candle, and treat volume that fades within 2-3 minutes of entry as an immediate exit signal. When exiting a thin stock, offer inside the spread first and only cross to the bid if it does not fill.

## Post-mortem of all 7 closed trades on 2026-09-25 (the user demanded this after 1 win in 7)

I measured each trade's path with 1-minute bars: MFE (best price reached after my fill) and MAE (worst price), hold time, and entry time.

| Trade | Entry (ET) | Held | MFE | MAE | Result |
|---|---|---|---|---|---|
| EVTL | 11:54 | 16 min | +2.8% | -0.7% | +$0.42 |
| SDEV | 12:11 | 4.5 min | +0.1% | -1.3% | -$0.28 |
| MRLN | 12:22 | 8.5 min | +0.1% | -0.9% | -$0.08 |
| SRFM | 12:35 | 10 min | 0.0% | -1.8% | -$0.44 |
| HUCK | 1:17 | 9.5 min | +0.1% | -0.7% | -$0.16 |
| AVAT | 1:33 | 6 min | 0.0% | -2.5% | -$0.54 |
| FATE | 2:48 | 8 min | 0.0% | -1.0% | $0.00 |

Findings:
1. In 6 of 7 trades the price never got meaningfully above my entry after I bought (MFE at most +0.1%). Only EVTL ever moved my way. My +1.5-3% targets were unreachable because the moves were over before I entered.
2. Root cause is scanner lag plus my confirmation rules. Every scan filters on how much a stock has already moved, and I then waited for a pullback or breakout confirmation. So I kept buying 1-5 minutes after the local peak (SDEV peak $1.48 three minutes before my $1.4585 entry; MRLN peak $2.067 two minutes before my $2.038; SRFM peak $1.10 two to four minutes before my $1.09) and got stalls.
3. Spread cost roughly equals the whole loss. Quoted spreads at entry were 0.3-0.9% (about 0.55% on average). Crossing it at entry and exit costs roughly 0.5% per round trip, about $0.11 on a $20 position, or about $0.75 across 7 trades, against a $1.08 total loss. With no directional edge on entry, the spread alone explains most of the loss.
4. Time of day: 7 of 8 entries were between 11:54 AM and 2:48 PM ET, the low-volume midday window the research says is worst for retail. Trades 1-4 came before I wrote the lull rule, and HUCK and AVAT came after the user told me to stop worrying about volume, so removing the volume filter let in thin stocks.
5. AVAT: a single 500-share print at $1.92 hit my stop one minute after entry, and the price recovered to $1.9695 within four minutes, then fell back. A stop in a thin book is a coin flip on noise.
6. What worked: cutting losers fast (average loss about -$0.29, about 1.3%) and always having protective orders. Losses stayed small. Nothing here is a risk-management failure; it is an entry-edge failure.
7. Sample is only 7 trades, so this is not proof of anything, but it matches the research: gross edge about equals trading costs.

What I should do differently: (a) do not trade midday; (b) stop entering after a move is confirmed; either trade only at the very start of an impulse with pre-set rules, or do not trade; (c) require depth and real volume; (d) no fixed cap on trades per day: the user said I can trade more than 2 a day if prices are right, so the limit is setup quality, not a count (I first proposed a 2-trade cap and the user overruled it); (d2) do pre-market research every trading day for real catalysts and trade off that watchlist (see the premarket-research-and-trade-count memory); (e) paper-track every setup, with entry, target, stop and MFE/MAE, until 20 setups show positive expectancy after spread, before risking live money.

## Rule changes adopted 2026-09-25 after 4 trades (the user approved applying these)

- Enter earlier, at the base or the first higher low, not after the breakout candle. Track whether this actually improves results, since it means a wider stop or a weaker signal.
- Use smaller targets of about +1.5% to +2.5%, and only take a trade if the target is at least 3x the current bid/ask spread.
- Time stop: if the trade has not moved in my favour within 3-5 minutes of entry, exit.
- Avoid entering during the midday lull (about 11:30-14:00 ET) unless the setup is exceptional (high relative volume and a spread of 1 cent or less). Focus on the open and the last hour. Still manage open positions and scan at all times.
- Keep score: after every closed trade, update the win rate and average win versus average loss. After about 20 trades, judge honestly whether the approach has an edge, and tell the user if it does not.

- **HUCK (Huckleberry AI), -0.7%:** failed, about -$0.15. After the user said not to worry about volume, I scanned without volume filters and took a range trade: bought 6 shares at $3.4776 right on $3.475 support with a 1-cent spread, target at the top of the range ($3.53) and stop just under support ($3.44). Support did not hold: it drifted to $3.46 and then $3.45 with no bounce over 9 minutes, so I exited at the bid before the stop. Lesson: a quiet range trade at support is a bet that buyers show up, and with almost no volume nobody showed up. A stock sitting on support with no volume tends to break down as easily as it bounces, so a tight spread alone does not make a setup. The user asked me not to worry about volume, but I did not save that as a permanent rule because I was unsure whether they meant it only for today.

- **AVAT (Avalanche Treasury), -2.3%:** failed, about -$0.54, the biggest loss of the day. I bought 12 shares at $1.97 right after a fresh 5-minute push (the exact mistake my own rules warn about), on an hour of steady higher lows and a 1-cent spread, without a volume filter. The book was very thin: only hundreds of shares traded per minute. One minute after entry a single 500-share print at $1.92 triggered my stop (filled at $1.93), and the quote showed a 6-cent spread ($1.91/$1.97). I cancelled the target and sold the other half at $1.9201 because a thin book with a wide spread makes unprotected shares too risky. Lessons: (1) do not knowingly break my own entry rule because I feel pressure to trade, (2) a stock with only hundreds of shares per minute is not really tradeable even with a tight quoted spread, because one print can trip a stop and the spread can widen to 6 cents in seconds, (3) volume is a liquidity check, not just a momentum signal, so removing it from the filters let thin names in.

- **FATE (Fate Therapeutics), $0.00 (flat):** the first trade taken under the full checklist. It broke out of a long flat base on 100k+ shares a minute, was above VWAP, and passed the price-book depth check (6,100 shares at the ask, 3,600/3,300 at the next bids, 17,900 at the $2.37 support wall, resistance walls at $2.50 and $2.53). I waited for a pullback ($2.465 to $2.42) and bought at the ask with a target under the $2.50 wall and a stop under the $2.37 wall. It then went nowhere: volume fell from ~100k a minute to a few thousand and it drifted to $2.40. After 7 minutes I hit my time stop, cancelled both exits, and sold at the bid $2.42 after a bounce back to my entry, for exactly breakeven. The lesson is that the time stop and pullback entry limited the damage, but even a good-looking volume breakout can stall right after my fill. Cost of the whole trade was the spread, with no commission.

- **OPEN (Opendoor), -0.7%:** failed, about -$0.14. It broke out of a tight 90-minute base ($2.57-$2.60) on 300k-share bars at 3:00 PM ET, was a $2.5B company with a very deep book (17-35k shares per level, 111k support wall at $2.55), and I bought the retest at $2.6099 with a target at $2.67 and a stop at $2.56. It never traded above my entry: volume collapsed from 60k+ to 1-2k shares a minute within seconds of my fill, and after about 9 minutes I hit my time stop and sold at $2.5921. This is the same pattern as the other trades, even with real liquidity, so the problem is not thin books. The post-mortem finding stands: I am buying after the impulse. Note also that prices above $1.00 cannot use half-cent limit prices (the API rejects them), and an offer at the ask did not fill, so I repriced to the bid.

Score so far (2026-09-25): 8 trades, 1 win (+$0.42), 6 losses, 1 flat ($0.00), net -$1.22 (account went from $24.55 to $23.33, verified against the broker). Earlier: 7 trades, 1 win (+$0.42), 5 losses (-$0.27, -$0.07, -$0.44, -$0.15, -$0.54), 1 flat ($0.00), net -$1.08 before OPEN. Win rate about 14%; average win +$0.42, average loss about -$0.29. No evidence yet of an edge; the two trades where I broke my own rules or removed a filter (HUCK, AVAT) lost the most between them.

## Working rules so far

- Do not buy the top of a volume burst. Prefer a pullback that holds its low on steady volume, or a breakout where volume stays elevated for several bars.
- A big percent gain plus huge relative volume is not enough. Skip vertical spikes, serial pump-and-dump names with tiny market caps, and prices pinned in a flat range (possible buyout price).
- Check the 1-minute and 5-minute tape before every entry, because scan results lag.
- Prefer tight spreads (about 1 cent or under 1%). A 3% spread eats most of a fast-money target.
- Fractional shares cannot carry stop orders, so use whole shares and split the position between a resting limit sell and a resting stop-market sell.
- Exit quickly when volume dries up, and trail the stop up right after the first target leg fills.

## Order types: how to use each one correctly (the user asked for this on 2026-09-25)

The user asked me to use all my tools and to use market, limit, stop (stop-loss), stop-limit and trailing stop orders correctly. `place_equity_order` supports exactly four types: market, limit, stop_market and stop_limit. There is NO trailing-stop or OCO order in the tools, and the Robinhood support page does not document one either; tell the user this plainly instead of pretending.
- **Limit:** the default for every entry (a marketable limit at or just above the ask, so I never pay more than my cap) and for every profit target. Offer sells inside the spread first, then at the bid.
- **Market:** only for an urgent full exit, in regular hours, on a name with real book depth (check get_equity_price_book). Never for entries or on thin stocks, because it can fill far from the quote. Fractional and dollar-amount orders are market-only and regular-hours-only, and cannot carry stops.
- **Stop-loss (stop_market):** the default protective stop. It becomes a market order when the stop price trades, so it guarantees an exit but not a price. Regular hours only, sell side sits below the market.
- **Stop-limit:** use only when a bad fill would be worse than no fill (very wide spread or thin book), with the limit a few cents below the stop. Risk: in a fast drop it may never fill and leave shares unprotected, so use it sparingly.
- **Trailing stop:** not available. Emulate it by cancelling and re-placing the stop_market higher as the price makes new highs (every pass, or right after the target leg fills), and use get_alerts/create_alert (price_crosses, VWAP crosses) plus get_alert_log polling as triggers. Alert events are not pushed to me, so they help the user more than the loop.
- Only one sell order can hold a given share, so split whole shares between the target and the stop.

## Tools to use (from Robinhood's "Trading with your agent" support page, read 2026-09-25)

The user told me to make sure I read the full tool list at https://robinhood.com/us/en/support/articles/trading-with-your-agent/. Tools I had not been using that I should:
- **get_equity_price_book** (Level 2 order book, up to 4 symbols): call it before every entry. Require real depth at the inside: roughly 1,000+ shares on both the best bid and the best ask, with no big gaps in the next few levels. On 2026-09-25 AVAT showed only 108 shares at the best bid ($1.92) and 696 at the next, which fits the stop whipsaw and 6-cent spread I hit; MRLN showed 2,151 and 13,060 at its inside bids.
- **get_pnl_trade_history / get_realized_pnl**: use these to verify my running score against the broker instead of my own arithmetic. Checked 2026-09-25: broker realized P&L for the 6 trades summed to -$1.08, matching the account drop from $24.55 to $23.47.
- **get_equity_technical_indicators** (RSI, MACD, Bollinger, moving averages, VWAP), **get_earnings_calendar**, **get_equity_news** and **get_equity_fundamentals** for context before entries.
- The page documents no bracket, OCO or trailing-stop orders, which is why I split shares between a limit sell and a stop-market sell. Limited-margin accounts can spend sale proceeds right away.
