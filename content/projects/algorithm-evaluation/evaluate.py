"""Original Quanta descriptive evaluation/report project; no strategy optimization."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import random
import statistics
import sys
from datetime import date
from pathlib import Path


def finite(value, name):
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number")
    try:
        number = float(value)
    except (ValueError, TypeError) as error:
        raise ValueError(f"{name} must be a finite number") from error
    if not math.isfinite(number):
        raise ValueError(f"{name} must be a finite number")
    return number


def load_manifest(path):
    manifest = json.loads(Path(path).read_text())
    if not isinstance(manifest, dict):
        raise ValueError("Manifest must be an object")
    for field in (
        "strategy",
        "source_version",
        "data_source",
        "benchmark",
        "frequency",
        "cost_model",
        "hardware",
        "build_flags",
    ):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            raise ValueError(f"Manifest requires {field}")
    periods = manifest.get("periods_per_year")
    if type(periods) is not int or not 1 <= periods <= 1000000:
        raise ValueError("periods_per_year must be an integer from 1 to 1000000")
    rate = finite(manifest.get("annual_risk_free"), "annual_risk_free")
    if not -1 < rate < 1:
        raise ValueError("annual_risk_free must be between -1 and 1")
    manifest["annual_risk_free"] = rate
    if manifest.get("equity_basis") != "net_of_modelled_costs":
        raise ValueError("Supply equity already net_of_modelled_costs; do not subtract costs twice")
    if manifest.get("evaluation_split") not in ("train", "validation", "test", "synthetic"):
        raise ValueError("Declare evaluation_split as train, validation, test, or synthetic")
    if type(manifest.get("selection_runs")) is not int or manifest["selection_runs"] < 1:
        raise ValueError("selection_runs must disclose at least one tried configuration")
    if type(manifest.get("test_used_for_selection")) is not bool:
        raise ValueError("Declare test_used_for_selection explicitly")
    return manifest


def load_equity(path):
    rows = []
    with Path(path).open(newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["date", "equity", "benchmark"]:
            raise ValueError("Equity CSV header must be date,equity,benchmark")
        for index, row in enumerate(reader, 2):
            if len(rows) >= 100000 or None in row:
                raise ValueError(f"Invalid or excessive equity rows at line {index}")
            try:
                day = date.fromisoformat(row["date"])
            except (ValueError, TypeError) as error:
                raise ValueError(f"Invalid date on line {index}") from error
            equity = finite(row["equity"], f"equity line {index}")
            benchmark = finite(row["benchmark"], f"benchmark line {index}")
            if equity <= 0 or benchmark <= 0:
                raise ValueError(
                    "Nonpositive equity needs an insolvency/return convention; never drop it silently"
                )
            if rows and day <= rows[-1]["date"]:
                raise ValueError(
                    "Dates must be unique and strictly increasing; input is not silently sorted"
                )
            rows.append({"date": day, "equity": equity, "benchmark": benchmark})
    if len(rows) < 3:
        raise ValueError("Supply an initial valuation and at least two return observations")
    return rows


def load_timings(path):
    rows, seen = [], set()
    with Path(path).open(newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["repeat", "serial_ms", "parallel_ms"]:
            raise ValueError("Timing CSV header must be repeat,serial_ms,parallel_ms")
        for row in reader:
            if None in row or len(rows) >= 10000:
                raise ValueError("Invalid or excessive timing records")
            identifier = row["repeat"]
            if not identifier or identifier in seen:
                raise ValueError("Timing repeat IDs must be nonempty and unique")
            seen.add(identifier)
            serial = finite(row["serial_ms"], "serial_ms")
            parallel = finite(row["parallel_ms"], "parallel_ms")
            if min(serial, parallel) <= 0:
                raise ValueError("Elapsed times must be positive")
            rows.append((serial, parallel))
    if len(rows) < 3:
        raise ValueError("At least three paired repetitions are required")
    serial = [row[0] for row in rows]
    parallel = [row[1] for row in rows]
    return {
        "repetitions": len(rows),
        "median_serial_ms": statistics.median(serial),
        "median_parallel_ms": statistics.median(parallel),
        "median_paired_speedup": statistics.median(a / b for a, b in rows),
        "parallel_min_ms": min(parallel),
        "parallel_max_ms": max(parallel),
    }


def drawdowns(values):
    peak = values[0]
    result = []
    for value in values:
        peak = max(peak, value)
        result.append(value / peak - 1)
    return result


def block_interval(values, block=3, repetitions=1000, seed=42):
    """Circular block bootstrap of mean periodic active return; not selection-adjusted."""
    if len(values) < 6:
        return None
    if not 1 <= block <= len(values) or not 100 <= repetitions <= 10000:
        raise ValueError("Invalid bootstrap block length or repetition count")
    rng = random.Random(seed)
    means = []
    for _ in range(repetitions):
        sample = []
        while len(sample) < len(values):
            start = rng.randrange(len(values))
            sample.extend(values[(start + j) % len(values)] for j in range(block))
        means.append(statistics.mean(sample[: len(values)]))
    means.sort()
    return [means[int(0.025 * (repetitions - 1))], means[int(0.975 * (repetitions - 1))]]


def evaluate(rows, manifest):
    equity = [row["equity"] for row in rows]
    benchmark = [row["benchmark"] for row in rows]
    returns = [b / a - 1 for a, b in zip(equity, equity[1:])]
    reference = [b / a - 1 for a, b in zip(benchmark, benchmark[1:])]
    if any(not math.isfinite(value) for value in returns + reference):
        raise ValueError("Return overflow: review valuation units before computing statistics")
    periods = manifest["periods_per_year"]
    rf = (1 + manifest["annual_risk_free"]) ** (1 / periods) - 1
    excess = [value - rf for value in returns]
    active = [a - b for a, b in zip(returns, reference)]
    sd = statistics.stdev(returns)
    tracking = statistics.stdev(active)
    downside = math.sqrt(sum(min(value, 0) ** 2 for value in excess) / len(excess))
    total = equity[-1] / equity[0] - 1
    benchmark_total = benchmark[-1] / benchmark[0] - 1
    metrics = {
        "observations": len(returns),
        "total_return": total,
        "benchmark_total_return": benchmark_total,
        "cumulative_return_difference": total - benchmark_total,
        "annualized_geometric_return": (1 + total) ** (periods / len(returns)) - 1
        if len(returns) >= periods
        else None,
        "annualized_volatility": sd * math.sqrt(periods),
        "sharpe": statistics.mean(excess) / sd * math.sqrt(periods) if sd > 0 else None,
        "sortino": statistics.mean(excess) / downside * math.sqrt(periods)
        if downside > 0
        else None,
        "maximum_drawdown": -min(drawdowns(equity)),
        "annualized_tracking_error": tracking * math.sqrt(periods),
        "information_ratio": statistics.mean(active) / tracking * math.sqrt(periods)
        if tracking > 0
        else None,
        "mean_periodic_active_return": statistics.mean(active),
        "active_mean_block_interval": block_interval(active),
    }
    warnings = [
        "Descriptive evaluation only; no automatic deploy/approve decision.",
        "Inputs must be aligned, regular valuation periods with no external deposits or withdrawals; calendar completeness is reviewed by the author.",
        "Equity is already net of the declared modelled costs; costs are not subtracted again.",
        "Annualization assumes the declared period frequency; serial dependence can invalidate simple square-root scaling.",
        "The 95% circular-block bootstrap interval uses block=3, repetitions=1000, seed=42; it does not correct selection bias or establish future performance.",
        "Dataset and split labels are author declarations, not independently certified provenance.",
    ]
    if len(returns) < 60:
        warnings.append(
            "Fewer than 60 return observations: estimates and bootstrap intervals are particularly unstable."
        )
    if manifest["test_used_for_selection"]:
        warnings.append(
            "The test period was used for selection and cannot be presented as untouched out-of-sample evidence."
        )
    if manifest["evaluation_split"] == "synthetic":
        warnings.append(
            "Synthetic fixture: these returns are a reporting demonstration, not investment evidence."
        )
    for value in metrics.values():
        numbers = value if isinstance(value, list) else [value]
        if any(number is not None and not math.isfinite(number) for number in numbers):
            raise ValueError("Metric overflow: review input units and annualization")
    return {"metrics": metrics, "warnings": warnings, "manifest": manifest}


LABELS = {
    "observations": ("Return observations (initial valuation excluded)", "count"),
    "total_return": ("Strategy total return, net of modelled costs", "percent"),
    "benchmark_total_return": ("Benchmark total return", "percent"),
    "cumulative_return_difference": (
        "Cumulative return difference (percentage points; not alpha)",
        "points",
    ),
    "annualized_geometric_return": (
        "Geometric annualized return (only with ≥1 declared year)",
        "percent",
    ),
    "annualized_volatility": ("Annualized sample volatility", "percent"),
    "sharpe": ("Sharpe (declared risk-free rate)", "ratio"),
    "sortino": ("Sortino (RMS downside over all periods)", "ratio"),
    "maximum_drawdown": ("Maximum drawdown magnitude (includes initial capital)", "percent"),
    "annualized_tracking_error": ("Annualized sample tracking error", "percent"),
    "information_ratio": ("Information ratio", "ratio"),
    "mean_periodic_active_return": ("Mean periodic active return", "percent"),
    "active_mean_block_interval": (
        "Descriptive 95% block interval, mean periodic active return",
        "interval",
    ),
}


def format_metric(value, kind):
    if value is None:
        return "Not defined / insufficient history"
    if kind == "interval":
        return f"[{value[0] * 100:.3f}%, {value[1] * 100:.3f}%]"
    if kind == "percent":
        return f"{value * 100:.3f}%"
    if kind == "points":
        return f"{value * 100:.3f} pp"
    if kind == "count":
        return str(value)
    return f"{value:.4f}"


def chart(rows, output):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"svg.hashsalt": "quanta-report", "font.family": "DejaVu Sans"})
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True, layout="constrained")
    dates = [row["date"] for row in rows]
    for field, label, color in (
        ("equity", "Strategy · net", "#245c4b"),
        ("benchmark", "Benchmark", "#6863a6"),
    ):
        values = [row[field] for row in rows]
        axes[0].plot(
            dates,
            [100 * value / values[0] for value in values],
            label=label,
            color=color,
            linewidth=2,
        )
        axes[1].plot(
            dates,
            [100 * value for value in drawdowns(values)],
            label=label,
            color=color,
            linewidth=2,
        )
    axes[0].set_ylabel("Wealth index · initial = 100")
    axes[0].set_title("Aligned strategy and benchmark valuations")
    axes[1].set_ylabel("Drawdown (%)")
    axes[1].set_xlabel("Valuation date")
    axes[1].axhline(0, color="#999999", linewidth=0.7)
    for axis in axes:
        axis.legend(loc="best")
        axis.grid(alpha=0.2)
    fig.savefig(output / "evaluation.svg", metadata={"Date": None})
    fig.savefig(output / "evaluation.png", dpi=160)
    plt.close(fig)


def write_reports(report, output, with_charts):
    table = [
        (label, format_metric(report["metrics"][key], kind))
        for key, (label, kind) in LABELS.items()
    ]
    title = f"Algorithm evaluation: {report['manifest']['strategy']}"
    # User text goes through HTML escaping; Markdown metacharacters are not used
    # as executable HTML in the generated HTML report.
    manifest_text = json.dumps(report["manifest"], indent=2, ensure_ascii=False)
    hashes = json.dumps(report["sha256"], indent=2)
    timing = json.dumps(report.get("timings", {"status": "No timing CSV supplied"}), indent=2)
    draft = "REVIEW REQUIRED: state the hypothesis, strongest evidence, failed checks, uncertainty, decision (reject/revise/paper study), and the next falsification test. Numerical output does not complete the analyst's conclusion."
    markdown = (
        "# "
        + html.escape(title.replace("\n", " "))
        + "\n\n"
        + draft
        + "\n\n## Metrics\n\n| Measure | Value |\n| --- | --- |\n"
    )
    markdown += "\n".join(f"| {label} | {value} |" for label, value in table)
    if with_charts:
        markdown += "\n\n![Aligned wealth and drawdown](evaluation.png)"
    markdown += "\n\n## Interpretation limits\n\n" + "\n".join(
        "- " + warning for warning in report["warnings"]
    )
    for heading, text in (
        ("Evaluation period", json.dumps(report.get("period", {}), indent=2)),
        ("Declared experiment", manifest_text),
        ("Report runtime", json.dumps(report.get("runtime", {}), indent=2)),
        ("Paired runtime summary (milliseconds)", timing),
        ("Input and evaluator SHA-256", hashes),
    ):
        markdown += f"\n\n## {heading}\n\n```json\n{text}\n```\n"
    markdown += "\n## References\n\n- [CFA Institute: performance evaluation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-performance-evaluation)\n- [Bailey et al.: probability of backtest overfitting](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf)\n- [Matplotlib figure export](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)\n"
    (output / "report.md").write_text(markdown)
    esc = html.escape
    body = f"<h1>{esc(title)}</h1><p class='review'>{esc(draft)}</p><h2>Metrics</h2><table><thead><tr><th>Measure</th><th>Value</th></tr></thead><tbody>"
    body += (
        "".join(f"<tr><td>{esc(label)}</td><td>{esc(value)}</td></tr>" for label, value in table)
        + "</tbody></table>"
    )
    if with_charts:
        body += "<figure><img src='evaluation.svg' alt='Strategy and benchmark wealth indexed to 100, with drawdowns including initial capital'><figcaption>Common dates and scales; inspect the full path, including losses.</figcaption></figure>"
    body += (
        "<h2>Interpretation limits</h2><ul>"
        + "".join(f"<li>{esc(warning)}</li>" for warning in report["warnings"])
        + "</ul>"
    )
    for heading, text in (
        ("Evaluation period", json.dumps(report.get("period", {}), indent=2)),
        ("Declared experiment", manifest_text),
        ("Report runtime", json.dumps(report.get("runtime", {}), indent=2)),
        ("Paired runtime summary (milliseconds)", timing),
        ("Input and evaluator SHA-256", hashes),
    ):
        body += f"<h2>{esc(heading)}</h2><pre>{esc(text)}</pre>"
    body += "<h2>References</h2><p><a href='https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-performance-evaluation'>CFA Institute: performance evaluation</a> · <a href='https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf'>Bailey et al.: backtest overfitting</a> · <a href='https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html'>Matplotlib</a></p>"
    style = "body{max-width:1000px;margin:40px auto;padding:0 24px;font:16px/1.7 system-ui;color:#243d35}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ddd;text-align:left;padding:10px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f6f4;padding:18px}img{max-width:100%;height:auto}figure{margin:28px 0}.review{background:#fff5d6;padding:20px}@media print{body{margin:0}pre,table{font-size:11px}}"
    (output / "report.html").write_text(
        f"<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(title)}</title><style>{style}</style><body>{body}</body></html>"
    )
    (output / "metrics.json").write_text(
        json.dumps(report, indent=2, allow_nan=False, ensure_ascii=False) + "\n"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--equity", default="equity.example.csv")
    parser.add_argument("--manifest", default="manifest.example.json")
    parser.add_argument("--timings", help="Optional paired timing CSV; sample: timings.example.csv")
    parser.add_argument("--out", default="report-output")
    parser.add_argument(
        "--no-charts",
        action="store_true",
        help="Generate tables and reports using only the Python standard library",
    )
    args = parser.parse_args(argv)
    try:
        manifest = load_manifest(args.manifest)
        rows = load_equity(args.equity)
        report = evaluate(rows, manifest)
        inputs = {
            "equity": Path(args.equity),
            "manifest": Path(args.manifest),
            "evaluator": Path(__file__),
        }
        if args.timings:
            report["timings"] = load_timings(args.timings)
            inputs["timings"] = Path(args.timings)
        report["sha256"] = {
            name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in inputs.items()
        }
        report["period"] = {
            "start": rows[0]["date"].isoformat(),
            "end": rows[-1]["date"].isoformat(),
        }
        report["runtime"] = {"python": sys.version.split()[0]}
        output = Path(args.out)
        output.mkdir(parents=True, exist_ok=True)
        if not args.no_charts:
            chart(rows, output)
            import matplotlib

            report["runtime"]["matplotlib"] = matplotlib.__version__
        write_reports(report, output, not args.no_charts)
    except (ValueError, OSError, ImportError, OverflowError) as error:
        parser.exit(2, f"Evaluation failed: {error}\n")
    print(
        f"Wrote {output / 'report.html'}, report.md and metrics.json; analyst review remains required."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
