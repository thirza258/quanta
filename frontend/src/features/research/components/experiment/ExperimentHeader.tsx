import type {
  ExperimentDetail,
  ReportFormat,
} from "@/features/research/model/registry";
import type { ActionKind } from "@/features/research/model/experiment";
import {
  hasProvenance,
  LIFECYCLE_LABEL,
  LIFECYCLE_TONE,
  lifecycleSteps,
  riskTone,
} from "@/features/research/model/experiment";
import {
  ArrowLeft,
  Check,
  Database,
  Download,
  FlaskConical,
  LoaderCircle,
  PencilLine,
  Play,
  RotateCcw,
  ShieldAlert,
  ShieldCheck,
  ShieldQuestion,
  ShieldX,
  Trash2,
} from "lucide-react";
import { Link } from "react-router-dom";
import { StatusBadge } from "./ui";

const RISK_ICON = {
  LOW: ShieldCheck,
  MEDIUM: ShieldAlert,
  HIGH: ShieldX,
} as const;

export function ExperimentHeader({
  experiment,
  running,
  busy,
  exporting,
  onRun,
  onRerun,
  onExport,
  onDelete,
}: {
  experiment: ExperimentDetail;
  running: boolean;
  busy: ActionKind | null;
  exporting: ReportFormat | null;
  onRun: () => void;
  onRerun: () => void;
  onExport: (format: ReportFormat) => void;
  onDelete: () => void;
}) {
  const current = experiment.current;
  const latestVersion = experiment.strategy_versions.reduce<number | null>(
    (max, v) => (max == null || v.version > max ? v.version : max),
    null,
  );
  const strategyName = current?.strategy.name ?? experiment.strategy;
  const version = current?.strategy.version ?? latestVersion;
  const dataset = hasProvenance(current?.provenance)
    ? current.provenance.dataset.label
    : experiment.dataset;
  const RiskIcon = experiment.risk
    ? RISK_ICON[experiment.risk]
    : ShieldQuestion;
  const blocked = running || busy !== null;
  const blockedTitle = running
    ? "A run is in progress"
    : busy
      ? "Another action is in progress"
      : undefined;
  return (
    <header className="xd-header">
      <Link to="/research" className="text-link xd-back">
        <ArrowLeft size={15} aria-hidden="true" />
        Research registry
      </Link>
      <div className="page-eyebrow">EXPERIMENT #{experiment.number}</div>
      <div className="xd-title-row">
        <div className="xd-title-block">
          <h1>{experiment.title}</h1>
          <ul className="xd-meta" aria-label="Experiment details">
            <li>
              <FlaskConical size={14} aria-hidden="true" />
              <span className="sr-only">Strategy: </span>
              {strategyName}
              {version != null ? (
                <span className="xd-version">v{version}</span>
              ) : null}
            </li>
            <li>
              <Database size={14} aria-hidden="true" />
              <span className="sr-only">Dataset: </span>
              {dataset}
            </li>
            <li>
              {experiment.run_count}{" "}
              {experiment.run_count === 1 ? "run" : "runs"}
            </li>
          </ul>
        </div>
        <dl className="xd-verdict">
          <div>
            <dt>Research risk</dt>
            <dd>
              <StatusBadge
                tone={riskTone(experiment.risk)}
                size="large"
                icon={<RiskIcon size={17} aria-hidden="true" />}
                label={experiment.risk ?? "Not assessed"}
              />
            </dd>
          </div>
          <div>
            <dt>Research quality</dt>
            <dd className="xd-quality-score">
              <strong>{experiment.quality.score ?? "—"}</strong>
              <span>/ 100</span>
            </dd>
            <dd className="xd-hint">Process quality, not investment quality</dd>
          </div>
        </dl>
      </div>
      <div className="xd-lifecycle">
        <StatusBadge
          tone={LIFECYCLE_TONE[experiment.lifecycle.status]}
          label={LIFECYCLE_LABEL[experiment.lifecycle.status]}
          title="Lifecycle status"
        />
        <ol className="xd-stepper" aria-label="Research lifecycle">
          {lifecycleSteps(experiment.lifecycle).map((step, index) => (
            <li
              key={step.id}
              className={`is-${step.state}`}
              aria-current={step.state === "current" ? "step" : undefined}
            >
              <span className="xd-step-mark" aria-hidden="true">
                {step.state === "done" ? <Check size={12} /> : index + 1}
              </span>
              <span>{step.label}</span>
              <span className="sr-only">
                {step.state === "done"
                  ? " (done)"
                  : step.state === "current"
                    ? " (next)"
                    : " (not yet)"}
              </span>
            </li>
          ))}
        </ol>
      </div>
      <div className="xd-actions">
        <button
          type="button"
          className="button primary small"
          onClick={onRun}
          disabled={blocked}
          title={blockedTitle}
        >
          {busy === "run" ? (
            <LoaderCircle size={14} className="spin" aria-hidden="true" />
          ) : (
            <Play size={13} fill="currentColor" aria-hidden="true" />
          )}
          {experiment.runs.length ? "Run again" : "Run experiment"}
        </button>
        <button
          type="button"
          className="button secondary small"
          onClick={onRerun}
          disabled={blocked || !current}
          title={!current ? "Complete a run first" : blockedTitle}
        >
          {busy === "rerun" ? (
            <LoaderCircle size={14} className="spin" aria-hidden="true" />
          ) : (
            <RotateCcw size={14} aria-hidden="true" />
          )}
          Reproduce
        </button>
        <Link
          className="button secondary small"
          to={`/research/new?edit=${encodeURIComponent(experiment.id)}`}
        >
          <PencilLine size={14} aria-hidden="true" />
          Edit specification
        </Link>
        <div
          className="xd-export"
          role="group"
          aria-label="Export research note"
        >
          {(["markdown", "html"] as const).map((format) => (
            <button
              key={format}
              type="button"
              className="button secondary small"
              onClick={() => onExport(format)}
              disabled={exporting !== null}
              aria-label={`Export research note as ${format === "html" ? "HTML" : "Markdown"}`}
            >
              {exporting === format ? (
                <LoaderCircle size={14} className="spin" aria-hidden="true" />
              ) : (
                <Download size={14} aria-hidden="true" />
              )}
              {format === "html" ? "HTML" : "Markdown"}
            </button>
          ))}
        </div>
        <button
          type="button"
          className="button secondary small xd-delete"
          onClick={onDelete}
          disabled={busy !== null}
        >
          <Trash2 size={14} aria-hidden="true" />
          Delete
        </button>
      </div>
    </header>
  );
}
