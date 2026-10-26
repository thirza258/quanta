"""The C++ simulator engine, loaded through ctypes.

The trading simulator's computation lives in `backend/engine`: the generated
market, the execution engine and the desk's per-bar analytics. This module is
the only place Python touches it. It owns the library handle, the argument
types, and the conversion between the run state the API stores and the arrays
and JSON the engine reads.

Build the library with `make -C backend/engine` (`npm run setup` does). Set
QUANTA_ENGINE_LIB to load a library from somewhere else, and QUANTA_SIM_THREADS
to cap the worker threads one request may use; the default is the hardware's
count, up to eight.
"""

import ctypes
import json
import os
import sys
import threading
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

from quanta.domain.errors import DomainError

ABI_VERSION = 1
_NAME = "libquanta_sim.dylib" if sys.platform == "darwin" else "libquanta_sim.so"
LIBRARY = Path(__file__).resolve().parents[2] / "engine" / "build" / _NAME
EASTERN = ZoneInfo("America/New_York")
EPOCH_DAY = datetime(1970, 1, 1).date().toordinal()

_lock = threading.Lock()
_lib = None


class EngineError(RuntimeError):
    """The engine refused its input. This is a bug or corrupt state, never a learner error."""


class Company(ctypes.Structure):
    _fields_ = [
        ("beta", ctypes.c_double),
        ("volatility", ctypes.c_double),
        ("volume", ctypes.c_double),
        ("sector", ctypes.c_int32),
        ("reserved", ctypes.c_int32),
    ]


class Bars(ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_int64),
        ("cents", ctypes.c_void_p * 4),
        ("values", ctypes.c_void_p * 4),
        ("volume_int", ctypes.c_void_p),
        ("volume_float", ctypes.c_void_p),
        ("time", ctypes.c_void_p),
        ("day", ctypes.c_void_p),
    ]


_P = ctypes.c_void_p
_I32 = ctypes.c_int32
_I64 = ctypes.c_int64
_SIGNATURES = {
    "qs_abi_version": ([], ctypes.c_int),
    "qs_last_error": ([], ctypes.c_char_p),
    "qs_generate_block": (
        [ctypes.c_uint64, _I64, _P, _I32, _I32, _P, _P, _I64, _I32, _P, _P, _P],
        ctypes.c_int,
    ),
    "qs_session_calendar": ([_I64, _I64, _P, _P], ctypes.c_int),
    "qs_legacy_paths": ([_P, _P, _I32, _I32, _P, _P], ctypes.c_int),
    "qs_aggregate": (
        [_P, _P, _P, _P, _P, _P, _P, _I64, _I64, _I64, _I32, _I32, _P, _P, _P, _P, _P, _P, _P],
        ctypes.c_int,
    ),
    "qs_engine": (
        [
            ctypes.c_char_p,
            ctypes.c_size_t,
            _P,
            _I32,
            ctypes.POINTER(_P),
            ctypes.POINTER(ctypes.c_size_t),
        ],
        ctypes.c_int,
    ),
    "qs_free": ([_P], None),
    "qs_sma": ([_P, _I64, _I32, _P], ctypes.c_int),
    "qs_ema": ([_P, _I64, _I32, _P], ctypes.c_int),
    "qs_rsi": ([_P, _I64, _I32, _P], ctypes.c_int),
    "qs_macd": ([_P, _I64, _I32, _I32, _I32, _P, _P, _P], ctypes.c_int),
    "qs_mark_to_market": (
        [_I64, _P, ctypes.c_double, _I64, _P, _P, _I64, _P, _P, _P, _I32, _P, _I32, _P, _P, _P],
        ctypes.c_int,
    ),
    "qs_decimal": (
        [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t],
        ctypes.c_int,
    ),
    "qs_round_hundredths": ([ctypes.c_double, ctypes.POINTER(_I64)], ctypes.c_int),
    "qs_standard_normals": ([_P, _I32, _I64, _P], ctypes.c_int),
    "qs_python_random": ([ctypes.c_uint64, _I64, _P, _P, _P], ctypes.c_int),
}


def _load():
    path = Path(os.environ.get("QUANTA_ENGINE_LIB") or LIBRARY)
    if not path.exists():
        raise RuntimeError(
            f"The simulator engine is not built: {path} is missing. "
            "Run `make -C backend/engine` (or `npm run setup`)."
        )
    lib = ctypes.CDLL(str(path))
    for name, (arguments, result) in _SIGNATURES.items():
        function = getattr(lib, name)
        function.argtypes = arguments
        function.restype = result
    if lib.qs_abi_version() != ABI_VERSION:
        raise RuntimeError(
            f"{path} implements engine ABI {lib.qs_abi_version()}, but this API expects "
            f"{ABI_VERSION}. Rebuild it with `make -C backend/engine`."
        )
    return lib


def library():
    """The loaded engine. Loading is deferred so the rest of the API starts without it."""
    global _lib
    if _lib is None:
        with _lock:
            if _lib is None:
                _lib = _load()
    return _lib


def workers():
    try:
        return max(0, int(os.environ.get("QUANTA_SIM_THREADS", "0")))
    except ValueError:
        return 0


def check(code):
    if code == 0:
        return
    message = library().qs_last_error().decode()
    if code == 2:
        raise DomainError(message)
    raise EngineError(message)


def address(array):
    return array.ctypes.data if array is not None else None


# ---------------------------------------------------------------------------
# Generated market


def generate_block(seed, first_session, companies, sector_count, carry, shocks):
    """One block of bars: cents (company, 4, bar), volume (company, bar), next carry."""
    from quanta.services.simulator_market import BLOCK_BARS

    count = len(companies)
    roster = (Company * count)(*[Company(*company, 0) for company in companies])
    opening = np.ascontiguousarray(carry, dtype=np.float64)
    schedule = np.ascontiguousarray(np.asarray(shocks, dtype=np.int32).reshape(-1, 6))
    cents = np.empty((count, 4, BLOCK_BARS), dtype=np.int32)
    volume = np.empty((count, BLOCK_BARS), dtype=np.int32)
    closing = np.empty(count, dtype=np.float64)
    check(
        library().qs_generate_block(
            seed,
            first_session,
            ctypes.cast(roster, _P),
            count,
            sector_count,
            address(opening),
            address(schedule),
            len(schedule),
            workers(),
            address(cents),
            address(volume),
            address(closing),
        )
    )
    return cents, volume, closing


def session_calendar(first_session, sessions):
    """Minute stamps and New York calendar days for consecutive weekday sessions."""
    from quanta.services.simulator_market import SESSION_BARS

    time = np.empty(sessions * SESSION_BARS, dtype=np.int64)
    day = np.empty(sessions * SESSION_BARS, dtype=np.int32)
    check(library().qs_session_calendar(first_session, sessions, address(time), address(day)))
    return time, day


def legacy_paths(seeds, initial):
    count = len(seeds)
    seeds = np.ascontiguousarray(seeds, dtype=np.uint64)
    initial = np.ascontiguousarray(initial, dtype=np.float64)
    cents = np.empty((count, 4, 6000), dtype=np.int32)
    volume = np.empty((count, 6000), dtype=np.int32)
    check(
        library().qs_legacy_paths(
            address(seeds), address(initial), count, workers(), address(cents), address(volume)
        )
    )
    return cents, volume


def aggregate(cents, volume, time, session, start, stop, per_bucket, aligned=False):
    """Buckets of `per_bucket` minutes over [start, stop): time, OHLC cents, volume."""
    size = max(0, stop - start)
    out_time = np.empty(size, dtype=np.int64)
    out_cents = np.empty((4, size), dtype=np.int32)
    out_volume = np.empty(size, dtype=np.int64)
    count = ctypes.c_int64()
    rows = [cents[k] for k in range(4)]
    for row in rows:
        assert row.flags.c_contiguous and row.dtype == np.int32
    check(
        library().qs_aggregate(
            *(address(row) for row in rows),
            address(volume),
            address(time),
            address(session),
            len(time),
            start,
            stop,
            per_bucket,
            1 if aligned else 0,
            address(out_time),
            *(address(out_cents[k]) for k in range(4)),
            address(out_volume),
            ctypes.byref(count),
        )
    )
    n = count.value
    return out_time[:n], out_cents[:, :n], out_volume[:n]


# ---------------------------------------------------------------------------
# Market data handed to the execution engine


class Columns:
    """One symbol's bars in the layout the engine reads, kept alive with the arrays."""

    __slots__ = ("cents", "values", "volume_int", "volume_float", "time", "day", "length")

    def __init__(self, *, time, day, cents=None, values=None, volume_int=None, volume_float=None):
        self.time = np.ascontiguousarray(time, dtype=np.int64)
        self.day = np.ascontiguousarray(day, dtype=np.int32)
        self.cents = cents
        self.values = values
        self.volume_int = volume_int
        self.volume_float = volume_float
        self.length = len(self.time)

    def struct(self):
        bars = Bars()
        bars.length = self.length
        for k in range(4):
            bars.cents[k] = address(self.cents[k]) if self.cents is not None else None
            bars.values[k] = address(self.values[k]) if self.values is not None else None
        bars.volume_int = address(self.volume_int)
        bars.volume_float = address(self.volume_float)
        bars.time = address(self.time)
        bars.day = address(self.day)
        return bars


def calendar_day(stamp):
    """Days since 1970-01-01 of the New York date a timestamp falls on."""
    return datetime.fromtimestamp(stamp, EASTERN).date().toordinal() - EPOCH_DAY


def rows_columns(rows):
    """Columns for bars held as dictionaries: imported datasets and test fixtures.

    The engine reads each value as Decimal(str(value)) would, so ints and floats
    are both carried as floats; a float's shortest repr is what str() prints.
    """
    count = len(rows)
    values = np.empty((4, count), dtype=np.float64)
    for k, key in enumerate(("open", "high", "low", "close")):
        values[k] = [float(row[key]) for row in rows]
    times = np.array([int(row["time"]) for row in rows], dtype=np.int64)
    return Columns(
        time=times,
        day=[calendar_day(int(stamp)) for stamp in times],
        values=values,
        volume_float=np.array([float(row["volume"]) for row in rows], dtype=np.float64),
    )


def series_columns(series):
    """Columns for a generated BarSeries, without copying its arrays."""
    cents = series.cents
    if not cents.flags.c_contiguous or cents.dtype != np.int32:
        cents = np.ascontiguousarray(cents, dtype=np.int32)
    volume = np.ascontiguousarray(series.volume, dtype=np.int32)
    return Columns(time=series.time, day=series.day, cents=cents, volume_int=volume)


def market_columns(data):
    """Engine columns for every symbol in a run's market, in run order."""
    cached = getattr(data, "engine_columns", None)
    if cached is not None:
        return cached
    out = []
    for series in data.values():
        out.append(series_columns(series) if hasattr(series, "cents") else rows_columns(series))
    return out


def run(payload, columns):
    """One engine request as bytes, against these columns; the response as bytes."""
    structs = (Bars * max(1, len(columns)))(*[column.struct() for column in columns])
    response = _P()
    length = ctypes.c_size_t()
    lib = library()
    check(
        lib.qs_engine(
            payload,
            len(payload),
            ctypes.cast(structs, _P) if columns else None,
            len(columns),
            ctypes.byref(response),
            ctypes.byref(length),
        )
    )
    try:
        return ctypes.string_at(response, length.value)
    finally:
        lib.qs_free(response)


def call(request, data=None):
    """Run one engine request; `data` is the run's market, or None when no bar is read."""
    columns = market_columns(data) if data is not None else []
    request = dict(request, symbols=list(data) if data is not None else [])
    return json.loads(run(json.dumps(request, separators=(",", ":")).encode(), columns))


# ---------------------------------------------------------------------------
# Analytics


def _series(function, values, *parameters):
    values = np.ascontiguousarray(values, dtype=np.float64)
    out = np.empty(len(values), dtype=np.float64)
    check(function(address(values), len(values), *parameters, address(out)))
    return out


def sma(values, period):
    return _series(library().qs_sma, values, period)


def ema(values, period):
    return _series(library().qs_ema, values, period)


def rsi(values, period):
    return _series(library().qs_rsi, values, period)


def macd(values, fast, slow, signal):
    values = np.ascontiguousarray(values, dtype=np.float64)
    line, smoothed, histogram = (np.empty(len(values)) for _ in range(3))
    check(
        library().qs_macd(
            address(values),
            len(values),
            fast,
            slow,
            signal,
            address(line),
            address(smoothed),
            address(histogram),
        )
    )
    return line, smoothed, histogram


def mark_to_market(
    times, opening, cash_times, cash_values, fill_symbol, fill_quantity, fill_time, closes
):
    """Equity, gross exposure and the equal-weighted index level on every bar."""
    times = np.ascontiguousarray(times, dtype=np.int64)
    cash_times = np.ascontiguousarray(cash_times, dtype=np.int64)
    cash_values = np.ascontiguousarray(cash_values, dtype=np.float64)
    fill_symbol = np.ascontiguousarray(fill_symbol, dtype=np.int32)
    fill_quantity = np.ascontiguousarray(fill_quantity, dtype=np.int64)
    fill_time = np.ascontiguousarray(fill_time, dtype=np.int64)
    closes = [np.ascontiguousarray(row, dtype=np.float64) for row in closes]
    pointers = (_P * len(closes))(*[address(row) for row in closes])
    bars = len(times)
    equity, gross, level = (np.empty(bars) for _ in range(3))
    check(
        library().qs_mark_to_market(
            bars,
            address(times),
            float(opening),
            len(cash_times),
            address(cash_times),
            address(cash_values),
            len(fill_symbol),
            address(fill_symbol),
            address(fill_quantity),
            address(fill_time),
            len(closes),
            ctypes.cast(pointers, _P),
            workers(),
            address(equity),
            address(gross),
            address(level),
        )
    )
    return equity, gross, level
