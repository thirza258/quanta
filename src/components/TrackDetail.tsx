import { Fragment } from "react";
import { Link, useParams } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Check,
  ChevronRight,
  Clock3,
  Play,
} from "lucide-react";
import { tracks, trackLabel } from "../lib/catalog";
import { examPassed, lessonExercises, trackProgress } from "../lib/learning";
import ExamCard from "./ExamCard";
import { useWorkspace } from "../lib/workspace";
import { TrackArt } from "./ui";
export default function TrackDetail() {
  const { trackId } = useParams(),
    track = tracks.find((t) => t.id === trackId),
    { state } = useWorkspace();
  if (!track)
    return (
      <div className="page">
        <h1>Track not found</h1>
        <Link className="button secondary" to="/curriculum">
          Return to curriculum
        </Link>
      </div>
    );
  const progress = trackProgress(track, state);
  const completed = progress.modules;
  const next = track.modules.find(
    (module) => !state.completed.includes(module.id),
  );
  const nextExam = track.exams.find((exam) => !examPassed(exam, state));
  const nextTrack =
    tracks[tracks.findIndex((item) => item.id === track.id) + 1];
  const nextPath = next
    ? `/learn/${next.id}`
    : nextExam
      ? `/exams/${nextExam.id}`
      : nextTrack
        ? `/curriculum/${nextTrack.id}`
        : "/curriculum";
  return (
    <div className="page track-detail">
      <Link to="/curriculum" className="text-link back-link">
        <ArrowLeft size={15} />
        All learning tracks
      </Link>
      <div className="track-detail-hero">
        <div>
          <div className="page-eyebrow">
            {trackLabel(track)}
            <span className="level-badge">{track.level}</span>
          </div>
          <h1>{track.title}</h1>
          <p className="page-subtitle">{track.description}</p>
          <p className="source-line">{track.source}</p>
          <div className="inline-meta">
            <span>
              <BookOpen size={16} />
              {track.modules.length} modules
            </span>
            <span>
              <Clock3 size={16} />
              {track.modules.reduce((n, m) => n + m.minutes, 0)} minutes of
              reading
            </span>
            <span>
              {track.modules.reduce(
                (count, lesson) => count + lessonExercises(lesson).length,
                0,
              )}{" "}
              practice questions
            </span>
            <span>
              {track.exams.length} {track.exams.length === 1 ? "exam" : "exams"}
            </span>
          </div>
          <Link className="button primary" to={nextPath}>
            {progress.complete
              ? nextTrack
                ? "Continue to next course"
                : "Browse curriculum"
              : next
                ? completed
                  ? "Continue course"
                  : "Start this course"
                : "Continue to exam"}
            <ArrowRight size={16} />
          </Link>
        </div>
        <TrackArt kind={track.icon} large />
      </div>
      {track.outcomes ? (
        <section className="course-outcomes">
          <h2>What you will learn</h2>
          <ul>
            {track.outcomes.map((outcome) => (
              <li key={outcome}>
                <Check size={16} />
                {outcome}
              </li>
            ))}
          </ul>
          <p>
            No prior finance or programming knowledge required. Start with the
            readings; Python examples are optional.
          </p>
        </section>
      ) : !trackProgress(tracks[0], state).complete ? (
        <p className="inline-notice">
          New to stocks or trading?{" "}
          <Link className="text-link" to="/curriculum/trading-fundamentals">
            Start with Trading & market fundamentals
          </Link>{" "}
          to build the vocabulary used in this track.
        </p>
      ) : null}
      <div className="track-progress-row">
        <span>
          {completed} of {track.modules.length} modules · {progress.exams} of{" "}
          {track.exams.length} exams passed
          {progress.complete ? " · Course complete" : ""}
        </span>
        <strong>{progress.percent}%</strong>
      </div>
      <div className="progress-track">
        <span style={{ width: `${progress.percent}%` }} />
      </div>
      <div className="section-heading">
        <div>
          <h2>Inside this course</h2>
          <p>
            Read each lesson, check your understanding, and apply it in the
            exams.
          </p>
        </div>
      </div>
      <div className="module-list">
        {track.modules.map((m, i) => (
          <Fragment key={m.id}>
            <Link to={`/learn/${m.id}`} className="module-row">
              <span
                className={`module-state ${state.completed.includes(m.id) ? "complete" : ""}`}
              >
                {state.completed.includes(m.id) ? (
                  <Check size={19} />
                ) : (
                  String(i + 1).padStart(2, "0")
                )}
              </span>
              <div>
                <span className="eyebrow">MODULE {m.id}</span>
                <h3>{m.title}</h3>
                <p>{m.subtitle}</p>
              </div>
              <span className="module-minutes">
                <Clock3 size={14} />
                {m.minutes} min
              </span>
              <span className="module-type">
                <Play size={12} />
                Interactive
              </span>
              <ChevronRight size={20} />
            </Link>
            {track.exams
              .filter((exam) => exam.moduleIds.at(-1) === m.id)
              .map((exam) => (
                <ExamCard key={exam.id} exam={exam} />
              ))}
          </Fragment>
        ))}
      </div>
    </div>
  );
}
