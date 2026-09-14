import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import { EmptyState, Modal } from "@/shared/components/ui";

import { download } from "@/shared/lib/download";
import { percent } from "@/shared/lib/format";
import {
  ArrowUpRight,
  Download,
  FlaskConical,
  FolderOpen,
  Plus,
  Search,
  Trash2,
} from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
export default function Experiments() {
  const { state, update } = useWorkspace(),
    [query, setQuery] = useState(""),
    [deleteId, setDeleteId] = useState<string | null>(null);
  const experiments = state.experiments.filter((e) =>
    e.title.toLowerCase().includes(query.toLowerCase()),
  );
  return (
    <div className="page">
      <div className="page-eyebrow">REPRODUCIBLE RESEARCH</div>
      <div className="page-title-row">
        <div>
          <h1>Saved experiments</h1>
          <p className="page-subtitle">
            Every idea, with the code and assumptions that made it.
          </p>
        </div>
        <Link className="button primary" to="/lab">
          <Plus size={16} />
          New experiment
        </Link>
      </div>
      <div className="catalog-toolbar">
        <span className="muted">
          {state.experiments.length} saved{" "}
          {state.experiments.length === 1 ? "experiment" : "experiments"}
        </span>
        <label className="search-input compact">
          <Search size={16} />
          <input
            aria-label="Search experiments"
            placeholder="Find an experiment…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
      </div>
      {experiments.length ? (
        <div className="experiments-list">
          {experiments.map((e) => (
            <article className="experiment-card" key={e.id}>
              <div className="experiment-icon">
                <FlaskConical size={23} />
              </div>
              <div className="experiment-info">
                <Link to={`/lab?experiment=${e.id}`}>
                  <h3>
                    {e.title}
                    <ArrowUpRight size={15} />
                  </h3>
                </Link>
                <p>
                  <span className="tag">{e.config.dataset_type}</span>
                  <span>{e.config.dataset_params.model.toUpperCase()}</span>
                  <span>Seed {e.config.dataset_params.seed}</span>
                  <span>{new Date(e.updatedAt).toLocaleDateString()}</span>
                </p>
              </div>
              <div className="experiment-metric">
                <label>CAGR</label>
                <strong
                  className={e.metrics && e.metrics.cagr > 0 ? "positive" : ""}
                >
                  {percent(e.metrics?.cagr)}
                </strong>
              </div>
              <div className="experiment-metric">
                <label>MAX DRAWDOWN</label>
                <strong>{percent(e.metrics?.max_drawdown)}</strong>
              </div>
              <button
                className="icon-button"
                aria-label={`Export ${e.title}`}
                onClick={() => download(`quanta-${e.id}.json`, e)}
              >
                <Download size={16} />
              </button>
              <button
                className="icon-button"
                aria-label={`Delete experiment ${e.title}`}
                onClick={() => setDeleteId(e.id)}
              >
                <Trash2 size={16} />
              </button>
            </article>
          ))}
        </div>
      ) : (
        <EmptyState
          icon={<FolderOpen size={29} />}
          title={
            query ? "No matching experiments" : "An idea is worth revisiting."
          }
          description={
            query
              ? "Try a different search."
              : "Run a strategy in the sandbox and save it here. Your code, parameters, and summary results stay together."
          }
        >
          <Link to="/lab" className="button secondary">
            Open the strategy lab
            <ArrowUpRight size={15} />
          </Link>
        </EmptyState>
      )}
      <Modal
        open={!!deleteId}
        onOpenChange={(v) => {
          if (!v) setDeleteId(null);
        }}
        title="Delete this experiment?"
        description="Export it first if you want to keep a copy of its code and parameters."
      >
        <div className="dialog-actions">
          <button
            className="button secondary"
            onClick={() => setDeleteId(null)}
          >
            Keep experiment
          </button>
          <button
            className="button danger"
            onClick={() => {
              update((s) => ({
                ...s,
                experiments: s.experiments.filter((e) => e.id !== deleteId),
              }));
              setDeleteId(null);
            }}
          >
            Delete experiment
          </button>
        </div>
      </Modal>
    </div>
  );
}
