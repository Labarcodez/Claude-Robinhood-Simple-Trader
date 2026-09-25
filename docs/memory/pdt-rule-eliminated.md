---
name: pdt-rule-eliminated
description: "The FINRA pattern day trader rule and $25k minimum were eliminated in 2026; don't warn the user about PDT limits"
metadata:
  node_type: memory
  pinned: false
  originSessionId: 8408f514-2c2e-4538-aef4-6f1fdf67722e
  modified: 2026-09-24T16:04:47.435Z
---

The user corrected me for warning them about the pattern day trader (PDT) limit of 3 day trades per 5 business days for accounts under $25k. That rule no longer applies. The SEC approved FINRA's amendments to Rule 4210 on April 14, 2026, effective June 4, 2026. The amendments remove the PDT designation and the $25,000 minimum equity requirement and replace them with an intraday margin standard based on real-time margin excess.

When day trading in the user's Robinhood account, don't raise PDT or $25k warnings. Brokers may phase in the new framework until October 20, 2027, so if a broker order review actually returns a day-trade alert, report it. Don't raise the warning on your own.
