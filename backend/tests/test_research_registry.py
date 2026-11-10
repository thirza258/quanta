"""HTTP tests for the research registry (/api/v1/research).

A run executes in a background job, so a test starts one and polls the run
until it leaves queued/running. Every test then waits until no research job is
pending in the process: a leaked job keeps forking sandbox processes into
whichever test runs next. Run starts share a budget of six a minute per guest
host or account; the `client` fixture resets it for each test.
"""

import copy
import hashlib
import html
import re
import time
import uuid
from html.parser import HTMLParser

import duckdb
import jwt
import pandas as pd
import pytest
import quanta
from fastapi.testclient import TestClient
from quanta.core.config import DATA_DIR
from quanta.core.limits import limiter
from quanta.db.models import ResearchExperiment, ResearchRun
from quanta.db.session import engine
from quanta.domain.analytics import DatasetParams, generate
from quanta.domain.research import provenance
from quanta.domain.research.spec import ExperimentSpec
from quanta.main import app
from quanta.services import experiments
from sqlmodel import Session, select
from test_api import signup

API = "/api/v1/research"
HEX64 = re.compile(r"[0-9a-f]{64}")
HYPOTHESIS = "A 20/150 moving-average crossover beats buy and hold after costs."
ACTIVE = ("queued", "running")

# Fields the frontend contract (frontend/src/features/research/model/registry.ts) reads.
RUN_FIELDS = {
    "id",
    "experiment_id",
    "number",
    "kind",
    "rerun_of",
    "status",
    "stage",
    "progress",
    "summary",
    "reproduction",
    "strategy",
    "error",
    "created_at",
    "started_at",
    "finished_at",
    "duration_ms",
}
RUN_DETAIL_FIELDS = RUN_FIELDS | {"spec", "provenance", "results"}
SUMMARY_FIELDS = {
    "id",
    "number",
    "title",
    "strategy",
    "dataset",
    "status",
    "risk",
    "metrics",
    "run_count",
    "active",
    "created_at",
    "updated_at",
}
DETAIL_FIELDS = SUMMARY_FIELDS | {
    "hypothesis",
    "hypothesis_registered_at",
    "hypothesis_locked",
    "spec",
    "notebook",
    "lifecycle",
    "quality",
    "spec_changed",
    "strategy_versions",
    "runs",
    "active_run",
    "current",
    "reproduction",
}
METRIC_FIELDS = {
    "total_return",
    "cagr",
    "sharpe",
    "sortino",
    "max_drawdown",
    "calmar",
    "volatility",
    "turnover",
    "win_rate",
    "profit_factor",
    "exposure",
    "trades",
    "final_equity",
}
SUMMARY_METRICS = {"cagr", "sharpe", "max_drawdown", "turnover", "total_return"}


# ---------------------------------------------------------------- fixtures


@pytest.fixture(autouse=True)
def no_job_left_behind():
    yield
    assert experiments.idle(60), "a research job outlived its test"


class HeldJobs:
    """Stands in for the research executor: submitted runs stay queued until released."""

    def __init__(self, executor):
        self.executor, self.jobs, self.holding = executor, [], True

    def submit(self, fn, *args):
        if not self.holding:
            return self.executor.submit(fn, *args)
        self.jobs.append((fn, args))

    def hold(self):
        self.holding = True

    def release(self):
        """Run the held jobs in this thread; later runs go to the real executor.

        A queued run executes; an interrupted or deleted one returns at once. Either
        way the service's pending count, which `idle()` waits on, comes back down.
        """
        self.holding = False
        while self.jobs:
            fn, args = self.jobs.pop(0)
            fn(*args)


@pytest.fixture
def held(monkeypatch):
    jobs = HeldJobs(experiments.JOBS)
    monkeypatch.setattr(experiments, "JOBS", jobs)
    yield jobs
    jobs.release()


@pytest.fixture
def imported():
    """An imported Parquet dataset under a unique symbol, and a writer that replaces its prices."""
    symbol = "ZQ" + uuid.uuid4().hex[:8].upper()  # sorts after test_api's TEST
    path = DATA_DIR / f"{symbol}.parquet"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    def write(seed: int) -> str:
        # Seeded synthetic prices stand in for licensed data; only the import path is tested.
        frame = pd.DataFrame(generate(DatasetParams(years=4, seed=seed))[:800])
        path.unlink(missing_ok=True)
        with duckdb.connect() as db:
            db.register("bars", frame)
            db.execute(
                "COPY (SELECT CAST(time AS DATE) AS time, open, high, low, close, volume "
                "FROM bars ORDER BY time) TO ? (FORMAT PARQUET)",
                [str(path)],
            )
        return hashlib.sha256(path.read_bytes()).hexdigest()

    try:
        yield symbol, write
    finally:
        path.unlink(missing_ok=True)


# ---------------------------------------------------------------- helpers


def small_spec() -> dict:
    """The default specification shrunk for speed: 3 years, a 2 x 2 grid, light stress tests."""
    spec = ExperimentSpec().model_dump(mode="json")
    spec["dataset"]["params"]["years"] = 3
    spec["strategy"]["parameters"] = [
        {"name": "fast", "values": [10, 20]},
        {"name": "slow", "values": [100, 150]},
    ]
    spec["strategy"]["base"] = {"fast": 20, "slow": 150}
    spec["validation"].update(permutations=20, seed_paths=1)
    return spec


def body(*, run=True, spec=None, title="Trend beats cash", hypothesis=HYPOTHESIS) -> dict:
    return {"title": title, "hypothesis": hypothesis, "spec": spec or small_spec(), "run": run}


def create(client, status=201, **fields) -> dict:
    response = client.post(f"{API}/experiments", json=body(**fields))
    assert response.status_code == status, response.text
    return response.json()


def get(client, experiment_id) -> dict:
    response = client.get(f"{API}/experiments/{experiment_id}")
    assert response.status_code == 200, response.text
    return response.json()


def patch(client, experiment_id, changes, status=200) -> dict:
    response = client.patch(f"{API}/experiments/{experiment_id}", json=changes)
    assert response.status_code == status, response.text
    return response.json()


def start(client, experiment_id, status=202) -> dict:
    response = client.post(f"{API}/experiments/{experiment_id}/runs")
    assert response.status_code == status, response.text
    return response.json()


def rerun(client, run_id, status=202) -> dict:
    response = client.post(f"{API}/runs/{run_id}/rerun")
    assert response.status_code == status, response.text
    return response.json()


def listed(client) -> list[dict]:
    response = client.get(f"{API}/experiments")
    assert response.status_code == 200, response.text
    return response.json()["experiments"]


def wait(client, run_id, timeout=120.0) -> dict:
    """Poll a run until it is no longer queued or running."""
    deadline = time.monotonic() + timeout
    while True:
        response = client.get(f"{API}/runs/{run_id}")
        assert response.status_code == 200, response.text
        run = response.json()
        if run["status"] not in ACTIVE:
            return run
        assert time.monotonic() < deadline, f"run {run_id} is still {run['status']}"
        time.sleep(0.05)


def finish(client, run_id) -> dict:
    run = wait(client, run_id)
    assert run["status"] == "completed", run["error"]
    return run


def completed(client, **fields) -> tuple[dict, dict]:
    """Create an experiment, run it to completion and return (detail, run)."""
    detail = create(client, **fields)
    run = finish(client, detail["active_run"]["id"])
    return get(client, detail["id"]), run


def steps(detail) -> dict:
    return {step["id"]: step["done"] for step in detail["lifecycle"]["steps"]}


def scores(detail) -> dict:
    return {part["id"]: part["score"] for part in detail["quality"]["components"]}


def edit_run(run_id, **changes):
    """Change a run row directly, as a crashed worker would leave it."""
    with Session(engine) as db:
        run = db.get(ResearchRun, run_id)
        for key, value in changes.items():
            setattr(run, key, value)
        db.add(run)
        db.commit()


class Tags(HTMLParser):
    """Every start tag and its attributes, as a browser would parse them."""

    def __init__(self, page: str):
        super().__init__()
        self.found: list[tuple[str, list]] = []
        self.feed(page)
        self.close()

    def handle_starttag(self, tag, attrs):
        self.found.append((tag, attrs))

    handle_startendtag = handle_starttag


# ---------------------------------------------------------------- options


def test_options_list_defaults_limits_templates_and_indicators(client):
    response = client.get(f"{API}/options")
    assert response.status_code == 200, response.text
    options = response.json()
    defaults = options["defaults"]
    assert defaults == ExperimentSpec().model_dump(mode="json")
    assert ExperimentSpec.model_validate(defaults).model_dump(mode="json") == defaults
    assert options["limits"] == {
        "parameters": 3,
        "values": 12,
        "configurations": 60,
        "code": 20000,
        "title": 120,
        "hypothesis_min": 12,
        "hypothesis_max": 2000,
        "notebook": 8000,
    }
    templates = options["templates"]
    assert [t["id"] for t in templates] == ["trend", "momentum", "reversion", "channel"]
    for template in templates:
        assert set(template) == {"id", "label", "description", "code", "parameters", "base"}
        assert template["label"] and template["description"]
        strategy = {key: template[key] for key in ("code", "parameters", "base")}
        assert (
            ExperimentSpec.model_validate({"strategy": strategy}).strategy.base == template["base"]
        )
    names = ["sma", "ema", "highest", "lowest", "change", "shift", "stdev", "zscore"]
    assert [i["name"] for i in options["indicators"]] == names
    for indicator in options["indicators"]:
        assert indicator["signature"] == f"{indicator['name']}(series, n)"
        assert indicator["description"]
    assert {m["id"] for m in options["synthetic"]["models"]} == {
        "gbm",
        "merton",
        "heston",
        "regime",
    }
    assert {"custom", "flash_crash"} <= {s["id"] for s in options["synthetic"]["scenarios"]}
    assert all(set(entry) == {"symbol", "versions"} for entry in options["historical"])


def test_every_template_completes_a_valid_run(client):
    options = client.get(f"{API}/options").json()
    assert len(options["templates"]) == 4  # four run starts: within the six-a-minute budget
    for template in options["templates"]:
        spec = copy.deepcopy(options["defaults"])
        spec["dataset"]["params"]["years"] = 3
        spec["validation"].update(permutations=20, seed_paths=1)
        spec["strategy"] = {
            "name": template["label"],
            "code": template["code"],
            "parameters": template["parameters"],
            "base": template["base"],
        }
        detail, run = completed(
            client,
            spec=spec,
            title=template["label"],
            hypothesis=f"{template['description']} It beats cash after costs.",
        )
        results = run["results"]
        assert results["valid"] is True, template["id"]
        assert results["lookahead"]["status"] == "pass", template["id"]
        grid = 1
        for parameter in template["parameters"]:
            grid *= len(parameter["values"])
        assert len(results["configurations"]) == grid == run["summary"]["configurations"]
        assert results["configurations"][results["base_index"]] == template["base"]
        assert detail["status"] in ("PASSED", "WARNINGS"), template["id"]


# ---------------------------------------------------------------- create and run


def test_create_and_run_records_a_complete_result(client, held):
    spec = small_spec()
    detail = create(client, spec=spec)
    experiment_id = detail["id"]
    assert set(detail) >= DETAIL_FIELDS
    assert detail["number"] == 1 and detail["spec"] == spec and detail["notebook"] == {}
    queued = detail["active_run"]
    assert set(queued) >= RUN_FIELDS
    assert (queued["kind"], queued["status"], queued["number"], queued["rerun_of"]) == (
        "run",
        "queued",
        1,
        None,
    )
    assert queued["progress"] == {"done": 0, "total": None}
    assert queued["strategy"]["version"] == 1
    assert detail["status"] == detail["lifecycle"]["status"] == "RUNNING"
    assert detail["active"] is True and detail["current"] is None
    assert detail["hypothesis_locked"] is False
    assert [r["id"] for r in detail["runs"]] == [queued["id"]]
    [row] = listed(client)
    assert (row["id"], row["active"], row["status"], row["run_count"]) == (
        experiment_id,
        True,
        "RUNNING",
        1,
    )

    held.release()
    run = finish(client, queued["id"])
    detail = get(client, experiment_id)
    current = detail["current"]
    assert current == run
    assert set(current) >= RUN_DETAIL_FIELDS
    assert current["stage"] == "completed" and current["error"] is None
    assert current["started_at"] and current["finished_at"] and current["duration_ms"] >= 0
    assert current["progress"]["done"] == current["progress"]["total"] > 0
    assert current["spec"]["experiment"] == spec and current["spec"]["prior_trials"] == 0

    # The experiment after its first result.
    risk = current["summary"]["risk"]
    assert risk in ("LOW", "MEDIUM", "HIGH")
    assert detail["risk"] == risk == current["results"]["redteam"]["risk"]["level"]
    assert detail["status"] == detail["lifecycle"]["status"]
    assert detail["status"] == ("PASSED" if risk == "LOW" else "WARNINGS")
    assert steps(detail) == {
        "configured": True,
        "completed": True,
        "validated": True,
        "documented": False,
        "reproducible": False,
    }
    assert detail["hypothesis_locked"] is True and detail["spec_changed"] is False
    assert detail["active"] is False and detail["active_run"] is None
    assert detail["reproduction"] is None
    code_sha = hashlib.sha256(spec["strategy"]["code"].encode()).hexdigest()
    assert [(v["version"], v["sha256"]) for v in detail["strategy_versions"]] == [(1, code_sha)]
    assert 0 <= detail["quality"]["score"] <= 100
    assert set(scores(detail)) == {
        "reproducibility",
        "validation",
        "costs",
        "robustness",
        "bias",
        "sample",
        "documentation",
    }

    # RunSummary.summary and the registry row.
    summary = current["summary"]
    assert set(summary) == {"risk", "valid", "configurations", "metrics"}
    assert summary["valid"] is True and summary["configurations"] == 4
    headline = current["results"]["headline"]["metrics"]
    assert summary["metrics"] == {key: headline[key] for key in SUMMARY_METRICS}
    [row] = listed(client)
    assert set(row) >= SUMMARY_FIELDS
    assert (row["run_count"], row["active"], row["status"], row["risk"]) == (
        1,
        False,
        detail["status"],
        risk,
    )
    assert row["metrics"] == summary["metrics"]
    assert row["strategy"] == "Trend rule"
    assert row["dataset"] == "Geometric Brownian motion · seed 42 · 3y"

    # Results: the fields the result views read.
    results = current["results"]
    assert set(results) >= {
        "valid",
        "seeds",
        "dataset",
        "configurations",
        "base_index",
        "headline",
        "benchmarks",
        "lookahead",
        "validation",
        "robustness",
        "diagnostics",
        "redteam",
    }
    assert results["valid"] is True and results["lookahead"]["status"] == "pass"
    assert len(results["lookahead"]["checks"]) == 3
    assert results["configurations"] == [
        {"fast": 10, "slow": 100},
        {"fast": 10, "slow": 150},
        {"fast": 20, "slow": 100},
        {"fast": 20, "slow": 150},
    ]
    assert results["base_index"] == 3
    assert results["dataset"]["bars"] == 3 * 252
    assert results["dataset"]["quality"]["issues"] == 0
    assert results["seeds"]["dataset"] == 42 and results["seeds"]["alternative_paths"] == [43]
    top = results["headline"]
    assert set(top) >= {
        "params",
        "metrics",
        "equity_curve",
        "yearly",
        "trades",
        "trades_total",
        "stdout",
    }
    assert top["params"] == spec["strategy"]["base"]
    assert set(top["metrics"]) >= METRIC_FIELDS | {
        "alpha",
        "beta",
        "var_95",
        "cvar_95",
        "round_trips",
    }
    assert set(top["equity_curve"][0]) == {"time", "equity", "benchmark", "drawdown"}
    rows = results["benchmarks"]["rows"]
    assert [r["id"] for r in rows] == ["strategy", "buy_hold", "trend", "cash"]
    assert all(set(r["metrics"]) == METRIC_FIELDS for r in rows)
    assert results["validation"]["train_test"]["status"] == "completed"
    walk = results["validation"]["walk_forward"]
    assert walk["status"] == "completed" and walk["folds"]
    assert set(walk["aggregate"]) >= {"mean_in_sample_sharpe", "out_of_sample", "decay"}
    surface = results["robustness"]["surface"]
    assert set(surface) >= {"configurations", "points", "base", "best", "stability", "influence"}
    assert surface["configurations"] == 4 and surface["base"] == 3
    assert set(results["robustness"]["costs"]) >= {"levels", "current_bps", "break_even_bps"}
    seeds = results["robustness"]["seeds"]
    assert seeds["status"] == "completed" and len(seeds["paths"]) == 1
    diagnostics = results["diagnostics"]
    assert set(diagnostics) == {
        "trials",
        "deflated_sharpe",
        "pbo",
        "random_timing",
        "concentration",
    }
    assert diagnostics["trials"] == {"run": 4, "strategy_configurations": 4}
    checks = results["redteam"]["checks"]
    assert checks[0]["id"] == "lookahead" and checks[0]["status"] == "pass"
    for check in checks:
        assert set(check) == {"id", "title", "status", "severity", "finding", "evidence", "lesson"}
        assert check["status"] in ("pass", "warn", "fail", "skip") and check["finding"]
    tally = results["redteam"]["risk"]
    assert tally["passed"] + tally["warnings"] + tally["failed"] + tally["skipped"] == len(checks)

    # Provenance: every fingerprint, and the result digest covers the stored results.
    prov = current["provenance"]
    assert prov["quanta_version"] == quanta.__version__ and prov["runtime"] == "guided"
    assert prov["engine"]["name"] == "quanta-research"
    assert set(prov["environment"]) >= {"python", "implementation", "numpy", "platform", "sha256"}
    assert prov["git_commit"] is None or isinstance(prov["git_commit"], str)
    for value in (
        prov["engine"]["sha256"],
        prov["environment"]["sha256"],
        prov["dataset"]["sha256"],
        prov["dataset"]["version_sha256"],
        prov["strategy"]["sha256"],
        prov["config_sha256"],
        prov["result_sha256"],
    ):
        assert HEX64.fullmatch(value), value
    assert prov["strategy"] == current["strategy"] == queued["strategy"]
    assert (prov["strategy"]["name"], prov["strategy"]["version"], prov["strategy"]["sha256"]) == (
        "Trend rule",
        1,
        code_sha,
    )
    dataset = prov["dataset"]
    assert dataset["kind"] == "synthetic" and dataset["key"].startswith("synthetic:")
    # Generated data is a pure function of its settings: one version, keyed by its bars.
    assert dataset["version"] == 1 and dataset["version_sha256"] == dataset["sha256"]
    assert (dataset["bars"], dataset["start"], dataset["end"]) == (
        3 * 252,
        results["dataset"]["start"],
        results["dataset"]["end"],
    )
    assert prov["configurations"] == 4 and prov["seeds"] == results["seeds"]
    assert prov["result_sha256"] == provenance.digest(results)


# ---------------------------------------------------------------- hypothesis and notebook


def test_hypothesis_locks_at_the_first_result_and_the_notebook_documents_it(client):
    detail = create(client, run=False)
    experiment_id = detail["id"]
    assert detail["status"] == detail["lifecycle"]["status"] == "CONFIGURED"
    assert detail["runs"] == [] and detail["active_run"] is None and detail["current"] is None
    assert detail["hypothesis_locked"] is False and detail["spec_changed"] is False
    assert detail["quality"] == {"score": None, "components": []}
    assert detail["notebook"] == {} and detail["reproduction"] is None
    assert [step for step, done in steps(detail).items() if done] == ["configured"]
    [row] = listed(client)
    assert (row["run_count"], row["risk"], row["metrics"], row["active"]) == (0, None, None, False)

    # Before any result the hypothesis may still be sharpened; registration restarts.
    revised = "Revised before any result: the crossover beats cash after costs."
    updated = patch(client, experiment_id, {"hypothesis": revised})
    assert updated["hypothesis"] == revised
    assert updated["hypothesis_registered_at"] > detail["hypothesis_registered_at"]
    # A write-up without a result does not document anything.
    written = {"conclusion": "Too early.", "limitations": "No data yet.", "decision": "trust"}
    updated = patch(client, experiment_id, {"notebook": written})
    assert updated["notebook"] == written
    assert updated["status"] == "CONFIGURED" and steps(updated)["documented"] is False

    run = finish(client, start(client, experiment_id)["id"])
    detail = get(client, experiment_id)
    assert detail["current"]["id"] == run["id"]
    assert detail["hypothesis_locked"] is True
    # The stored spec re-validated for the run is unchanged: nothing drifted.
    assert detail["spec_changed"] is False
    assert detail["status"] == "DOCUMENTED" and steps(detail)["documented"] is True
    assert scores(detail)["documentation"] == 100

    # After the first result the hypothesis is locked; the same text is not a change.
    response = client.patch(
        f"{API}/experiments/{experiment_id}", json={"hypothesis": "A new claim after the result."}
    )
    assert response.status_code == 409
    assert "locked" in response.json()["detail"]
    assert get(client, experiment_id)["hypothesis"] == revised
    assert patch(client, experiment_id, {"hypothesis": revised})["hypothesis"] == revised
    renamed = patch(client, experiment_id, {"title": "  Crossover after costs  "})
    assert renamed["title"] == "Crossover after costs" and renamed["hypothesis_locked"] is True
    undocumented = "PASSED" if detail["risk"] == "LOW" else "WARNINGS"

    # Notebook patches merge: fields left out are kept, an empty string clears one.
    cleared = patch(client, experiment_id, {"notebook": {"conclusion": ""}})
    assert cleared["notebook"] == {**written, "conclusion": ""}
    assert cleared["status"] == undocumented and steps(cleared)["documented"] is False
    assert scores(cleared)["documentation"] == 70
    restored = patch(client, experiment_id, {"notebook": {"conclusion": "  Survives costs.  "}})
    assert restored["notebook"] == {**written, "conclusion": "Survives costs."}
    assert restored["status"] == "DOCUMENTED"
    undecided = patch(client, experiment_id, {"notebook": {"decision": ""}})
    assert undecided["notebook"]["decision"] == "" and undecided["status"] == undocumented
    decided = patch(client, experiment_id, {"notebook": {"decision": "reject"}})
    assert decided["notebook"] == {**written, "conclusion": "Survives costs.", "decision": "reject"}
    assert decided["status"] == "DOCUMENTED"
    patch(client, experiment_id, {"notebook": {"decision": "maybe"}}, status=422)
    patch(client, experiment_id, {"notebook": {"conclusion": "x" * 8001}}, status=422)
    unchanged = patch(client, experiment_id, {})
    assert unchanged["notebook"] == decided["notebook"] and unchanged["title"] == renamed["title"]


# ---------------------------------------------------------------- reproduction


def test_rerun_reproduces_the_original_and_a_rerun_of_a_rerun_targets_it(client):
    detail, original = completed(client)
    experiment_id = detail["id"]
    queued = rerun(client, original["id"])
    assert set(queued) >= RUN_FIELDS
    assert (queued["kind"], queued["rerun_of"], queued["status"], queued["number"]) == (
        "rerun",
        original["id"],
        "queued",
        2,
    )
    copied = finish(client, queued["id"])
    reproduction = copied["reproduction"]
    assert reproduction["verdict"] == "identical"
    assert reproduction["output_identical"] is True
    assert reproduction["changed_inputs"] == []
    assert [i["id"] for i in reproduction["inputs"]] == [
        "dataset",
        "strategy",
        "config",
        "engine",
        "environment",
        "runtime",
        "trials",
    ]
    assert all(i["same"] and i["original"] == i["rerun"] for i in reproduction["inputs"])
    assert reproduction["metric_differences"] == []
    assert reproduction["largest_relative_difference"] == 0
    assert copied["provenance"]["result_sha256"] == original["provenance"]["result_sha256"]
    assert copied["results"] == original["results"]
    assert copied["spec"] == original["spec"]

    detail = get(client, experiment_id)
    assert detail["reproduction"] == reproduction
    assert steps(detail)["reproducible"] is True
    assert scores(detail)["reproducibility"] == 100
    assert detail["current"]["id"] == original["id"]
    assert [(r["kind"], r["number"]) for r in detail["runs"]] == [("rerun", 2), ("run", 1)]
    assert detail["run_count"] == 1 == listed(client)[0]["run_count"]
    # Reproduced but not written up: the result still reads as passed or warned.
    assert detail["status"] == ("PASSED" if detail["risk"] == "LOW" else "WARNINGS")

    # Reproducing the copy reproduces the original it copied.
    nested = rerun(client, copied["id"])
    assert (nested["kind"], nested["rerun_of"]) == ("rerun", original["id"])
    assert finish(client, nested["id"])["reproduction"]["verdict"] == "identical"
    rerun(client, str(uuid.uuid4()), status=404)

    documented = patch(
        client,
        experiment_id,
        {
            "notebook": {
                "conclusion": "The crossover lost to buy and hold on this path.",
                "limitations": "One synthetic path; costs fixed at 8 bps a fill.",
                "decision": "reject",
            }
        },
    )
    assert documented["status"] == documented["lifecycle"]["status"] == "REPRODUCIBLE"
    assert all(steps(documented).values())


def test_a_changed_strategy_registers_a_new_version_and_trials_accumulate(client):
    detail, first = completed(client)
    experiment_id = detail["id"]
    source = detail["spec"]["strategy"]["code"]
    spec = copy.deepcopy(detail["spec"])
    spec["strategy"]["code"] = source.replace("slow = sma(", "slow = ema(")
    assert spec["strategy"]["code"] != source
    updated = patch(client, experiment_id, {"spec": spec})
    assert updated["spec"] == spec and updated["spec_changed"] is True
    # A version is registered when a run freezes the source, not on every edit.
    assert [v["version"] for v in updated["strategy_versions"]] == [1]
    assert updated["current"]["id"] == first["id"]

    second = finish(client, start(client, experiment_id)["id"])
    assert second["strategy"]["version"] == 2
    assert (
        second["strategy"]["sha256"]
        == hashlib.sha256(spec["strategy"]["code"].encode()).hexdigest()
    )
    # Every configuration tried under this strategy name counts against the new result.
    assert second["spec"]["prior_trials"] == 4
    assert second["results"]["diagnostics"]["trials"] == {"run": 4, "strategy_configurations": 8}
    # Only the source moved: the configuration fingerprint (grid, data, costs) is the same.
    assert second["provenance"]["config_sha256"] == first["provenance"]["config_sha256"]
    assert second["provenance"]["strategy"]["sha256"] != first["provenance"]["strategy"]["sha256"]
    detail = get(client, experiment_id)
    assert [v["version"] for v in detail["strategy_versions"]] == [1, 2]
    assert detail["spec_changed"] is False and detail["current"]["id"] == second["id"]
    assert detail["run_count"] == 2

    # Restoring the old source reuses version 1: versions are content-addressed. Its four
    # configurations were already tried, so only version 2's four count as earlier trials.
    spec["strategy"]["code"] = source
    patch(client, experiment_id, {"spec": spec})
    third = finish(client, start(client, experiment_id)["id"])
    assert third["strategy"] == first["strategy"]
    assert third["spec"]["prior_trials"] == 4
    assert third["results"]["diagnostics"]["trials"] == {"run": 4, "strategy_configurations": 8}
    assert [v["version"] for v in get(client, experiment_id)["strategy_versions"]] == [1, 2]


def test_running_an_unchanged_specification_again_reproduces_its_result(client):
    # Repeating a configuration is not a new trial: the second run sees the same
    # multiple-testing count, so identical inputs give an identical result digest.
    detail, first = completed(client)
    second = finish(client, start(client, detail["id"])["id"])
    assert second["kind"] == "run" and second["number"] == first["number"] + 1
    assert second["spec"]["prior_trials"] == first["spec"]["prior_trials"] == 0
    assert second["results"]["diagnostics"]["trials"] == first["results"]["diagnostics"]["trials"]
    for key in ("dataset", "strategy"):
        assert second["provenance"][key]["sha256"] == first["provenance"][key]["sha256"]
    assert second["provenance"]["config_sha256"] == first["provenance"]["config_sha256"]
    assert second["provenance"]["result_sha256"] == first["provenance"]["result_sha256"]


def test_historical_data_is_versioned_and_a_changed_file_breaks_reproduction(client, imported):
    symbol, write = imported
    first_sha = write(seed=7)
    spec = small_spec()
    spec["dataset"] = {
        "kind": "historical",
        "params": {**spec["dataset"]["params"], "symbol": symbol},
    }
    detail, first = completed(client, spec=spec)
    experiment_id = detail["id"]
    dataset = first["provenance"]["dataset"]
    assert (dataset["kind"], dataset["key"], dataset["version"]) == (
        "historical",
        f"historical:{symbol}",
        1,
    )
    assert dataset["version_sha256"] == first_sha
    assert dataset["bars"] == first["results"]["dataset"]["bars"] == 3 * 252
    assert dataset["start"] == "2020-01-02"
    assert first["results"]["seeds"]["dataset"] is None
    assert first["results"]["seeds"]["alternative_paths"] == []
    assert first["results"]["robustness"]["seeds"]["status"] == "skipped"
    assert detail["dataset"] == f"{symbol} · imported · 3y"

    def versions():
        entries = client.get(f"{API}/options").json()["historical"]
        [entry] = [e for e in entries if e["symbol"] == symbol]
        return [(v["version"], v["sha256"]) for v in entry["versions"]]

    assert versions() == [(1, first_sha)]

    second_sha = write(seed=8)
    assert second_sha != first_sha
    copied = finish(client, rerun(client, first["id"])["id"])
    reproduction = copied["reproduction"]
    assert reproduction["verdict"] == "different" and reproduction["output_identical"] is False
    assert reproduction["changed_inputs"] == ["Dataset"]
    assert reproduction["metric_differences"]
    assert copied["provenance"]["dataset"]["version"] == 2
    assert copied["provenance"]["dataset"]["version_sha256"] == second_sha
    detail = get(client, experiment_id)
    assert detail["reproduction"]["verdict"] == "different"
    assert steps(detail)["reproducible"] is False
    assert scores(detail)["reproducibility"] == 50

    fresh = finish(client, start(client, experiment_id)["id"])
    assert fresh["provenance"]["dataset"]["version"] == 2
    assert fresh["provenance"]["dataset"]["version_sha256"] == second_sha
    assert fresh["provenance"]["dataset"]["sha256"] == copied["provenance"]["dataset"]["sha256"]
    assert versions() == [(1, first_sha), (2, second_sha)]


# ---------------------------------------------------------------- failures


def source(code):
    def change(spec):
        spec["strategy"]["code"] = code

    return change


def missing_dataset(spec):
    spec["dataset"] = {
        "kind": "historical",
        "params": {**spec["dataset"]["params"], "symbol": "NOSUCHFILE"},
    }


def missing_parameter(spec):
    spec["strategy"]["parameters"] = [{"name": "window", "values": [10, 20]}]
    spec["strategy"]["base"] = {"window": 10}


FAILURES = {
    "syntax error": (
        source('def strategy(data, params):\n    return data["close"] >\n'),
        "SyntaxError",
    ),
    "runtime error": (
        source('def strategy(data, params):\n    return data["close"] > 1 / 0\n'),
        "ZeroDivisionError",
    ),
    "grid ignored": (
        source('def strategy(data):\n    return data["close"] > data["sma_50"]\n'),
        "strategy(data, params)",
    ),
    "missing parameter": (missing_parameter, "has no row in the parameter grid"),
    "dataset missing": (missing_dataset, "No imported dataset named NOSUCHFILE"),
}


@pytest.mark.parametrize("change, message", FAILURES.values(), ids=list(FAILURES))
def test_a_run_that_cannot_complete_fails_with_a_readable_error(client, change, message):
    spec = small_spec()
    change(spec)
    detail = create(client, spec=spec)
    run = wait(client, detail["active_run"]["id"])
    assert run["status"] == run["stage"] == "failed"
    assert message in run["error"], run["error"]
    assert run["results"] is None and run["summary"] == {} and run["finished_at"]
    detail = get(client, detail["id"])
    assert detail["status"] == detail["lifecycle"]["status"] == "FAILED"
    assert detail["current"] is None and detail["risk"] is None
    assert detail["runs"][0]["error"] == run["error"]
    # A failed run proves nothing: the hypothesis stays open, and there is nothing to
    # reproduce or export.
    assert detail["hypothesis_locked"] is False
    patch(client, detail["id"], {"hypothesis": "Revised after the failure: it beats cash."})
    response = client.post(f"{API}/runs/{run['id']}/rerun")
    assert response.status_code == 409 and "completed run" in response.json()["detail"]
    assert client.get(f"{API}/experiments/{detail['id']}/report").status_code == 409


def grid(parameters, base):
    spec = small_spec()
    spec["strategy"].update(parameters=parameters, base=base)
    return spec


def historical_without_symbol():
    spec = small_spec()
    spec["dataset"]["kind"] = "historical"
    return spec


INVALID = {
    "over 60 configurations": (
        grid(
            [
                {"name": "a", "values": list(range(1, 9))},
                {"name": "b", "values": list(range(1, 9))},
            ],
            {"a": 1, "b": 1},
        ),
        "the limit is 60",
    ),
    "base outside the grid": (
        grid([{"name": "fast", "values": [10, 20]}], {"fast": 15}),
        "must be one of its grid values",
    ),
    "duplicate parameter names": (
        grid([{"name": "fast", "values": [10, 20]}, {"name": "fast", "values": [30]}], {}),
        "Parameter names must be distinct",
    ),
    "historical without a symbol": (
        historical_without_symbol(),
        "Choose an imported dataset symbol",
    ),
}


@pytest.mark.parametrize("spec, message", INVALID.values(), ids=list(INVALID))
def test_an_invalid_specification_is_refused(client, spec, message):
    response = client.post(f"{API}/experiments", json=body(spec=spec))
    assert response.status_code == 422, response.text
    assert message in response.text
    existing = create(client, run=False)
    response = client.patch(f"{API}/experiments/{existing['id']}", json={"spec": spec})
    assert response.status_code == 422 and message in response.text
    assert get(client, existing["id"])["spec"] == small_spec()
    assert [e["id"] for e in listed(client)] == [existing["id"]]


def test_a_short_hypothesis_or_blank_title_is_refused(client):
    create(client, run=False, hypothesis="Too short", status=422)
    create(client, run=False, title="   ", status=422)
    existing = create(client, run=False)
    patch(client, existing["id"], {"hypothesis": "Short"}, status=422)
    patch(client, existing["id"], {"title": ""}, status=422)
    assert [e["id"] for e in listed(client)] == [existing["id"]]


def test_a_lookahead_strategy_completes_but_is_invalid(client):
    spec = small_spec()
    spec["strategy"].update(
        code=(
            "from numpy import mean\n\n"
            "def strategy(data):\n"
            '    return data["close"] > mean(data["close"])\n'
        ),
        parameters=[],
        base={},
    )
    detail, run = completed(client, spec=spec)
    results = run["results"]
    assert results["configurations"] == [{}]
    assert results["valid"] is False and run["summary"]["valid"] is False
    assert results["lookahead"]["status"] == "fail"
    assert any(not check["match"] for check in results["lookahead"]["checks"])
    checks = {check["id"]: check for check in results["redteam"]["checks"]}
    assert checks["lookahead"]["status"] == "fail"
    assert (
        results["redteam"]["risk"]["level"] == "HIGH" and results["redteam"]["risk"]["failed"] >= 1
    )
    assert run["summary"]["risk"] == detail["risk"] == "HIGH"
    assert detail["status"] == "WARNINGS"
    note = client.get(f"{API}/experiments/{detail['id']}/report").text
    assert "Look-ahead detected: the figures below are not valid evidence." in note


# ---------------------------------------------------------------- limits


def test_one_run_at_a_time_per_owner(client, held):
    first = create(client)
    run_id = first["active_run"]["id"]
    assert first["active_run"]["status"] == "queued"  # its job is held
    for response in (
        client.post(f"{API}/experiments/{first['id']}/runs"),
        client.post(f"{API}/experiments", json=body(title="A second experiment")),
    ):
        assert response.status_code == 409, response.text
        assert "already in progress" in response.json()["detail"]
    # The refused create-and-run registered nothing.
    assert [e["id"] for e in listed(client)] == [first["id"]]

    # Another owner is not blocked by this one's run.
    with TestClient(app) as other:
        theirs = create(other)
        assert theirs["active_run"]["status"] == "queued"
        held.release()
        finish(other, theirs["active_run"]["id"])
    finish(client, run_id)
    # With the run finished, the owner may start the next one.
    finish(client, start(client, first["id"])["id"])


def test_a_full_queue_is_refused(client, monkeypatch):
    detail = create(client, run=False)
    monkeypatch.setattr(experiments, "MAX_PENDING", 0)
    response = client.post(f"{API}/experiments/{detail['id']}/runs")
    assert response.status_code == 503 and "queue is full" in response.json()["detail"]
    assert get(client, detail["id"])["runs"] == []
    response = client.post(f"{API}/experiments", json=body(title="Refused on a full queue"))
    assert response.status_code == 503, response.text
    # A create-and-run the queue refuses registers nothing.
    assert [e["id"] for e in listed(client)] == [detail["id"]]
    monkeypatch.undo()
    finish(client, start(client, detail["id"])["id"])


def test_run_starts_are_rate_limited(client):
    detail = create(client, run=False)  # registering without running costs nothing
    run = finish(client, start(client, detail["id"])["id"])
    # Refused starts count too: the budget is spent before the request is served.
    for _ in range(5):
        rerun(client, str(uuid.uuid4()), status=404)
    for response in (
        client.post(f"{API}/experiments/{detail['id']}/runs"),
        client.post(f"{API}/runs/{run['id']}/rerun"),
        client.post(f"{API}/experiments", json=body(title="Over budget")),
    ):
        assert response.status_code == 429, response.text
        assert response.headers["retry-after"] == "60"
    assert len(get(client, detail["id"])["runs"]) == 1
    create(client, run=False, title="Registered without a run")
    # The budget is per account: a signed-in researcher still starts runs.
    with TestClient(app) as member:
        signup(member)
        theirs = create(member)
        finish(member, theirs["active_run"]["id"])


def test_a_run_whose_worker_vanished_is_reported_interrupted(client, held):
    detail = create(client)
    experiment_id, run_id = detail["id"], detail["active_run"]["id"]
    # A queued run may wait longer for a worker than a running one may stay silent.
    edit_run(run_id, heartbeat_at=time.time() - experiments.STALE_RUNNING - 30)
    assert client.get(f"{API}/runs/{run_id}").json()["status"] == "queued"
    start(client, experiment_id, status=409)

    edit_run(run_id, heartbeat_at=time.time() - experiments.STALE_QUEUED - 5)
    run = client.get(f"{API}/runs/{run_id}").json()
    assert run["status"] == "interrupted"
    assert "stopped before this run finished" in run["error"] and run["finished_at"]
    detail = get(client, experiment_id)
    assert detail["status"] == "FAILED"
    assert detail["active"] is False and detail["active_run"] is None
    # The lost job, if it ever ran, does not resurrect the interrupted run.
    held.release()
    assert client.get(f"{API}/runs/{run_id}").json()["status"] == "interrupted"

    fresh = finish(client, start(client, experiment_id)["id"])
    assert fresh["number"] == 2
    detail = get(client, experiment_id)
    assert detail["current"]["id"] == fresh["id"]
    assert detail["status"] in ("PASSED", "WARNINGS")

    # A running run that stops reporting progress is interrupted after STALE_RUNNING.
    held.hold()
    silent = start(client, experiment_id)
    edit_run(
        silent["id"], status="running", heartbeat_at=time.time() - experiments.STALE_RUNNING - 5
    )
    assert listed(client)[0]["active"] is False
    assert client.get(f"{API}/runs/{silent['id']}").json()["status"] == "interrupted"
    held.release()
    assert client.get(f"{API}/runs/{silent['id']}").json()["status"] == "interrupted"
    assert get(client, experiment_id)["current"]["id"] == fresh["id"]


# ---------------------------------------------------------------- ownership


def assert_hidden(outsider, experiment_id, run_id, cookies=None):
    """Every endpoint answers 404 for someone else's experiment and run.

    `cookies`, when given, is restored before each request: the server answers a
    rejected guest token with a new guest cookie, which would replace it.
    """
    if cookies:
        outsider.cookies = cookies
    assert experiment_id not in [e["id"] for e in listed(outsider)]
    for method, path, payload in (
        ("GET", f"/experiments/{experiment_id}", None),
        ("PATCH", f"/experiments/{experiment_id}", {"title": "Taken over"}),
        ("DELETE", f"/experiments/{experiment_id}", None),
        ("GET", f"/experiments/{experiment_id}/report", None),
        ("GET", f"/experiments/{experiment_id}/report?format=html", None),
        ("POST", f"/experiments/{experiment_id}/runs", None),
        ("GET", f"/runs/{run_id}", None),
        ("POST", f"/runs/{run_id}/rerun", None),
    ):
        if cookies:
            outsider.cookies = cookies
        response = outsider.request(method, API + path, json=payload)
        assert response.status_code == 404, (method, path, response.status_code, response.text)


def test_experiments_are_private_to_their_owner(client):
    mine, my_run = completed(client)
    claims = jwt.decode(
        client.cookies.get("quanta_trading_guest"), options={"verify_signature": False}
    )
    # This guest's id, signed with a key other than the server's.
    forged = {"quanta_trading_guest": jwt.encode(claims, uuid.uuid4().hex * 2, algorithm="HS256")}
    with TestClient(app) as stranger, TestClient(app) as member, TestClient(app) as impostor:
        signup(member)
        # A guest without the cookie, a guest with the forged token and a signed-in
        # account all see nothing.
        assert_hidden(stranger, mine["id"], my_run["id"])
        assert_hidden(impostor, mine["id"], my_run["id"], cookies=forged)
        assert_hidden(member, mine["id"], my_run["id"])
        assert listed(member) == [] and listed(stranger) == []
        impostor.cookies = forged
        response = impostor.get(f"{API}/experiments")
        assert response.json() == {"experiments": []}
        # The forged token is rejected and replaced by a new guest identity.
        reissued = jwt.decode(
            response.cookies["quanta_trading_guest"], options={"verify_signature": False}
        )
        assert reissued["sub"] != claims["sub"]

        # Every guest client in this test shares one run budget (keyed by host).
        limiter.records.clear()
        theirs, their_run = completed(member)
        for outsider in (client, stranger):
            assert_hidden(outsider, theirs["id"], their_run["id"])
        assert [e["id"] for e in listed(member)] == [theirs["id"]]

    # Nothing the outsiders tried changed either experiment.
    assert [e["id"] for e in listed(client)] == [mine["id"]]
    after = get(client, mine["id"])
    assert after["title"] == mine["title"] and [r["id"] for r in after["runs"]] == [my_run["id"]]


# ---------------------------------------------------------------- reports


def test_report_downloads_and_escaped_learner_text(client):
    attack = "<script>alert(1)</script> <img src=x onerror=alert(1)>"
    title = f"Crossover {attack}"
    hypothesis = f"The crossover beats cash {attack}"
    conclusion = f"It did not {attack}"
    limitations = f"One path {attack}"
    spec = small_spec()
    spec["strategy"]["name"] = "Trend <script>alert(1)</script>"
    detail = create(client, run=False, spec=spec, title=title, hypothesis=hypothesis)
    experiment_id = detail["id"]
    response = client.get(f"{API}/experiments/{experiment_id}/report")
    assert response.status_code == 409 and "Run the experiment" in response.json()["detail"]

    run = finish(client, start(client, experiment_id)["id"])
    notebook = {"conclusion": conclusion, "limitations": limitations, "decision": "inconclusive"}
    patch(client, experiment_id, {"notebook": notebook})
    stem = f"quanta-experiment-{detail['number']}"

    markdown = client.get(f"{API}/experiments/{experiment_id}/report?format=markdown")
    assert markdown.status_code == 200, markdown.text
    assert markdown.headers["content-type"] == "text/markdown; charset=utf-8"
    assert markdown.headers["content-disposition"] == f'attachment; filename="{stem}.md"'
    assert markdown.headers["cache-control"] == "no-store"
    assert client.get(f"{API}/experiments/{experiment_id}/report").text == markdown.text
    note = markdown.text
    assert note.startswith(f"# {title}\n")
    assert f"> {hypothesis}" in note
    assert "## Research red team" in note
    for check in run["results"]["redteam"]["checks"]:
        assert check["title"] in note
    assert conclusion in note and limitations in note and "Decision: Inconclusive" in note
    assert "## Provenance" in note
    prov = run["provenance"]
    for fingerprint in (
        prov["dataset"]["sha256"],
        prov["strategy"]["sha256"],
        prov["config_sha256"],
        prov["engine"]["sha256"],
        prov["environment"]["sha256"],
        prov["result_sha256"],
    ):
        assert fingerprint in note

    page = client.get(f"{API}/experiments/{experiment_id}/report?format=html")
    assert page.status_code == 200, page.text
    assert page.headers["content-type"] == "text/html; charset=utf-8"
    assert page.headers["content-disposition"] == f'attachment; filename="{stem}.html"'
    assert "default-src 'none'" in page.headers["content-security-policy"]
    text = page.text
    # The escaped text keeps "onerror=" as harmless characters, so look for tags instead.
    assert "<script" not in text.lower() and "<img" not in text.lower()
    tags = Tags(text).found
    assert not {"script", "img", "iframe", "object", "embed"} & {tag for tag, _ in tags}
    assert not [name for _, attrs in tags for name, _ in attrs if name.startswith("on")]
    for typed in (title, spec["strategy"]["name"]):
        assert html.escape(typed) in text
    for paragraph in (hypothesis, conclusion, limitations):
        assert f"<p>{html.escape(paragraph)}</p>" in text
    assert client.get(f"{API}/experiments/{experiment_id}/report?format=pdf").status_code == 422


# ---------------------------------------------------------------- delete and headers


def test_delete_removes_the_experiment_and_its_runs(client, held):
    detail = create(client)
    experiment_id, run_id = detail["id"], detail["active_run"]["id"]
    response = client.delete(f"{API}/experiments/{experiment_id}")
    assert response.status_code == 409 and "Wait for the run" in response.json()["detail"]
    assert get(client, experiment_id)["active_run"]["id"] == run_id
    held.release()
    finish(client, run_id)
    copy_id = finish(client, rerun(client, run_id)["id"])["id"]

    response = client.delete(f"{API}/experiments/{experiment_id}")
    assert response.status_code == 200 and response.json() == {"ok": True}
    assert client.get(f"{API}/experiments/{experiment_id}").status_code == 404
    for gone in (run_id, copy_id):
        assert client.get(f"{API}/runs/{gone}").status_code == 404
    assert client.get(f"{API}/experiments/{experiment_id}/report").status_code == 404
    assert client.delete(f"{API}/experiments/{experiment_id}").status_code == 404
    assert listed(client) == []
    with Session(engine) as db:
        assert db.get(ResearchExperiment, experiment_id) is None
        query = select(ResearchRun).where(ResearchRun.experiment_id == experiment_id)
        assert db.exec(query).all() == []


def test_research_responses_are_never_cached(client):
    created = client.post(f"{API}/experiments", json=body(run=False))
    experiment_id = created.json()["id"]
    responses = [
        created,
        client.get(f"{API}/options"),
        client.get(f"{API}/experiments"),
        client.get(f"{API}/experiments/{experiment_id}"),
        client.patch(f"{API}/experiments/{experiment_id}", json={"title": "Renamed"}),
        client.get(f"{API}/experiments/{experiment_id}/report"),
        client.get(f"{API}/experiments/{uuid.uuid4()}"),
        client.get(f"{API}/runs/{uuid.uuid4()}"),
        client.post(f"{API}/experiments", json={}),
        client.delete(f"{API}/experiments/{experiment_id}"),
    ]
    assert [r.status_code for r in responses] == [201, 200, 200, 200, 200, 409, 404, 404, 422, 200]
    for response in responses:
        assert response.headers["cache-control"] == "no-store", response.request.url
