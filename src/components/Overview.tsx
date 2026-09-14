import { Link } from "react-router-dom";
import {
  ArrowRight,
  ArrowUpRight,
  BookOpen,
  Check,
  ChevronRight,
  Clock3,
  FlaskConical,
  Play,
  Search,
  Sparkles,
} from "lucide-react";
import { useState } from "react";
import {
  tracks,
  lessons,
  exams,
  findLesson,
  lessonTrack,
  trackLabel,
} from "../lib/catalog";
import {
  examPassed,
  exerciseKey,
  lessonExercises,
  trackProgress,
} from "../lib/learning";
import ExamCard from "./ExamCard";
import { useWorkspace } from "../lib/workspace";
import { TrackArt, TrackIcon } from "./ui";
import type { Track } from "../lib/types";
function TrackCard({ track }: { track: Track }) {
  const { state } = useWorkspace(),
    progress = trackProgress(track, state);
  return (
    <Link className="track-card" to={`/curriculum/${track.id}`}>
      <div className="track-card-top">
        <span className="track-number">{trackLabel(track)}</span>
        <span className={`level-badge ${track.level.toLowerCase()}`}>
          {track.level}
        </span>
      </div>
      <div className="track-art-wrap">
        <TrackArt kind={track.icon} />
        <span className="track-icon">
          <TrackIcon kind={track.icon} />
        </span>
      </div>
      <h3>{track.title}</h3>
      <p>{track.description}</p>
      <div className="track-card-footer">
        <span>
          <BookOpen size={13} />
          {track.modules.length} modules<span className="dot-separator">·</span>
          {Math.round(
            (track.modules.reduce((n, l) => n + l.minutes, 0) / 60) * 10,
          ) / 10}{" "}
          hrs
        </span>
        <ArrowUpRight size={17} />
      </div>
      <div className="track-assessment-meta">
        <span>
          {track.exams.length} {track.exams.length === 1 ? "exam" : "exams"}
        </span>
        <span>
          {progress.complete
            ? "Course complete"
            : `${progress.percent}% complete`}
        </span>
      </div>
      {progress.percent > 0 ? (
        <div
          className="card-progress"
          style={{ width: `${progress.percent}%` }}
        />
      ) : null}
    </Link>
  );
}
export default function Overview() {
  const { state, user } = useWorkspace(),
    next = lessons.find((l) => !state.completed.includes(l.id)) || lessons[0],
    last = findLesson(state.lastLesson) || next,
    track = lessonTrack(last.id)!,
    completed = lessons.filter((lesson) =>
      state.completed.includes(lesson.id),
    ).length,
    passedExams = exams.filter((exam) => examPassed(exam, state)).length,
    totalProgress = Math.round(
      ((completed + passedExams) / (lessons.length + exams.length)) * 100,
    ),
    pendingExams = exams.filter(
      (exam) =>
        state.examDrafts[exam.id] ||
        (!examPassed(exam, state) &&
          exam.moduleIds.every((id) => state.completed.includes(id))),
    ),
    hasStarted =
      state.lastLesson !== lessons[0].id ||
      state.runs > 0 ||
      completed > 0 ||
      Object.keys(state.drafts).length > 0 ||
      Object.keys(state.submissions).length > 0 ||
      Object.keys(state.examDrafts).length > 0 ||
      Object.keys(state.examAttempts).length > 0;
  return (
    <div className="page overview-page">
      <div className="page-eyebrow">
        <span className="green-dot" /> YOUR LEARNING WORKSPACE
      </div>
      <div className="page-title-row">
        <div>
          <h1>
            {user
              ? `Welcome back, ${user.name.split(" ")[0]}.`
              : "A little theory. A lot of understanding."}
          </h1>
          <p className="page-subtitle">
            Build a deeper understanding of markets, one principle at a time.
          </p>
        </div>
        <Link to="/lab" className="button secondary">
          <FlaskConical size={16} />
          Open sandbox
          <ArrowUpRight size={15} />
        </Link>
      </div>
      <div className="stats-strip">
        <div>
          <span className="stat-icon">
            <BookOpen size={18} />
          </span>
          <span>
            <strong>
              {completed}
              <small> / {lessons.length}</small>
            </strong>
            <label>Modules completed</label>
          </span>
        </div>
        <div>
          <span className="stat-icon">
            <Check size={18} />
          </span>
          <span>
            <strong>
              {totalProgress}
              <small>%</small>
            </strong>
            <label>Overall progress</label>
          </span>
          <div className="mini-progress">
            <span style={{ width: `${totalProgress}%` }} />
          </div>
        </div>
        <div>
          <span className="stat-icon">
            <FlaskConical size={18} />
          </span>
          <span>
            <strong>{state.runs.toString().padStart(2, "0")}</strong>
            <label>Experiments run</label>
          </span>
        </div>
        <div>
          <span className="stat-icon">
            <Clock3 size={18} />
          </span>
          <span>
            <strong>{state.notes.length.toString().padStart(2, "0")}</strong>
            <label>Research notes</label>
          </span>
        </div>
      </div>
      <div className="feature-row">
        <section className="continue-card">
          <div className="continue-copy">
            <span className="eyebrow">
              <span className="small-circle">
                <Play size={9} fill="currentColor" />
              </span>
              {hasStarted
                ? "PICK UP WHERE YOU LEFT OFF"
                : "A GOOD PLACE TO BEGIN"}
            </span>
            <div className="continue-track">
              {trackLabel(track)}
              <span>/</span>
              {track.title}
            </div>
            <h2>{last.title}</h2>
            <p>
              {last.subtitle}. Read the idea, work through the numbers, and test
              it for yourself.
            </p>
            <div className="continue-bottom">
              <Link to={`/learn/${last.id}`} className="button primary">
                {hasStarted ? "Continue learning" : "Start learning"}
                <ArrowRight size={16} />
              </Link>
              <span>
                <Clock3 size={14} />
                {last.minutes} min read
              </span>
            </div>
          </div>
          <div className="continue-art">
            <div className="orbital-line" />
            <TrackArt kind="book" large />
            <span className="formula-tag">
              {track.number === 0
                ? "Understand before you trade"
                : "Value ≠ Price"}
            </span>
          </div>
        </section>
        <section className="toolkit-card">
          <span className="eyebrow">THEORY, MEET PRACTICE</span>
          <h3>Your ideas. Put to the test.</h3>
          <p>A research environment built into every lesson.</p>
          <div className="toolkit-links">
            <Link to="/lab?tool=market">
              <span>
                <FlaskConical size={17} />
              </span>
              <div>
                <strong>Synthetic market lab</strong>
                <small>Explore what-if scenarios</small>
              </div>
              <ChevronRight size={16} />
            </Link>
            <Link to="/lab?tool=valuation">
              <span>
                <BookOpen size={17} />
              </span>
              <div>
                <strong>Fundamental valuation</strong>
                <small>Find your margin of safety</small>
              </div>
              <ChevronRight size={16} />
            </Link>
          </div>
        </section>
      </div>
      {pendingExams.length ? (
        <section
          className="overview-exams"
          aria-label="Continue your assessments"
        >
          <div className="section-heading">
            <div>
              <h2>Your next assessments</h2>
              <p>
                {passedExams} of {exams.length} exams passed. Apply what you
                have learned.
              </p>
            </div>
          </div>
          {pendingExams.slice(0, 3).map((exam) => (
            <ExamCard key={exam.id} exam={exam} />
          ))}
        </section>
      ) : null}
      <div className="section-heading">
        <div>
          <h2>
            Your learning path{" "}
            <span className="count-pill">{tracks.length} courses</span>
          </h2>
          <p>From fundamental principles to systematic strategies.</p>
        </div>
        <Link to="/curriculum" className="text-link">
          View curriculum
          <ArrowRight size={15} />
        </Link>
      </div>
      <div className="track-grid">
        {tracks.map((t) => (
          <TrackCard key={t.id} track={t} />
        ))}
      </div>
      <div className="overview-footer">
        <span>
          <span className="green-dot" />
          Built for thoughtful investors.
        </span>
        <span>Read. Question. Experiment. Repeat.</span>
      </div>
    </div>
  );
}
export function Curriculum() {
  const [query, setQuery] = useState(""),
    [filter, setFilter] = useState("All tracks");
  const { state } = useWorkspace();
  const filtered = tracks.filter((track) => {
    const progress = trackProgress(track, state);
    const started =
      progress.percent > 0 ||
      track.modules.some(
        (lesson) =>
          state.drafts[lesson.id] ||
          lessonExercises(lesson).some(
            (_, index) => state.submissions[exerciseKey(lesson.id, index)],
          ),
      ) ||
      track.exams.some(
        (exam) =>
          state.examDrafts[exam.id] || state.examAttempts[exam.id]?.length,
      );
    return (
      `${track.title} ${track.description} ${track.modules.map((module) => module.title).join(" ")}`
        .toLowerCase()
        .includes(query.toLowerCase()) &&
      (filter === "All tracks" ||
        (filter === "In progress" && started && !progress.complete) ||
        (filter === "Not started" && !started) ||
        (filter === "Completed" && progress.complete))
    );
  });
  return (
    <div className="page">
      <div className="page-eyebrow">A CONNECTED CURRICULUM</div>
      <h1>Start with the basics. Build your perspective.</h1>
      <p className="page-subtitle">
        One beginner course, then six specialist tracks. Learn the language of
        markets before building your investment and research skills.
      </p>
      <div className="catalog-toolbar">
        <div className="tabs">
          {["All tracks", "In progress", "Not started", "Completed"].map(
            (f) => (
              <button
                key={f}
                className={filter === f ? "active" : ""}
                onClick={() => setFilter(f)}
              >
                {f}
              </button>
            ),
          )}
        </div>
        <label className="search-input compact">
          <Search size={16} />
          <input
            aria-label="Search curriculum"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search curriculum…"
          />
        </label>
      </div>
      <div className="track-grid">
        {filtered.map((t) => (
          <TrackCard key={t.id} track={t} />
        ))}
      </div>
      {!filtered.length ? (
        <div className="empty-state">
          <Search size={28} />
          <h3>No matching tracks</h3>
          <p>Try another topic or switch to all tracks.</p>
        </div>
      ) : null}
      <div className="curriculum-note">
        <Sparkles size={20} />
        <p>
          <strong>Learning happens in the details.</strong> Each module includes
          original reading, a worked example, a runnable Python template, and a
          practice check. Course exams bring the ideas together with new
          scenarios, feedback, and retakes.
        </p>
      </div>
    </div>
  );
}
