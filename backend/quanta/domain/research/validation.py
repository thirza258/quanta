"""Chronological validation: a train/test split and walk-forward selection.

Signals are computed once per configuration on the full history. Cutting them
into windows is equivalent to re-running the strategy on each window only if
the strategy is causal, which the look-ahead test establishes first; when it
fails, the pipeline marks these results invalid. Each window starts with fresh
capital and acts at its first open on the signal from the close before it.
"""

from __future__ import annotations

import statistics

from quanta.domain.research.metrics import HEADLINE, compact_curve, evaluate, sharpe_of

MIN_TRAIN = 126
MIN_TEST = 63
MAX_FOLDS = 40


def subset(metrics: dict) -> dict:
    return {key: metrics.get(key) for key in (*HEADLINE, "final_equity")}


def segment(bars, signals, start, end, costs):
    prior = bool(signals[start - 1]) if start > 0 else False
    return evaluate(bars[start:end], signals[start:end], costs, prior_signal=prior)


def best_index(metrics_list) -> int:
    """Highest Sharpe; undefined Sharpe never wins; ties go to the earlier configuration."""
    best = 0
    for i, metrics in enumerate(metrics_list):
        if sharpe_of(metrics) > sharpe_of(metrics_list[best]):
            best = i
    return best


def decay(in_sample, out_of_sample):
    """Share of the in-sample Sharpe lost out of sample; defined only for a positive IS Sharpe."""
    if in_sample is None or out_of_sample is None or in_sample <= 0:
        return None
    return 1 - out_of_sample / in_sample


def span(bars, start, end):
    return {"start": bars[start]["time"], "end": bars[end - 1]["time"], "bars": end - start}


def split_point(n: int, split: float) -> int | None:
    cut = int(round(n * split))
    if cut < MIN_TRAIN or n - cut < MIN_TEST:
        return None
    return cut


def train_test(bars, signal_sets, configs, base_index, costs, split):
    n = len(bars)
    cut = split_point(n, split)
    if cut is None:
        return {
            "status": "skipped",
            "reason": f"A {split:.0%} split of {n} bars leaves fewer than {MIN_TRAIN} "
            f"training or {MIN_TEST} test bars.",
        }
    in_sample = [segment(bars, s, 0, cut, costs)["metrics"] for s in signal_sets]
    chosen = best_index(in_sample)
    base_oos = segment(bars, signal_sets[base_index], cut, n, costs)["metrics"]
    chosen_oos = (
        base_oos
        if chosen == base_index
        else segment(bars, signal_sets[chosen], cut, n, costs)["metrics"]
    )
    return {
        "status": "completed",
        "split": split,
        "in_sample": span(bars, 0, cut),
        "out_of_sample": span(bars, cut, n),
        "base": {
            "index": base_index,
            "params": configs[base_index],
            "in_sample": subset(in_sample[base_index]),
            "out_of_sample": subset(base_oos),
            "decay": decay(in_sample[base_index]["sharpe"], base_oos["sharpe"]),
        },
        "selected": {
            "index": chosen,
            "params": configs[chosen],
            "in_sample": subset(in_sample[chosen]),
            "out_of_sample": subset(chosen_oos),
            "decay": decay(in_sample[chosen]["sharpe"], chosen_oos["sharpe"]),
        },
    }


def folds(n: int, train: int, test: int, anchored: bool) -> list[tuple[int, int, int, int]]:
    """(train_start, train_end, test_start, test_end) with contiguous test windows."""
    out = []
    test_start = train
    while test_start + MIN_TEST <= n and len(out) < MAX_FOLDS:
        test_end = min(test_start + test, n)
        out.append((0 if anchored else test_start - train, test_start, test_start, test_end))
        test_start = test_end
    return out


def walk_forward(bars, signal_sets, configs, base_index, costs, validation):
    n = len(bars)
    windows = folds(n, validation.train_bars, validation.test_bars, validation.anchored)
    if len(windows) < 2:
        # A full first test window, then at least MIN_TEST bars for the second.
        needed = validation.train_bars + validation.test_bars + MIN_TEST
        return {
            "status": "skipped",
            "reason": f"Walk-forward needs at least {needed} bars "
            f"for two test windows after {validation.train_bars} training bars; the dataset has {n}.",
        }
    rows, choices = [], []
    for k, (a, b, c, d) in enumerate(windows):
        in_sample = [segment(bars, s, a, b, costs)["metrics"] for s in signal_sets]
        chosen = best_index(in_sample)
        choices.append(chosen)
        oos = segment(bars, signal_sets[chosen], c, d, costs)["metrics"]
        base_oos = (
            oos
            if chosen == base_index
            else segment(bars, signal_sets[base_index], c, d, costs)["metrics"]
        )
        rows.append(
            {
                "fold": k + 1,
                "train": span(bars, a, b),
                "test": span(bars, c, d),
                "chosen": chosen,
                "params": configs[chosen],
                "in_sample_sharpe": in_sample[chosen]["sharpe"],
                "out_of_sample_sharpe": oos["sharpe"],
                "out_of_sample_return": oos["total_return"],
                "base_out_of_sample_sharpe": base_oos["sharpe"],
                "base_out_of_sample_return": base_oos["total_return"],
            }
        )
    # Stitch the out-of-sample windows into one continuous account. The position
    # at each open comes from the configuration chosen for that bar's fold,
    # evaluated at the previous close, when that choice was already known.
    first, end = windows[0][2], windows[-1][3]
    owner = [chosen for (_, _, c, d), chosen in zip(windows, choices) for _ in range(c, d)]
    stitched = [
        signal_sets[owner[j + 1] if j + 1 < len(owner) else owner[j]][first + j]
        for j in range(end - first)
    ]
    prior = bool(signal_sets[owner[0]][first - 1])
    oos = evaluate(bars[first:end], stitched, costs, prior_signal=prior)
    base = segment(bars, signal_sets[base_index], first, end, costs)
    in_sample = [r["in_sample_sharpe"] for r in rows if r["in_sample_sharpe"] is not None]
    mean_in_sample = statistics.fmean(in_sample) if in_sample else None
    oos_sharpes = [r["out_of_sample_sharpe"] for r in rows]
    return {
        "status": "completed",
        "mode": "anchored" if validation.anchored else "rolling",
        "train_bars": validation.train_bars,
        "test_bars": validation.test_bars,
        "folds": rows,
        "out_of_sample": span(bars, first, end),
        # Bars after the last full test window (fewer than MIN_TEST) are not tested.
        "untested_tail_bars": n - end,
        "aggregate": {
            "mean_in_sample_sharpe": mean_in_sample,
            "out_of_sample": subset(oos["metrics"]),
            "base_out_of_sample": subset(base["metrics"]),
            "decay": decay(mean_in_sample, oos["metrics"]["sharpe"]),
            "positive_folds": sum(1 for s in oos_sharpes if s is not None and s > 0),
            "distinct_choices": len(set(choices)),
        },
        "equity_curve": compact_curve(oos["result"]),
    }
