"""The research note: one experiment rendered as Markdown or standalone HTML.

Hypothesis, method, results, validation, robustness, red team, conclusion,
limitations and provenance, in that order. Every field a learner typed is
escaped in HTML; the page needs no script and no network.
"""

from __future__ import annotations

import html

from quanta.domain.research.robustness import COST_LEVELS

DISCLAIMER = (
    "Research quality is not investment quality. This note describes a simulated, "
    "educational experiment; it is not investment advice."
)
STATUS_MARK = {"pass": "✓", "warn": "⚠", "fail": "✗", "skip": "–"}
ROWS = (
    ("CAGR", "cagr", "pct"),
    ("Total return", "total_return", "pct"),
    ("Sharpe", "sharpe", "num"),
    ("Sortino", "sortino", "num"),
    ("Max drawdown", "max_drawdown", "pct"),
    ("Calmar", "calmar", "num"),
    ("Volatility", "volatility", "pct"),
    ("Turnover (×/yr)", "turnover", "num"),
    ("Win rate", "win_rate", "pct"),
    ("Profit factor", "profit_factor", "num"),
    ("Exposure", "exposure", "pct"),
    ("Trades", "trades", "int"),
)


def fmt(value, kind="num"):
    if value is None:
        return "—"
    if kind == "pct":
        return f"{value * 100:.1f}%"
    if kind == "int":
        return f"{int(value):,}"
    return f"{value:.2f}"


def params_text(params: dict) -> str:
    return ", ".join(f"{k} = {v}" for k, v in params.items()) or "no parameters"


def _method(experiment, run) -> list[str]:
    spec, prov = run["spec"]["experiment"], run["provenance"]
    dataset, strategy = prov["dataset"], prov["strategy"]
    validation = spec["validation"]
    grid = spec["strategy"]["parameters"]
    lines = [
        f"Dataset: {dataset['label']} — {run['results']['dataset']['bars']} daily bars, "
        f"{run['results']['dataset']['start']} to {run['results']['dataset']['end']} "
        f"(version {dataset['version']}).",
        f"Strategy: {strategy['name']} v{strategy['version']}; base configuration "
        f"{params_text(spec['strategy']['base'])}.",
        "Parameter grid: "
        + (
            "; ".join(f"{p['name']} ∈ {{{', '.join(str(v) for v in p['values'])}}}" for p in grid)
            + f" ({len(run['results']['configurations'])} configurations)."
            if grid
            else "none (one configuration)."
        ),
        f"Execution: signals at the close fill at the next open; {spec['costs']['commission_bps']} bps "
        f"commission and {spec['costs']['slippage_bps']} bps slippage per fill; "
        f"{spec['costs']['capital']:,.0f} starting capital; long or cash only.",
        f"Validation: {validation['split']:.0%} / {1 - validation['split']:.0%} chronological split"
        + (
            f"; {'anchored' if validation['anchored'] else 'rolling'} walk-forward with "
            f"{validation['train_bars']} training and {validation['test_bars']} test bars."
            if validation["walk_forward"]
            else "; walk-forward off."
        ),
        f"Stress: one-way costs from {COST_LEVELS[0]} to {COST_LEVELS[-1]} bps; "
        f"{validation['permutations']} random re-timings"
        + (
            f"; {validation['seed_paths']} alternative synthetic paths."
            if dataset["kind"] == "synthetic"
            else "."
        ),
    ]
    return lines


def _limitations(run) -> list[str]:
    notes = [
        c["finding"] for c in run["results"]["redteam"]["checks"] if c["status"] in ("warn", "fail")
    ]
    if run["provenance"]["dataset"]["kind"] == "synthetic":
        notes.append(
            "The data is a synthetic stochastic path; it shows how the rule behaves, not how it "
            "would have behaved in any real market."
        )
    else:
        notes.append(
            "Imported history is one asset without a point-in-time universe, corporate-action "
            "audit or survivorship control."
        )
    return notes


def _provenance(run) -> list[tuple[str, str]]:
    prov = run["provenance"]
    return [
        (
            "Dataset",
            f"{prov['dataset']['key']} v{prov['dataset']['version']} · {prov['dataset']['sha256']}",
        ),
        (
            "Strategy",
            f"{prov['strategy']['name']} v{prov['strategy']['version']} · {prov['strategy']['sha256']}",
        ),
        ("Configuration", prov["config_sha256"]),
        (
            "Engine",
            f"{prov['engine']['name']} {prov['engine']['version']} · {prov['engine']['sha256']}",
        ),
        (
            "Environment",
            f"Python {prov['environment']['python']}, NumPy {prov['environment']['numpy']}, {prov['environment']['platform']} · {prov['environment']['sha256']}",
        ),
        ("Runtime", prov["runtime"]),
        ("Git commit", prov.get("git_commit") or "not recorded"),
        ("Seeds", ", ".join(f"{k} {v}" for k, v in prov["seeds"].items())),
        ("Result", prov["result_sha256"]),
    ]


def markdown(experiment: dict, run: dict) -> str:
    results = run["results"]
    risk = results["redteam"]["risk"]
    notebook = experiment["notebook"]
    out = [
        f"# {experiment['title']}",
        "",
        f"Experiment #{experiment['number']} · run {run['number']} · {run['provenance']['strategy']['name']} "
        f"v{run['provenance']['strategy']['version']} · {run['provenance']['dataset']['label']}",
        "",
        f"**Research risk: {risk['level']}** · research quality "
        f"{experiment['quality']['score']}/100 · status {experiment['lifecycle']['status']}",
        "",
        "## Hypothesis",
        "",
        "> " + experiment["hypothesis"].replace("\n", "\n> "),
        "",
        f"Registered {experiment['hypothesis_registered_at'][:10]}, before any result.",
        "",
        "## Method",
        "",
        *[f"- {line}" for line in _method(experiment, run)],
        "",
        "## Results",
        "",
    ]
    if not results["valid"]:
        out += ["**Look-ahead detected: the figures below are not valid evidence.**", ""]
    rows = results["benchmarks"]["rows"]
    out.append("| Metric | " + " | ".join(r["label"] for r in rows) + " |")
    out.append("| --- " * (len(rows) + 1) + "|")
    for label, key, kind in ROWS:
        out.append(
            f"| {label} | " + " | ".join(fmt(r["metrics"].get(key), kind) for r in rows) + " |"
        )
    out += ["", "## Out-of-sample validation", ""]
    split = results["validation"]["train_test"]
    if split["status"] == "completed":
        out += [
            f"Chronological split at {split['out_of_sample']['start']} "
            f"({split['in_sample']['bars']} / {split['out_of_sample']['bars']} bars).",
            "",
            "| Configuration | In-sample Sharpe | Out-of-sample Sharpe | Decay |",
            "| --- | --- | --- | --- |",
            f"| Base ({params_text(split['base']['params'])}) | {fmt(split['base']['in_sample']['sharpe'])} | "
            f"{fmt(split['base']['out_of_sample']['sharpe'])} | {fmt(split['base']['decay'], 'pct')} |",
            f"| Best in-sample ({params_text(split['selected']['params'])}) | "
            f"{fmt(split['selected']['in_sample']['sharpe'])} | {fmt(split['selected']['out_of_sample']['sharpe'])} | "
            f"{fmt(split['selected']['decay'], 'pct')} |",
            "",
        ]
    else:
        out += [f"Train/test split skipped: {split['reason']}", ""]
    wf = results["validation"]["walk_forward"]
    if wf["status"] == "completed":
        agg = wf["aggregate"]
        out += [
            f"Walk-forward ({wf['mode']}, {len(wf['folds'])} folds): mean in-sample Sharpe "
            f"{fmt(agg['mean_in_sample_sharpe'])}, stitched out-of-sample Sharpe "
            f"{fmt(agg['out_of_sample']['sharpe'])}, decay {fmt(agg['decay'], 'pct')}; "
            f"{agg['distinct_choices']} distinct configurations chosen.",
            "",
            "| Fold | Test window | Chosen | IS Sharpe | OOS Sharpe | OOS return |",
            "| --- | --- | --- | --- | --- | --- |",
            *[
                f"| {f['fold']} | {f['test']['start']} – {f['test']['end']} | {params_text(f['params'])} | "
                f"{fmt(f['in_sample_sharpe'])} | {fmt(f['out_of_sample_sharpe'])} | {fmt(f['out_of_sample_return'], 'pct')} |"
                for f in wf["folds"]
            ],
            "",
        ]
    else:
        out += [f"Walk-forward skipped: {wf['reason']}", ""]
    surface = results["robustness"]["surface"]
    stress = results["robustness"]["costs"]
    out += [
        "## Robustness",
        "",
        f"- Stability of the base configuration: {surface['stability']['class']}"
        + (
            f" ({surface['stability']['score']}/100)"
            if surface["stability"]["score"] is not None
            else ""
        )
        + f". {surface['stability']['reason']}",
        f"- Grid of {surface['configurations']}: best {params_text(results['configurations'][surface['best']])}, "
        f"median {params_text(results['configurations'][surface['median']])}, worst "
        f"{params_text(results['configurations'][surface['worst']])}; {fmt(surface['positive_share'], 'pct')} with a positive Sharpe; "
        f"base ranks {surface['base_rank']} of {surface['configurations']}.",
        "- Break-even cost: "
        + (
            f"{stress['break_even_bps']:.1f} bps per fill against {stress['current_bps']:.1f} assumed."
            if stress.get("break_even_bps") is not None
            else stress.get("reason", "not computed.")
        ),
        "",
        "| One-way cost (bps) | Sharpe | CAGR |",
        "| --- | --- | --- |",
        *[
            f"| {lv['cost_bps']} | {fmt(lv['sharpe'])} | {fmt(lv['cagr'], 'pct')} |"
            for lv in stress["levels"]
        ],
        "",
        "## Research red team",
        "",
        *[
            f"- {STATUS_MARK[c['status']]} **{c['title']}** — {c['finding']}"
            for c in results["redteam"]["checks"]
        ],
        "",
        f"Overall: **{risk['level']} research risk** ({risk['passed']} passed, {risk['warnings']} warnings, "
        f"{risk['failed']} failed, {risk['skipped']} not applicable).",
        "",
        "## Conclusion",
        "",
        notebook.get("conclusion") or "_Not written yet._",
        "",
        f"Decision: {(notebook.get('decision') or 'not recorded').capitalize()}",
        "",
        "## Limitations",
        "",
        notebook.get("limitations") or "_Not written yet._",
        "",
        "Recorded by the red team:",
        "",
        *[f"- {line}" for line in _limitations(run)],
        "",
        "## Provenance",
        "",
        "| Artifact | Fingerprint |",
        "| --- | --- |",
        *[f"| {label} | `{value}` |" for label, value in _provenance(run)],
        "",
    ]
    reproduction = experiment.get("reproduction")
    if reproduction:
        out += [f"Rerun verdict: {reproduction['verdict']}.", ""]
    out += [f"_{DISCLAIMER}_", ""]
    return "\n".join(out)


def _svg_lines(
    series: list[list[float]], labels: list[str], colors: list[str], width=720, height=220
):
    values = [v for s in series for v in s if v is not None]
    if not values:
        return ""
    low, high = min(values), max(values)
    span = (high - low) or 1.0
    paths = []
    for points, color in zip(series, colors):
        step = width / max(1, len(points) - 1)
        coords = " ".join(
            f"{i * step:.1f},{height - (v - low) / span * (height - 20) - 10:.1f}"
            for i, v in enumerate(points)
            if v is not None
        )
        paths.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{coords}"/>')
    legend = " ".join(
        f'<span class="key"><i style="background:{c}"></i>{html.escape(label)}</span>'
        for label, c in zip(labels, colors)
    )
    return (
        f'<figure><svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(", ".join(labels))}">'
        + "".join(paths)
        + f"</svg><figcaption>{legend}</figcaption></figure>"
    )


def page(experiment: dict, run: dict) -> str:
    """Standalone HTML: escape everything, embed the charts, print cleanly."""
    e = html.escape
    results = run["results"]
    risk = results["redteam"]["risk"]
    notebook = experiment["notebook"]
    rows = results["benchmarks"]["rows"]
    curve = results["headline"]["equity_curve"]
    equity_chart = _svg_lines(
        [[p["equity"] for p in curve], [p["benchmark"] for p in curve]],
        ["Strategy", "Buy & hold"],
        ["#295b48", "#9aa39c"],
    )
    stress = results["robustness"]["costs"]
    cost_chart = _svg_lines(
        [[lv["sharpe"] for lv in stress["levels"]]], ["Sharpe by one-way cost"], ["#b76070"]
    )

    def table(head, body):
        return (
            "<table><thead><tr>"
            + "".join(f"<th>{e(str(h))}</th>" for h in head)
            + "</tr></thead><tbody>"
            + "".join(
                "<tr>" + "".join(f"<td>{e(str(c))}</td>" for c in row) + "</tr>" for row in body
            )
            + "</tbody></table>"
        )

    def para(text):
        return "".join(f"<p>{e(line)}</p>" for line in (text or "").split("\n") if line.strip())

    checks = "".join(
        f'<li class="{c["status"]}"><strong>{STATUS_MARK[c["status"]]} {e(c["title"])}</strong> — {e(c["finding"])}</li>'
        for c in results["redteam"]["checks"]
    )
    wf = results["validation"]["walk_forward"]
    folds = (
        table(
            ["Fold", "Test window", "Chosen", "IS Sharpe", "OOS Sharpe", "OOS return"],
            [
                [
                    f["fold"],
                    f"{f['test']['start']} – {f['test']['end']}",
                    params_text(f["params"]),
                    fmt(f["in_sample_sharpe"]),
                    fmt(f["out_of_sample_sharpe"]),
                    fmt(f["out_of_sample_return"], "pct"),
                ]
                for f in wf["folds"]
            ],
        )
        if wf["status"] == "completed"
        else f"<p>Walk-forward skipped: {e(wf['reason'])}</p>"
    )
    body = f"""
<header>
  <p class="eyebrow">Quanta research note · experiment #{experiment["number"]} · run {run["number"]}</p>
  <h1>{e(experiment["title"])}</h1>
  <p class="meta"><span class="risk {risk["level"].lower()}">{risk["level"]} research risk</span>
  Research quality {experiment["quality"]["score"]}/100 · {e(experiment["lifecycle"]["status"])}</p>
</header>
<section><h2>Hypothesis</h2><blockquote>{para(experiment["hypothesis"])}</blockquote>
<p class="fine">Registered {e(experiment["hypothesis_registered_at"][:10])}, before any result.</p></section>
<section><h2>Method</h2><ul>{"".join(f"<li>{e(line)}</li>" for line in _method(experiment, run))}</ul></section>
<section><h2>Results</h2>
{'<p class="alert">Look-ahead detected: these figures are not valid evidence.</p>' if not results["valid"] else ""}
{equity_chart}
{table(["Metric", *[r["label"] for r in rows]], [[label, *[fmt(r["metrics"].get(key), kind) for r in rows]] for label, key, kind in ROWS])}
</section>
<section><h2>Out-of-sample validation</h2>{folds}</section>
<section><h2>Robustness</h2>
<p>Stability of the base configuration: {e(results["robustness"]["surface"]["stability"]["class"])}. {e(results["robustness"]["surface"]["stability"]["reason"])}</p>
{cost_chart}
{table(["One-way cost (bps)", "Sharpe", "CAGR"], [[lv["cost_bps"], fmt(lv["sharpe"]), fmt(lv["cagr"], "pct")] for lv in stress["levels"]])}
</section>
<section><h2>Research red team</h2><ul class="checks">{checks}</ul>
<p><strong>Overall: {risk["level"]} research risk.</strong></p></section>
<section><h2>Conclusion</h2>{para(notebook.get("conclusion")) or "<p><em>Not written yet.</em></p>"}
<p>Decision: {e((notebook.get("decision") or "not recorded").capitalize())}</p></section>
<section><h2>Limitations</h2>{para(notebook.get("limitations")) or "<p><em>Not written yet.</em></p>"}
<ul>{"".join(f"<li>{e(line)}</li>" for line in _limitations(run))}</ul></section>
<section><h2>Provenance</h2>{table(["Artifact", "Fingerprint"], _provenance(run))}</section>
<footer><p>{e(DISCLAIMER)}</p></footer>
"""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(experiment["title"])} · Quanta research note</title>
<style>
:root{{color-scheme:light;--ink:#28342f;--muted:#6d776f;--line:#e7eae5;--accent:#295b48;--warn:#9a6b16;--bad:#b76070}}
body{{font:15px/1.6 system-ui,-apple-system,sans-serif;color:var(--ink);max-width:880px;margin:40px auto;padding:0 20px;background:#fff}}
h1{{font-size:28px;line-height:1.25;margin:4px 0 8px}}h2{{font-size:19px;margin:32px 0 10px;border-bottom:1px solid var(--line);padding-bottom:6px}}
.eyebrow,.fine,.meta{{color:var(--muted);font-size:13px}}blockquote{{margin:0;padding:4px 16px;border-left:3px solid var(--accent);background:#f8faf8}}
table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:13px;font-variant-numeric:tabular-nums}}
th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top;word-break:break-word}}
th{{color:var(--muted);font-weight:600}}figure{{margin:12px 0}}svg{{width:100%;height:auto;background:#f8faf8;border:1px solid var(--line);border-radius:6px}}
figcaption{{font-size:12px;color:var(--muted)}}.key{{margin-right:14px}}.key i{{display:inline-block;width:10px;height:3px;margin-right:6px;vertical-align:middle}}
.risk{{display:inline-block;padding:2px 10px;border-radius:999px;font-weight:600;margin-right:8px}}.risk.low{{background:#eaf0e9;color:var(--accent)}}
.risk.medium{{background:#f6eedd;color:var(--warn)}}.risk.high{{background:#f6e3e6;color:var(--bad)}}
.checks{{list-style:none;padding:0}}.checks li{{padding:6px 0;border-bottom:1px solid var(--line)}}.checks .warn strong{{color:var(--warn)}}
.checks .fail strong{{color:var(--bad)}}.alert{{padding:10px 14px;background:#f6e3e6;color:var(--bad);border-radius:6px;font-weight:600}}
footer{{margin-top:40px;color:var(--muted);font-size:12px}}
@media print{{body{{margin:0}}section{{break-inside:avoid}}}}
</style></head><body>{body}</body></html>
"""
