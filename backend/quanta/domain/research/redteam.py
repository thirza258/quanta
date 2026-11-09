"""The research red team: checks that try to break a result, and what they add up to.

Each check reports `pass`, `warn` (with a `medium` or `high` severity),
`fail` or `skip`, a plain-language finding and the lesson that teaches it.
Research risk summarizes the checks; the research-quality score grades the
process instead (validation, robustness, documentation, reproduction), so a
carefully documented losing strategy can score well. Neither is a judgement
of whether to invest.
"""

from __future__ import annotations

import math

LESSONS = {
    "lookahead": "2.27",
    "oos": "4.22",
    "split": "4.29",
    "multiple_testing": "4.30",
    "overfitting": "4.30",
    "parameters": "14.8",
    "costs": "14.8",
    "sample": "10.10",
    "concentration": "12.10",
    "benchmark": "4.6",
    "timing": "4.6",
    "seeds": "14.8",
    "data": "12.11",
}
DSR_THRESHOLD = 0.95
PBO_THRESHOLD = 0.2
TIMING_ALPHA = 0.05
MIN_ROUND_TRIPS = 30
FEW_ROUND_TRIPS = 10
CONCENTRATION_LIMIT = 0.5
DECAY_LIMIT = 0.5


def _check(key, title, status, finding, severity=None, evidence=None):
    return {
        "id": key,
        "title": title,
        "status": status,
        "severity": severity if status == "warn" else None,
        "finding": finding,
        "evidence": evidence or {},
        "lesson": LESSONS.get(key),
    }


def _num(value, digits=2):
    return "undefined" if value is None or not math.isfinite(value) else f"{value:.{digits}f}"


def _pct(value, digits=0):
    return "undefined" if value is None else f"{value:.{digits}%}"


def checks(results: dict) -> list[dict]:
    out = []
    headline = results["headline"]["metrics"]
    look = results["lookahead"]
    if look["status"] == "pass":
        cuts = ", ".join(str(c["bars"]) for c in look["checks"])
        out.append(
            _check(
                "lookahead",
                "No look-ahead detected",
                "pass",
                f"Re-run on histories cut at {cuts} bars, the rule reproduced every earlier signal.",
            )
        )
    else:
        bad = next(c for c in look["checks"] if not c["match"])
        detail = (
            f"it failed on a history ending {bad['time']}: {bad['error']}"
            if bad.get("error")
            else f"its signal on {bad['first_difference']} changed when bars after {bad['time']} were removed"
        )
        out.append(
            _check(
                "lookahead",
                "Look-ahead detected",
                "fail",
                f"The rule uses information it could not have had: {detail}. "
                "Every other figure in this run is unreliable until it is fixed.",
                evidence={"checks": look["checks"]},
            )
        )

    wf = results["validation"]["walk_forward"]
    split = results["validation"]["train_test"]
    if wf["status"] == "completed":
        agg = wf["aggregate"]
        oos, ins = agg["out_of_sample"]["sharpe"], agg["mean_in_sample_sharpe"]
        evidence = {"in_sample_sharpe": ins, "out_of_sample_sharpe": oos, "decay": agg["decay"]}
        folds = len(wf["folds"])
        if oos is None or oos <= 0:
            out.append(
                _check(
                    "oos",
                    "No out-of-sample edge",
                    "warn",
                    f"Walk-forward selection across {folds} folds earned an out-of-sample Sharpe of "
                    f"{_num(oos)} (in-sample mean {_num(ins)}).",
                    "high" if ins is not None and ins > 0 else "medium",
                    evidence,
                )
            )
        elif agg["decay"] is not None and agg["decay"] > DECAY_LIMIT:
            out.append(
                _check(
                    "oos",
                    "Large in-sample to out-of-sample decay",
                    "warn",
                    f"Out-of-sample Sharpe {_num(oos)} kept only {_pct(1 - agg['decay'])} of the "
                    f"in-sample {_num(ins)} across {folds} folds.",
                    "medium",
                    evidence,
                )
            )
        else:
            out.append(
                _check(
                    "oos",
                    "Survives walk-forward validation",
                    "pass",
                    f"Out-of-sample Sharpe {_num(oos)} across {folds} folds "
                    f"(in-sample mean {_num(ins)}; {agg['positive_folds']} of {folds} folds positive).",
                    evidence=evidence,
                )
            )
    elif split["status"] == "completed":
        oos = split["selected"]["out_of_sample"]["sharpe"]
        status = "pass" if oos is not None and oos > 0 else "warn"
        out.append(
            _check(
                "split",
                "Holdout result" if status == "pass" else "No holdout edge",
                status,
                f"The best in-sample configuration scored a holdout Sharpe of {_num(oos)}. "
                f"Walk-forward was skipped: {wf['reason']}",
                "medium",
            )
        )
    else:
        out.append(
            _check(
                "oos",
                "Not validated out of sample",
                "warn",
                f"The dataset is too short for a holdout: {split['reason']}",
                "high",
            )
        )

    dsr = results["diagnostics"]["deflated_sharpe"]
    trials = results["diagnostics"]["trials"]
    if dsr["status"] == "completed":
        count, here = trials["strategy_configurations"], trials["run"]
        tried = f"{count} configurations" if count != 1 else "a single configuration"
        history = (
            f" ({here} in this run, {count - here} in earlier runs of this strategy)"
            if count > here
            else ""
        )
        finding = (
            f"Counting {tried}{history}, the deflated Sharpe ratio is {_pct(dsr['dsr'], 1)}: the "
            f"chance that this Sharpe ({_num(dsr['sharpe'])}) is more than the luckiest of "
            f"{count} skill-less tries would show (about {_num(dsr['expected_max_sharpe'])})."
        )
        status = "pass" if dsr["dsr"] >= DSR_THRESHOLD else "warn"
        out.append(
            _check(
                "multiple_testing",
                "Sharpe survives the number of trials"
                if status == "pass"
                else "Sharpe may be selection luck",
                status,
                finding,
                "high" if dsr["dsr"] < 0.5 else "medium",
                {"dsr": dsr["dsr"], "psr": dsr["psr"], "trials": count, "run_trials": here},
            )
        )
    else:
        out.append(_check("multiple_testing", "Deflated Sharpe ratio", "skip", dsr["reason"]))

    pbo = results["diagnostics"]["pbo"]
    if pbo["status"] == "completed":
        value = pbo["pbo"]
        out.append(
            _check(
                "overfitting",
                "Low probability of backtest overfitting"
                if value <= PBO_THRESHOLD
                else "Selection overfits",
                "pass" if value <= PBO_THRESHOLD else "warn",
                f"In {pbo['combinations']} combinatorial splits, the in-sample winner ranked at or below "
                f"the out-of-sample median {_pct(value)} of the time.",
                "high" if value >= 0.5 else "medium",
                {"pbo": value},
            )
        )
    else:
        out.append(
            _check("overfitting", "Probability of backtest overfitting", "skip", pbo["reason"])
        )

    stability = results["robustness"]["surface"]["stability"]
    kind = stability["class"]
    out.append(
        _check(
            "parameters",
            {
                "robust": "Robust to its parameters",
                "sensitive": "Sensitive to its parameters",
                "fragile": "Fragile parameter choice",
                "untested": "Parameter sensitivity untested",
                "no-edge": "No edge to test for robustness",
            }[kind],
            "pass" if kind == "robust" else "skip" if kind == "no-edge" else "warn",
            stability["reason"],
            "high" if kind == "fragile" else "medium",
            {"score": stability["score"]},
        )
    )

    stress = results["robustness"]["costs"]
    current = stress["current_bps"]
    if stress.get("break_even_bps") is not None:
        be = stress["break_even_bps"]
        if be <= current:
            status, severity, title = "warn", "high", "Costs consume the edge"
        elif be < max(2 * current, 10):
            status, severity, title = "warn", "medium", "Thin margin over costs"
        else:
            status, severity, title = "pass", None, "Survives higher costs"
        out.append(
            _check(
                "costs",
                title,
                status,
                f"Sharpe reaches zero at {be:.1f} bps per fill, against {current:.1f} bps assumed.",
                severity,
                {"break_even_bps": be, "current_bps": current},
            )
        )
    elif stress.get("break_even_above"):
        out.append(_check("costs", "Survives higher costs", "pass", stress["reason"]))
    else:
        out.append(_check("costs", "Cost stress", "skip", stress["reason"]))

    trips = headline["round_trips"]
    years = results["dataset"]["bars"] / 252
    if trips < MIN_ROUND_TRIPS or years < 3:
        reason = (
            "too few trades to tell skill from luck"
            if trips < MIN_ROUND_TRIPS
            else "too short a history to span more than one market regime"
        )
        out.append(
            _check(
                "sample",
                "Small sample",
                "warn",
                f"{trips} closed round trips over {years:.1f} years: {reason}.",
                "high" if trips < FEW_ROUND_TRIPS else "medium",
                {"round_trips": trips, "years": years},
            )
        )
    else:
        out.append(
            _check(
                "sample",
                "Adequate sample",
                "pass",
                f"{trips} closed round trips over {years:.1f} years.",
            )
        )

    conc = results["diagnostics"]["concentration"]
    if conc["status"] == "completed":
        share = conc["share"]
        out.append(
            _check(
                "concentration",
                f"Profit concentrated in {conc['best_year']}"
                if share > CONCENTRATION_LIMIT
                else "Profit spread across years",
                "warn" if share > CONCENTRATION_LIMIT else "pass",
                f"{conc['best_year']} contributed {_pct(share)} of net profit over {conc['years']} years.",
                "high" if share > 0.8 else "medium",
                {"share": share, "year": conc["best_year"]},
            )
        )
    else:
        out.append(_check("concentration", "Regime concentration", "skip", conc["reason"]))

    mine = headline["sharpe"]
    losers, compared = [], []
    for row in results["benchmarks"]["rows"][1:]:
        other = row["metrics"]["sharpe"]
        if row["id"] == "cash":
            # Sharpe is already excess of cash, so cash is the zero line.
            if mine is None or mine <= 0:
                losers.append(row["label"])
            continue
        compared.append(f"{row['label']} {_num(other)}")
        if mine is None or (other is not None and other >= mine):
            losers.append(row["label"])
    out.append(
        _check(
            "benchmark",
            "Beats its baselines" if not losers else "Does not beat a simple baseline",
            "pass" if not losers else "warn",
            f"Strategy Sharpe {_num(mine)} against {', '.join(compared)}; cash at 3% is the zero line."
            + (f" Not beaten: {', '.join(losers)}." if losers else ""),
            "high" if "Cash at 3%" in losers else "medium",
            {"not_beaten": losers},
        )
    )

    timing = results["diagnostics"]["random_timing"]
    if timing["status"] == "completed":
        p = timing["p_value"]
        out.append(
            _check(
                "timing",
                "Timing beats random entries"
                if p <= TIMING_ALPHA
                else "Timing indistinguishable from random",
                "pass" if p <= TIMING_ALPHA else "warn",
                f"Against {timing['permutations']} random re-timings with the same exposure, p = {p:.3f}.",
                "high" if p > 0.5 else "medium",
                {"p_value": p},
            )
        )
    else:
        out.append(_check("timing", "Random-timing test", "skip", timing["reason"]))

    seeds = results["robustness"]["seeds"]
    if seeds["status"] == "completed":
        share = seeds["beats_benchmark_share"]
        flattering = seeds["original_beats_benchmark"] and share < 0.4
        ok = share >= 0.6 and (seeds["mean_sharpe"] or 0) > 0
        out.append(
            _check(
                "seeds",
                "Holds on other market paths" if ok else "Depends on this market path",
                "pass" if ok else "warn",
                f"On {len(seeds['paths'])} other draws of the same market, it beat buy-and-hold "
                f"{_pct(share)} of the time (mean Sharpe {_num(seeds['mean_sharpe'])}).",
                "high" if flattering else "medium",
            )
        )
    else:
        out.append(_check("seeds", "Alternative market paths", "skip", seeds["reason"]))

    quality = results["dataset"]["quality"]
    out.append(
        _check(
            "data",
            "Dataset integrity" if not quality["issues"] else "Dataset integrity issues",
            "pass" if not quality["issues"] else "warn",
            "All integrity checks passed."
            if not quality["issues"]
            else "; ".join(c["detail"] for c in quality["checks"] if c["status"] == "warn") + ".",
            "medium",
        )
    )
    return out


def risk(items: list[dict]) -> dict:
    warns = [c for c in items if c["status"] == "warn"]
    high = [c for c in warns if c["severity"] == "high"]
    failed = [c for c in items if c["status"] == "fail"]
    if failed or len(high) >= 2 or len(warns) >= 5:
        level = "HIGH"
    elif warns:
        level = "MEDIUM"
    else:
        level = "LOW"
    return {
        "level": level,
        "passed": sum(1 for c in items if c["status"] == "pass"),
        "warnings": len(warns),
        "high": len(high),
        "failed": len(failed),
        "skipped": sum(1 for c in items if c["status"] == "skip"),
    }


def quality(results: dict | None, notebook: dict, reproduction: dict | None) -> dict:
    """Research-quality score: how thoroughly the claim was tested and recorded (0-100)."""
    components = []

    def add(key, label, weight, score, note):
        components.append(
            {
                "id": key,
                "label": label,
                "weight": weight,
                "score": round(max(0, min(100, score))),
                "note": note,
            }
        )

    if results is None:
        return {"score": None, "components": []}
    verdict = (reproduction or {}).get("verdict")
    add(
        "reproducibility",
        "Reproducibility",
        15,
        100 if verdict == "identical" else 85 if verdict == "equivalent" else 50,
        "A rerun matched exactly."
        if verdict == "identical"
        else "A rerun matched within tolerance."
        if verdict == "equivalent"
        else "A rerun did not match; see the comparison."
        if verdict == "different"
        else "Inputs are pinned; rerun it to prove the result reproduces.",
    )
    wf, split = results["validation"]["walk_forward"], results["validation"]["train_test"]
    folds = len(wf["folds"]) if wf["status"] == "completed" else 0
    add(
        "validation",
        "Out-of-sample validation",
        20,
        100 if folds >= 3 else 80 if folds == 2 else 50 if split["status"] == "completed" else 0,
        f"Walk-forward with {folds} folds."
        if folds
        else "Holdout split only."
        if split["status"] == "completed"
        else "No out-of-sample test.",
    )
    costs = results["robustness"]["costs"]
    add(
        "costs",
        "Cost testing",
        10,
        100 if costs["levels"] else 0,
        f"Stressed from 0 to {costs['levels'][-1]['cost_bps']} bps per fill.",
    )
    configurations = results["robustness"]["surface"]["configurations"]
    seeds = results["robustness"]["seeds"]
    robustness = (
        100
        if configurations >= 9
        else 60
        if configurations >= 3
        else 30
        if configurations == 2
        else 0
    )
    if seeds["status"] == "completed":
        robustness = min(100, robustness + 20)
    add(
        "robustness",
        "Robustness",
        15,
        robustness,
        f"{configurations} configurations"
        + (
            f" and {len(seeds['paths'])} alternative paths."
            if seeds["status"] == "completed"
            else "."
        ),
    )
    lookahead_ok = results["lookahead"]["status"] == "pass"
    issues = results["dataset"]["quality"]["issues"]
    add(
        "bias",
        "Bias controls",
        15,
        (100 if lookahead_ok else 0) - min(40, 20 * issues),
        ("Look-ahead test passed" if lookahead_ok else "Look-ahead test failed")
        + (f"; {issues} data-integrity issues." if issues else "."),
    )
    trips = results["headline"]["metrics"]["round_trips"]
    years = results["dataset"]["bars"] / 252
    add(
        "sample",
        "Sample size",
        10,
        (min(1, trips / MIN_ROUND_TRIPS) + min(1, years / 5)) * 50,
        f"{trips} round trips over {years:.1f} years.",
    )
    written = [
        notebook.get("hypothesis"),
        notebook.get("conclusion"),
        notebook.get("limitations"),
        notebook.get("decision"),
    ]
    documentation = (
        (40 if written[0] else 0)
        + (30 if written[1] else 0)
        + (20 if written[2] else 0)
        + (10 if written[3] else 0)
    )
    add(
        "documentation",
        "Documentation",
        15,
        documentation,
        "Hypothesis registered before results"
        + ("; conclusion" if written[1] else "")
        + ("; limitations" if written[2] else "")
        + ("; decision" if written[3] else "")
        + ".",
    )
    total = sum(c["weight"] for c in components)
    score = sum(c["score"] * c["weight"] for c in components) / total
    return {"score": round(score), "components": components}
