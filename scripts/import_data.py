"""Usage: backend/.venv/bin/python scripts/import_data.py data.csv SYMBOL.
CSV columns: time (ISO date), open, high, low, close, volume.
Supply properly adjusted, licensed data; import does not infer survivorship coverage.
"""

import argparse
import re
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from quanta.data_store import DATA_DIR

parser = argparse.ArgumentParser()
parser.add_argument("csv", type=Path)
parser.add_argument("symbol")
args = parser.parse_args()
if not re.fullmatch(r"[A-Z0-9.-]{1,12}", args.symbol):
    parser.error("Use an uppercase symbol of at most 12 characters.")
frame = pd.read_csv(args.csv)
columns = ["time", "open", "high", "low", "close", "volume"]
if set(columns) - set(frame):
    parser.error("Missing required OHLCV columns.")
frame = frame[columns].copy()
frame["time"] = pd.to_datetime(frame["time"], format="%Y-%m-%d", errors="raise").dt.date
if frame["time"].duplicated().any():
    parser.error("Duplicate dates are not allowed.")
for col in columns[1:]:
    frame[col] = pd.to_numeric(frame[col], errors="raise")
if not np.isfinite(frame[columns[1:]].to_numpy()).all():
    parser.error("Values must be finite.")
if (frame[columns[1:-1]] <= 0).any().any() or (frame.volume < 0).any():
    parser.error("Prices must be positive and volume nonnegative.")
if (
    (frame.high < frame[["open", "close", "low"]].max(axis=1))
    | (frame.low > frame[["open", "close", "high"]].min(axis=1))
).any():
    parser.error("OHLC bounds are inconsistent.")
if len(frame) < 2:
    parser.error("Supply at least two observations.")
frame = frame.sort_values("time")
DATA_DIR.mkdir(parents=True, exist_ok=True)
target = DATA_DIR / f"{args.symbol}.parquet"
if target.exists():
    parser.error("Dataset exists. Choose another symbol or explicitly remove the old import.")
with duckdb.connect() as db:
    db.register("source_frame", frame)
    db.execute("COPY source_frame TO ? (FORMAT PARQUET)", [str(target)])
print(f"Imported {len(frame)} bars to {target}")
