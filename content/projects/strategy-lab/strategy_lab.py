"""Offline, synthetic multi-asset research lab. Python 3.10+, standard library only."""

import argparse
import csv
import hashlib
import json
import math
import platform
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

STRATEGIES = ("equal-weight", "value-quality", "momentum")


@dataclass(frozen=True)
class Config:
    initial_cash: float = 10000.0
    cost_bps: float = 20.0
    participation: float = 0.05
    top_n: int = 2
    target_cap: float = 0.4
    lookback: int = 5
    skip: int = 1
    max_filing_age_days: int = 180

    def validate(self):
        for field, lower, upper in (
            ("initial_cash", 1, 1e12),
            ("cost_bps", 0, 1000),
            ("participation", 0, 1),
            ("target_cap", 0, 1),
        ):
            value = getattr(self, field)
            if isinstance(value, bool) or not math.isfinite(value) or not lower <= value <= upper:
                raise ValueError(f"Invalid {field}")
        for field, lower, upper in (
            ("top_n", 1, 1000),
            ("lookback", 1, 10000),
            ("skip", 0, 10000),
            ("max_filing_age_days", 1, 3650),
        ):
            value = getattr(self, field)
            if type(value) is not int or not lower <= value <= upper:
                raise ValueError(f"Invalid {field}")


def number(raw, field, lower=-1e12, upper=1e12):
    try:
        value = float(raw)
    except (ValueError, TypeError) as error:
        raise ValueError(f"{field} must be numeric") from error
    if not math.isfinite(value) or not lower <= value <= upper:
        raise ValueError(f"{field} outside supported finite range")
    return value


def read_csv(path, fields):
    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != fields:
            raise ValueError(f"Expected CSV fields: {','.join(fields)}")
        rows = list(reader)
    if not rows or any(None in row or None in row.values() for row in rows):
        raise ValueError("CSV must contain complete rows")
    return rows


def load_inputs(prices_path, fundamentals_path):
    prices = read_csv(prices_path, ["date", "symbol", "open", "close", "volume"])
    sessions = {}
    previous = None
    for row in prices:
        day = date.fromisoformat(row["date"])
        symbol = row["symbol"]
        if not symbol.isascii() or not symbol.isalpha() or not symbol.isupper():
            raise ValueError("Symbols must be uppercase ASCII letters")
        key = (day, symbol)
        if previous is not None and key <= previous:
            raise ValueError("Price rows must be unique and sorted by date, symbol")
        previous = key
        volume = number(row["volume"], "volume", 0, 1e10)
        if not volume.is_integer():
            raise ValueError("Volume must be an integer")
        sessions.setdefault(day, {})[symbol] = {
            "open": number(row["open"], "open", 0.0001, 1e8),
            "close": number(row["close"], "close", 0.0001, 1e8),
            "volume": int(volume),
        }
    symbols = set(next(iter(sessions.values())))
    if len(sessions) < 3 or any(set(panel) != symbols for panel in sessions.values()):
        raise ValueError("Require at least three complete sessions; no missing-price fill model")
    filings = read_csv(
        fundamentals_path,
        [
            "symbol",
            "period_end",
            "available",
            "ncav_per_share",
            "earnings_yield",
            "roic",
            "coverage",
        ],
    )
    seen = set()
    for row in filings:
        row["period_end"] = date.fromisoformat(row["period_end"])
        row["available"] = date.fromisoformat(row["available"])
        key = (row["symbol"], row["period_end"], row["available"])
        if row["symbol"] not in symbols or key in seen or row["available"] < row["period_end"]:
            raise ValueError("Invalid or duplicate filing identity/dates")
        seen.add(key)
        for field in ("ncav_per_share", "earnings_yield", "roic", "coverage"):
            row[field] = number(row[field], field)
    return list(sessions.items()), filings


def available_filing(filings, symbol, decision_day, max_age):
    # Date-only fixture: releases first become usable on a later session.
    eligible = [
        row
        for row in filings
        if row["symbol"] == symbol
        and row["available"] < decision_day
        and row["period_end"] <= decision_day
    ]
    if not eligible:
        return None
    latest = max(eligible, key=lambda row: (row["period_end"], row["available"]))
    return latest if (decision_day - latest["period_end"]).days <= max_age else None


def rank_scores(sessions, filings, index, strategy, config):
    day, panel = sessions[index]
    if strategy == "equal-weight":
        return {symbol: 0.0 for symbol in panel}
    if strategy == "momentum":
        end = index - config.skip
        start = end - config.lookback
        if start < 0:
            return {}
        return {
            symbol: score
            for symbol in panel
            if (
                score := sessions[end][1][symbol]["close"] / sessions[start][1][symbol]["close"] - 1
            )
            > 0
        }
    if strategy != "value-quality":
        raise ValueError("Unknown strategy")
    candidates = {}
    for symbol, bar in panel.items():
        filing = available_filing(filings, symbol, day, config.max_filing_age_days)
        if (
            filing
            and filing["earnings_yield"] > 0
            and filing["roic"] > 0
            and filing["coverage"] >= 2
        ):
            if bar["close"] < filing["ncav_per_share"] * 2 / 3:
                candidates[symbol] = filing
    scores = {symbol: 0.0 for symbol in candidates}
    for field in ("earnings_yield", "roic"):
        for symbol in candidates:
            # Midranks give equal values equal scores; symbol breaks final selection ties.
            values = [row[field] for row in candidates.values()]
            value = candidates[symbol][field]
            scores[symbol] += (
                sum(v < value for v in values) + (sum(v == value for v in values) - 1) / 2
            )
    return scores


def targets(sessions, filings, index, strategy, config, equity):
    scores = rank_scores(sessions, filings, index, strategy, config)
    ranked = sorted(scores, key=lambda symbol: (-scores[symbol], symbol))
    chosen = ranked if strategy == "equal-weight" else ranked[: config.top_n]
    weight = min(1 / len(chosen), config.target_cap) if chosen else 0.0
    panel = sessions[index][1]
    quantities = {
        symbol: int(equity * weight / bar["close"]) if symbol in chosen else 0
        for symbol, bar in panel.items()
    }
    return quantities, scores


def fill_orders(cash, holdings, target, panel, prior_panel, config, signal_day, fill_day):
    events = []
    fee_rate = config.cost_bps / 10000
    # Stable symbol order is the disclosed priority when buys compete for cash.
    for selling in (True, False):
        for symbol in sorted(holdings):
            requested = target[symbol] - holdings[symbol]
            if requested == 0 or (requested < 0) != selling:
                continue
            price = panel[symbol]["open"]
            quantity = min(
                abs(requested), int(prior_panel[symbol]["volume"] * config.participation)
            )
            if selling:
                filled = -min(quantity, holdings[symbol])
            else:
                quantity = min(quantity, max(0, int(cash / (price * (1 + fee_rate)))))
                filled = quantity
            fee = abs(filled) * price * fee_rate
            cash -= filled * price + fee
            holdings[symbol] += filled
            if cash < -1e-7 or holdings[symbol] < 0 or not math.isfinite(cash):
                raise ValueError("Cash or holding invariant failed")
            cash = max(0.0, cash)
            events.append(
                {
                    "signal_date": signal_day.isoformat(),
                    "date": fill_day.isoformat(),
                    "symbol": symbol,
                    "requested": requested,
                    "filled": filled,
                    "unfilled": requested - filled,
                    "price": price,
                    "fee": fee,
                    "status": "filled"
                    if filled == requested
                    else "partial"
                    if filled
                    else "unfilled",
                }
            )
    return cash, events


def backtest(sessions, filings, strategy, start, end, config):
    config.validate()
    if strategy not in STRATEGIES or not 0 <= start < end < len(sessions):
        raise ValueError("Invalid strategy or sample bounds")
    cash = config.initial_cash
    holdings = dict.fromkeys(sessions[start][1], 0)
    benchmark = cash
    equity_rows = [{"date": sessions[start][0].isoformat(), "equity": cash, "benchmark": benchmark}]
    trades, signals, positions = [], [], []
    total_turnover = 0.0
    for index in range(start + 1, end + 1):
        decision_day, prior = sessions[index - 1]
        day, panel = sessions[index]
        decision_equity = cash + sum(holdings[s] * prior[s]["close"] for s in holdings)
        target, scores = targets(sessions, filings, index - 1, strategy, config, decision_equity)
        signals.extend(
            {
                "date": decision_day.isoformat(),
                "symbol": symbol,
                "score": scores.get(symbol),
                "target_shares": target[symbol],
            }
            for symbol in sorted(holdings)
        )
        cash, events = fill_orders(cash, holdings, target, panel, prior, config, decision_day, day)
        trades.extend(events)
        total_turnover += sum(abs(e["filled"]) * e["price"] for e in events) / decision_equity
        equity = cash + sum(holdings[s] * panel[s]["close"] for s in holdings)
        benchmark *= sum(panel[s]["close"] / prior[s]["close"] for s in holdings) / len(holdings)
        if not math.isfinite(equity) or equity <= 0 or not math.isfinite(benchmark):
            raise ValueError("Nonfinite or nonpositive portfolio valuation")
        equity_rows.append({"date": day.isoformat(), "equity": equity, "benchmark": benchmark})
        positions.append(
            {
                "date": day.isoformat(),
                "cash": cash,
                "equity": equity,
                **{f"shares_{s}": holdings[s] for s in sorted(holdings)},
                **{f"value_{s}": holdings[s] * panel[s]["close"] for s in sorted(holdings)},
            }
        )
    high = config.initial_cash
    drawdown = 0.0
    for row in equity_rows:
        high = max(high, row["equity"])
        drawdown = max(drawdown, 1 - row["equity"] / high)
    return {
        "strategy": strategy,
        "equity": equity_rows,
        "trades": trades,
        "signals": signals,
        "positions": positions,
        "metrics": {
            "total_return": equity_rows[-1]["equity"] / config.initial_cash - 1,
            "benchmark_return": benchmark / config.initial_cash - 1,
            "maximum_drawdown": drawdown,
            "fees": sum(t["fee"] for t in trades),
            "traded_notional_over_decision_equity": total_turnover,
            "fill_count": sum(t["filled"] != 0 for t in trades),
        },
    }


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def export_result(output, result, config, provenance, split, test_used_for_selection=False):
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "equity.csv", result["equity"], ["date", "equity", "benchmark"])
    for name, fields in (
        (
            "trades",
            [
                "signal_date",
                "date",
                "symbol",
                "requested",
                "filled",
                "unfilled",
                "price",
                "fee",
                "status",
            ],
        ),
        ("signals", ["date", "symbol", "score", "target_shares"]),
        ("positions", list(result["positions"][0])),
    ):
        write_csv(output / f"{name}.csv", result[name], fields)
    manifest = {
        "strategy": f"Synthetic Strategy Lab: {result['strategy']}",
        "source_version": f"strategy-lab-v1 sha256:{provenance['source_sha256']}",
        "data_source": "Supplied teaching fixture treated as synthetic; fixed universe, no actions or external flows; see input hashes",
        "benchmark": "Frictionless daily-rebalanced equal-weight close-to-close index on the same dates",
        "frequency": "Business-session closing valuations with initial decision-close cash",
        "periods_per_year": 252,
        "annual_risk_free": 0.0,
        "equity_basis": "net_of_modelled_costs",
        "cost_model": f"{config.cost_bps} bps per traded notional; prior-volume quantity cap {config.participation}; no impact, taxes, borrow or terminal liquidation",
        "evaluation_split": "synthetic",
        "research_segment": split,
        "selection_runs": len(STRATEGIES),
        "test_used_for_selection": test_used_for_selection,
        "hardware": platform.platform(),
        "build_flags": f"Python {platform.python_version()}, standard library",
        "config": asdict(config),
        "provenance": provenance,
        "sample": {
            "first_valuation": result["equity"][0]["date"],
            "last_valuation": result["equity"][-1]["date"],
        },
        "boundary_policy": "Reset to initial cash; earlier prices provide historical warm-up only",
        "timing": "Completed-close target, next-open fill; release dates strictly before decision dates",
        "unfilled_policy": "Remainder expires after one open; next close generates a new target",
        "cap_policy": "Target cap at decision close; gaps and subsequent drift can exceed it",
        "selection_disclosure": "Three validation candidates; two later stresses of the selected rule are diagnostics. Add external/manual trials to the ledger.",
    }
    for filename, value in (("manifest.json", manifest), ("metrics.json", result["metrics"])):
        (output / filename).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def run_research(sessions, filings, validation_start, test_start, config):
    if not (0 <= validation_start and validation_start + 4 <= test_start <= len(sessions) - 3):
        raise ValueError("Require at least three return intervals per validation/test segment")
    validation = [
        backtest(sessions, filings, s, validation_start, test_start - 1, config) for s in STRATEGIES
    ]
    # Candidate-order tie-break is fixed before evaluating the later segment.
    winner = max(validation, key=lambda result: result["metrics"]["total_return"])["strategy"]
    selected = backtest(sessions, filings, winner, test_start - 1, len(sessions) - 1, config)
    return validation, selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prices", default="prices.csv")
    parser.add_argument("--fundamentals", default="fundamentals.csv")
    parser.add_argument("--output", default="strategy-output")
    args = parser.parse_args()
    try:
        sessions, filings = load_inputs(args.prices, args.fundamentals)
        if len(sessions) < 30:
            raise ValueError("CLI requires at least 30 complete sessions")
        config = Config()
        validation_start = len(sessions) // 3
        test_start = len(sessions) * 2 // 3
        validation, selected = run_research(sessions, filings, validation_start, test_start, config)
        output = Path(args.output)
        if output.exists() and (not output.is_dir() or any(output.iterdir())):
            raise ValueError("Choose a new or empty output directory to preserve prior experiments")
        provenance = {
            "source_sha256": digest(__file__),
            "prices_sha256": digest(args.prices),
            "fundamentals_sha256": digest(args.fundamentals),
        }
        for result in validation:
            export_result(
                output / "validation" / result["strategy"], result, config, provenance, "validation"
            )
        export_result(output / "test", selected, config, provenance, "test")
        stresses = []
        for name, changes in (
            ("double-cost", {"cost_bps": config.cost_bps * 2}),
            ("tight-liquidity", {"participation": config.participation / 5}),
        ):
            stressed = Config(**{**asdict(config), **changes})
            result = backtest(
                sessions, filings, selected["strategy"], test_start - 1, len(sessions) - 1, stressed
            )
            export_result(output / "stress" / name, result, stressed, provenance, "test-stress")
            stresses.append({"name": name, "changed": changes, "metrics": result["metrics"]})
        ledger = {
            "synthetic": True,
            "selected_strategy": selected["strategy"],
            "selection_objective": "Maximum validation net total return; fixed candidate order breaks ties",
            "validation_start": sessions[validation_start][0].isoformat(),
            "test_first_return_date": sessions[test_start][0].isoformat(),
            "validation_trials": [
                {"strategy": r["strategy"], "metrics": r["metrics"]} for r in validation
            ],
            "selected_test": selected["metrics"],
            "post_selection_stresses": stresses,
            "additional_trials": "Record any manual modifications/repeated test inspection in research-notebook.md",
            "conclusion": "Synthetic engineering exercise; analyst interpretation and independent market evidence required",
        }
        (output / "experiments.json").write_text(
            json.dumps(ledger, indent=2, allow_nan=False) + "\n"
        )
    except (ValueError, OSError) as error:
        parser.exit(2, f"Strategy Lab input error: {error}\n")
    print(f"Selected on validation: {selected['strategy']}")
    print(f"Synthetic test return: {selected['metrics']['total_return']:.6%}")
    print(
        f"Research bundle: {output}; use test/equity.csv and test/manifest.json in the reporting course"
    )


if __name__ == "__main__":
    main()
