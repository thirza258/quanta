from __future__ import annotations

import os
import time

from fastapi import HTTPException

from quanta.domain import analytics, broker
from quanta.domain.econometrics import FactorRequest, PortfolioRequest, factor_model, portfolio
from quanta.execution import runner
from quanta.services import data_store


def datasets():
    return {
        "datasets": data_store.catalog(),
        "note": "No historical market data is bundled. Synthetic scenarios are counterfactual illustrations, not reconstructions of named periods.",
    }


def generate(
    payload: analytics.DatasetParams,
):
    bars = analytics.generate(payload)
    return {
        "bars": bars,
        "params": payload.model_dump(),
        "provenance": "Synthetic · seeded stochastic model · weekday calendar (no holiday adjustment)",
    }


def execute(
    payload: analytics.ExecuteRequest,
):
    start = time.perf_counter()
    try:
        bars = (
            analytics.generate(payload.dataset_params)
            if payload.dataset_type == "synthetic"
            else data_store.historical(payload.dataset_params.symbol, payload.dataset_params.years)
        )
        output = runner.run(
            payload.code, analytics.strategy_data(bars, payload.dataset_params.window)
        )
        result = analytics.backtest(
            bars,
            output["signals"],
            payload.capital,
            payload.commission_bps,
            payload.slippage_bps,
        )
    except (ValueError, ArithmeticError) as error:
        raise HTTPException(422, str(error)) from None
    return {
        **result,
        "stdout": output.get("stdout", ""),
        "stderr": output.get("stderr", ""),
        "execution_ms": round((time.perf_counter() - start) * 1000, 1),
        "dataset_type": payload.dataset_type,
        "params": payload.dataset_params.model_dump(),
        "runtime": os.getenv("QUANTA_SANDBOX", "guided"),
    }


def valuation(payload: analytics.ValuationRequest):
    return analytics.valuation(payload)


def amm(payload: analytics.AmmRequest):
    return analytics.amm(payload)


def order(payload: broker.OrderRequest):
    return broker.place(payload)


def factors(
    payload: FactorRequest,
):
    try:
        return factor_model(payload)
    except ValueError as error:
        raise HTTPException(422, str(error)) from None


def optimize(
    payload: PortfolioRequest,
):
    try:
        return portfolio(payload)
    except ValueError as error:
        raise HTTPException(422, str(error)) from None
