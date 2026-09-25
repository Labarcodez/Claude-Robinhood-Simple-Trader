---
name: robinhood-unsettled-funds
description: "In the user's Robinhood agentic account, sale proceeds are spendable immediately; unsettled_funds is not extra money"
metadata:
  node_type: memory
  pinned: false
  originSessionId: fcae140b-d7ca-43de-aebf-79c1eb0ef8b9
  modified: 2026-09-24T20:09:16.663Z
---

The user's Robinhood agentic account is a limited margin account, so money from a sale can be spent again right away. The `unsettled_funds` field from `get_accounts` is not extra cash waiting to arrive. It is already counted in the buying power that `get_portfolio` reports. The user corrected me after I told them $20.39 of unsettled funds would add to their buying power the next day.

Use `get_portfolio` buying power as the only figure for how much can be spent. Never add `unsettled_funds` to it, and never tell the user that more money will become available after settlement.
