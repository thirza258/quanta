import "@/features/research/experiment-detail.css";
import { ExperimentHeader } from "@/features/research/components/experiment/ExperimentHeader";
import {
  HypothesisQuote,
  MethodCard,
  NotebookSection,
} from "@/features/research/components/experiment/NotebookSection";
import { OverviewSection } from "@/features/research/components/experiment/OverviewSection";
import {
  ProvenanceSection,
  RunHistory,
} from "@/features/research/components/experiment/ProvenanceSection";
import { RedTeamSection } from "@/features/research/components/experiment/RedTeamSection";
import { RobustnessSection } from "@/features/research/components/experiment/RobustnessSection";
import { RunProgress } from "@/features/research/components/experiment/RunProgress";
import { SectionNav } from "@/features/research/components/experiment/SectionNav";
import { ValidationSection } from "@/features/research/components/experiment/ValidationSection";
import { Notice } from "@/features/research/components/experiment/ui";
import type { ActionKind } from "@/features/research/model/experiment";
import {
  describeActionError,
  isRunActive,
  runNotice,
} from "@/features/research/model/experiment";
import type {
  ExperimentDetail as Experiment,
  ReportFormat,
  RunSummary,
} from "@/features/research/model/registry";
import { researchApi } from "@/features/research/model/registry";
import { ApiError } from "@/shared/api/client";
import { EmptyState, Loading, Modal } from "@/shared/components/ui";
import {
  FlaskConical,
  LoaderCircle,
  Play,
  RefreshCw,
  SearchX,
  TriangleAlert,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

type Load =
  | { status: "loading" }
  | { status: "not-found" }
  | { status: "error"; message: string }
  | { status: "ready"; experiment: Experiment };

const errorOf = (error: unknown) =>
  error instanceof ApiError
    ? error
    : new ApiError((error as Error)?.message || "Unexpected error.", 0);

const POLL_MS = 1000;

export default function ExperimentDetail() {
  const { experimentId = "" } = useParams();
  const navigate = useNavigate();
  const [state, setState] = useState<Load>({ status: "loading" });
  const [refreshError, setRefreshError] = useState("");
  // The run started from this page, tracked until the server reports it.
  const [launched, setLaunched] = useState<RunSummary | null>(null);
  // The latest polled state of the active run.
  const [live, setLive] = useState<RunSummary | null>(null);
  // Runs the poll has seen finish; a stale `active_run` is ignored for them.
  const [finished, setFinished] = useState<string[]>([]);
  const [pollError, setPollError] = useState("");
  const [busy, setBusy] = useState<ActionKind | null>(null);
  const [actionError, setActionError] = useState("");
  const [exporting, setExporting] = useState<ReportFormat | null>(null);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [deleteError, setDeleteError] = useState("");
  const request = useRef(0);
  const inFlight = useRef(false);
  const hasData = useRef(false);
  const retry = useRef(0);

  const load = useCallback(async (): Promise<Experiment | null> => {
    const id = ++request.current;
    try {
      const experiment = await researchApi.get(experimentId);
      if (id !== request.current) return null;
      hasData.current = true;
      setState({ status: "ready", experiment });
      setRefreshError("");
      return experiment;
    } catch (e) {
      if (id !== request.current) return null;
      const error = errorOf(e);
      if (error.status === 404 || error.status === 422) {
        hasData.current = false;
        setState({ status: "not-found" });
      } else if (hasData.current) setRefreshError(error.message);
      else setState({ status: "error", message: error.message });
      return null;
    }
  }, [experimentId]);

  // (Re)load when the route changes; reset everything tied to the old id.
  useEffect(() => {
    hasData.current = false;
    setState({ status: "loading" });
    setLaunched(null);
    setLive(null);
    setFinished([]);
    setActionError("");
    setRefreshError("");
    void load();
    return () => {
      request.current++;
      window.clearTimeout(retry.current);
    };
  }, [load]);

  const experiment = state.status === "ready" ? state.experiment : null;
  const serverActive =
    experiment?.active_run && isRunActive(experiment.active_run.status)
      ? experiment.active_run
      : null;
  const tracked = launched ?? serverActive;
  const activeId =
    tracked && !finished.includes(tracked.id) ? tracked.id : null;

  // Poll the active run every second (chained, never overlapping) until it
  // stops, then refetch the experiment for the new results.
  useEffect(() => {
    if (!activeId) return;
    let cancelled = false;
    let timer = 0;
    const settle = async () => {
      const fresh = await load();
      if (cancelled) return;
      setFinished((ids) => (ids.includes(activeId) ? ids : [...ids, activeId]));
      setLaunched((run) => (run?.id === activeId ? null : run));
      // The server may still list the run as active for a moment: look again.
      if (
        fresh?.active_run?.id === activeId &&
        isRunActive(fresh.active_run.status)
      ) {
        window.clearTimeout(retry.current);
        retry.current = window.setTimeout(() => void load(), 1500);
      }
    };
    const poll = async () => {
      try {
        const run = await researchApi.getRun(activeId);
        if (cancelled) return;
        setLive(run);
        setPollError("");
        if (!isRunActive(run.status)) {
          await settle();
          return;
        }
      } catch (e) {
        if (cancelled) return;
        const error = errorOf(e);
        if (error.status === 404) {
          await settle();
          return;
        }
        setPollError(error.message);
      }
      if (!cancelled) timer = window.setTimeout(poll, POLL_MS);
    };
    timer = window.setTimeout(poll, launched?.id === activeId ? 0 : POLL_MS);
    return () => {
      cancelled = true;
      window.clearTimeout(timer);
    };
    // `launched` only picks the first delay; restarting on it would double-poll.
  }, [activeId, load]);

  const start = useCallback(
    async (kind: "run" | "rerun") => {
      if (inFlight.current || !experiment) return;
      const runId = experiment.current?.id;
      if (kind === "rerun" && !runId) return;
      inFlight.current = true;
      setBusy(kind);
      setActionError("");
      setPollError("");
      try {
        const run =
          kind === "run"
            ? await researchApi.run(experiment.id)
            : await researchApi.rerun(runId!);
        if (isRunActive(run.status)) {
          setLive(run);
          setLaunched(run);
        }
        void load();
      } catch (e) {
        const error = errorOf(e);
        setActionError(describeActionError(error.status, error.message, kind));
        // A conflict usually means a run is already going: show it.
        if (error.status === 409) void load();
      } finally {
        inFlight.current = false;
        setBusy(null);
      }
    },
    [experiment, load],
  );
  const runAgain = useCallback(() => void start("run"), [start]);
  const reproduce = useCallback(() => void start("rerun"), [start]);

  const exportReport = useCallback(
    async (format: ReportFormat) => {
      if (!experiment) return;
      setExporting(format);
      setActionError("");
      try {
        await researchApi.downloadReport(experiment.id, format);
      } catch (e) {
        const error = errorOf(e);
        setActionError(
          describeActionError(error.status, error.message, "export"),
        );
      } finally {
        setExporting(null);
      }
    },
    [experiment],
  );

  const remove = async () => {
    if (!experiment || inFlight.current) return;
    inFlight.current = true;
    setBusy("delete");
    setDeleteError("");
    try {
      await researchApi.remove(experiment.id);
      navigate("/research", { replace: true });
    } catch (e) {
      const error = errorOf(e);
      setDeleteError(
        describeActionError(error.status, error.message, "delete"),
      );
      setBusy(null);
    } finally {
      inFlight.current = false;
    }
  };

  const applySaved = useCallback((updated: Experiment) => {
    request.current++; // a slower refetch must not overwrite the saved notebook
    hasData.current = true;
    setState({ status: "ready", experiment: updated });
  }, []);

  const order = useMemo(
    () => experiment?.spec.strategy.parameters.map((p) => p.name) ?? [],
    [experiment],
  );

  if (state.status === "loading")
    return (
      <div className="page xd">
        <Loading label="Loading experiment…" />
      </div>
    );

  if (state.status === "not-found")
    return (
      <div className="page xd">
        <EmptyState
          icon={<SearchX size={28} />}
          title="Experiment not found"
          description="It may have been deleted, or the link is incomplete."
        >
          <Link className="button secondary" to="/research">
            Back to the research registry
          </Link>
        </EmptyState>
      </div>
    );

  if (state.status === "error")
    return (
      <div className="page xd">
        <EmptyState
          icon={<TriangleAlert size={28} />}
          title="The experiment could not be loaded"
          description={state.message}
        >
          <div className="xd-inline-actions">
            <button
              type="button"
              className="button primary"
              onClick={() => {
                setState({ status: "loading" });
                void load();
              }}
            >
              <RefreshCw size={15} aria-hidden="true" />
              Try again
            </button>
            <Link className="button secondary" to="/research">
              Research registry
            </Link>
          </div>
        </EmptyState>
      </div>
    );

  const exp = state.experiment;
  const current = exp.current;
  const results = current?.results ?? null;
  const running = activeId !== null;
  const progressRun =
    live && live.id === activeId ? live : tracked && running ? tracked : null;
  const notice = running ? null : runNotice(exp.runs);
  const runButton = (label: string) => (
    <button
      type="button"
      className="button primary small"
      onClick={runAgain}
      disabled={running || busy !== null}
    >
      {busy === "run" ? (
        <LoaderCircle size={14} className="spin" aria-hidden="true" />
      ) : (
        <Play size={13} fill="currentColor" aria-hidden="true" />
      )}
      {label}
    </button>
  );

  return (
    <div className="page xd">
      <ExperimentHeader
        experiment={exp}
        running={running}
        busy={busy}
        exporting={exporting}
        onRun={runAgain}
        onRerun={reproduce}
        onExport={exportReport}
        onDelete={() => {
          setDeleteError("");
          setConfirmDelete(true);
        }}
      />
      <div className="xd-notices">
        {actionError ? (
          <Notice tone="fail" onDismiss={() => setActionError("")}>
            {actionError}
          </Notice>
        ) : null}
        {refreshError ? (
          <Notice
            tone="warn"
            title="The latest state could not be fetched."
            action={
              <button
                type="button"
                className="button secondary small"
                onClick={() => void load()}
              >
                <RefreshCw size={13} aria-hidden="true" />
                Retry
              </button>
            }
          >
            {refreshError}
          </Notice>
        ) : null}
        {results && !results.valid ? (
          <Notice
            tone="fail"
            title="Look-ahead detected: these results are not valid evidence."
          >
            The strategy's signals changed when future bars were removed, so it
            used information it could not have had. Fix the strategy and run
            again; the red team's look-ahead test shows where it diverged.
          </Notice>
        ) : null}
        {exp.spec_changed && current ? (
          <Notice
            tone="warn"
            title={`The specification changed since run #${current.number}.`}
            action={running ? null : runButton("Run again")}
          >
            The results below belong to the previous specification. Run again to
            test the current one.
          </Notice>
        ) : null}
        {current && notice?.kind === "failed" ? (
          <Notice tone="fail" title={`Run #${notice.run.number} failed.`}>
            {notice.run.error || "No error message was recorded."} Showing the
            results of run #{current.number}.
          </Notice>
        ) : null}
        {current && notice?.kind === "interrupted" ? (
          <Notice
            tone="warn"
            title={`Run #${notice.run.number} was interrupted before it finished.`}
          >
            Showing the results of run #{current.number}.
          </Notice>
        ) : null}
      </div>
      {running && progressRun ? (
        <RunProgress
          run={progressRun}
          pollError={pollError}
          hasResults={!!results}
        />
      ) : null}
      {results && current ? (
        <>
          <SectionNav />
          <OverviewSection experiment={exp} run={current} results={results} />
          <ValidationSection results={results} order={order} />
          <RobustnessSection results={results} />
          <RedTeamSection results={results} />
          <NotebookSection
            experiment={exp}
            results={results}
            onSaved={applySaved}
          />
          <ProvenanceSection
            experiment={exp}
            running={running}
            busy={busy}
            onRerun={reproduce}
          />
        </>
      ) : (
        <div className="xd-empty">
          {running ? null : notice?.kind === "never" ? (
            <EmptyState
              icon={<FlaskConical size={28} />}
              title="This hypothesis has not been tested yet."
              description="Run the experiment to backtest every configuration and let the red team try to break the result."
            >
              {runButton("Run experiment")}
            </EmptyState>
          ) : notice?.kind === "failed" ? (
            <div className="xd-card xd-failure" role="alert">
              <h2>Run #{notice.run.number} failed</h2>
              <pre className="xd-error-text">
                {notice.run.error || "No error message was recorded."}
              </pre>
              <p className="xd-hint">
                Fix the strategy or the specification, then run again.
              </p>
              <div className="xd-inline-actions">
                {runButton("Run again")}
                <Link
                  className="button secondary small"
                  to={`/research/new?edit=${encodeURIComponent(exp.id)}`}
                >
                  Edit specification
                </Link>
              </div>
            </div>
          ) : notice?.kind === "interrupted" ? (
            <div className="xd-card xd-failure" role="status">
              <h2>Run #{notice.run.number} was interrupted</h2>
              <p>
                The run stopped before it finished, for example because the
                server restarted. Nothing was recorded; start it again.
              </p>
              <div className="xd-inline-actions">{runButton("Run again")}</div>
            </div>
          ) : (
            <div className="xd-card xd-failure" role="status">
              <h2>No results to show</h2>
              <p>The latest run finished without results. Run it again.</p>
              <div className="xd-inline-actions">{runButton("Run again")}</div>
            </div>
          )}
          <HypothesisQuote experiment={exp} />
          <MethodCard spec={exp.spec} />
          {exp.runs.length ? (
            <div className="xd-card">
              <div className="xd-card-head">
                <h3>Run history</h3>
              </div>
              <RunHistory runs={exp.runs} currentId={null} />
            </div>
          ) : null}
        </div>
      )}
      <Modal
        open={confirmDelete}
        onOpenChange={(open) => {
          if (busy !== "delete") setConfirmDelete(open);
        }}
        title="Delete this experiment?"
        description={`Experiment #${exp.number}, its ${exp.runs.length} ${exp.runs.length === 1 ? "run" : "runs"} and its notebook will be removed. This cannot be undone; export the research note first if you want a copy.`}
      >
        {deleteError ? (
          <p className="error-message" role="alert">
            {deleteError}
          </p>
        ) : null}
        <div className="dialog-actions">
          <button
            type="button"
            className="button secondary"
            onClick={() => setConfirmDelete(false)}
            disabled={busy === "delete"}
          >
            Keep experiment
          </button>
          <button
            type="button"
            className="button danger"
            onClick={() => void remove()}
            disabled={busy === "delete"}
          >
            {busy === "delete" ? (
              <LoaderCircle size={15} className="spin" aria-hidden="true" />
            ) : null}
            Delete experiment
          </button>
        </div>
      </Modal>
    </div>
  );
}
