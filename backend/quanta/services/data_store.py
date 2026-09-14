"""Local historical data registry. No generated dataset is labeled historical."""

import duckdb

from quanta.core.config import DATA_DIR


def catalog():
    return [
        {
            "symbol": p.stem,
            "type": "real",
            "source": "Locally imported OHLCV; verify corporate actions and universe coverage",
        }
        for p in sorted(DATA_DIR.glob("*.parquet"))
    ]


def historical(symbol: str | None, years: int):
    if not symbol or symbol not in {d["symbol"] for d in catalog()}:
        raise ValueError(
            "No imported historical dataset matches this symbol. Import a licensed CSV using backend/scripts/import_data.py."
        )
    path = DATA_DIR / f"{symbol}.parquet"
    with duckdb.connect() as db:
        rows = db.execute(
            "SELECT time, open, high, low, close, volume FROM read_parquet(?) ORDER BY time LIMIT ?",
            [str(path), years * 252],
        ).fetchall()
    if len(rows) < 2:
        raise ValueError("Dataset requires at least two bars.")
    return [
        dict(zip(("time", "open", "high", "low", "close", "volume"), (str(r[0]), *r[1:])))
        for r in rows
    ]
