"""The numpy market generator the C++ generator replaced, kept as a test oracle.

These are the functions that generated every stored run's bars before the port,
copied unchanged: the price paths, the shock arrays the newsroom used to build,
the session calendar, the original six-path generator and the chart bucketing.
The parity tests generate the same blocks through both and require identical
cents and volumes. Do not edit them to match the engine; they are the
definition the engine is held to.
"""

import math
import random
from datetime import datetime, timedelta
from functools import lru_cache
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import numpy as np
from quanta.services.simulator_universe import COMPANIES, LEGACY_SYMBOLS, SECTORS

SESSION_BARS = 390
BLOCK_SESSIONS = 21
BLOCK_BARS = BLOCK_SESSIONS * SESSION_BARS
MARKET_VOL = 0.15
SECTOR_VOL = 0.11
SECTOR_LOAD = 0.62
EASTERN = ZoneInfo("America/New_York")
OPENING = datetime(2025, 1, 6, 9, 30, tzinfo=EASTERN)
POINT = 0.0001
SECTOR_MEMBERS = {sector: [c.symbol for c in COMPANIES if c.sector == sector] for sector in SECTORS}


def shock_room(shocks, total=BLOCK_BARS):
    """The shock arrays the newsroom used to build, from the shocks it now schedules."""
    room = SimpleNamespace(
        market=np.zeros(total),
        sector={name: np.zeros(total) for name in SECTORS},
        company={c.symbol: np.zeros(total) for c in COMPANIES},
        volatility={c.symbol: np.zeros(total) for c in COMPANIES},
        volume={c.symbol: np.zeros(total) for c in COMPANIES},
    )
    for scope, target, index, points, sign, span in shocks:
        if scope == 0:
            _apply(room, index, points, sign, span, market=True)
        elif scope == 1:
            _apply(room, index, points, sign, span, sector=SECTORS[target])
        else:
            _apply(room, index, points, sign, span, symbol=COMPANIES[target].symbol)
    return room


def _drift(target, start, span, amount):
    """Spread `amount` over an exponentially decaying window from `start`.

    Only the affected slice is touched. Building a full-length array per event
    dominated both generation time and peak memory when this ran per headline.
    """
    end = min(len(target), start + span)
    if end <= start:
        return
    weights = np.exp(-np.arange(end - start) / max(span / 3.0, 1.0))
    total = weights.sum()
    if total:
        target[start:end] += amount * (weights / total)


def _excite(room, index, magnitude, span, symbols, scale=1.0):
    """Raise modeled volatility and traded volume around a shock, then decay."""
    for symbol in symbols:
        series = room.volatility[symbol]
        window = slice(index, min(len(series), index + span))
        steps = np.arange(window.stop - window.start)
        weight = scale * magnitude / 0.02
        series[window] += min(3.0, weight) * np.exp(-steps / max(span / 4.0, 1))
        room.volume[symbol][window] += min(6.0, 2.2 * weight) * np.exp(-steps / max(span / 5.0, 1))


def _apply(room, index, points, sign, span, market=False, sector=None, symbol=None):
    """Split a scored shock into an immediate move and a decaying follow-through."""
    magnitude = abs(points) * POINT
    target = room.market if market else room.sector[sector] if sector else room.company[symbol]
    length = len(target)
    if index >= length:
        return
    target[index] += 0.58 * magnitude * sign
    _drift(target, index + 1, span, 0.42 * magnitude * sign)
    if symbol:
        _excite(room, index, magnitude, span, [symbol])
    elif sector:
        _excite(room, index, magnitude, span, SECTOR_MEMBERS[sector], 0.7)
    else:
        _excite(room, index, magnitude, min(span, 200), list(room.volume), 0.9)


@lru_cache(maxsize=4096)
def session_open(session):
    """Opening minute of a session on the weekday-only calendar. Holidays omitted."""
    day, remaining = OPENING, session
    while remaining:
        day += timedelta(days=1)
        if day.weekday() < 5:
            remaining -= 1
    return day


@lru_cache(maxsize=64)
def session_times(first_session, sessions):
    """Minute stamps for a block of sessions, 09:30-16:00 America/New_York."""
    stamps = []
    for offset in range(sessions):
        day = session_open(first_session + offset)
        stamps.extend(int((day + timedelta(minutes=i)).timestamp()) for i in range(SESSION_BARS))
    return np.array(stamps, dtype=np.int64)


def _shape(minutes, floor, open_weight, open_scale, close_weight, close_scale):
    """U-shaped intraday profile: busiest at the open, firm again into the close."""
    return (
        floor
        + open_weight * np.exp(-minutes / open_scale)
        + close_weight * np.exp(-(SESSION_BARS - 1 - minutes) / close_scale)
    )


def _persistence(rng, shape, phi, eta):
    """AR(1) log-variance, the source of quiet stretches and busy stretches.

    Normalized to unit mean square so clustering redistributes volatility through
    the run without changing how much of it there is.
    """
    steps, series = shape[0], np.zeros(shape)
    noise = rng.normal(0, eta, size=shape)
    for t in range(1, steps):
        series[t] = phi * series[t - 1] + noise[t]
    multiplier = np.exp(series)
    return multiplier / np.sqrt((multiplier**2).mean(axis=0))


def _unit(series):
    """Rescale a positive multiplier to unit mean square."""
    return series / math.sqrt(float((series**2).mean()))


def _paths(seed, room, first_session, carry):
    """One block of bars, continuing from the closing prices handed in."""
    rng = np.random.default_rng([seed, first_session, 0x9E3779B9])
    times = session_times(first_session, BLOCK_SESSIONS)
    minutes = np.arange(BLOCK_BARS) % SESSION_BARS
    session = first_session + np.arange(BLOCK_BARS) // SESSION_BARS
    opens_session = minutes == 0
    openings = int(opens_session.sum())
    price_shape = _unit(_shape(minutes, 0.55, 1.35, 45.0, 0.85, 55.0))
    volume_shape = _shape(minutes, 0.50, 1.80, 35.0, 1.10, 40.0)
    per_bar = 1 / math.sqrt(252 * SESSION_BARS)

    # One market factor, one factor per sector, then company-specific noise. Each
    # is calibrated in annualized volatility and carved out of the company's own
    # budget below, so a stock's realized volatility stays near its stated level.
    market_vol = MARKET_VOL * per_bar
    market_noise = (
        market_vol
        * price_shape
        * _persistence(rng, (BLOCK_BARS,), 0.985, 0.055)
        * rng.standard_normal(BLOCK_BARS)
    )
    # Overnight gaps carry more of the move than a single minute inside a session.
    market_noise[opens_session] += 2.6 * market_vol * rng.standard_normal(openings)
    sector_noise = {
        name: SECTOR_VOL * per_bar * price_shape * rng.standard_normal(BLOCK_BARS)
        for name in room.sector
    }

    count = len(COMPANIES)
    clustering = _persistence(rng, (BLOCK_BARS, count), 0.992, 0.05)
    noise = rng.standard_normal((BLOCK_BARS, count))
    output, closing = {}, {}
    for position, company in enumerate(COMPANIES):
        excited = _unit(1 + room.volatility[company.symbol])
        factors = company.beta * market_noise + SECTOR_LOAD * sector_noise[company.sector]
        story = (
            company.beta * room.market
            + SECTOR_LOAD * room.sector[company.sector]
            + room.company[company.symbol]
        )
        budget = (company.volatility * per_bar) ** 2
        spare = budget - float(factors.var()) - float(story.var())
        idio = math.sqrt(max(spare, 0.25 * budget))
        returns = (
            factors
            + story
            + idio * price_shape * clustering[:, position] * excited * noise[:, position]
        )
        returns[opens_session] += (
            1.9 * idio * excited[opens_session] * rng.standard_normal(openings)
        )
        # Remove the Itô drift so a flat expectation stays flat over the block.
        returns = np.clip(returns - 0.5 * float(returns.var()), -0.25, 0.25)
        opened = carry[company.symbol]
        closes = opened * np.exp(np.cumsum(returns))
        previous = np.concatenate(([opened], closes[:-1]))
        # Part of each bar's move is already present at its opening print, and
        # most of an overnight move is, which is what makes a gap look like one.
        share = np.where(opens_session, 0.78, 0.26)
        opening = previous * np.exp(share * returns)
        span = np.abs(returns) + idio * price_shape * 0.9
        upper = np.abs(rng.standard_normal(BLOCK_BARS)) * span * 0.55
        lower = np.abs(rng.standard_normal(BLOCK_BARS)) * span * 0.55
        high = np.maximum(opening, closes) * (1 + upper)
        low = np.minimum(opening, closes) * (1 - lower)
        turnover = (
            company.volume
            * volume_shape
            * (1 + room.volume[company.symbol])
            * np.exp(rng.normal(0, 0.35, BLOCK_BARS))
            * (1 + 6 * np.abs(returns))
        )
        cents = np.stack(
            [
                np.rint(np.maximum(value, 0.01) * 100).astype(np.int32)
                for value in (opening, high, low, closes)
            ]
        )
        output[company.symbol] = BarSeries(
            times,
            cents,
            np.maximum(np.rint(turnover), 100).astype(np.int32),
            session,
        )
        # The next block opens where this one closed, to the cent that was printed.
        closing[company.symbol] = float(cents[3][-1]) / 100
    return output, closing


@lru_cache(maxsize=8)
def legacy_synthetic(seed):
    """The original six fictional paths. Preserved so existing runs replay unchanged."""
    start = datetime(2025, 1, 6, 9, 30, tzinfo=EASTERN)
    times = []
    date = start
    while len(times) < 6000:
        if date.weekday() < 5:
            times.extend(int((date + timedelta(minutes=i)).timestamp()) for i in range(390))
        date += timedelta(days=1)
    times = times[:6000]
    output = {}
    for number, (symbol, (_, initial)) in enumerate(LEGACY_SYMBOLS.items()):
        rng = random.Random(seed + number * 100003)
        price = initial
        rows = []
        for i, stamp in enumerate(times):
            opening = price * math.exp(rng.gauss(0, 0.0008 if i % 390 else 0.006))
            closing = opening * math.exp(rng.gauss(0.000015, 0.0018))
            high = max(opening, closing) * (1 + rng.random() * 0.0015)
            low = min(opening, closing) * (1 - rng.random() * 0.0015)
            rows.append(
                {
                    "time": stamp,
                    "open": round(opening, 2),
                    "high": round(high, 2),
                    "low": round(low, 2),
                    "close": round(closing, 2),
                    "volume": rng.randint(2000, 30000),
                }
            )
            price = closing
        output[symbol] = rows
    return output


class BarSeries:
    """Columnar OHLCV with bars materialized only when they are read.

    The engine reads one bar per symbol per request in most paths, so keeping the
    full series as arrays avoids holding hundreds of thousands of dictionaries
    per cached seed while preserving the `rows[index]["close"]` interface used by
    the execution model and its tests.
    """

    __slots__ = ("time", "cents", "volume", "session")

    def __init__(self, time, cents, volume, session):
        self.time, self.cents, self.volume, self.session = time, cents, volume, session

    def __len__(self):
        return int(self.time.shape[0])

    def extend(self, block):
        """Append the next block's prices and volumes in place.

        The time and session arrays are shared across every company and are
        replaced by the market itself, so they are not copied here.
        """
        self.cents = np.concatenate((self.cents, block.cents), axis=1)
        self.volume = np.concatenate((self.volume, block.volume))

    @property
    def open(self):
        return self.cents[0] / 100.0

    @property
    def high(self):
        return self.cents[1] / 100.0

    @property
    def low(self):
        return self.cents[2] / 100.0

    @property
    def close(self):
        return self.cents[3] / 100.0

    def _row(self, index):
        return {
            "time": int(self.time[index]),
            "open": int(self.cents[0][index]) / 100,
            "high": int(self.cents[1][index]) / 100,
            "low": int(self.cents[2][index]) / 100,
            "close": int(self.cents[3][index]) / 100,
            "volume": int(self.volume[index]),
        }

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self._row(i) for i in range(*index.indices(len(self)))]
        if index < 0:
            index += len(self)
        if not 0 <= index < len(self):
            raise IndexError(index)
        return self._row(index)

    def __iter__(self):
        return (self._row(i) for i in range(len(self)))

    def aggregate(self, start, stop, per_bucket):
        """Group observations into coarser bars without materializing each one.

        Sessions are fixed-length and start on the hour-and-a-half boundary, so a
        bucket is decided by arithmetic on the index rather than by reading a
        timestamp, and only the buckets themselves become dictionaries.
        """
        if stop <= start:
            return []
        index = np.arange(start, stop)
        key = (
            self.session[start:stop].astype(np.int64) * SESSION_BARS
            + (index % SESSION_BARS) // per_bucket
        )
        opens = np.flatnonzero(np.concatenate(([True], key[1:] != key[:-1])))
        closes = np.concatenate((opens[1:], [stop - start])) - 1
        window = slice(start, stop)
        high = np.maximum.reduceat(self.cents[1][window], opens)
        low = np.minimum.reduceat(self.cents[2][window], opens)
        volume = np.add.reduceat(self.volume[window].astype(np.int64), opens)
        return [
            {
                # A bucket is stamped with its first observation, which is the
                # session-anchored boundary it starts on.
                "time": int(self.time[window][first]),
                "open": int(self.cents[0][window][first]) / 100,
                "high": int(high[position]) / 100,
                "low": int(low[position]) / 100,
                "close": int(self.cents[3][window][last]) / 100,
                "volume": int(volume[position]),
            }
            for position, (first, last) in enumerate(zip(opens, closes, strict=True))
        ]

    def prior_session_close(self, cursor):
        """Close of the last bar before the cursor's own session."""
        day = self.session[cursor]
        earlier = np.flatnonzero(self.session[:cursor] < day)
        index, row = (earlier[-1], 3) if earlier.size else (0, 0)
        return int(self.cents[row][index]) / 100
