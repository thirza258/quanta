"""Generated market data for a run.

Two generators serve runs. `legacy_synthetic` is the original six-path model,
kept so runs created before the fictional universe still resolve their stored
cursors, fills and positions against the same bars.

`simulated_market` is the current model: a news-driven, factor-based market over
fictional companies. The newsroom schedule is produced first, and its macro,
sector and company shocks enter the return, volatility and volume processes, so
a visible move on the chart has a headline on the same bar.

Both are pure functions of the run's stored seed, and both are computed by the
C++ engine (backend/engine) to the cent the original numpy and random-module
generators produced. Nothing here reads the clock, and no generated series is
ever presented as observed market history.
"""

import threading
from collections import OrderedDict
from datetime import datetime
from functools import lru_cache
from zoneinfo import ZoneInfo

import numpy as np
from fastapi import HTTPException

from quanta import engine
from quanta.db.models import TradingDataset
from quanta.services.simulator_news import Newsroom, schedule
from quanta.services.simulator_universe import (
    COMPANIES,
    LEGACY_SYMBOLS,
    SECTORS,
    UNIVERSE_ID,
)

SYMBOLS = LEGACY_SYMBOLS
SESSION_BARS = 390
# A run has no fixed end. Sessions are generated a block at a time as the replay
# clock reaches them, and one block beyond the cursor is always kept ahead so the
# next bar, the next headline and the next scheduled report already exist.
BLOCK_SESSIONS = 21
BLOCK_BARS = BLOCK_SESSIONS * SESSION_BARS
SESSIONS = BLOCK_SESSIONS
TOTAL_BARS = BLOCK_BARS
EASTERN = ZoneInfo("America/New_York")
OPENING = datetime(2025, 1, 6, 9, 30, tzinfo=EASTERN)
WARMUP = 499
LEGACY_BARS = 6000


class BarSeries:
    """Columnar OHLCV with bars materialized only when they are read.

    The engine reads one bar per symbol per request in most paths, so keeping the
    full series as arrays avoids holding hundreds of thousands of dictionaries
    per cached seed while preserving the `rows[index]["close"]` interface used by
    the execution model and its tests.
    """

    __slots__ = ("time", "cents", "volume", "session", "day")

    def __init__(self, time, cents, volume, session, day=None):
        self.time, self.cents, self.volume, self.session = time, cents, volume, session
        self.day = day

    def __len__(self):
        return int(self.time.shape[0])

    def extend(self, block):
        """Append the next block's prices and volumes in place.

        The time, session and day arrays are shared across every company and are
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
        timestamp, and only the buckets themselves become dictionaries. A bucket
        is stamped with its first observation, which is the session-anchored
        boundary it starts on.
        """
        if stop <= start:
            return []
        times, cents, volume = engine.aggregate(
            self.cents, self.volume, self.time, self.session, start, stop, per_bucket
        )
        return _bucket_rows(times, cents, volume)

    def prior_session_close(self, cursor):
        """Close of the last bar before the cursor's own session."""
        day = self.session[cursor]
        earlier = np.flatnonzero(self.session[:cursor] < day)
        index, row = (earlier[-1], 3) if earlier.size else (0, 0)
        return int(self.cents[row][index]) / 100


def _bucket_rows(times, cents, volume):
    return [
        {
            "time": stamp,
            "open": opening / 100,
            "high": high / 100,
            "low": low / 100,
            "close": closing / 100,
            "volume": traded,
        }
        for stamp, opening, high, low, closing, traded in zip(
            times.tolist(), *cents.tolist(), volume.tolist(), strict=True
        )
    ]


class EngineMarket(dict):
    """A run's bars by symbol, with the engine's columnar copy attached.

    Consumers read it as the plain dictionary of rows it has always been; the
    execution engine reads `engine_columns` instead of converting every row per request.
    """

    engine_columns = None
    sessions = None


@lru_cache(maxsize=4096)
def session_open(session):
    """Opening minute of a session on the weekday-only calendar. Holidays omitted."""
    stamps, _ = engine.session_calendar(session, 1)
    return datetime.fromtimestamp(int(stamps[0]), EASTERN)


@lru_cache(maxsize=64)
def session_times(first_session, sessions):
    """Minute stamps for a block of sessions, 09:30-16:00 America/New_York."""
    stamps, _ = engine.session_calendar(first_session, sessions)
    stamps.flags.writeable = False
    return stamps


class Market:
    """A generated market that grows a block of sessions at a time.

    A run has no fixed end. Blocks are produced in order, each continuing from the
    closing prices of the one before, so the clock can keep advancing for as long
    as a learner wants to replay. A block is a pure function of the seed and its
    own first session, so the same block regenerated later is identical, and a
    stored cursor always resolves to the same bar.
    """

    def __init__(self, seed):
        self.seed = seed
        self.blocks = 0
        self.series = {}
        self.room = Newsroom()
        self.carry = {company.symbol: float(company.price) for company in COMPANIES}
        # One copy of the clock, shared by all 32 series.
        self.time = np.empty(0, dtype=np.int64)
        self.session = np.empty(0, dtype=np.int64)
        self.day = np.empty(0, dtype=np.int32)
        self._lock = threading.Lock()

    def __len__(self):
        return self.blocks * BLOCK_BARS

    def ensure(self, cursor):
        """Generate through the block after the one holding the cursor."""
        target = (max(int(cursor), 0) // BLOCK_BARS + 2) * BLOCK_BARS
        if len(self) >= target:
            return
        with self._lock:
            while len(self) < target:
                self._extend()

    def _extend(self):
        first = self.blocks * BLOCK_SESSIONS
        room = schedule(self.seed, first, BLOCK_SESSIONS, SESSION_BARS, self.room.books or None)
        block, self.carry = _paths(self.seed, room, first, self.carry)
        times, days = engine.session_calendar(first, BLOCK_SESSIONS)
        self.time = np.concatenate((self.time, times))
        self.session = np.concatenate((self.session, first + np.arange(BLOCK_BARS) // SESSION_BARS))
        self.day = np.concatenate((self.day, days))
        for symbol, series in block.items():
            if symbol in self.series:
                self.series[symbol].extend(series)
            else:
                self.series[symbol] = series
            self.series[symbol].time = self.time
            self.series[symbol].session = self.session
            self.series[symbol].day = self.day
        self.room.events.extend(room.events)
        self.room.books = room.books
        self.room.calendar = room.calendar
        room.release()
        self.blocks += 1


# One entry per seed. A block of 21 sessions costs a few tens of milliseconds to
# generate, most of it the newsroom's text, and an entry grows only as far as its
# own run is actually replayed: roughly 5 MB of bars per simulated month, plus
# its headlines. A run carried through a simulated year holds around 60 MB, so
# four are kept rather than the two dozen a fixed-size market allowed.
@lru_cache(maxsize=4)
def _market(seed):
    return Market(seed)


def simulated_market(seed, cursor=0):
    """Fictional companies whose prices are moved by the run's simulated news."""
    market = _market(seed)
    market.ensure(cursor)
    return market.series


def newsroom(seed, cursor=0):
    """The run's headlines, reporting calendar and generated statements."""
    market = _market(seed)
    market.ensure(cursor)
    return market.room


SECTOR_INDEX = {name: position for position, name in enumerate(SECTORS)}
ROSTER = [
    (company.beta, company.volatility, float(company.volume), SECTOR_INDEX[company.sector])
    for company in COMPANIES
]


def _paths(seed, room, first_session, carry):
    """One block of bars, continuing from the closing prices handed in.

    The factor model, the shock processes and the bar construction run in the
    engine (backend/engine/src/market.cpp); the random draws are numpy's own
    PCG64 stream for [seed, first_session, 0x9E3779B9], drawn in the same order.
    """
    cents, volume, closing = engine.generate_block(
        seed,
        first_session,
        ROSTER,
        len(SECTORS),
        [carry[company.symbol] for company in COMPANIES],
        room.shocks,
    )
    times = session_times(first_session, BLOCK_SESSIONS)
    session = first_session + np.arange(BLOCK_BARS) // SESSION_BARS
    output = {
        company.symbol: BarSeries(times, cents[position], volume[position], session)
        for position, company in enumerate(COMPANIES)
    }
    # The next block opens where this one closed, to the cent that was printed.
    return output, {
        company.symbol: float(closing[position]) for position, company in enumerate(COMPANIES)
    }


@lru_cache(maxsize=8)
def legacy_synthetic(seed):
    """The original six fictional paths. Preserved so existing runs replay unchanged.

    Each symbol draws from random.Random(seed + number * 100003), as it always
    has; the engine reproduces that stream and CPython's round(x, 2).
    """
    symbols = list(LEGACY_SYMBOLS)
    cents, volume = engine.legacy_paths(
        [seed + number * 100003 for number in range(len(symbols))],
        [float(initial) for _, initial in LEGACY_SYMBOLS.values()],
    )
    sessions = -(-LEGACY_BARS // SESSION_BARS)
    stamps, days = engine.session_calendar(0, sessions)
    stamps, days = stamps[:LEGACY_BARS], days[:LEGACY_BARS]
    times = stamps.tolist()
    output = EngineMarket()
    for position, symbol in enumerate(symbols):
        rows = cents[position].tolist()
        traded = volume[position].tolist()
        output[symbol] = [
            {
                "time": times[i],
                "open": rows[0][i] / 100,
                "high": rows[1][i] / 100,
                "low": rows[2][i] / 100,
                "close": rows[3][i] / 100,
                "volume": traded[i],
            }
            for i in range(LEGACY_BARS)
        ]
    output.engine_columns = [
        engine.Columns(time=stamps, day=days, cents=cents[position], volume_int=volume[position])
        for position in range(len(symbols))
    ]
    output.sessions = np.arange(LEGACY_BARS, dtype=np.int64) // SESSION_BARS
    return output


# Retained for callers of the previous name.
synthetic = legacy_synthetic


def legacy_buckets(data, symbol, start, stop, per_bucket):
    """Coarser bars for an original six-path run.

    Those charts stamp a bucket with the boundary it starts on, even when the
    window begins partway through it, so the engine is asked for aligned stamps.
    """
    if stop <= start:
        return []
    columns = data.engine_columns[list(data).index(symbol)]
    times, cents, volume = engine.aggregate(
        columns.cents,
        columns.volume_int,
        columns.time,
        data.sessions,
        start,
        stop,
        per_bucket,
        aligned=True,
    )
    return _bucket_rows(times, cents, volume)


# Imported datasets are immutable snapshots, so their engine columns are built
# once per dataset rather than once per request.
_IMPORTED = OrderedDict()
_IMPORTED_LOCK = threading.Lock()


def _imported(dataset_id, symbol, bars):
    with _IMPORTED_LOCK:
        cached = _IMPORTED.get(dataset_id)
        if cached is not None:
            _IMPORTED.move_to_end(dataset_id)
            return cached
    data = EngineMarket({symbol: bars})
    data.engine_columns = [engine.rows_columns(bars)]
    with _IMPORTED_LOCK:
        _IMPORTED[dataset_id] = data
        while len(_IMPORTED) > 8:
            _IMPORTED.popitem(last=False)
    return data


def markets(state, db):
    config = state["config"]
    if config["mode"] == "synthetic":
        if config.get("universe") == UNIVERSE_ID:
            # Generation follows the replay clock, so the market never runs out.
            return simulated_market(config["seed"], state["cursor"])
        return legacy_synthetic(config["seed"])
    dataset = db.get(TradingDataset, config["dataset_id"])
    if not dataset:
        raise HTTPException(503, "The run's historical data snapshot is unavailable.")
    return _imported(config["dataset_id"], config["symbol"], dataset.bars)
