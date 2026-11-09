"""One interface over every market-data source (PRD 8.4).

A strategy never knows where its bars came from. Each provider lists what it
offers, describes a dataset for provenance and returns OHLCV bars. Synthetic
data is a pure function of its parameters; imported history is a Parquet file
read through DuckDB, never silently replaced with generated data.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Protocol

from quanta.core.config import DATA_DIR
from quanta.domain.analytics import DatasetParams, generate
from quanta.domain.research.provenance import digest
from quanta.services import data_store

MODELS = {
    "gbm": "Geometric Brownian motion",
    "merton": "Merton jump-diffusion",
    "heston": "Heston stochastic volatility",
    "regime": "Markov regime switching",
}
SCENARIOS = {
    "custom": "Custom market",
    "pure_random_walk": "Pure random walk",
    "1929_crash": "Deflationary crash · 1929-inspired",
    "1970s_stagflation": "Stagflation · 1970s-inspired",
    "2008_liquidity_crisis": "Liquidity crisis · 2008-inspired",
    "flash_crash": "Crypto flash crash · −50%",
}


class MarketDataProvider(Protocol):
    kind: str

    def symbols(self) -> list[dict]: ...

    def describe(self, params: DatasetParams) -> dict: ...

    def bars(self, params: DatasetParams) -> list[dict]: ...


class SyntheticProvider:
    kind = "synthetic"

    def symbols(self) -> list[dict]:
        return [{"id": key, "label": label, "kind": "model"} for key, label in MODELS.items()] + [
            {"id": key, "label": label, "kind": "scenario"} for key, label in SCENARIOS.items()
        ]

    def describe(self, params: DatasetParams) -> dict:
        settings = params.model_dump(exclude={"symbol", "window"})
        label = (
            SCENARIOS[params.scenario]
            if params.scenario != "custom"
            else f"{MODELS[params.model]} (μ {params.mu:.0%}, σ {params.sigma:.0%})"
        )
        return {
            "kind": self.kind,
            "key": f"synthetic:{digest(settings)[:16]}",
            "label": f"{label} · seed {params.seed} · {params.years}y",
            "source": "Quanta seeded generator; weekday calendar, 252 sessions a year",
            "settings": settings,
        }

    def bars(self, params: DatasetParams) -> list[dict]:
        return generate(params)


class ParquetProvider:
    kind = "historical"

    def symbols(self) -> list[dict]:
        return [
            {"id": entry["symbol"], "label": entry["symbol"], "kind": "imported"}
            for entry in data_store.catalog()
        ]

    def describe(self, params: DatasetParams) -> dict:
        path = DATA_DIR / f"{params.symbol}.parquet"
        if not path.is_file():
            raise ValueError(f"No imported dataset named {params.symbol}.")
        stat = path.stat()
        return {
            "kind": self.kind,
            "key": f"historical:{params.symbol}",
            "label": f"{params.symbol} · imported · first {params.years}y",
            "source": "Locally imported OHLCV (Parquet via DuckDB); verify corporate actions and universe",
            "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "file_modified": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            "settings": {"symbol": params.symbol, "years": params.years},
        }

    def bars(self, params: DatasetParams) -> list[dict]:
        return data_store.historical(params.symbol, params.years)

    def full(self, symbol: str) -> list[dict]:
        return data_store.historical(symbol, 10**6)


PROVIDERS: dict[str, MarketDataProvider] = {
    "synthetic": SyntheticProvider(),
    "historical": ParquetProvider(),
}


def provider(kind: str) -> MarketDataProvider:
    return PROVIDERS[kind]
