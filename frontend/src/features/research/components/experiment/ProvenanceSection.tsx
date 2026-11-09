import type {
  ExperimentDetail,
  Reproduction,
  RunSummary,
} from "@/features/research/model/registry";
import type { ActionKind } from "@/features/research/model/experiment";
import {
  fingerprintRows,
  formatDuration,
  formatTimestamp,
  hasProvenance,
  REPRODUCTION,
  riskTone,
  RUN_STATUS,
  shortHash,
} from "@/features/research/model/experiment";
import { LoaderCircle, RotateCcw } from "lucide-react";
import { HashValue, SectionHeading, StatusBadge } from "./ui";

const HEX = /^[0-9a-f]{32,}$/i;
const showValue = (value: string) =>
  HEX.test(value) ? (
    <code title={value}>{shortHash(value)}</code>
  ) : (
    value || "—"
  );

const showDifference = (value: number | string | null) =>
  value == null ? "—" : typeof value === "number" ? String(value) : value;

/** Every run of the experiment, newest first. */
export function RunHistory({
  runs,
  currentId,
}: {
  runs: RunSummary[];
  currentId: string | null;
}) {
  const ordered = [...runs].sort((a, b) => b.number - a.number);
  const numberOf = (id: string | null) =>
    runs.find((run) => run.id === id)?.number;
  return (
    <div className="table-scroll xd-table xd-table-full">
      <table>
        <caption className="sr-only">Run history</caption>
        <thead>
          <tr>
            <th scope="col">Run</th>
            <th scope="col">Kind</th>
            <th scope="col">Status</th>
            <th scope="col">Created</th>
            <th scope="col" className="num">
              Duration
            </th>
            <th scope="col">Research risk</th>
            <th scope="col">Reproduction</th>
          </tr>
        </thead>
        <tbody>
          {ordered.map((run) => {
            const status = RUN_STATUS[run.status];
            const verdict = run.reproduction
              ? REPRODUCTION[run.reproduction.verdict]
              : null;
            const of = numberOf(run.rerun_of);
            return (
              <tr
                key={run.id}
                className={run.id === currentId ? "is-marked" : undefined}
              >
                <th scope="row">
                  #{run.number}
                  {run.id === currentId ? (
                    <span className="tag">shown</span>
                  ) : null}
                </th>
                <td>
                  {run.kind === "rerun"
                    ? `Rerun${of != null ? ` of #${of}` : ""}`
                    : "Run"}
                </td>
                <td>
                  <StatusBadge
                    tone={status.tone}
                    label={status.label}
                    title={run.error ?? undefined}
                  />
                </td>
                <td>{formatTimestamp(run.created_at)}</td>
                <td className="num">{formatDuration(run.duration_ms)}</td>
                <td>
                  {run.summary.risk ? (
                    <StatusBadge
                      tone={riskTone(run.summary.risk)}
                      label={run.summary.risk}
                    />
                  ) : (
                    "—"
                  )}
                </td>
                <td>
                  {verdict ? (
                    <StatusBadge tone={verdict.tone} label={verdict.label} />
                  ) : (
                    "—"
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function ReproductionPanel({ reproduction }: { reproduction: Reproduction }) {
  const verdict = REPRODUCTION[reproduction.verdict];
  return (
    <>
      <div className="xd-repro-verdict">
        <StatusBadge tone={verdict.tone} size="large" label={verdict.label} />
        <p>
          {verdict.text}{" "}
          {reproduction.output_identical
            ? "The result fingerprint is byte-for-byte the same."
            : `Largest relative difference in a metric: ${
                reproduction.largest_relative_difference < 0.001
                  ? reproduction.largest_relative_difference.toExponential(2)
                  : `${(reproduction.largest_relative_difference * 100).toFixed(2)}%`
              }.`}
        </p>
      </div>
      <div className="table-scroll xd-table xd-table-full">
        <table>
          <caption className="sr-only">
            Pinned inputs of the original run and the rerun
          </caption>
          <thead>
            <tr>
              <th scope="col">Input</th>
              <th scope="col">Status</th>
              <th scope="col">Original</th>
              <th scope="col">Rerun</th>
            </tr>
          </thead>
          <tbody>
            {reproduction.inputs.map((input) => (
              <tr key={input.id}>
                <th scope="row">{input.label}</th>
                <td>
                  <StatusBadge
                    tone={input.same ? "pass" : "warn"}
                    label={input.same ? "Same" : "Changed"}
                  />
                </td>
                <td>{showValue(input.original)}</td>
                <td>{showValue(input.rerun)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {reproduction.metric_differences.length ? (
        <>
          <h4 className="xd-subhead">Metric differences</h4>
          <div className="table-scroll xd-table xd-table-full">
            <table>
              <caption className="sr-only">
                Metrics that differ between the runs
              </caption>
              <thead>
                <tr>
                  <th scope="col">Metric</th>
                  <th scope="col" className="num">
                    Original
                  </th>
                  <th scope="col" className="num">
                    Rerun
                  </th>
                </tr>
              </thead>
              <tbody>
                {reproduction.metric_differences.map((row) => (
                  <tr key={row.metric}>
                    <th scope="row">{row.metric.replaceAll("_", " ")}</th>
                    <td className="num">{showDifference(row.original)}</td>
                    <td className="num">{showDifference(row.rerun)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <p className="fine-print">No metric differs between the two runs.</p>
      )}
    </>
  );
}

export function ProvenanceSection({
  experiment,
  running,
  busy,
  onRerun,
}: {
  experiment: ExperimentDetail;
  running: boolean;
  busy: ActionKind | null;
  onRerun: () => void;
}) {
  const run = experiment.current;
  const provenance = hasProvenance(run?.provenance) ? run.provenance : null;
  return (
    <section
      id="provenance"
      className="xd-section"
      aria-labelledby="provenance-title"
    >
      <SectionHeading
        id="provenance"
        eyebrow="PROVENANCE"
        title="Can someone else get the same answer?"
        description="Every input that shaped the result is pinned by a SHA-256 fingerprint, so a rerun can prove it reproduces."
      />
      <div className="xd-card">
        <div className="xd-card-head">
          <h3>Fingerprints{run ? ` · run #${run.number}` : ""}</h3>
          {run ? (
            <p className="xd-hint">
              Finished {formatTimestamp(run.finished_at)}
            </p>
          ) : null}
        </div>
        {provenance ? (
          <div className="table-scroll xd-table xd-table-full xd-fingerprints">
            <table>
              <caption className="sr-only">Provenance fingerprints</caption>
              <thead>
                <tr>
                  <th scope="col">Input</th>
                  <th scope="col">Detail</th>
                  <th scope="col">Fingerprint</th>
                </tr>
              </thead>
              <tbody>
                {fingerprintRows(provenance).map((row) => (
                  <tr key={row.id}>
                    <th scope="row">{row.label}</th>
                    <td className="xd-wrap">{row.detail || "—"}</td>
                    <td>
                      {row.hashLabel ? (
                        <HashValue value={row.hash} label={row.hashLabel} />
                      ) : (
                        <span className="muted">—</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="xd-hint">No provenance was recorded for this run.</p>
        )}
      </div>
      <div className="xd-card">
        <div className="xd-card-head">
          <h3>Reproduction</h3>
          <button
            type="button"
            className="button secondary small"
            onClick={onRerun}
            disabled={!run || running || busy !== null}
            title={running ? "A run is in progress" : undefined}
          >
            {busy === "rerun" ? (
              <LoaderCircle size={14} className="spin" aria-hidden="true" />
            ) : (
              <RotateCcw size={14} aria-hidden="true" />
            )}
            Reproduce this run
          </button>
        </div>
        {experiment.reproduction ? (
          <ReproductionPanel reproduction={experiment.reproduction} />
        ) : (
          <p className="xd-lede">
            Not reproduced yet. A rerun repeats run{" "}
            {run ? `#${run.number}` : ""} with the same pinned inputs and
            compares every fingerprint and metric.
          </p>
        )}
      </div>
      <div className="xd-card">
        <div className="xd-card-head">
          <h3>Run history</h3>
          <p className="xd-hint">
            {experiment.runs.length}{" "}
            {experiment.runs.length === 1 ? "run" : "runs"}
          </p>
        </div>
        <RunHistory runs={experiment.runs} currentId={run?.id ?? null} />
      </div>
    </section>
  );
}
