import math
import random
from datetime import datetime, timedelta
from functools import lru_cache
from zoneinfo import ZoneInfo

from fastapi import HTTPException

from quanta.db.models import TradingDataset

SYMBOLS = {
    "AAPL": ("Apple", 224),
    "MSFT": ("Microsoft", 418),
    "NVDA": ("NVIDIA", 128),
    "TSLA": ("Tesla", 245),
    "AMZN": ("Amazon", 195),
    "META": ("Meta Platforms", 530),
}


@lru_cache(maxsize=12)
def synthetic(seed):
    """Six fictional price paths, 6,000 minute observations, weekday-only calendar."""
    start = datetime(2025, 1, 6, 9, 30, tzinfo=ZoneInfo("America/New_York"))
    times = []
    date = start
    while len(times) < 6000:
        if date.weekday() < 5:
            times.extend(int((date + timedelta(minutes=i)).timestamp()) for i in range(390))
        date += timedelta(days=1)
    times = times[:6000]
    output = {}
    for number, (symbol, (_, initial)) in enumerate(SYMBOLS.items()):
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


def markets(state, db):
    config = state["config"]
    if config["mode"] == "synthetic":
        return synthetic(config["seed"])
    dataset = db.get(TradingDataset, config["dataset_id"])
    if not dataset:
        raise HTTPException(503, "The run's historical data snapshot is unavailable.")
    return {config["symbol"]: dataset.bars}
