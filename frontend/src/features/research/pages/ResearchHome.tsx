import { ExperimentCard } from "@/features/research/components/registry/ExperimentCard";
import { ResearchLoop } from "@/features/research/components/registry/ResearchLoop";
import {
  researchApi,
  type ExperimentSummary,
} from "@/features/research/model/registry";
import "@/features/research/research-registry.css";
import { EmptyState, Loading } from "@/shared/components/ui";
import {
  ArrowUpRight,
  CloudOff,
  FolderOpen,
  Microscope,
  Plus,
  RotateCcw,
  Search,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

const POLL_MS = 2000;
const RETRY_MS = 5000;

/** The registry list, refreshed every 2 s while any experiment has a run in progress. */
function useExperimentList() {
  const [experiments, setExperiments] = useState<ExperimentSummary[] | null>(
    null,
  );
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  const latest = useRef<ExperimentSummary[] | null>(null);
  useEffect(() => {
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    async function load() {
      try {
        const { experiments } = await researchApi.list();
        if (cancelled) return;
        latest.current = experiments;
        setExperiments(experiments);
        setError("");
        // The next request is scheduled only after this one has answered.
        if (experiments.some((e) => e.active))
          timer = setTimeout(load, POLL_MS);
      } catch (e) {
        if (cancelled) return;
        setError((e as Error).message);
        if (latest.current?.some((item) => item.active))
          timer = setTimeout(load, RETRY_MS);
      }
    }
    void load();
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [attempt]);
  return {
    experiments,
    error,
    retry: () => {
      setError("");
      setAttempt((n) => n + 1);
    },
  };
}

export default function ResearchHome() {
  const { experiments, error, retry } = useExperimentList();
  const [query, setQuery] = useState("");
  const needle = query.trim().toLowerCase();
  const shown = (experiments ?? []).filter(
    (e) =>
      !needle ||
      e.title.toLowerCase().includes(needle) ||
      e.strategy.toLowerCase().includes(needle) ||
      `#${e.number}` === needle.replace(/^#?/, "#"),
  );
  const total = experiments?.length ?? 0;
  const running = experiments?.filter((e) => e.active).length ?? 0;

  return (
    <div className="page registry-page">
      <div className="page-eyebrow">
        <span className="green-dot" />
        RESEARCH REGISTRY
      </div>
      <div className="page-title-row">
        <div>
          <h1>Don’t just backtest it. Try to break it.</h1>
          <p className="page-subtitle">
            Register a falsifiable hypothesis before you see a result. Quanta
            runs the rule across a parameter grid, attacks it with
            out-of-sample, overfitting and cost tests, and keeps the hashes
            needed to reproduce the verdict.
          </p>
        </div>
        <Link className="button primary" to="/research/new">
          <Plus size={16} />
          New experiment
        </Link>
      </div>
      <ResearchLoop />
      {experiments === null ? (
        error ? (
          <div role="alert">
            <EmptyState
              icon={<CloudOff size={28} />}
              title="The research registry is unavailable."
              description={error}
            >
              <button
                type="button"
                className="button secondary"
                onClick={retry}
              >
                <RotateCcw size={15} />
                Try again
              </button>
            </EmptyState>
          </div>
        ) : (
          <Loading label="Opening the registry…" />
        )
      ) : (
        <section aria-label="Registered experiments">
          <div className="catalog-toolbar registry-toolbar">
            <span className="muted" role="status">
              {needle
                ? `${shown.length} of ${total} ${total === 1 ? "experiment" : "experiments"}`
                : `${total} registered ${total === 1 ? "experiment" : "experiments"}`}
              {running ? ` · ${running} running` : ""}
            </span>
            {total ? (
              <label className="search-input compact">
                <Search size={16} />
                <input
                  type="search"
                  aria-label="Search experiments by title or strategy"
                  placeholder="Search title or strategy…"
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                />
              </label>
            ) : null}
          </div>
          {error ? (
            <p className="registry-note is-warning" role="status">
              The list could not be refreshed: {error}
              {running ? " Retrying…" : ""}
            </p>
          ) : null}
          {shown.length ? (
            <div className="registry-list">
              {shown.map((experiment) => (
                <ExperimentCard key={experiment.id} experiment={experiment} />
              ))}
            </div>
          ) : total ? (
            <EmptyState
              icon={<Search size={28} />}
              title="No matching experiments"
              description="Try another title or strategy name."
            >
              <button
                type="button"
                className="button secondary"
                onClick={() => setQuery("")}
              >
                Clear search
              </button>
            </EmptyState>
          ) : (
            <EmptyState
              icon={<Microscope size={28} />}
              title="Register your first hypothesis."
              description="Write down what you expect before you see a result. Quanta runs the rule across a parameter grid and tries to break it, so the evidence has to survive more than one lucky backtest."
            >
              <Link className="button primary" to="/research/new">
                <Plus size={16} />
                New experiment
              </Link>
            </EmptyState>
          )}
        </section>
      )}
      <aside className="registry-callout" aria-label="Sandbox snapshots">
        <span className="registry-callout-icon">
          <FolderOpen size={18} aria-hidden="true" />
        </span>
        <p>
          <strong>Have a sandbox snapshot?</strong> Saved experiments from the
          strategy lab record one run of one setting. Choose Validate on any of
          them to register it here with a hypothesis.
        </p>
        <Link className="text-link" to="/experiments">
          Browse snapshots
          <ArrowUpRight size={15} />
        </Link>
      </aside>
    </div>
  );
}
