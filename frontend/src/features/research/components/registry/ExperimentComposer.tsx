import {
  composerIssues,
  resolveGrid,
  specFromForm,
  type ComposerForm,
} from "@/features/research/model/grid";
import type {
  ExperimentSpec,
  ResearchOptions,
} from "@/features/research/model/registry";
import { ApiError } from "@/shared/api/client";
import {
  ArrowRight,
  CircleAlert,
  CircleCheck,
  CircleDashed,
  LoaderCircle,
  Lock,
  Play,
  Save,
} from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { DataFields } from "./DataFields";
import { ComposerSection, FieldMessage, messageProps } from "./fields";
import { StrategyFields } from "./StrategyFields";
import { CostFields, ValidationFields } from "./ValidationFields";

export type ComposerSubmit = (
  input: { title: string; hypothesis: string; spec: ExperimentSpec },
  run: boolean,
) => Promise<void>;

type Failure = {
  message: string;
  hint?: string;
  link?: { to: string; label: string };
};

/** A failure the caller has already explained, e.g. "saved, but not run". */
export class SubmitFailure extends Error {
  constructor(public failure: Failure) {
    super(failure.message);
  }
}

function describeFailure(error: unknown, run: boolean, editing: boolean) {
  if (error instanceof SubmitFailure) return error.failure;
  const message =
    error instanceof Error ? error.message : "The request did not complete.";
  const status = error instanceof ApiError ? error.status : 0;
  if (!run || editing || !status) return { message };
  // The server refuses a run (busy owner, rate limit, full queue) before keeping
  // anything. A proxy's own 503 (backend down) arrives as "The API is unavailable…".
  const refused =
    status === 409 ||
    status === 429 ||
    (status === 503 && !message.startsWith("The API is unavailable"));
  if (refused)
    return {
      message,
      hint: "Nothing was registered. You can save without running now and start the run from the experiment page later.",
    };
  return { message };
}

const sections = [
  {
    id: "composer-question",
    label: "Question",
    owns: (key: string) => key === "title" || key === "hypothesis",
  },
  {
    id: "composer-data",
    label: "Data",
    owns: (key: string) => key.startsWith("dataset."),
  },
  {
    id: "composer-strategy",
    label: "Strategy",
    owns: (key: string) =>
      ["name", "code", "grid", "arity"].includes(key) ||
      key.startsWith("grid:"),
  },
  {
    id: "composer-validation",
    label: "Validation",
    owns: (key: string) => key.startsWith("validation."),
  },
  {
    id: "composer-costs",
    label: "Costs",
    owns: (key: string) => key.startsWith("costs."),
  },
];

// Fields that start empty explain themselves only after a blur or a submit.
const quiet = new Set(["title", "hypothesis", "name", "dataset.symbol"]);

function jumpTo(id: string) {
  const heading = document.getElementById(`${id}-title`);
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  heading?.scrollIntoView({
    behavior: reduce ? "auto" : "smooth",
    block: "start",
  });
  heading?.focus({ preventScroll: true });
}

export function ExperimentComposer({
  options,
  initial,
  editing,
  onSubmit,
}: {
  options: ResearchOptions;
  initial: ComposerForm;
  editing?: {
    number: number;
    hypothesisLocked: boolean;
    registeredAt: string;
    active: boolean;
  };
  onSubmit: ComposerSubmit;
}) {
  const { limits } = options;
  const [form, setForm] = useState(initial),
    [attempted, setAttempted] = useState(false),
    [touched, setTouched] = useState<Record<string, true>>({}),
    [busy, setBusy] = useState<"run" | "save" | null>(null),
    [failure, setFailure] = useState<Failure | null>(null),
    [focusRequest, setFocusRequest] = useState(0);
  const lock = useRef(false),
    mounted = useRef(true),
    formRef = useRef<HTMLFormElement>(null);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  useEffect(() => {
    if (!focusRequest) return;
    formRef.current
      ?.querySelector<HTMLElement>('[aria-invalid="true"], [data-issue]')
      ?.focus();
  }, [focusRequest]);
  const grid = useMemo(
    () => resolveGrid(form.grid, limits),
    [form.grid, limits],
  );
  const issues = useMemo(
    () => composerIssues(form, grid, options),
    [form, grid, options],
  );
  const visible = useMemo(
    () =>
      Object.fromEntries(
        Object.entries(issues).filter(
          ([key]) => attempted || touched[key] || !quiet.has(key),
        ),
      ),
    [issues, attempted, touched],
  );
  const issueCount = Object.keys(issues).length;
  const locked = !!editing?.hypothesisLocked;

  const patch = (next: Partial<ComposerForm>) => {
    setForm((current) => ({ ...current, ...next }));
    setFailure(null);
  };
  const touch = (key: string) =>
    setTouched((current) =>
      current[key] ? current : { ...current, [key]: true },
    );

  async function submit(run: boolean) {
    if (lock.current) return;
    if (issueCount) {
      setAttempted(true);
      setFocusRequest((n) => n + 1);
      return;
    }
    lock.current = true;
    setBusy(run ? "run" : "save");
    setFailure(null);
    try {
      await onSubmit(
        {
          title: form.title.trim(),
          hypothesis: form.hypothesis.trim(),
          spec: specFromForm(form, grid, options.defaults),
        },
        run,
      );
    } catch (error) {
      if (mounted.current) setFailure(describeFailure(error, run, !!editing));
    } finally {
      lock.current = false;
      if (mounted.current) setBusy(null);
    }
  }

  const titleError = visible.title,
    hypothesisError = visible.hypothesis;
  const registered = editing ? new Date(editing.registeredAt) : null;
  const hypothesisHint = locked ? (
    <>
      <Lock size={12} aria-hidden="true" /> Locked: registered
      {registered && !Number.isNaN(registered.getTime())
        ? ` on ${registered.toLocaleDateString()}`
        : ""}{" "}
      and frozen by the first completed run. Record what you learned in the
      conclusion instead.
    </>
  ) : (
    "It locks after the first completed run, so the record shows what you expected before the evidence."
  );
  return (
    <form
      ref={formRef}
      className="registry-composer"
      aria-label={
        editing
          ? `Edit experiment #${editing.number}`
          : "Register an experiment"
      }
      noValidate
      onSubmit={(event) => event.preventDefault()}
    >
      <div className="registry-composer-main">
        <ComposerSection
          id="composer-question"
          step={1}
          title="Question"
          description="What do you expect to happen, and which result would prove you wrong?"
        >
          <div
            className={`field registry-field${titleError ? " has-error" : ""}`}
          >
            <label htmlFor="composer-title">Title</label>
            <input
              id="composer-title"
              value={form.title}
              maxLength={limits.title}
              placeholder="Trend crossover survives realistic costs"
              autoComplete="off"
              {...messageProps("composer-title", titleError)}
              onChange={(event) => patch({ title: event.target.value })}
              onBlur={() => touch("title")}
            />
            <FieldMessage id="composer-title" error={titleError} />
          </div>
          <div
            className={`field registry-field registry-hypothesis${hypothesisError ? " has-error" : ""}${locked ? " is-locked" : ""}`}
          >
            <label htmlFor="composer-hypothesis">Hypothesis</label>
            <p id="composer-hypothesis-guidance" className="registry-guidance">
              A claim that could be shown false, written before you see results.
              Name the rule, the market, the benchmark, and the result that
              would count as failure.
            </p>
            <textarea
              id="composer-hypothesis"
              rows={5}
              value={form.hypothesis}
              readOnly={locked}
              maxLength={limits.hypothesis_max}
              placeholder="Holding while the 20-day average is above the 150-day average beats buy-and-hold on Sharpe out of sample after 8 bps of costs, and neighbouring settings do nearly as well. A lower Sharpe than buy-and-hold would refute it."
              aria-invalid={hypothesisError ? true : undefined}
              aria-describedby="composer-hypothesis-guidance composer-hypothesis-message"
              onChange={(event) => patch({ hypothesis: event.target.value })}
              onBlur={() => touch("hypothesis")}
            />
            <div className="registry-hypothesis-foot">
              <FieldMessage
                id="composer-hypothesis"
                error={hypothesisError}
                hint={hypothesisHint}
              />
              <span className="mono registry-count" aria-hidden="true">
                {form.hypothesis.trim().length} / {limits.hypothesis_max}
              </span>
            </div>
          </div>
        </ComposerSection>
        <ComposerSection
          id="composer-data"
          step={2}
          title="Data"
          description="The market the rule is tested on. A synthetic market is rebuilt exactly from its seed."
        >
          <DataFields
            dataset={form.dataset}
            options={options}
            issues={visible}
            onChange={(dataset) => patch({ dataset })}
          />
        </ComposerSection>
        <ComposerSection
          id="composer-strategy"
          step={3}
          title="Strategy"
          description="The rule and the parameter values it may choose from, fixed before any result exists."
        >
          <StrategyFields
            form={form}
            grid={grid}
            options={options}
            issues={visible}
            revealed={attempted}
            onChange={patch}
            onTouch={touch}
          />
        </ComposerSection>
        <ComposerSection
          id="composer-validation"
          step={4}
          title="Validation"
          description="How the result is checked on data the rule did not get to choose from."
        >
          <ValidationFields
            validation={form.validation}
            dataset={form.dataset}
            issues={visible}
            onChange={(validation) => patch({ validation })}
          />
        </ComposerSection>
        <ComposerSection
          id="composer-costs"
          step={5}
          title="Costs"
          description="What trading costs, so the edge is measured after paying for it."
        >
          <CostFields
            costs={form.costs}
            issues={visible}
            onChange={(costs) => patch({ costs })}
          />
        </ComposerSection>
      </div>
      <aside
        className="registry-composer-aside"
        aria-label="Registration summary"
      >
        <div className="registry-summary">
          <span className="registry-label">
            {editing ? `EXPERIMENT #${editing.number}` : "PRE-REGISTRATION"}
          </span>
          <ol className="registry-checklist">
            {sections.map((section, index) => {
              const count = Object.keys(issues).filter(section.owns).length;
              const state = !count ? "done" : attempted ? "error" : "todo";
              const Icon =
                state === "done"
                  ? CircleCheck
                  : state === "error"
                    ? CircleAlert
                    : CircleDashed;
              return (
                <li key={section.id} className={`is-${state}`}>
                  <button type="button" onClick={() => jumpTo(section.id)}>
                    <Icon size={15} aria-hidden="true" />
                    <span>
                      {index + 1}. {section.label}
                    </span>
                    <small>
                      {state === "done"
                        ? "Ready"
                        : state === "error"
                          ? `${count} to fix`
                          : "To complete"}
                    </small>
                  </button>
                </li>
              );
            })}
          </ol>
          <p className="registry-summary-count">
            <strong className="mono">{grid.complete ? grid.count : "—"}</strong>{" "}
            {grid.complete && grid.count === 1
              ? "configuration"
              : "configurations"}{" "}
            <small>(limit {limits.configurations})</small>
          </p>
          <p className="registry-hint">
            Each configuration is a trial. The more trials, the higher the bar a
            deflated Sharpe ratio has to clear.
          </p>
          {attempted && issueCount ? (
            <p className="registry-error" role="alert">
              {issueCount === 1
                ? "One thing to fix"
                : `${issueCount} things to fix`}{" "}
              before {editing ? "saving" : "registering"}. The first one is
              selected.
            </p>
          ) : null}
          {failure ? (
            <div className="error-message registry-failure" role="alert">
              <p>{failure.message}</p>
              {failure.hint ? <p>{failure.hint}</p> : null}
              {failure.link ? (
                <Link className="text-link" to={failure.link.to}>
                  {failure.link.label}
                  <ArrowRight size={14} />
                </Link>
              ) : null}
            </div>
          ) : null}
          <div className="registry-actions">
            <button
              type="button"
              className="button primary"
              disabled={!!busy}
              onClick={() => void submit(true)}
            >
              {busy === "run" ? (
                <LoaderCircle className="spin" size={15} />
              ) : (
                <Play size={13} fill="currentColor" />
              )}
              {busy === "run"
                ? editing
                  ? "Saving…"
                  : "Registering…"
                : editing
                  ? "Save & run"
                  : "Register & run"}
            </button>
            <button
              type="button"
              className="button secondary"
              disabled={!!busy}
              onClick={() => void submit(false)}
            >
              {busy === "save" ? (
                <LoaderCircle className="spin" size={15} />
              ) : (
                <Save size={14} />
              )}
              {busy === "save" ? "Saving…" : "Save without running"}
            </button>
          </div>
          <p className="registry-hint">
            {editing
              ? editing.active
                ? "A run is in progress: save now, and start the next run once it finishes."
                : "Earlier runs keep the specification they ran with; the next run uses this one."
              : "Registering stores the hypothesis with a timestamp. It locks after the first completed run."}
          </p>
        </div>
      </aside>
    </form>
  );
}
