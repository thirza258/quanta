"""One research run, from signals to the red-team verdict.

The service supplies `run_many`, which executes strategy jobs in the sandbox
(in parallel, results in submission order), and `progress`, which records how
far the run has got. Everything else here is deterministic: the same
specification and data give the same result, byte for byte.
"""

from __future__ import annotations

from typing import Callable

from quanta.domain.analytics import generate, strategy_data
from quanta.domain.research import diagnostics, redteam, robustness, validation
from quanta.domain.research.metrics import (
    compact_curve,
    evaluate,
    per_period_sharpe,
    risk_free_reference,
    yearly_pnl,
)
from quanta.domain.research.provenance import digest
from quanta.domain.research.spec import ExperimentSpec, expand_grid

MAX_TRADES = 1000
MAX_STDOUT = 4000

# run_many(jobs, on_done) -> results; each job is (data, params); each result is
# {"signals": [...], "stdout": str, "arity": int} or {"error": str}.
RunMany = Callable[[list[tuple[dict, dict]], Callable[[], None]], list[dict]]
Progress = Callable[[str, int, int], None]


class StrategyFailure(ValueError):
    """The learner's strategy could not run; the message is safe to show."""


def _row(key, label, metrics):
    return {"id": key, "label": label, "metrics": validation.subset(metrics)}


def execute(
    spec: ExperimentSpec,
    bars: list[dict],
    run_many: RunMany,
    progress: Progress,
    prior_trials: int = 0,
) -> dict:
    n = len(bars)
    window = spec.dataset.params.window
    configs = expand_grid(spec.strategy.parameters)
    base_index = configs.index(spec.strategy.base)
    code_seed = int(digest(spec.model_dump(mode="json"))[:8], 16)
    data = strategy_data(bars, window)
    cuts = diagnostics.cut_points(n)
    alternates = []
    if spec.dataset.kind == "synthetic":
        params = spec.dataset.params
        for k in range(1, spec.validation.seed_paths + 1):
            seed = (params.seed + k) % 2**32
            alternates.append((seed, generate(params.model_copy(update={"seed": seed}))))
    total = len(configs) + len(cuts) + len(alternates) + 4
    done = [0]

    def tick(stage):
        def step():
            done[0] += 1
            progress(stage, done[0], total)

        return step

    progress("strategies", 0, total)
    base = run_many([(data, spec.strategy.base)], tick("strategies"))[0]
    if "error" in base:
        raise StrategyFailure(base["error"])
    if spec.strategy.parameters and base.get("arity", 1) < 2:
        raise StrategyFailure(
            "strategy(data) ignores the parameter grid. Declare strategy(data, params) and read "
            'values such as params["fast"].'
        )
    jobs = [(strategy_data(bars[:k], window), spec.strategy.base) for k in cuts]
    others = [i for i in range(len(configs)) if i != base_index]
    jobs += [(data, configs[i]) for i in others]
    jobs += [(strategy_data(path, window), spec.strategy.base) for _, path in alternates]
    outputs = run_many(jobs, tick("strategies"))
    truncated = [
        {"bars": k, **({"error": o["error"]} if "error" in o else {"signals": o["signals"]})}
        for k, o in zip(cuts, outputs[: len(cuts)])
    ]
    signal_sets: list[list[bool] | None] = [None] * len(configs)
    signal_sets[base_index] = base["signals"]
    for i, output in zip(others, outputs[len(cuts) : len(cuts) + len(others)]):
        if "error" in output:
            raise StrategyFailure(f"Configuration {configs[i]} failed: {output['error']}")
        signal_sets[i] = output["signals"]
    path_signals = outputs[len(cuts) + len(others) :]
    for (seed, _), output in zip(alternates, path_signals):
        if "error" in output:
            raise StrategyFailure(f"The strategy failed on market seed {seed}: {output['error']}")

    costs = spec.costs
    lookahead = diagnostics.lookahead(bars, base["signals"], truncated)
    headline = evaluate(bars, base["signals"], costs)
    buy_hold = evaluate(bars, [True] * n, costs, prior_signal=True)
    trend = evaluate(bars, [c > s for c, s in zip(data["close"], data["sma_200"])], costs)

    progress("validation", done[0], total)
    split = validation.train_test(
        bars, signal_sets, configs, base_index, costs, spec.validation.split
    )
    walk = (
        validation.walk_forward(bars, signal_sets, configs, base_index, costs, spec.validation)
        if spec.validation.walk_forward
        else {"status": "skipped", "reason": "Walk-forward validation was switched off."}
    )
    done[0] += 1

    progress("robustness", done[0], total)
    evaluations = [
        headline if i == base_index else evaluate(bars, signal_sets[i], costs)
        for i in range(len(configs))
    ]
    grid = [e["metrics"] for e in evaluations]
    surface = robustness.surface(configs, grid, spec.strategy.parameters, base_index)
    stress = robustness.cost_stress(bars, base["signals"], costs)
    seeds = {
        "status": "skipped",
        "reason": "Historical data has a single path; rely on walk-forward.",
    }
    if spec.dataset.kind == "synthetic":
        seeds = {"status": "skipped", "reason": "Alternative paths were switched off."}
    if alternates:
        paths = []
        for (seed, path), output in zip(alternates, path_signals):
            paths.append(
                {
                    "seed": seed,
                    "strategy": validation.subset(
                        evaluate(path, output["signals"], costs)["metrics"]
                    ),
                    "benchmark": validation.subset(
                        evaluate(path, [True] * len(path), costs, prior_signal=True)["metrics"]
                    ),
                }
            )
        original = {
            "seed": spec.dataset.params.seed,
            "strategy": validation.subset(headline["metrics"]),
            "benchmark": validation.subset(buy_hold["metrics"]),
        }
        seeds = robustness.seed_dispersion(original, paths)
    done[0] += 1

    progress("diagnostics", done[0], total)
    trial_sharpes = [per_period_sharpe(e["returns"]) for e in evaluations]
    returns = [e["returns"] for e in evaluations]
    matrix = [list(row) for row in zip(*returns)]
    years = yearly_pnl(headline["result"], costs.capital)
    diagnostic = {
        "trials": {"run": len(configs), "strategy_configurations": prior_trials + len(configs)},
        # Every configuration tried for this strategy is a trial (Bailey & López de Prado
        # count all of them); the spread of Sharpe ratios comes from this run's grid.
        "deflated_sharpe": diagnostics.deflated_sharpe(
            headline["returns"], trial_sharpes, prior_trials + len(configs)
        ),
        "pbo": diagnostics.probability_of_overfitting(matrix),
        "random_timing": diagnostics.random_timing(
            bars,
            base["signals"],
            costs,
            headline["metrics"]["sharpe"],
            spec.validation.permutations,
            code_seed,
        ),
        "concentration": diagnostics.concentration(years),
    }
    done[0] += 1

    progress("red team", done[0], total)
    trades = headline["result"]["trades"]
    results = {
        "valid": lookahead["status"] == "pass",
        "seeds": {
            "dataset": spec.dataset.params.seed if spec.dataset.kind == "synthetic" else None,
            "random_timing": code_seed,
            "alternative_paths": [seed for seed, _ in alternates],
        },
        "dataset": {
            "bars": n,
            "start": bars[0]["time"],
            "end": bars[-1]["time"],
            "quality": diagnostics.data_quality(bars),
        },
        "configurations": configs,
        "base_index": base_index,
        "headline": {
            "params": spec.strategy.base,
            "metrics": headline["metrics"],
            "equity_curve": compact_curve(headline["result"]),
            "yearly": years,
            "trades": trades[:MAX_TRADES],
            "trades_total": len(trades),
            "stdout": base.get("stdout", "")[:MAX_STDOUT],
        },
        "benchmarks": {
            "rows": [
                _row("strategy", "Strategy", headline["metrics"]),
                _row("buy_hold", "Buy & hold (same asset)", buy_hold["metrics"]),
                _row("trend", "Trend baseline (close > 200-day average)", trend["metrics"]),
                _row("cash", "Cash at 3%", risk_free_reference(bars, costs.capital)),
            ],
        },
        "lookahead": lookahead,
        "validation": {"train_test": split, "walk_forward": walk},
        "robustness": {"surface": surface, "costs": stress, "seeds": seeds},
        "diagnostics": diagnostic,
    }
    checks = redteam.checks(results)
    results["redteam"] = {"checks": checks, "risk": redteam.risk(checks)}
    done[0] += 1
    progress("completed", done[0], total)
    return results
