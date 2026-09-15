import PracticeQuestions from "@/features/assessments/components/PracticeQuestions";
import CourseAssistant from "@/features/assistant/components/CourseAssistant";
import RealWorldCase from "@/features/learning/components/RealWorldCase";
import {
  caseNotebookPrompt,
  lessonCase,
} from "@/features/learning/model/cases";
import {
  findLesson,
  lessons,
  lessonTrack,
  trackLabel,
} from "@/features/learning/model/catalog";
import { practiceComplete } from "@/features/learning/model/progress";
import type { Lesson } from "@/features/learning/model/types";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import { Loading, Modal } from "@/shared/components/ui";

import "katex/dist/katex.min.css";
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
import { lazy, Suspense, useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { Link, useNavigate, useParams } from "react-router-dom";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
// Course prose uses $ for money and $$ for equations.
const markdownComponents = {
  table: ({ children }: { children?: React.ReactNode }) => (
    <div
      className="prose-table"
      role="region"
      aria-label="Lesson table"
      tabIndex={0}
    >
      <table>{children}</table>
    </div>
  ),
};
const Sandbox = lazy(() => import("@/features/research/components/Sandbox"));
const LocalCodeLab = lazy(
  () => import("@/features/learning/components/LocalCodeLab"),
);
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
  const isC = lesson.codeLanguage === "c";
  const { state, update } = useWorkspace(),
    navigate = useNavigate(),
    track = lessonTrack(lesson.id)!,
    [view, setView] = useState<"split" | "reader" | "sandbox">(
      ["fundamentals", "book-study", "applied-study"].includes(lesson.kind)
        ? "reader"
        : "split",
    ),
    [noteOpen, setNoteOpen] = useState(false),
    [note, setNote] = useState(""),
    [executionError, setExecutionError] = useState(""),
    [assistantEdit, setAssistantEdit] = useState<{
      previous: string;
      applied: string;
    } | null>(null),
    [templateVersion, setTemplateVersion] = useState(0);
  const completed = state.completed.includes(lesson.id),
    practicePassed = practiceComplete(lesson, state),
    exam = track.exams.find((exam) => exam.moduleIds.at(-1) === lesson.id),
    next = lessons[lessons.findIndex((l) => l.id === lesson.id) + 1];
  const caseStudy = lessonCase(track, lesson);
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
            aria-pressed={view === "reader"}
            aria-label="Reading view"
            title="Reading view"
            onClick={() => setView("reader")}
          >
            <BookOpen size={16} />
          </button>
          <button
            className={view === "split" ? "active" : ""}
            aria-pressed={view === "split"}
            aria-label="Split view"
            title="Split view"
            onClick={() => setView("split")}
          >
            <Columns2 size={16} />
          </button>
          <button
            className={view === "sandbox" ? "active" : ""}
            aria-pressed={view === "sandbox"}
            aria-label={isC ? "C lab view" : "Sandbox view"}
            title={isC ? "C lab view" : "Sandbox view"}
            onClick={() => setView("sandbox")}
          >
            <Code2 size={16} />
          </button>
        </div>
        <CourseAssistant
          course={track}
          lesson={lesson}
          executionError={executionError}
          onApply={(code) => {
            const previous = state.drafts[lesson.id] ?? lesson.code;
            if (previous !== code)
              setAssistantEdit({ previous, applied: code });
            update((s) => ({
              ...s,
              drafts: { ...s.drafts, [lesson.id]: code },
            }));
            setExecutionError("");
            setTemplateVersion((version) => version + 1);
            setView("split");
          }}
        />
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
      {assistantEdit ? (
        <div className="assistant-editor-notice" role="status">
          <span>
            Assistant code added. Review it, then{" "}
            {isC ? "download and compile" : "run the experiment"}.
          </span>
          <button
            className="text-link"
            disabled={state.drafts[lesson.id] !== assistantEdit.applied}
            onClick={() => {
              update((s) => ({
                ...s,
                drafts: { ...s.drafts, [lesson.id]: assistantEdit.previous },
              }));
              setAssistantEdit(null);
              setExecutionError("");
              setTemplateVersion((version) => version + 1);
            }}
          >
            Undo code replacement
          </button>
          <button className="text-link" onClick={() => setAssistantEdit(null)}>
            Dismiss
          </button>
        </div>
      ) : null}
      <div className="learning-panes">
        <article className="lesson-article">
          <div className="page-eyebrow">
            {trackLabel(track)}
            <ChevronRight size={12} />
            MODULE {lesson.id}
          </div>
          <h1>{lesson.title}</h1>
          {lesson.subtitle !== lesson.objective ? (
            <p className="lesson-subtitle">{lesson.subtitle}</p>
          ) : null}
          <div className="lesson-meta">
            <span>
              <Clock3 size={14} />
              {lesson.minutes} min{" "}
              {lesson.kind.endsWith("study") ? "study" : "read"}
            </span>
            <span>
              <Code2 size={15} />
              Interactive lesson
            </span>
            <button className="text-link" onClick={() => setNoteOpen(true)}>
              <BookmarkPlus size={15} />
              Add a note
            </button>
            {caseStudy ? (
              <a className="text-link" href="#real-world-case">
                Explore the real-world case <ArrowRight size={14} />
              </a>
            ) : null}
          </div>
          {lesson.reading ? (
            <aside
              className="lesson-reading"
              aria-label={
                track.studyType === "applied" ? "Applied study" : "Book reading"
              }
            >
              <BookOpen size={18} />
              <div>
                <span className="eyebrow">
                  {track.studyType === "applied"
                    ? "COURSE CONNECTION"
                    : "BOOK CONNECTION"}
                </span>
                <p>{lesson.reading}</p>
                <Link className="text-link" to={`/curriculum/${track.id}`}>
                  {track.studyType === "applied"
                    ? "View the course plan"
                    : "View the reading plan"}{" "}
                  <ArrowRight size={14} />
                </Link>
              </div>
            </aside>
          ) : null}
          <div className="lesson-objective">
            <span className="eyebrow">WHAT YOU WILL LEARN</span>
            <p>
              {lesson.objective ??
                "Explain the principle, reproduce the worked example, and identify an assumption that could change the result."}
            </p>
          </div>
          <div className="prose">
            <ReactMarkdown
              remarkPlugins={[
                [remarkMath, { singleDollarTextMath: false }],
                remarkGfm,
              ]}
              rehypePlugins={[rehypeKatex]}
              components={markdownComponents}
            >
              {lesson.content}
            </ReactMarkdown>
          </div>
          {caseStudy ? (
            <RealWorldCase
              lesson={lesson}
              caseStudy={caseStudy}
              onWrite={() => {
                setNote((draft) =>
                  [draft, caseNotebookPrompt(lesson, caseStudy)]
                    .filter(Boolean)
                    .join("\n\n"),
                );
                setNoteOpen(true);
              }}
            />
          ) : null}
          {lesson.assignment ? (
            <section
              className="lesson-assignment"
              aria-labelledby="assignment-title"
            >
              <span className="eyebrow">APPLY THE METHOD</span>
              <h2 id="assignment-title">Research assignment</h2>
              <p>{lesson.assignment.prompt}</p>
              <button
                className="button secondary small"
                onClick={() => {
                  setNote(
                    `Assignment: ${lesson.assignment!.prompt}\n\nMy calculation and evidence:\n\nAssumptions and limitations:\n\nDecision and next check:\n`,
                  );
                  setNoteOpen(true);
                }}
              >
                <BookmarkPlus size={15} /> Write in notebook
              </button>
              <details>
                <summary>Review the worked solution</summary>
                <p>{lesson.assignment.solution}</p>
              </details>
            </section>
          ) : null}
          <div className="lesson-code-card">
            <div>
              <Code2 size={16} />
              <strong>Try the lesson template</strong>
              <span>{isC ? "C17" : "Python"}</span>
            </div>
            <pre>{lesson.code}</pre>
            <button
              className="text-link"
              onClick={() => {
                if (!isC)
                  update((s) => ({
                    ...s,
                    drafts: { ...s.drafts, [lesson.id]: lesson.code },
                  }));
                setTemplateVersion((v) => v + 1);
                setView("split");
              }}
            >
              <Play size={13} />
              {isC ? "Open C lab" : "Run in sandbox"}
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
          {["0.4", "0.5", "0.7", "0.8"].includes(lesson.id) ? (
            <div className="lesson-objective">
              <span className="eyebrow">PUT IT INTO PRACTICE</span>
              <p>
                Practice this lesson with a virtual $100,000 account. Read a
                stock chart, place a paper order, and record your reasoning.
              </p>
              <Link className="text-link" to={`/simulator?lesson=${lesson.id}`}>
                Open trading simulator <ArrowRight size={15} />
              </Link>
            </div>
          ) : null}
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
            <Suspense
              fallback={
                <Loading
                  label={isC ? "Opening C laboratory…" : "Opening sandbox…"}
                />
              }
            >
              {isC ? (
                <LocalCodeLab lesson={lesson} />
              ) : (
                <Sandbox
                  key={`${lesson.id}-${templateVersion}`}
                  lessonId={lesson.id}
                  initialCode={lesson.code}
                  onExecutionError={setExecutionError}
                  onExpand={() =>
                    setView(view === "sandbox" ? "split" : "sandbox")
                  }
                  expanded={view === "sandbox"}
                />
              )}
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
