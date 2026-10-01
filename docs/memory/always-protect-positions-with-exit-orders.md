---
name: position-exit-protection
description: "Historical lesson: use protective exit orders when Robinhood supports them, while respecting session-specific order mechanics"
metadata:
  node_type: memory
  modified: 2026-10-01
---

Historical lesson from live trading: positions need explicit exit planning and
should not depend entirely on a future software polling cycle.

Current rule: use the executable Robinhood order types supported for the
security and current session. In regular hours, protective resting exits may be
appropriate when supported. In extended hours, do not assume stop or trailing
orders execute; use supported limit-order workflows and active broker
reconciliation instead.

This note is subordinate to STRATEGY.md and the current Robinhood tool response.
