---
name: always-protect-positions-with-exit-orders
description: "Every Robinhood position I open must immediately have resting exit orders — a stop loss plus a limit sell target, or a trailing stop — not just monitoring"
metadata:
  node_type: memory
  pinned: false
  originSessionId: b28dde51-ee23-43e1-aba8-925f0dd6c325
  modified: 2026-09-25T15:58:04.715Z
---

When I open a position in the user's Robinhood agentic account, I must set protective exit orders right away: a stop loss and a limit sell (profit target), or a trailing stop. The user told me "remember to set a stop loss and a limit sell or a trailing stop. be smart." Relying on my periodic loop to notice a drop and sell is not enough for fast-moving penny stocks, because price can gap through a stop level between checks.

Why: the user day trades volatile sub-$5 stocks in a tiny account, where a sudden drop between 5-minute checks can wipe out much of the balance. In one trade I only had a resting take-profit sell and a "software" stop that depended on my next pass, and the user corrected that.

How to apply: Robinhood will not let the same shares back two sell orders at once, and the order tool only supports market, limit, stop_market and stop_limit (no trailing stop or OCO). So with whole shares I split the position: some shares on a resting limit sell at the target, the rest on a resting stop_market below entry. When one leg fills or the setup changes, I cancel and re-place the other leg so the remaining shares are always protected. Then confirm both orders are live with get_equity_orders.
