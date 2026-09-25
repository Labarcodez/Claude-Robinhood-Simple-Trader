# Day trading: what the evidence says

Research compiled 2026-09-25 from public sources. Confidence notes are included where a source is weak.

## Bottom line

Day trading almost never makes money after costs. The best-known "working" strategy (the opening range breakout) reproduces gross of costs but nets out at about zero after spreads and slippage. Retail traders who trade intraday systematically underperform.

## Do day traders make money?

- **Taiwan, 1992-2006 (Barber, Lee, Liu, Odean).** A small skilled group exists: the top 500 day traders earned about +38 basis points per day after fees, while the bottom-ranked lost about 29 bps a day. Learning was slow and costly, and 80% of day traders quit within 2 years. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=529063). Summaries put the persistently profitable share below 1% ([summary](https://becoin.net/blog/day-trading-success-rate); secondary source).
- **Brazil futures (Chague, De-Losso, Giovannetti).** 97% of people who day-traded more than 300 days lost money, only 1.1% earned more than the Brazilian minimum wage, and there was no evidence of learning. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101).
- **Where the returns are.** Nearly all of the S&P 500 ETF's long-run return arrives overnight, while the intraday part wanders near zero. Retail traders tend to buy at the open and sell at the close. [SSRN](https://papers.ssrn.com/sol3/Delivery.cfm/4752520.pdf?abstractid=4752520&mirid=1), [Forbes](https://www.forbes.com/sites/hershshefrin/2025/05/03/why-stocks-appreciate-much-more-overnight-than-during-trading-hours/).

## Strategies and their evidence

| Strategy | Evidence | Verdict |
|---|---|---|
| Opening range breakout on "stocks in play" | Original paper reports 41.6%/yr, 2.81 Sharpe on high-volume stocks, simplified execution, no spread or slippage modelling ([summary](https://danfin.net/opening-range-breakout-research)). Replication on five indices: gross edge reproduced, net of costs four of five markets negative, Nasdaq about zero (+0.002 R) ([replication](https://www.mql5.com/en/blogs/post/776235)). QQQ replication: full-sample Sharpe -0.06 over 16 years ([replication](https://paperswithbacktest.com/strategies/orb-trading-strategy)). | Gross edge roughly equals trading cost. Replications are single-author blog posts, not peer reviewed. |
| Market intraday momentum (first half-hour predicts last half-hour) | S&P ETF, 1993-2013, JFE 2018, R-squared 1.6%, stronger on volatile high-volume days ([JFE](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351)). | Real but small, index ETFs only. |
| VWAP reversion / momentum reclaim | Practitioner guides only ([overview](https://www.tradezella.com/blog/vwap-trading-strategy)). | Not rigorously tested in what I found. |
| Gap-and-go small caps | Educator material, results stated as not typical, no verified win rates ([Medium](https://medium.com/@WarriorTrading/navigating-the-gap-and-go-strategy-b040f6b50938)). | Unverified. |
| Penny stocks | Wide spreads and slippage; pump-and-dump names fall sharply afterward ([summary](https://pro.stockalarm.io/blog/what-are-penny-stocks)). Popular claims such as "SEC: 90% lose" and "6% profitable" appear only on aggregator blogs and are unverified. | Costs dominate. |

## Practical takeaways

1. The signal is small and costs are large. On liquid index products the ORB edge is about 0.1 R, roughly the cost of execution.
2. Volume matters as a liquidity check, not just a momentum signal. The only strategy with a strong backtest depends on abnormally high opening volume.
3. Midday (about 11:30-14:00 ET) is the low-volume, mean-reverting window that is worst for retail trading.
4. Before risking money, paper-track setups for at least 20 trades and require positive expectancy after spreads.
