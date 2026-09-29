#!/usr/bin/env python3
"""Render Robinhood OHLCV as candlesticks + volume with optional VWAP/EMAs."""

import argparse
import json
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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


def _timestamp(row, i):
    value = row.get("timestamp")
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def render(rows, symbol, output):
    times = [_timestamp(r, i) for i, r in enumerate(rows)]
    use_time = all(t is not None for t in times)
    x = mdates.date2num(times) if use_time else list(range(len(rows)))
    step = min((x[i + 1] - x[i] for i in range(len(x) - 1) if x[i + 1] > x[i]), default=1)
    width = step * 0.72 if use_time else 0.72

    fig, (ax_price, ax_volume) = plt.subplots(
        2, 1, sharex=True, figsize=(13, 8),
        gridspec_kw={"height_ratios": [3, 1]}
    )

    typical = []
    volumes = []
    for i, row in enumerate(rows):
        o, h, l, c = map(float, (row["open"], row["high"], row["low"], row["close"]))
        v = float(row["volume"])
        xi = x[i]
        typical.append((h + l + c) / 3)
        volumes.append(v)

        ax_price.vlines(xi, l, h, linewidth=1)
        rect = Rectangle((xi - width / 2, min(o, c)), width,
                         max(abs(c - o), 1e-12),
                         fill=(c >= o), alpha=0.75)
        ax_price.add_patch(rect)
        ax_volume.bar(xi, v, width=width, alpha=0.55)

    # Rolling EMA and session VWAP.
    closes = [float(r["close"]) for r in rows]
    def ema(values, span):
        alpha = 2 / (span + 1)
        out = []
        current = values[0]
        for value in values:
            current = alpha * value + (1 - alpha) * current
            out.append(current)
        return out

    cumulative_pv = 0.0
    cumulative_v = 0.0
    vwap = []
    for tp, vol in zip(typical, volumes):
        cumulative_pv += tp * vol
        cumulative_v += vol
        vwap.append(cumulative_pv / cumulative_v if cumulative_v else tp)

    ax_price.plot(x, ema(closes, 9), linewidth=1.2, label="EMA 9")
    ax_price.plot(x, ema(closes, 20), linewidth=1.2, label="EMA 20")
    ax_price.plot(x, vwap, linewidth=1.2, label="VWAP")
    ax_price.legend(loc="upper left")

    ax_price.set_title(f"{symbol} — Robinhood OHLCV Candles + Volume")
    ax_price.set_ylabel("Price")
    ax_volume.set_ylabel("Volume")
    ax_volume.set_xlabel("Time" if use_time else "Bar")
    if use_time:
        locator = mdates.AutoDateLocator()
        ax_volume.xaxis.set_major_locator(locator)
        ax_volume.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
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
