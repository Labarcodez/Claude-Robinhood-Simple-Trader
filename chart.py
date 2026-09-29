#!/usr/bin/env python3
"""Render Robinhood OHLCV bars as a candlestick + volume chart.

Input JSON format:
[
  {"timestamp": "...", "open": 1.0, "high": 1.1, "low": 0.9, "close": 1.05, "volume": 12345},
  ...
]

This is intentionally broker-data-only: Claude supplies the OHLCV returned by
Robinhood get_equity_historicals; this script only renders it.
"""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def load_bars(path):
    rows = json.loads(Path(path).read_text())
    if not rows:
        raise ValueError("No OHLCV bars supplied.")
    required = {"open", "high", "low", "close", "volume"}
    for i, row in enumerate(rows):
        missing = required - set(row)
        if missing:
            raise ValueError(f"Bar {i} missing fields: {sorted(missing)}")
    return rows


def render(rows, symbol, output):
    fig, (ax_price, ax_volume) = plt.subplots(
        2, 1, sharex=True, figsize=(12, 7),
        gridspec_kw={"height_ratios": [3, 1]}
    )

    width = 0.72
    for i, row in enumerate(rows):
        o, h, l, c = map(float, (row["open"], row["high"], row["low"], row["close"]))
        v = float(row["volume"])

        ax_price.vlines(i, l, h, linewidth=1)
        body_low = min(o, c)
        body_height = max(abs(c - o), 1e-12)
        rect = Rectangle(
            (i - width / 2, body_low),
            width,
            body_height,
            fill=(c >= o),
            alpha=0.75,
        )
        ax_price.add_patch(rect)

        ax_volume.bar(i, v, width=width, alpha=0.55)

    ax_price.set_title(f"{symbol} — Robinhood OHLCV Candles + Volume")
    ax_price.set_ylabel("Price")
    ax_volume.set_ylabel("Volume")
    ax_volume.set_xlabel("Bar")
    ax_price.grid(True, alpha=0.2)
    ax_volume.grid(True, alpha=0.2)
    fig.tight_layout()

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    render(load_bars(args.input), args.symbol.upper(), args.output)


if __name__ == "__main__":
    main()
