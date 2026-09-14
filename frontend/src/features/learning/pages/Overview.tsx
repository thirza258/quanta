import ExamCard from "@/features/assessments/components/ExamCard";
import { TrackArt } from "@/features/learning/components/TrackVisuals";
import {
  exams,
  findLesson,
  lessons,
  lessonTrack,
  trackLabel,
  tracks,
} from "@/features/learning/model/catalog";
import { examPassed } from "@/features/learning/model/progress";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import {
  ArrowRight,
  ArrowUpRight,
  BookOpen,
  Check,
  ChevronRight,
  Clock3,
  FlaskConical,
  Play,
} from "lucide-react";
import { Link } from "react-router-dom";
import TrackCard from "../components/TrackCard";
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
