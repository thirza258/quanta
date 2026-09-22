"""Generated market data for a run.

Two generators live here. `legacy_synthetic` is the original six-path model and
is kept byte-for-byte so runs created before the fictional universe still resolve
their stored cursors, fills and positions against the same bars.

`simulated_market` is the current model: a news-driven, factor-based market over
fictional companies. The newsroom schedule is produced first, and its macro,
sector and company shocks enter the return, volatility and volume processes, so
a visible move on the chart has a headline on the same bar.

Both are pure functions of the run's stored seed. Nothing here reads the clock,
and no generated series is ever presented as observed market history.
"""

import math
import random
from datetime import datetime, timedelta
from functools import lru_cache
from zoneinfo import ZoneInfo

import numpy as np
from fastapi import HTTPException

from quanta.db.models import TradingDataset
from quanta.services.simulator_news import schedule
from quanta.services.simulator_universe import (
    COMPANIES,
    LEGACY_SYMBOLS,
    UNIVERSE_ID,
)

SYMBOLS = LEGACY_SYMBOLS
SESSIONS = 20
SESSION_BARS = 390
TOTAL_BARS = SESSIONS * SESSION_BARS
MARKET_VOL = 0.15
SECTOR_VOL = 0.11
SECTOR_LOAD = 0.62
EASTERN = ZoneInfo("America/New_York")
OPENING = datetime(2025, 1, 6, 9, 30, tzinfo=EASTERN)
WARMUP = 499


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

    def prior_session_close(self, cursor):
        """Close of the last bar before the cursor's own session."""
        day = self.session[cursor]
        earlier = np.flatnonzero(self.session[:cursor] < day)
        index, row = (earlier[-1], 3) if earlier.size else (0, 0)
        return int(self.cents[row][index]) / 100


@lru_cache(maxsize=2)
def session_times(total):
    """Weekday-only minute stamps, 09:30–16:00 America/New_York. Holidays omitted."""
    stamps = []
    day = OPENING
    while len(stamps) < total:
        if day.weekday() < 5:
            stamps.extend(
                int((day + timedelta(minutes=i)).timestamp()) for i in range(SESSION_BARS)
            )
        day += timedelta(days=1)
    return np.array(stamps[:total], dtype=np.int64)


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


# One entry per seed holds a run's bars, headlines and statements. Prices are
# stored as whole cents and the shock arrays are released once the paths are
# built, so an entry costs roughly 8 MB; 24 keeps that many accounts warm inside
# a 1 GiB API container, and a cold generation costs roughly 70 ms.
@lru_cache(maxsize=24)
def generated(seed):
    """Bars and the newsroom for one run, built together from its seed."""
    room = schedule(seed, SESSIONS, SESSION_BARS)
    return _paths(seed, room), room.release()


def simulated_market(seed):
    """Fictional companies whose prices are moved by the run's simulated news."""
    return generated(seed)[0]


def newsroom(seed):
    """The run's headlines, reporting calendar and generated statements."""
    return generated(seed)[1]


def _paths(seed, room):
    rng = np.random.default_rng((seed * 6364136223846793005 + 1442695040888963407) % (2**63))
    times = session_times(TOTAL_BARS)
    minutes = np.arange(TOTAL_BARS) % SESSION_BARS
    session = np.arange(TOTAL_BARS) // SESSION_BARS
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
        * _persistence(rng, (TOTAL_BARS,), 0.985, 0.055)
        * rng.standard_normal(TOTAL_BARS)
    )
    # Overnight gaps carry more of the move than a single minute inside a session.
    market_noise[opens_session] += 2.6 * market_vol * rng.standard_normal(openings)
    sector_noise = {
        name: SECTOR_VOL * per_bar * price_shape * rng.standard_normal(TOTAL_BARS)
        for name in room.sector
    }

    count = len(COMPANIES)
    clustering = _persistence(rng, (TOTAL_BARS, count), 0.992, 0.05)
    noise = rng.standard_normal((TOTAL_BARS, count))
    output = {}
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
        # Remove the Itô drift so a flat expectation stays flat over the run.
        returns = np.clip(returns - 0.5 * float(returns.var()), -0.25, 0.25)
        closes = company.price * np.exp(np.cumsum(returns))
        previous = np.concatenate(([company.price], closes[:-1]))
        # Part of each bar's move is already present at its opening print, and
        # most of an overnight move is, which is what makes a gap look like one.
        share = np.where(opens_session, 0.78, 0.26)
        opening = previous * np.exp(share * returns)
        span = np.abs(returns) + idio * price_shape * 0.9
        upper = np.abs(rng.standard_normal(TOTAL_BARS)) * span * 0.55
        lower = np.abs(rng.standard_normal(TOTAL_BARS)) * span * 0.55
        high = np.maximum(opening, closes) * (1 + upper)
        low = np.minimum(opening, closes) * (1 - lower)
        turnover = (
            company.volume
            * volume_shape
            * (1 + room.volume[company.symbol])
            * np.exp(rng.normal(0, 0.35, TOTAL_BARS))
            * (1 + 6 * np.abs(returns))
        )
        output[company.symbol] = BarSeries(
            times,
            np.stack(
                [
                    np.rint(np.maximum(value, 0.01) * 100).astype(np.int32)
                    for value in (opening, high, low, closes)
                ]
            ),
            np.maximum(np.rint(turnover), 100).astype(np.int32),
            session,
        )
    return output


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


# Retained for callers of the previous name.
synthetic = legacy_synthetic


def markets(state, db):
    config = state["config"]
    if config["mode"] == "synthetic":
        if config.get("universe") == UNIVERSE_ID:
            return simulated_market(config["seed"])
        return legacy_synthetic(config["seed"])
    dataset = db.get(TradingDataset, config["dataset_id"])
    if not dataset:
        raise HTTPException(503, "The run's historical data snapshot is unavailable.")
    return {config["symbol"]: dataset.bars}
