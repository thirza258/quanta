"""Fingerprints that make a run reproducible, and a changed input visible.

A run records SHA-256 digests of its dataset, strategy source, configuration,
research engine and environment, and of its own deterministic output. A rerun
repeats the stored specification and compares both sides: identical inputs
should give an identical output digest, and a different digest is explained by
whichever input changed.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
from functools import lru_cache
from pathlib import Path

import numpy as np

ENGINE_NAME = "quanta-research"
ENGINE_VERSION = "1.0.0"
PACKAGE = Path(__file__).resolve().parents[2]
PROJECT = PACKAGE.parents[1]
# Every source file whose behaviour can change a research result.
ENGINE_SOURCES = (
    "domain/analytics.py",
    "domain/research/__init__.py",
    "domain/research/diagnostics.py",
    "domain/research/metrics.py",
    "domain/research/pipeline.py",
    "domain/research/redteam.py",
    "domain/research/robustness.py",
    "domain/research/spec.py",
    "domain/research/validation.py",
    "execution/native_worker.py",
    "execution/runner.py",
    "execution/sandbox_worker.py",
)
TOLERANCE = 1e-9


def canonical(value) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode()


def digest(value) -> str:
    data = value if isinstance(value, bytes) else canonical(value)
    return hashlib.sha256(data).hexdigest()


def _engine() -> dict:
    hasher = hashlib.sha256()
    for name in ENGINE_SOURCES:
        hasher.update(name.encode() + b"\0")
        hasher.update((PACKAGE / name).read_bytes() + b"\0")
    return {"name": ENGINE_NAME, "version": ENGINE_VERSION, "sha256": hasher.hexdigest()}


def _environment() -> dict:
    info = {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "numpy": np.__version__,
        "platform": f"{platform.system()}-{platform.machine()}",
    }
    return {**info, "sha256": digest(info)}


# Hashed once, when the code that produced the result was loaded.
ENGINE = _engine()
ENVIRONMENT = _environment()


@lru_cache(maxsize=1)
def git_commit() -> str | None:
    """The deployed commit, from QUANTA_GIT_COMMIT or the checkout; None when unknowable."""
    configured = os.getenv("QUANTA_GIT_COMMIT", "").strip()
    if configured:
        return configured[:64]
    if not (PROJECT / ".git").exists():
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2,
        )
    except OSError, subprocess.TimeoutExpired:
        return None
    commit = result.stdout.strip()
    return commit if result.returncode == 0 and len(commit) == 40 else None


def compare(original: dict, rerun: dict) -> dict:
    """Explain whether a rerun reproduced the original, and if not, which input moved."""
    first, second = original["provenance"], rerun["provenance"]
    inputs = []
    for key, label, a, b in (
        ("dataset", "Dataset", first["dataset"]["sha256"], second["dataset"]["sha256"]),
        ("strategy", "Strategy source", first["strategy"]["sha256"], second["strategy"]["sha256"]),
        ("config", "Configuration", first["config_sha256"], second["config_sha256"]),
        ("engine", "Research engine", first["engine"]["sha256"], second["engine"]["sha256"]),
        (
            "environment",
            "Environment",
            first["environment"]["sha256"],
            second["environment"]["sha256"],
        ),
        ("runtime", "Python runtime", first["runtime"], second["runtime"]),
        (
            "trials",
            "Earlier trials counted",
            str(first.get("prior_trials", "not recorded")),
            str(second.get("prior_trials", "not recorded")),
        ),
    ):
        inputs.append({"id": key, "label": label, "same": a == b, "original": a, "rerun": b})
    same_output = first["result_sha256"] == second["result_sha256"]
    differences = []
    if not same_output:
        a = original["results"]["headline"]["metrics"]
        b = rerun["results"]["headline"]["metrics"]
        for key in sorted(set(a) | set(b)):
            x, y = a.get(key), b.get(key)
            if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                scale = max(abs(x), abs(y), 1e-12)
                if abs(x - y) / scale > 0:
                    differences.append({"metric": key, "original": x, "rerun": y})
            elif x != y:
                differences.append({"metric": key, "original": x, "rerun": y})
    largest = max(
        (
            abs(d["original"] - d["rerun"]) / max(abs(d["original"]), abs(d["rerun"]), 1e-12)
            for d in differences
            if isinstance(d["original"], (int, float)) and isinstance(d["rerun"], (int, float))
        ),
        default=0.0,
    )
    changed = [i["label"] for i in inputs if not i["same"]]
    numeric = all(
        isinstance(d["original"], (int, float)) and isinstance(d["rerun"], (int, float))
        for d in differences
    )
    if same_output:
        verdict = "identical"
    elif differences and numeric and largest <= TOLERANCE:
        verdict = "equivalent"
    else:
        # Includes a metric turning undefined (None) on one side: that is never rounding.
        verdict = "different"
    return {
        "verdict": verdict,
        "inputs": inputs,
        "changed_inputs": changed,
        "output_identical": same_output,
        "metric_differences": differences[:20],
        "largest_relative_difference": largest,
    }
