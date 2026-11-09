import type { ExperimentSummary } from "@/features/research/model/registry";
import { decimal, percent } from "@/shared/lib/format";
import { Code2, Database, LoaderCircle } from "lucide-react";
import { Link } from "react-router-dom";
import { RiskBadge, StatusBadge } from "./Badges";

function formatDate(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? value
    : date.toLocaleDateString(undefined, {
        day: "numeric",
        month: "short",
        year: "numeric",
      });
}

const signClass = (value: number | null | undefined) =>
  value == null || value === 0 ? "" : value > 0 ? "positive" : "negative";

export function ExperimentCard({
  experiment: e,
}: {
  experiment: ExperimentSummary;
}) {
  const metrics = e.metrics;
  return (
    <article
      className={`registry-card${e.active ? " is-active" : ""}`}
      aria-busy={e.active || undefined}
    >
      <div className="registry-card-head">
        <span className="registry-card-number mono">#{e.number}</span>
        <h2 className="registry-card-title">
          <Link to={`/research/${e.id}`}>{e.title}</Link>
        </h2>
      </div>
      <div className="registry-card-badges">
        <StatusBadge status={e.status} />
        {e.risk ? <RiskBadge risk={e.risk} /> : null}
        {e.active && e.status !== "RUNNING" ? (
          <span className="registry-badge tone-active">
            <LoaderCircle size={13} className="spin" aria-hidden="true" />
            Run in progress
          </span>
        ) : null}
      </div>
      <p className="registry-card-meta">
        <span>
          <Code2 size={13} aria-hidden="true" />
          <span className="sr-only">Strategy: </span>
          {e.strategy}
        </span>
        <span>
          <Database size={13} aria-hidden="true" />
          <span className="sr-only">Dataset: </span>
          {e.dataset}
        </span>
      </p>
      {metrics ? (
        <dl className="registry-card-metrics">
          <div>
            <dt>CAGR</dt>
            <dd className={signClass(metrics.cagr)}>{percent(metrics.cagr)}</dd>
          </div>
          <div>
            <dt>Sharpe</dt>
            <dd>{decimal(metrics.sharpe)}</dd>
          </div>
          <div>
            <dt>Max drawdown</dt>
            <dd className={signClass(metrics.max_drawdown)}>
              {percent(metrics.max_drawdown)}
            </dd>
          </div>
        </dl>
      ) : (
        <p className="registry-card-pending">
          {e.active
            ? "Running the grid and the red-team checks…"
            : e.status === "FAILED"
              ? "The last run failed. Open the experiment to read why."
              : "No results yet."}
        </p>
      )}
      <p className="registry-card-updated">
        <span>
          {e.run_count} {e.run_count === 1 ? "run" : "runs"}
        </span>
        <span>
          Updated{" "}
          <time dateTime={e.updated_at}>{formatDate(e.updated_at)}</time>
        </span>
      </p>
    </article>
  );
}
