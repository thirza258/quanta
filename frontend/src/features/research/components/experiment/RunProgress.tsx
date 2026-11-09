import type { RunSummary } from "@/features/research/model/registry";
import {
  formatElapsed,
  progressFraction,
  runElapsed,
  stageLabel,
} from "@/features/research/model/experiment";
import { LoaderCircle } from "lucide-react";
import { useEffect, useState } from "react";

function useNow(interval: number) {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), interval);
    return () => window.clearInterval(timer);
  }, [interval]);
  return now;
}

/** Live status of a queued or running run, refreshed by the page's poll. */
export function RunProgress({
  run,
  pollError,
  hasResults,
}: {
  run: RunSummary;
  pollError: string;
  hasResults: boolean;
}) {
  const now = useNow(1000);
  const fraction = progressFraction(run.progress);
  const stage = stageLabel(run.stage, run.status);
  return (
    <section className="xd-progress" aria-labelledby="xd-progress-title">
      <div className="xd-progress-head">
        <LoaderCircle size={18} className="spin" aria-hidden="true" />
        <div>
          <h2 id="xd-progress-title">
            {run.kind === "rerun" ? "Reproducing" : "Running"} · run #
            {run.number}
          </h2>
          <p aria-live="polite">{stage}</p>
        </div>
        <span className="xd-progress-elapsed">
          Elapsed <strong>{formatElapsed(runElapsed(run, now))}</strong>
        </span>
      </div>
      <div
        className={`xd-progress-bar${fraction == null ? " is-indeterminate" : ""}`}
        role="progressbar"
        aria-label="Run progress"
        aria-valuemin={0}
        aria-valuemax={run.progress.total ?? undefined}
        aria-valuenow={fraction == null ? undefined : run.progress.done}
        aria-valuetext={
          fraction == null
            ? `${run.progress.done} steps done`
            : `${run.progress.done} of ${run.progress.total} steps`
        }
      >
        <span
          style={fraction == null ? undefined : { width: `${fraction * 100}%` }}
        />
      </div>
      <p className="xd-progress-foot">
        {fraction == null
          ? `${run.progress.done} steps done`
          : `${run.progress.done} of ${run.progress.total} steps · ${Math.round(fraction * 100)}%`}
        {hasResults
          ? " · The results below are from the previous completed run until this one finishes."
          : " · Results appear here when the run finishes."}
      </p>
      {pollError ? (
        <p className="xd-hint" role="status">
          Lost contact with the runner; retrying. {pollError}
        </p>
      ) : null}
    </section>
  );
}
