"""The Python desk analytics the C++ kernels replaced, kept as a test oracle.

The indicator loops, the per-fill mark-to-market and the six-path chart
bucketing, copied unchanged from the services they were part of.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

import numpy as np


def sma_series(values, period):
    """Rolling mean, with no value until the window is full."""
    out, total = [], 0.0
    for index, value in enumerate(values):
        total += float(value)
        if index >= period:
            total -= float(values[index - period])
        out.append(total / period if index >= period - 1 else None)
    return out


def ema_series(values, period):
    """Seeded with the first full simple average, then exponentially smoothed."""
    out, total, previous = [], 0.0, None
    alpha = 2 / (period + 1)
    for index, value in enumerate(values):
        total += float(value)
        if index < period - 1:
            out.append(None)
            continue
        previous = (
            total / period if previous is None else alpha * float(value) + (1 - alpha) * previous
        )
        out.append(previous)
    return out


def rsi_series(values, period=14):
    """Wilder smoothing, matching the definition the courses teach."""
    out, gain, loss = [], 0.0, 0.0
    for index, value in enumerate(values):
        if index == 0:
            out.append(None)
            continue
        change = float(value) - float(values[index - 1])
        if index <= period:
            gain += max(change, 0.0) / period
            loss += max(-change, 0.0) / period
        else:
            gain = (gain * (period - 1) + max(change, 0.0)) / period
            loss = (loss * (period - 1) + max(-change, 0.0)) / period
        if index < period:
            out.append(None)
        elif loss == 0:
            out.append(100.0 if gain else 50.0)
        else:
            out.append(100 - 100 / (1 + gain / loss))
    return out


def macd_series(values, fast=12, slow=26, signal=9):
    quick, slack = ema_series(values, fast), ema_series(values, slow)
    line = [None if a is None or b is None else a - b for a, b in zip(quick, slack, strict=True)]
    present = [value for value in line if value is not None]
    offset = len(line) - len(present)
    smoothed = [None] * offset + ema_series(present, signal)
    return {
        "line": line,
        "signal": smoothed,
        "histogram": [
            None if a is None or b is None else a - b for a, b in zip(line, smoothed, strict=True)
        ],
    }


def holdings(state, data, cursor, start):
    """The mark-to-market loop from the Python desk.performance(), verbatim."""
    first = next(iter(data.values()))
    times = (
        np.asarray(first.time[: cursor + 1], dtype=np.int64)[start:]
        if hasattr(first, "time")
        else np.array([row["time"] for row in first[: cursor + 1]], dtype=np.int64)[start:]
    )
    opening = float(state["ledger"][0]["cash"]) if state["ledger"] else 100000.0

    cash = np.full(len(times), opening)
    for entry in state["ledger"]:
        if entry["time"] is None:
            continue
        at = int(np.searchsorted(times, entry["time"]))
        if at < len(cash):
            cash[at:] = float(entry["cash"])

    holdings = np.zeros(len(times))
    by_symbol = {}
    marks = {}
    for fill in state["fills"]:
        symbol = fill["symbol"]
        if symbol not in data:
            continue
        if symbol not in marks:
            marks[symbol] = _closes(data[symbol], cursor)[start:]
        at = int(np.searchsorted(times, fill["time"]))
        if at >= len(times):
            continue
        quantity = fill["quantity"] * (1 if fill["side"] == "buy" else -1)
        leg = quantity * np.concatenate((np.zeros(at), marks[symbol][at:]))
        holdings += leg
        by_symbol[symbol] = by_symbol.get(symbol, np.zeros(len(times))) + leg
    equity = cash + holdings
    gross = sum((np.abs(values) for values in by_symbol.values()), np.zeros(len(times)))
    prices = np.vstack([_closes(series, cursor)[start:] for series in data.values()])
    level = (prices / prices[:, :1]).mean(axis=0)
    return equity, gross, level


def _closes(rows, cursor):
    if hasattr(rows, "close"):
        return np.asarray(rows.close[: cursor + 1], dtype=float)
    return np.array([row["close"] for row in rows[: cursor + 1]], dtype=float)


def grouped(rows, interval):
    """The chart bucketing the original six-path runs used, from simulator.market()."""
    grouped = {}
    size = {"5m": 300, "15m": 900, "1h": 3600, "1D": 86400}[interval]
    for bar in rows:
        session_start = datetime.fromtimestamp(bar["time"], ZoneInfo("America/New_York")).replace(
            hour=9, minute=30, second=0
        )
        anchor = int(session_start.timestamp())
        timestamp = anchor if interval == "1D" else anchor + (bar["time"] - anchor) // size * size
        if timestamp not in grouped:
            grouped[timestamp] = {**bar, "time": timestamp}
        else:
            item = grouped[timestamp]
            item.update(
                high=max(item["high"], bar["high"]),
                low=min(item["low"], bar["low"]),
                close=bar["close"],
                volume=item["volume"] + bar["volume"],
            )
    return list(grouped.values())
