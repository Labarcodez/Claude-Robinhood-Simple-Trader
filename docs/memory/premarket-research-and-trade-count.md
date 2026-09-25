---
name: premarket-research-and-trade-count
description: "The user wants Claude to research stocks that could skyrocket before the market opens each trading day, and does not want a hard cap of 2 trades a day — trade more when prices are right"
metadata:
  node_type: memory
  pinned: false
  originSessionId: b28dde51-ee23-43e1-aba8-925f0dd6c325
  modified: 2026-09-25T19:11:44.216Z
---

On 2026-09-25, after I proposed capping myself at two trades a day, the user told me: "you can do more than 2 trades a day if prices are right. You need to do research before market opens for equities that could skyrocket." So there is no fixed daily trade cap. The limit is whether a setup is genuinely good (price, spread, depth, reward-to-risk), not a count.

The user also wants pre-market research every trading day, before the 9:30 AM ET open, aimed at finding equities with a real chance of a big move. This is the opposite of what I did on 2026-09-25, when I only reacted to intraday scanner lists after the moves had already happened and lost money buying late.

Why: my post-mortem showed that scanners lag, so I was buying stocks 1-5 minutes after their move ended. Researching catalysts ahead of time lets me know which names to watch and lets me act at the start of a move instead of after it.

How to apply: before each market open (and over the weekend for Monday), build a watchlist from real catalysts: earnings reports scheduled for that day (get_earnings_calendar), overnight and pre-market news and SEC filings (get_equity_news, edgar tools, web search), analyst upgrades and initiations, FDA or other scheduled events, unusual pre-market gappers, and sector news. For each name note the catalyst, the previous close, key support and resistance, float and average volume, and the exact trigger and price levels I would trade. Keep the watchlist short and specific. Then during the session only trade names on that list, or genuinely exceptional new ones, and still check price-book depth, spread and reward-to-risk before entering. Stay honest that "could skyrocket" is speculative and most catalyst stocks do not move, so keep sizing small and keep protective orders on every position.
