import type {
  Decision,
  ExperimentDetail,
  ExperimentSpec,
  Results,
} from "@/features/research/model/registry";
import { researchApi } from "@/features/research/model/registry";
import {
  appendLimitation,
  CHECK_STATUS,
  describeActionError,
  formatTimestamp,
  hasProvenance,
  methodSummary,
  normalizeNotebook,
  NOTEBOOK_LIMIT,
  notebookDirty,
  qualityBreakdown,
  suggestedLimitations,
} from "@/features/research/model/experiment";
import type { ApiError } from "@/shared/api/client";
import {
  Check,
  CircleHelp,
  LoaderCircle,
  Lock,
  Plus,
  Save,
  ShieldCheck,
  ShieldX,
} from "lucide-react";
import { useEffect, useState } from "react";
import { Meter, SectionHeading, ToneIcon } from "./ui";

const DECISIONS: {
  id: Exclude<Decision, "">;
  label: string;
  hint: string;
  Icon: typeof ShieldCheck;
}[] = [
  {
    id: "trust",
    label: "Trust",
    hint: "The evidence supports the hypothesis.",
    Icon: ShieldCheck,
  },
  {
    id: "reject",
    label: "Reject",
    hint: "The evidence contradicts it.",
    Icon: ShieldX,
  },
  {
    id: "inconclusive",
    label: "Inconclusive",
    hint: "The tests cannot tell.",
    Icon: CircleHelp,
  },
];

/** The registered hypothesis, quoted, with when it was locked in. */
export function HypothesisQuote({
  experiment,
}: {
  experiment: ExperimentDetail;
}) {
  return (
    <figure className="xd-quote">
      <figcaption>
        <span className="eyebrow">HYPOTHESIS</span>
        {experiment.hypothesis_locked ? (
          <span className="xd-lock">
            <Lock size={12} aria-hidden="true" />
            Locked
          </span>
        ) : null}
      </figcaption>
      <blockquote>
        <p>{experiment.hypothesis}</p>
      </blockquote>
      <p className="xd-hint">
        Registered {formatTimestamp(experiment.hypothesis_registered_at)}
        {experiment.hypothesis_locked
          ? ", before any result. It can no longer be edited."
          : ". It can be edited until the first run."}
      </p>
    </figure>
  );
}

/** A method section written from the specification the results came from. */
export function MethodCard({
  spec,
  datasetLabel,
  note,
}: {
  spec: ExperimentSpec;
  datasetLabel?: string | null;
  note?: string;
}) {
  return (
    <div className="xd-card">
      <div className="xd-card-head">
        <h3>Method</h3>
        <p className="xd-hint">Generated from the specification</p>
      </div>
      <dl className="xd-method">
        {methodSummary(spec, datasetLabel).map((line) => (
          <div key={line.label}>
            <dt>{line.label}</dt>
            <dd>{line.text}</dd>
          </div>
        ))}
      </dl>
      {note ? <p className="fine-print">{note}</p> : null}
    </div>
  );
}

export function NotebookSection({
  experiment,
  results,
  onSaved,
}: {
  experiment: ExperimentDetail;
  results: Results;
  onSaved: (experiment: ExperimentDetail) => void;
}) {
  const saved = normalizeNotebook(experiment.notebook);
  const [base, setBase] = useState(saved);
  const [draft, setDraft] = useState(saved);
  const [saving, setSaving] = useState(false);
  const [justSaved, setJustSaved] = useState(false);
  const [error, setError] = useState("");
  // A refetch brought a different server copy: adopt it unless edits are pending.
  if (notebookDirty(base, saved)) {
    setBase(saved);
    if (!notebookDirty(base, draft)) setDraft(saved);
  }
  const dirty = notebookDirty(saved, draft);
  useEffect(() => {
    if (!dirty) return;
    const warn = (event: BeforeUnloadEvent) => event.preventDefault();
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [dirty]);

  const edit = (patch: Partial<typeof draft>) => {
    setDraft({ ...draft, ...patch });
    setJustSaved(false);
  };
  const save = async () => {
    if (saving || !dirty) return;
    setSaving(true);
    setError("");
    try {
      const updated = await researchApi.update(experiment.id, {
        notebook: draft,
      });
      onSaved(updated);
      setJustSaved(true);
    } catch (e) {
      const err = e as ApiError;
      setError(describeActionError(err.status ?? 0, err.message, "save"));
    } finally {
      setSaving(false);
    }
  };

  const suggestions = suggestedLimitations(results.redteam.checks);
  const quality = qualityBreakdown(experiment.quality.components);
  const run = experiment.current;
  const datasetLabel = hasProvenance(run?.provenance)
    ? run.provenance.dataset.label
    : null;
  const state = saving
    ? "Saving…"
    : dirty
      ? "Unsaved changes"
      : justSaved
        ? "Saved"
        : "All changes saved";

  return (
    <section
      id="notebook"
      className="xd-section"
      aria-labelledby="notebook-title"
    >
      <SectionHeading
        id="notebook"
        eyebrow="RESEARCH NOTEBOOK"
        title="What do you conclude?"
        description="Write down the decision and its limits. The registered hypothesis and the method stay fixed; the conclusion is yours."
      />
      <HypothesisQuote experiment={experiment} />
      <MethodCard
        spec={run?.spec.experiment ?? experiment.spec}
        datasetLabel={datasetLabel}
        note={
          experiment.spec_changed && run
            ? `This describes the specification of run #${run.number}, which produced the results above. The specification has changed since.`
            : undefined
        }
      />
      <form
        className="xd-card xd-notebook"
        onSubmit={(event) => {
          event.preventDefault();
          void save();
        }}
      >
        <div className="xd-card-head">
          <h3>Conclusion</h3>
          <span
            className={`xd-save-state${dirty ? " is-dirty" : ""}`}
            role="status"
          >
            {dirty ? (
              <span className="xd-dirty-dot" aria-hidden="true" />
            ) : (
              <Check size={13} aria-hidden="true" />
            )}
            {state}
          </span>
        </div>
        <fieldset className="xd-decision-field">
          <legend>Decision</legend>
          <div className="segmented xd-decision">
            {DECISIONS.map(({ id, label, Icon }) => (
              <button
                key={id}
                type="button"
                className={draft.decision === id ? "active" : undefined}
                aria-pressed={draft.decision === id}
                onClick={() =>
                  edit({ decision: draft.decision === id ? "" : id })
                }
              >
                <Icon size={14} aria-hidden="true" />
                {label}
              </button>
            ))}
          </div>
          <p className="xd-hint">
            {DECISIONS.find((d) => d.id === draft.decision)?.hint ??
              "No decision recorded. Select again to clear a decision."}
          </p>
        </fieldset>
        <label className="field">
          Conclusion
          <textarea
            value={draft.conclusion}
            maxLength={NOTEBOOK_LIMIT}
            rows={6}
            placeholder="What did the evidence show, and how sure are you?"
            onChange={(event) => edit({ conclusion: event.target.value })}
            aria-describedby="conclusion-count"
          />
          <span id="conclusion-count" className="xd-counter">
            {draft.conclusion.length.toLocaleString("en-US")} /{" "}
            {NOTEBOOK_LIMIT.toLocaleString("en-US")}
          </span>
        </label>
        <label className="field">
          Limitations
          <textarea
            value={draft.limitations}
            maxLength={NOTEBOOK_LIMIT}
            rows={6}
            placeholder="What could make this conclusion wrong?"
            onChange={(event) => edit({ limitations: event.target.value })}
            aria-describedby="limitations-count"
          />
          <span id="limitations-count" className="xd-counter">
            {draft.limitations.length.toLocaleString("en-US")} /{" "}
            {NOTEBOOK_LIMIT.toLocaleString("en-US")}
          </span>
        </label>
        {suggestions.length ? (
          <div className="xd-suggestions">
            <h4 className="xd-subhead">Suggested limitations</h4>
            <p className="xd-hint">
              From the red team's warnings and failures.
            </p>
            <ul>
              {suggestions.map((item) => {
                const meta = CHECK_STATUS[item.status];
                const added = draft.limitations.includes(item.text);
                const next = appendLimitation(draft.limitations, item.text);
                return (
                  <li key={item.id}>
                    <ToneIcon tone={meta.tone} />
                    <span>
                      <strong>{item.title}.</strong>{" "}
                      {item.text.slice(item.title.length + 2)}
                      <span className="sr-only"> ({meta.label})</span>
                    </span>
                    <button
                      type="button"
                      className="button secondary small"
                      disabled={added || next.length > NOTEBOOK_LIMIT}
                      onClick={() => edit({ limitations: next })}
                    >
                      {added ? (
                        <Check size={13} aria-hidden="true" />
                      ) : (
                        <Plus size={13} aria-hidden="true" />
                      )}
                      {added ? "Added" : "Add"}
                      <span className="sr-only">
                        {" "}
                        to limitations: {item.title}
                      </span>
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>
        ) : null}
        {error ? (
          <p className="error-message" role="alert">
            {error}
          </p>
        ) : null}
        <div className="xd-save-row">
          <button
            type="submit"
            className="button primary small"
            disabled={!dirty || saving}
          >
            {saving ? (
              <LoaderCircle size={14} className="spin" aria-hidden="true" />
            ) : (
              <Save size={14} aria-hidden="true" />
            )}
            Save notebook
          </button>
          {dirty ? (
            <button
              type="button"
              className="button secondary small"
              disabled={saving}
              onClick={() => {
                setDraft(saved);
                setError("");
              }}
            >
              Discard changes
            </button>
          ) : null}
        </div>
      </form>
      <div className="xd-card">
        <div className="xd-card-head">
          <h3>Research quality</h3>
          <p className="xd-quality-total">
            <strong>{experiment.quality.score ?? "—"}</strong> / 100
          </p>
        </div>
        <p className="xd-caption">
          <strong>Research quality ≠ investment quality.</strong> It grades how
          thoroughly the claim was tested and recorded; a carefully documented
          losing strategy can score well.
        </p>
        {quality.length ? (
          <ul className="xd-quality">
            {quality.map((part) => (
              <li key={part.id}>
                <div className="xd-quality-head">
                  <strong>{part.label}</strong>
                  <span>
                    {Math.round(part.points)} / {Math.round(part.maxPoints)} pts
                  </span>
                </div>
                <Meter value={part.score / 100} label={`${part.label} score`} />
                <p>{part.note}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="xd-hint">The score appears once a run completes.</p>
        )}
      </div>
    </section>
  );
}
