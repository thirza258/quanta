"""Experiment registry: ownership, versions, the run queue and reproduction.

An experiment holds a hypothesis, a specification and a write-up. Each run
freezes the specification, executes in a background job (the sandbox calls in
parallel, results in submission order) and stores results with provenance.
Status, progress and a heartbeat live in the database, so any request can
follow a run, and a run whose process died is reported as interrupted instead
of spinning for ever. Every query is scoped to the owner: a signed-in account
or the signed guest cookie the simulator already uses.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Literal

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import defer
from sqlmodel import Session, select

import quanta
from quanta.db.models import DatasetVersion, ResearchExperiment, ResearchRun, StrategyVersion
from quanta.db.session import engine
from quanta.domain.research import pipeline, provenance, redteam, report
from quanta.domain.research.diagnostics import data_quality
from quanta.domain.research.spec import (
    INDICATORS,
    MAX_CONFIGURATIONS,
    MAX_PARAMETERS,
    MAX_VALUES,
    TEMPLATES,
    ExperimentSpec,
    expand_grid,
)
from quanta.execution import runner
from quanta.services import market_data

log = logging.getLogger("quanta.research")
if not log.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(_handler)
    log.setLevel(logging.INFO)
    log.propagate = False

WORKERS = max(1, int(os.getenv("QUANTA_RESEARCH_WORKERS", str(min(4, os.cpu_count() or 2)))))
JOBS = ThreadPoolExecutor(max_workers=2, thread_name_prefix="quanta-research")
SANDBOX = ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix="quanta-research-sandbox")
MAX_PENDING = 8
MAX_EXPERIMENTS = 200
STALE_RUNNING = 90
STALE_QUEUED = 600
ACTIVE = ("queued", "running")
TITLE_MAX, HYPOTHESIS_MIN, HYPOTHESIS_MAX, NOTEBOOK_MAX = 120, 12, 2000, 8000
_pending = 0
_pending_lock = threading.Lock()
_version_lock = threading.Lock()
# Serializes the active-run check with the insert, so one owner cannot queue two runs at once.
_enqueue_lock = threading.Lock()
SUMMARY_METRICS = ("cagr", "sharpe", "max_drawdown", "turnover", "total_return")


class NotebookUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    conclusion: str | None = Field(None, max_length=NOTEBOOK_MAX)
    limitations: str | None = Field(None, max_length=NOTEBOOK_MAX)
    decision: Literal["trust", "reject", "inconclusive", ""] | None = None


class ExperimentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=TITLE_MAX)
    hypothesis: str = Field(min_length=HYPOTHESIS_MIN, max_length=HYPOTHESIS_MAX)
    spec: ExperimentSpec = Field(default_factory=ExperimentSpec)
    run: bool = True


class ExperimentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str | None = Field(None, min_length=1, max_length=TITLE_MAX)
    hypothesis: str | None = Field(None, min_length=HYPOTHESIS_MIN, max_length=HYPOTHESIS_MAX)
    spec: ExperimentSpec | None = None
    notebook: NotebookUpdate | None = None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------- options


def options() -> dict:
    with Session(engine) as db:
        versions = db.exec(
            select(DatasetVersion)
            .where(DatasetVersion.kind == "historical")
            .order_by(DatasetVersion.version)
        ).all()
    history = {}
    for row in versions:
        history.setdefault(row.key.split(":", 1)[1], []).append(
            {"version": row.version, "sha256": row.sha256, "created_at": row.created_at}
        )
    synthetic = market_data.provider("synthetic").symbols()
    return {
        "defaults": ExperimentSpec().model_dump(mode="json"),
        "limits": {
            "parameters": MAX_PARAMETERS,
            "values": MAX_VALUES,
            "configurations": MAX_CONFIGURATIONS,
            "code": 20000,
            "title": TITLE_MAX,
            "hypothesis_min": HYPOTHESIS_MIN,
            "hypothesis_max": HYPOTHESIS_MAX,
            "notebook": NOTEBOOK_MAX,
        },
        "synthetic": {
            "models": [
                {"id": s["id"], "label": s["label"]} for s in synthetic if s["kind"] == "model"
            ],
            "scenarios": [
                {"id": s["id"], "label": s["label"]} for s in synthetic if s["kind"] == "scenario"
            ],
        },
        "historical": [
            {"symbol": s["id"], "versions": history.get(s["id"], [])}
            for s in market_data.provider("historical").symbols()
        ],
        "indicators": [
            {"name": name, "signature": signature, "description": description}
            for name, signature, description in INDICATORS
        ],
        "templates": list(TEMPLATES),
    }


# ---------------------------------------------------------------- views


def _stale(run: ResearchRun) -> bool:
    if run.status not in ACTIVE:
        return False
    limit = STALE_QUEUED if run.status == "queued" else STALE_RUNNING
    return time.time() - run.heartbeat_at > limit


def _settle(db: Session, runs: list[ResearchRun]) -> None:
    """Report runs whose worker vanished (restart, reload, crash) as interrupted."""
    changed = False
    for run in runs:
        if _stale(run):
            run.status = "interrupted"
            run.error = "The server stopped before this run finished. Start it again."
            run.finished_at = _now()
            db.add(run)
            changed = True
    if changed:
        db.commit()


def _runs(db: Session, experiment_id: str, full: bool = False) -> list[ResearchRun]:
    query = select(ResearchRun).where(ResearchRun.experiment_id == experiment_id)
    if not full:
        query = query.options(defer(ResearchRun.results))
    runs = list(db.exec(query.order_by(ResearchRun.number.desc())).all())
    _settle(db, runs)
    return runs


def _current(runs: list[ResearchRun]) -> ResearchRun | None:
    return next((r for r in runs if r.kind == "run" and r.status == "completed"), None)


def _reproduction(runs: list[ResearchRun], current: ResearchRun | None) -> dict | None:
    if current is None:
        return None
    rerun = next(
        (
            r
            for r in runs
            if r.kind == "rerun" and r.rerun_of == current.id and r.status == "completed"
        ),
        None,
    )
    return rerun.reproduction if rerun else None


def _documented(notebook: dict) -> bool:
    return bool(
        notebook.get("conclusion") and notebook.get("limitations") and notebook.get("decision")
    )


def _lifecycle(exp: ResearchExperiment, runs, current, reproduction) -> dict:
    active = any(r.status in ACTIVE for r in runs)
    reproduced = bool(reproduction and reproduction["verdict"] in ("identical", "equivalent"))
    documented = _documented(exp.notebook)
    steps = [
        {"id": "configured", "label": "Hypothesis registered", "done": True},
        {"id": "completed", "label": "Backtested", "done": current is not None},
        {"id": "validated", "label": "Red-teamed", "done": current is not None},
        {"id": "documented", "label": "Documented", "done": current is not None and documented},
        {"id": "reproducible", "label": "Reproduced", "done": reproduced},
    ]
    if active:
        status = "RUNNING"
    elif current is None:
        status = "FAILED" if runs and runs[0].status in ("failed", "interrupted") else "CONFIGURED"
    elif documented and reproduced:
        status = "REPRODUCIBLE"
    elif documented:
        status = "DOCUMENTED"
    else:
        status = "PASSED" if current.summary.get("risk") == "LOW" else "WARNINGS"
    return {"status": status, "steps": steps}


def _dataset_label(spec: dict) -> str:
    params = spec["dataset"]["params"]
    if spec["dataset"]["kind"] == "historical":
        return f"{params.get('symbol')} · imported · {params['years']}y"
    scenario = params["scenario"]
    name = (
        market_data.SCENARIOS[scenario]
        if scenario != "custom"
        else market_data.MODELS[params["model"]]
    )
    return f"{name} · seed {params['seed']} · {params['years']}y"


def _run_view(run: ResearchRun, full: bool = False) -> dict:
    view = {
        "id": run.id,
        "experiment_id": run.experiment_id,
        "number": run.number,
        "kind": run.kind,
        "rerun_of": run.rerun_of,
        "status": run.status,
        "stage": run.stage,
        "progress": {"done": run.progress.get("done", 0), "total": run.progress.get("total")},
        "summary": run.summary or {},
        "reproduction": run.reproduction,
        "strategy": run.spec["strategy"],
        "error": run.error,
        "created_at": run.created_at,
        "started_at": run.started_at,
        "finished_at": run.finished_at,
        "duration_ms": run.duration_ms,
    }
    if full:
        view.update(spec=run.spec, provenance=run.provenance, results=run.results)
    return view


def _summary(exp: ResearchExperiment, runs: list[ResearchRun]) -> dict:
    current = _current(runs)
    reproduction = _reproduction(runs, current)
    return {
        "id": exp.id,
        "number": exp.number,
        "title": exp.title,
        "strategy": exp.spec["strategy"]["name"],
        "dataset": _dataset_label(exp.spec),
        "status": _lifecycle(exp, runs, current, reproduction)["status"],
        "risk": current.summary.get("risk") if current else None,
        "metrics": current.summary.get("metrics") if current else None,
        "run_count": sum(1 for r in runs if r.kind == "run"),
        "active": any(r.status in ACTIVE for r in runs),
        "created_at": exp.created_at,
        "updated_at": exp.updated_at,
    }


def _detail(db: Session, exp: ResearchExperiment) -> dict:
    runs = _runs(db, exp.id)
    current = _current(runs)
    full = db.get(ResearchRun, current.id) if current else None
    reproduction = _reproduction(runs, current)
    versions = db.exec(
        select(StrategyVersion)
        .where(
            StrategyVersion.owner == exp.owner, StrategyVersion.name == exp.spec["strategy"]["name"]
        )
        .order_by(StrategyVersion.version)
    ).all()
    active = next((r for r in runs if r.status in ACTIVE), None)
    return {
        **_summary(exp, runs),
        "hypothesis": exp.hypothesis,
        "hypothesis_registered_at": exp.hypothesis_registered_at,
        "hypothesis_locked": current is not None,
        "spec": exp.spec,
        "notebook": exp.notebook,
        "lifecycle": _lifecycle(exp, runs, current, reproduction),
        "quality": redteam.quality(
            full.results if full else None,
            {**exp.notebook, "hypothesis": exp.hypothesis},
            reproduction,
        ),
        "spec_changed": bool(full)
        and provenance.digest(full.spec["experiment"]) != provenance.digest(exp.spec),
        "strategy_versions": [
            {"version": v.version, "sha256": v.sha256, "created_at": v.created_at} for v in versions
        ],
        "runs": [_run_view(r) for r in runs],
        "active_run": _run_view(active) if active else None,
        "current": _run_view(full, full=True) if full else None,
        "reproduction": reproduction,
    }


def _owned(db: Session, owner: str, experiment_id: str) -> ResearchExperiment:
    exp = db.get(ResearchExperiment, experiment_id)
    if exp is None or exp.owner != owner:
        raise HTTPException(404, "Experiment not found.")
    return exp


# ---------------------------------------------------------------- experiments


def list_experiments(db: Session, owner: str) -> dict:
    experiments = db.exec(
        select(ResearchExperiment)
        .where(ResearchExperiment.owner == owner)
        .order_by(ResearchExperiment.updated_at.desc())
    ).all()
    runs = db.exec(
        select(ResearchRun)
        .where(ResearchRun.owner == owner)
        .options(defer(ResearchRun.results))
        .order_by(ResearchRun.number.desc())
    ).all()
    _settle(db, list(runs))
    grouped: dict[str, list[ResearchRun]] = {}
    for run in runs:
        grouped.setdefault(run.experiment_id, []).append(run)
    return {"experiments": [_summary(e, grouped.get(e.id, [])) for e in experiments]}


def get_experiment(db: Session, owner: str, experiment_id: str) -> dict:
    return _detail(db, _owned(db, owner, experiment_id))


def create(db: Session, owner: str, payload: ExperimentCreate) -> dict:
    count = db.exec(
        select(func.count())
        .select_from(ResearchExperiment)
        .where(ResearchExperiment.owner == owner)
    ).one()
    if count >= MAX_EXPERIMENTS:
        raise HTTPException(
            409, f"Delete an experiment first: the registry holds {MAX_EXPERIMENTS}."
        )
    if payload.run:
        _guard_active(db, owner)
    number = (
        db.exec(
            select(func.max(ResearchExperiment.number)).where(ResearchExperiment.owner == owner)
        ).one()
        or 0
    ) + 1
    now = _now()
    exp = ResearchExperiment(
        id=str(uuid.uuid4()),
        owner=owner,
        number=number,
        title=payload.title,
        hypothesis=payload.hypothesis,
        hypothesis_registered_at=now,
        spec=payload.spec.model_dump(mode="json"),
        notebook={},
        created_at=now,
        updated_at=now,
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    if payload.run:
        try:
            _enqueue(db, owner, exp, payload.spec, "run")
        except HTTPException:
            # The queue refused the run before inserting it (full, or another run won the
            # race): register nothing, so retrying the request cannot leave a duplicate.
            db.delete(exp)
            db.commit()
            raise
    return _detail(db, exp)


def update(db: Session, owner: str, experiment_id: str, payload: ExperimentUpdate) -> dict:
    exp = _owned(db, owner, experiment_id)
    data = payload.model_dump(exclude_unset=True)
    if data.get("hypothesis") is not None and data["hypothesis"] != exp.hypothesis:
        if _current(_runs(db, exp.id)) is not None:
            raise HTTPException(
                409,
                "The hypothesis was registered before the first result and is now locked. "
                "Record what you learned in the conclusion instead.",
            )
        exp.hypothesis = data["hypothesis"]
        exp.hypothesis_registered_at = _now()
    if data.get("title") is not None:
        exp.title = data["title"]
    if payload.spec is not None:
        exp.spec = payload.spec.model_dump(mode="json")
    if payload.notebook is not None:
        exp.notebook = {**exp.notebook, **payload.notebook.model_dump(exclude_unset=True)}
    exp.updated_at = _now()
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return _detail(db, exp)


def delete(db: Session, owner: str, experiment_id: str) -> dict:
    exp = _owned(db, owner, experiment_id)
    runs = _runs(db, exp.id)
    if any(r.status in ACTIVE for r in runs):
        raise HTTPException(409, "Wait for the run in progress to finish before deleting.")
    for run in runs:
        db.delete(run)
    db.flush()
    db.delete(exp)
    db.commit()
    return {"ok": True}


# ---------------------------------------------------------------- runs


def _guard_active(db: Session, owner: str) -> None:
    runs = list(
        db.exec(
            select(ResearchRun)
            .where(ResearchRun.owner == owner, ResearchRun.status.in_(ACTIVE))
            .options(defer(ResearchRun.results))
        ).all()
    )
    _settle(db, runs)
    if any(r.status in ACTIVE for r in runs):
        raise HTTPException(409, "A research run is already in progress. Wait for it to finish.")


def _strategy_version(db: Session, owner: str, name: str, code: str) -> StrategyVersion:
    sha = hashlib.sha256(code.encode()).hexdigest()
    query = select(StrategyVersion).where(
        StrategyVersion.owner == owner, StrategyVersion.name == name, StrategyVersion.sha256 == sha
    )
    # The lock covers this process; the unique constraints cover several API processes,
    # where a lost race on the version number is retried with the next number.
    with _version_lock:
        for _ in range(5):
            found = db.exec(query).first()
            if found:
                return found
            latest = (
                db.exec(
                    select(func.max(StrategyVersion.version)).where(
                        StrategyVersion.owner == owner, StrategyVersion.name == name
                    )
                ).one()
                or 0
            )
            row = StrategyVersion(
                id=str(uuid.uuid4()),
                owner=owner,
                name=name,
                version=latest + 1,
                sha256=sha,
                code=code,
            )
            db.add(row)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                continue
            db.refresh(row)
            return row
    raise HTTPException(503, "Could not register the strategy version. Try again.")


def _enqueue(db, owner, exp, spec: ExperimentSpec, kind: str, rerun_of: str | None = None) -> dict:
    with _enqueue_lock:
        return _enqueue_locked(db, owner, exp, spec, kind, rerun_of)


def _enqueue_locked(db, owner, exp, spec, kind, rerun_of) -> dict:
    global _pending
    _guard_active(db, owner)
    with _pending_lock:
        if _pending >= MAX_PENDING:
            raise HTTPException(503, "The research queue is full. Try again in a minute.")
        _pending += 1
    try:
        strategy = _strategy_version(db, owner, spec.strategy.name, spec.strategy.code)
        # The trial count is history, not specification: freeze it with the run so
        # that a rerun repeats the original's multiple-testing context exactly.
        if kind == "rerun":
            prior = db.get(ResearchRun, rerun_of).spec.get("prior_trials", 0)
        else:
            prior = _prior_trials(owner, spec, strategy.sha256)
        number = (
            db.exec(
                select(func.max(ResearchRun.number)).where(ResearchRun.experiment_id == exp.id)
            ).one()
            or 0
        ) + 1
        run = ResearchRun(
            id=str(uuid.uuid4()),
            experiment_id=exp.id,
            owner=owner,
            number=number,
            kind=kind,
            rerun_of=rerun_of,
            status="queued",
            stage="queued",
            progress={"done": 0, "total": None},
            spec={
                "experiment": spec.model_dump(mode="json"),
                "prior_trials": prior,
                "strategy": {
                    "id": strategy.id,
                    "name": strategy.name,
                    "version": strategy.version,
                    "sha256": strategy.sha256,
                },
            },
            heartbeat_at=time.time(),
        )
        db.add(run)
        exp.updated_at = _now()
        db.add(exp)
        db.commit()
        db.refresh(run)
        view = _run_view(run)
        JOBS.submit(_execute, run.id)
    except BaseException:
        with _pending_lock:
            _pending -= 1
        raise
    return view


def start_run(db: Session, owner: str, experiment_id: str) -> dict:
    exp = _owned(db, owner, experiment_id)
    return _enqueue(db, owner, exp, ExperimentSpec.model_validate(exp.spec), "run")


def rerun(db: Session, owner: str, run_id: str) -> dict:
    original = db.get(ResearchRun, run_id)
    if original is None or original.owner != owner:
        raise HTTPException(404, "Run not found.")
    if original.kind == "rerun" and original.rerun_of:
        original = db.get(ResearchRun, original.rerun_of)
    if original is None or original.status != "completed":
        raise HTTPException(409, "Only a completed run can be reproduced.")
    exp = _owned(db, owner, original.experiment_id)
    spec = ExperimentSpec.model_validate(original.spec["experiment"])
    return _enqueue(db, owner, exp, spec, "rerun", rerun_of=original.id)


def get_run(db: Session, owner: str, run_id: str) -> dict:
    run = db.get(ResearchRun, run_id)
    if run is None or run.owner != owner:
        raise HTTPException(404, "Run not found.")
    _settle(db, [run])
    return _run_view(run, full=True)


# ---------------------------------------------------------------- the job


class _Progress:
    """Throttled, thread-safe progress and heartbeat writes from a running job."""

    def __init__(self, run_id: str):
        self.run_id, self.lock, self.stage, self.last = run_id, threading.Lock(), None, 0.0

    def __call__(self, stage: str, done: int, total: int) -> None:
        with self.lock:
            now = time.time()
            if stage == self.stage and now - self.last < 0.4 and done < total:
                return
            self.stage, self.last = stage, now
            with Session(engine) as db:
                run = db.get(ResearchRun, self.run_id)
                if run is None or run.status != "running":
                    return
                run.stage, run.progress, run.heartbeat_at = (
                    stage,
                    {"done": done, "total": total},
                    now,
                )
                db.add(run)
                db.commit()


def _run_many(code: str):
    def run_many(jobs, on_done):
        def one(job):
            data, params = job
            try:
                output = runner.run(code, data, params)
            except runner.ExecutionError as error:
                output = {"error": str(error)}
            on_done()
            return output

        return list(SANDBOX.map(one, jobs))

    return run_many


def _dataset_version(described: dict, kind: str, bars: list[dict], bars_sha: str) -> DatasetVersion:
    """Register the dataset's content as a version, reusing it when the content is unchanged."""
    if kind == "historical":
        source = market_data.provider("historical")
        version_sha = described["file_sha256"]
        full = None
    else:
        version_sha, full = bars_sha, bars
    key = described["key"]
    query = select(DatasetVersion).where(
        DatasetVersion.key == key, DatasetVersion.sha256 == version_sha
    )
    with _version_lock, Session(engine) as db:
        for _ in range(5):
            found = db.exec(query).first()
            if found:
                return found
            if full is None:
                full = source.full(described["settings"]["symbol"])
            latest = (
                db.exec(
                    select(func.max(DatasetVersion.version)).where(DatasetVersion.key == key)
                ).one()
                or 0
            )
            row = _dataset_row(key, latest + 1, version_sha, kind, described, full)
            db.add(row)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                continue
            db.refresh(row)
            return row
    raise ValueError("Could not register the dataset version. Try again.")


def _dataset_row(key, version, version_sha, kind, described, full) -> DatasetVersion:
    return DatasetVersion(
        id=str(uuid.uuid4()),
        key=key,
        version=version,
        sha256=version_sha,
        kind=kind,
        meta={
            "label": described["label"],
            "source": described["source"],
            "settings": described["settings"],
            "bars": len(full),
            "start": full[0]["time"],
            "end": full[-1]["time"],
            "retrieved": described.get("file_modified") or _now(),
        },
        quality=data_quality(full),
    )


def _trial_keys(experiment: dict, strategy_sha: str) -> set[str]:
    """One key per configuration a run evaluates: the code, the data it saw and its params.

    Re-running the same configuration is not a new trial, so keys, not run sizes, are
    what the multiple-testing count adds up.
    """
    spec = ExperimentSpec.model_validate(experiment)
    dataset = spec.dataset.model_dump(mode="json")
    return {
        provenance.digest({"strategy": strategy_sha, "dataset": dataset, "params": params})[:24]
        for params in expand_grid(spec.strategy.parameters)
    }


def _prior_trials(owner: str, spec: ExperimentSpec, strategy_sha: str) -> int:
    """Distinct configurations of this strategy name tried in earlier completed runs,
    excluding the ones this run repeats."""
    name = spec.strategy.name
    with Session(engine) as db:
        rows = db.exec(
            select(ResearchRun.spec).where(
                ResearchRun.owner == owner,
                ResearchRun.kind == "run",
                ResearchRun.status == "completed",
            )
        ).all()
    earlier: set[str] = set()
    for frozen in rows:
        if frozen["experiment"]["strategy"]["name"] == name:
            earlier |= _trial_keys(frozen["experiment"], frozen["strategy"]["sha256"])
    return len(earlier - _trial_keys(spec.model_dump(mode="json"), strategy_sha))


def _finish(run_id: str, **changes) -> None:
    with Session(engine) as db:
        run = db.get(ResearchRun, run_id)
        # A reader may have declared the run interrupted (its heartbeat went quiet) and let
        # the owner start another; never bring it back, or two runs would be live at once.
        if run is None or run.status != "running":
            return
        for key, value in changes.items():
            setattr(run, key, value)
        run.heartbeat_at = time.time()
        db.add(run)
        db.commit()


def _execute(run_id: str) -> None:
    global _pending
    started = time.perf_counter()
    record = {"event": "research_run", "run_id": run_id}
    try:
        with Session(engine) as db:
            run = db.get(ResearchRun, run_id)
            if run is None or run.status != "queued":
                return
            run.status, run.stage, run.started_at = "running", "data", _now()
            run.heartbeat_at = time.time()
            db.add(run)
            db.commit()
            spec = ExperimentSpec.model_validate(run.spec["experiment"])
            strategy = run.spec["strategy"]
            kind, rerun_of = run.kind, run.rerun_of
            prior = run.spec.get("prior_trials", 0)
            record.update(
                experiment_id=run.experiment_id, kind=kind, strategy_version=strategy["version"]
            )
        source = market_data.provider(spec.dataset.kind)
        described = source.describe(spec.dataset.params)
        bars = source.bars(spec.dataset.params)
        bars_sha = provenance.digest(bars)
        version = _dataset_version(described, spec.dataset.kind, bars, bars_sha)
        record["dataset_version"] = f"{version.key}@v{version.version}"
        results = pipeline.execute(
            spec, bars, _run_many(spec.strategy.code), _Progress(run_id), prior
        )
        spec_json = spec.model_dump(mode="json")
        configuration = {
            "dataset": spec_json["dataset"],
            "strategy": {
                "parameters": spec_json["strategy"]["parameters"],
                "base": spec_json["strategy"]["base"],
            },
            "costs": spec_json["costs"],
            "validation": spec_json["validation"],
        }
        prov = {
            "quanta_version": quanta.__version__,
            "engine": provenance.ENGINE,
            "environment": provenance.ENVIRONMENT,
            "runtime": os.getenv("QUANTA_SANDBOX", "guided"),
            "git_commit": provenance.git_commit(),
            "dataset": {
                "kind": spec.dataset.kind,
                "key": version.key,
                "label": described["label"],
                "source": described["source"],
                "version": version.version,
                "version_sha256": version.sha256,
                "sha256": bars_sha,
                "bars": len(bars),
                "start": bars[0]["time"],
                "end": bars[-1]["time"],
            },
            "strategy": strategy,
            "config_sha256": provenance.digest(configuration),
            "seeds": results["seeds"],
            "configurations": len(results["configurations"]),
            "prior_trials": prior,
            "result_sha256": provenance.digest(results),
        }
        reproduction = None
        if kind == "rerun" and rerun_of:
            with Session(engine) as db:
                original = db.get(ResearchRun, rerun_of)
                if original is not None and original.results is not None:
                    reproduction = provenance.compare(
                        {"provenance": original.provenance, "results": original.results},
                        {"provenance": prov, "results": results},
                    )
        headline = results["headline"]["metrics"]
        risk = results["redteam"]["risk"]["level"]
        duration = round((time.perf_counter() - started) * 1000)
        _finish(
            run_id,
            status="completed",
            stage="completed",
            results=results,
            provenance=prov,
            reproduction=reproduction,
            summary={
                "risk": risk,
                "valid": results["valid"],
                "configurations": len(results["configurations"]),
                "metrics": {key: headline.get(key) for key in SUMMARY_METRICS},
            },
            finished_at=_now(),
            duration_ms=duration,
            error=None,
        )
        record.update(
            status="completed",
            risk=risk,
            configurations=len(results["configurations"]),
            engine_version=provenance.ENGINE["version"],
            result_sha256=prov["result_sha256"],
            verdict=(reproduction or {}).get("verdict"),
        )
    except (pipeline.StrategyFailure, ValueError, ArithmeticError) as error:
        message = str(error)[:1000] or type(error).__name__
        _finish(
            run_id,
            status="failed",
            stage="failed",
            error=message,
            finished_at=_now(),
            duration_ms=round((time.perf_counter() - started) * 1000),
        )
        record.update(status="failed", error=message)
    except Exception:
        log.exception("research run %s failed", run_id)
        _finish(
            run_id,
            status="failed",
            stage="failed",
            error="The research run failed unexpectedly. Try again; report it if it persists.",
            finished_at=_now(),
            duration_ms=round((time.perf_counter() - started) * 1000),
        )
        record.update(status="error")
    finally:
        with _pending_lock:
            _pending -= 1
        record.update(duration_ms=round((time.perf_counter() - started) * 1000), workers=WORKERS)
        log.info(json.dumps(record, default=str))


def idle(timeout: float = 60.0) -> bool:
    """Wait until no research job is queued or running in this process (used by tests)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        with _pending_lock:
            if _pending == 0:
                return True
        time.sleep(0.05)
    return False


# ---------------------------------------------------------------- reports


def report_file(db: Session, owner: str, experiment_id: str, fmt: str) -> tuple[str, str, str]:
    detail = get_experiment(db, owner, experiment_id)
    if detail["current"] is None:
        raise HTTPException(409, "Run the experiment before exporting its research note.")
    stem = f"quanta-experiment-{detail['number']}"
    if fmt == "html":
        return report.page(detail, detail["current"]), "text/html; charset=utf-8", f"{stem}.html"
    return report.markdown(detail, detail["current"]), "text/markdown; charset=utf-8", f"{stem}.md"
