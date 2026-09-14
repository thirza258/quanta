import { lazy, Suspense, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  BookmarkPlus,
  BookOpen,
  Check,
  ChevronRight,
  Clock3,
  Code2,
  Columns2,
  Play,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import remarkGfm from "remark-gfm";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import { findLesson, lessons, lessonTrack, trackLabel } from "../lib/catalog";
import { practiceComplete } from "../lib/learning";
import { useWorkspace } from "../lib/workspace";
import { Loading, Modal } from "./ui";
import PracticeQuestions from "./PracticeQuestions";
const Sandbox = lazy(() => import("./Sandbox"));
import type { Lesson } from "../lib/types";
export default function LessonReader() {
  const { user } = useWorkspace();
  const { lessonId } = useParams(),
    lesson = findLesson(lessonId || "");
  return lesson ? (
    <Reader key={`${user?.id ?? "guest"}:${lesson.id}`} lesson={lesson} />
  ) : (
    <div className="page">
      <h1>Lesson not found</h1>
      <Link to="/curriculum">Browse the curriculum</Link>
    </div>
  );
}
function Reader({ lesson }: { lesson: Lesson }) {
  const { state, update } = useWorkspace(),
    navigate = useNavigate(),
    track = lessonTrack(lesson.id)!,
    [view, setView] = useState<"split" | "reader" | "sandbox">(
      lesson.kind === "fundamentals" ? "reader" : "split",
    ),
    [noteOpen, setNoteOpen] = useState(false),
    [note, setNote] = useState(""),
    [templateVersion, setTemplateVersion] = useState(0);
  const completed = state.completed.includes(lesson.id),
    practicePassed = practiceComplete(lesson, state),
    exam = track.exams.find((exam) => exam.moduleIds.at(-1) === lesson.id),
    next = lessons[lessons.findIndex((l) => l.id === lesson.id) + 1];
  useEffect(() => {
    update((s) => ({ ...s, lastLesson: lesson.id }));
  }, [lesson.id, update]);
  return (
    <div className={`learning-room view-${view}`}>
      <div className="lesson-toolbar">
        <Link to={`/curriculum/${track.id}`} className="text-link">
          <ArrowLeft size={16} />
          <span>{track.title}</span>
        </Link>
        <div className="view-controls">
          <button
            className={view === "reader" ? "active" : ""}
            aria-label="Reading view"
            title="Reading view"
            onClick={() => setView("reader")}
          >
            <BookOpen size={16} />
          </button>
          <button
            className={view === "split" ? "active" : ""}
            aria-label="Split view"
            title="Split view"
            onClick={() => setView("split")}
          >
            <Columns2 size={16} />
          </button>
          <button
            className={view === "sandbox" ? "active" : ""}
            aria-label="Sandbox view"
            title="Sandbox view"
            onClick={() => setView("sandbox")}
          >
            <Code2 size={16} />
          </button>
        </div>
        <select
          className="lesson-select"
          aria-label="Navigate to module"
          value={lesson.id}
          onChange={(e) => navigate(`/learn/${e.target.value}`)}
        >
          {track.modules.map((m) => (
            <option key={m.id} value={m.id}>
              {m.id} {m.title}
            </option>
          ))}
        </select>
      </div>
      <div className="learning-panes">
        <article className="lesson-article">
          <div className="page-eyebrow">
            {trackLabel(track)}
            <ChevronRight size={12} />
            MODULE {lesson.id}
          </div>
          <h1>{lesson.title}</h1>
          <p className="lesson-subtitle">{lesson.subtitle}</p>
          <div className="lesson-meta">
            <span>
              <Clock3 size={14} />
              {lesson.minutes} min read
            </span>
            <span>
              <Code2 size={15} />
              Interactive lesson
            </span>
            <button className="text-link" onClick={() => setNoteOpen(true)}>
              <BookmarkPlus size={15} />
              Add a note
            </button>
          </div>
          <div className="lesson-objective">
            <span className="eyebrow">YOUR OBJECTIVE</span>
            <p>
              {lesson.objective ??
                "Explain the principle, reproduce the worked example, and identify an assumption that could change the result."}
            </p>
          </div>
          <div className="prose">
            <ReactMarkdown
              remarkPlugins={[remarkMath, remarkGfm]}
              rehypePlugins={[rehypeKatex]}
            >
              {lesson.content}
            </ReactMarkdown>
          </div>
          <div className="lesson-code-card">
            <div>
              <Code2 size={16} />
              <strong>Try the lesson template</strong>
              <span>Python</span>
            </div>
            <pre>{lesson.code}</pre>
            <button
              className="text-link"
              onClick={() => {
                update((s) => ({
                  ...s,
                  drafts: { ...s.drafts, [lesson.id]: lesson.code },
                }));
                setTemplateVersion((v) => v + 1);
                setView("split");
              }}
            >
              <Play size={13} />
              Run in sandbox
              <ArrowRight size={14} />
            </button>
          </div>
          {lesson.terms ? (
            <section className="lesson-glossary" aria-label="Key terms">
              <h2>Key terms to remember</h2>
              <dl>
                {lesson.terms.map(({ term, definition }) => (
                  <div key={term}>
                    <dt>{term}</dt>
                    <dd>{definition}</dd>
                  </div>
                ))}
              </dl>
            </section>
          ) : null}
          <PracticeQuestions lesson={lesson} />
          <div className="lesson-completion">
            <button
              className={`button ${completed ? "secondary" : "primary"}`}
              disabled={!completed && !practicePassed}
              onClick={() =>
                update((s) => ({
                  ...s,
                  completed: completed
                    ? s.completed.filter((id) => id !== lesson.id)
                    : [...new Set([...s.completed, lesson.id])],
                }))
              }
            >
              <Check size={16} />
              {completed ? "Completed · undo" : "Mark module complete"}
            </button>
            {!completed && !practicePassed ? (
              <span>
                Answer all practice questions correctly to complete this module.
              </span>
            ) : null}
            {exam ? (
              <Link to={`/exams/${exam.id}`} className="text-link">
                {exam.kind === "checkpoint"
                  ? "Take checkpoint"
                  : "Take final exam"}
                <ArrowRight size={15} />
              </Link>
            ) : next ? (
              <Link to={`/learn/${next.id}`} className="text-link">
                Next module
                <ArrowRight size={15} />
              </Link>
            ) : null}
          </div>
        </article>
        <div className="lesson-sandbox-pane">
          {view !== "reader" ? (
            <Suspense fallback={<Loading label="Opening sandbox…" />}>
              <Sandbox
                key={`${lesson.id}-${templateVersion}`}
                lessonId={lesson.id}
                initialCode={lesson.code}
                onExpand={() =>
                  setView(view === "sandbox" ? "split" : "sandbox")
                }
                expanded={view === "sandbox"}
              />
            </Suspense>
          ) : null}
        </div>
      </div>
      <Modal
        open={noteOpen}
        onOpenChange={setNoteOpen}
        title="Capture your thinking"
        description={`Linked to module ${lesson.id}: ${lesson.title}`}
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            update((s) => ({
              ...s,
              notes: [
                {
                  id: crypto.randomUUID(),
                  title: lesson.title,
                  body: note,
                  lessonId: lesson.id,
                  updatedAt: new Date().toISOString(),
                },
                ...s.notes,
              ],
            }));
            setNote("");
            setNoteOpen(false);
          }}
        >
          <label className="field">
            Research note
            <textarea
              autoFocus
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="What surprised you? Which assumption would you test next?"
              rows={7}
              required
              maxLength={20000}
            />
          </label>
          <button className="button primary full-width">
            Save to notebook
            <BookmarkPlus size={16} />
          </button>
        </form>
      </Modal>
    </div>
  );
}
