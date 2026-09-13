import { useState } from "react";
import { Link } from "react-router-dom";
import {
  ArrowUpRight,
  Download,
  FileText,
  Plus,
  Search,
  Trash2,
} from "lucide-react";
import { useWorkspace } from "../lib/workspace";
import { download } from "../lib/api";
import { EmptyState, Modal } from "./ui";
import type { Note } from "../lib/types";
export default function Notebook() {
  const { state, update } = useWorkspace(),
    [query, setQuery] = useState(""),
    [editing, setEditing] = useState<Note | null>(null),
    [deleteId, setDeleteId] = useState<string | null>(null);
  const notes = state.notes.filter((n) =>
    `${n.title} ${n.body}`.toLowerCase().includes(query.toLowerCase()),
  );
  return (
    <div className="page">
      <div className="page-eyebrow">A RECORD OF YOUR THINKING</div>
      <div className="page-title-row">
        <div>
          <h1>My notebook</h1>
          <p className="page-subtitle">
            The questions, observations, and assumptions worth keeping.
          </p>
        </div>
        <button
          className="button primary"
          onClick={() =>
            setEditing({
              id: crypto.randomUUID(),
              title: "",
              body: "",
              updatedAt: new Date().toISOString(),
            })
          }
        >
          <Plus size={16} />
          New note
        </button>
      </div>
      <div className="catalog-toolbar">
        <label className="search-input compact">
          <Search size={16} />
          <input
            aria-label="Search notes"
            placeholder="Search your notes…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
        <button
          className="text-link"
          disabled={!state.notes.length}
          onClick={() =>
            download(
              "quanta-notebook.md",
              state.notes
                .map(
                  (n) =>
                    `# ${n.title}\n\n${n.body}\n\n${n.lessonId ? `Module ${n.lessonId} · ` : ""}${n.updatedAt}\n\n---`,
                )
                .join("\n\n"),
              "text/markdown",
            )
          }
        >
          <Download size={15} />
          Export notebook
        </button>
      </div>
      {notes.length ? (
        <div className="notes-grid">
          {notes.map((n) => (
            <article key={n.id} className="note-card">
              <div className="note-card-top">
                <span>
                  <FileText size={15} />
                  {n.lessonId ? `MODULE ${n.lessonId}` : "RESEARCH NOTE"}
                </span>
                <button
                  className="icon-button"
                  aria-label={`Delete note ${n.title}`}
                  onClick={() => setDeleteId(n.id)}
                >
                  <Trash2 size={14} />
                </button>
              </div>
              <button
                className="note-edit"
                onClick={() => setEditing({ ...n })}
              >
                <h3>{n.title}</h3>
                <p>{n.body}</p>
              </button>
              <footer>
                <span>
                  {new Date(n.updatedAt).toLocaleDateString("en-US", {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                  })}
                </span>
                {n.lessonId ? (
                  <Link className="text-link" to={`/learn/${n.lessonId}`}>
                    Go to lesson
                    <ArrowUpRight size={14} />
                  </Link>
                ) : null}
              </footer>
            </article>
          ))}
        </div>
      ) : (
        <EmptyState
          icon={<FileText size={28} />}
          title={
            query ? "No matching notes" : "Make space for a good question."
          }
          description={
            query
              ? "Try a different word or phrase."
              : "Capture insights as you read, or start a research note of your own."
          }
        >
          <button
            className="button secondary"
            onClick={() =>
              setEditing({
                id: crypto.randomUUID(),
                title: "",
                body: "",
                updatedAt: new Date().toISOString(),
              })
            }
          >
            <Plus size={16} />
            Write your first note
          </button>
        </EmptyState>
      )}
      <Modal
        open={!!editing}
        onOpenChange={(open) => {
          if (!open) setEditing(null);
        }}
        title={
          state.notes.some((n) => n.id === editing?.id)
            ? "Edit research note"
            : "A new line of thinking"
        }
        description="Notes are saved to your workspace."
        wide
      >
        {editing ? (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const note = { ...editing, updatedAt: new Date().toISOString() };
              update((s) => ({
                ...s,
                notes: [note, ...s.notes.filter((n) => n.id !== note.id)],
              }));
              setEditing(null);
            }}
          >
            <label className="field">
              Title
              <input
                autoFocus
                value={editing.title}
                onChange={(e) =>
                  setEditing({ ...editing, title: e.target.value })
                }
                placeholder="A question worth exploring"
                required
                maxLength={150}
              />
            </label>
            <label className="field">
              Your note
              <textarea
                rows={10}
                value={editing.body}
                onChange={(e) =>
                  setEditing({ ...editing, body: e.target.value })
                }
                placeholder="Write your observations, reasoning, and next steps…"
                required
                maxLength={20000}
              />
            </label>
            <button className="button primary full-width">Save note</button>
          </form>
        ) : null}
      </Modal>
      <Modal
        open={!!deleteId}
        onOpenChange={(open) => {
          if (!open) setDeleteId(null);
        }}
        title="Delete this note?"
        description="This removes the note from your workspace."
      >
        <div className="dialog-actions">
          <button
            className="button secondary"
            onClick={() => setDeleteId(null)}
          >
            Keep note
          </button>
          <button
            className="button danger"
            onClick={() => {
              update((s) => ({
                ...s,
                notes: s.notes.filter((n) => n.id !== deleteId),
              }));
              setDeleteId(null);
            }}
          >
            Delete note
          </button>
        </div>
      </Modal>
    </div>
  );
}
