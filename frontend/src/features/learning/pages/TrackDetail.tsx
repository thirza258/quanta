import ExamCard from "@/features/assessments/components/ExamCard";
import CourseAssistant from "@/features/assistant/components/CourseAssistant";
import CourseCases, {
  UnitCases,
} from "@/features/learning/components/CourseCases";
import { TrackArt } from "@/features/learning/components/TrackVisuals";
import { trackLabel, tracks } from "@/features/learning/model/catalog";
import {
  examPassed,
  lessonExercises,
  trackProgress,
} from "@/features/learning/model/progress";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import {
  ArrowLeft,
  ArrowRight,
  Award,
  BookOpen,
  Check,
  ChevronRight,
  Clock3,
  Network,
  Play,
} from "lucide-react";
import { Fragment } from "react";
import MarkdownRenderer from "@/shared/components/MarkdownRenderer";
import { Link, useParams } from "react-router-dom";
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
  const bookStudy = track.modules.some(
    (lesson) => lesson.kind === "book-study",
  );
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
            {track.language?.length ? (
              <span
                className="lang-badge"
                style={{
                  marginLeft: "0.5rem",
                  fontSize: "0.75rem",
                  padding: "0.15rem 0.5rem",
                  borderRadius: "4px",
                  background: "rgba(255,255,255,0.08)",
                  border: "1px solid rgba(255,255,255,0.12)",
                }}
              >
                {track.language.map((l) => l.toUpperCase()).join(" / ")}
              </span>
            ) : null}
            {track.audience_tags?.map((tag) => (
              <span
                key={tag}
                className="tag-badge"
                style={{
                  marginLeft: "0.4rem",
                  fontSize: "0.7rem",
                  padding: "0.1rem 0.4rem",
                  borderRadius: "4px",
                  background: "rgba(56, 189, 248, 0.12)",
                  color: "#38bdf8",
                }}
              >
                #{tag}
              </span>
            ))}
          </div>
          <h1>{track.title}</h1>
          <p className="page-subtitle">
            <MarkdownRenderer content={track.description} inline />
          </p>
          <p className="source-line">{track.source}</p>
          <div className="inline-meta">
            <span>
              <BookOpen size={16} />
              {track.modules.length} modules
            </span>
            <span>
              <Clock3 size={16} />
              {track.modules.reduce((n, m) => n + m.minutes, 0)} minutes of{" "}
              {track.parts ? "guided study" : "reading"}
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
          <div className="course-hero-actions">
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
            <a className="button secondary" href="#course-outline">
              View course outline <BookOpen size={16} />
            </a>
            <Link
              className="button secondary"
              to={`/certifications/course/${track.id}`}
            >
              <Award size={16} />
              {progress.complete
                ? "View certificate"
                : "Certificate requirements"}
            </Link>
            <Link className="button secondary" to="/course-map">
              <Network size={16} /> Course map
            </Link>
          </div>
        </div>
        <TrackArt kind={track.icon} large />
      </div>
      <section
        className="course-assistant-callout"
        aria-label="Course AI assistance"
      >
        <div>
          <h2>A helping hand, whenever you get stuck</h2>
          <p>
            Ask about the course, prepare your environment, or build a code
            example.
          </p>
        </div>
        <CourseAssistant course={track} />
      </section>
      <CourseCases track={track} />
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
            {track.prerequisites ??
              "No prior finance or programming knowledge required. Start with the readings; Python examples are optional."}
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
      {track.readingGuide ? (
        <section
          className="course-reading-guide"
          aria-labelledby="reading-guide-title"
        >
          <span className="eyebrow">
            {bookStudy ? "READ ALONG WITH THE BOOK" : "LEARN AT YOUR OWN PACE"}
          </span>
          <h2 id="reading-guide-title">
            {bookStudy ? "Your reading plan" : "Your course plan"}
          </h2>
          {track.readingGuide.split("\n\n").map((paragraph) => (
            <p key={paragraph}>
              <MarkdownRenderer content={paragraph} inline />
            </p>
          ))}
          <div className="course-references">
            {track.references?.map((reference) => (
              <a
                key={reference.url}
                className="text-link"
                href={reference.url}
                target="_blank"
                rel="noreferrer"
              >
                {reference.title} <ArrowRight size={14} />
              </a>
            ))}
          </div>
          {track.parts?.length ? (
            <nav
              className="course-unit-links"
              aria-label={bookStudy ? "Book units" : "Course units"}
            >
              {track.parts?.map((part) => (
                <a key={part.id} href={`#unit-${part.id}`}>
                  <span>{part.id}</span>
                  {part.title}
                </a>
              ))}
            </nav>
          ) : null}
        </section>
      ) : null}
      {track.resources?.length ? (
        <div className="course-resources" aria-label="Course downloads">
          {track.resources.map((resource) => (
            <a
              key={resource.url}
              className="button secondary"
              href={resource.url}
              download
            >
              {resource.title} <ArrowRight size={15} />
            </a>
          ))}
        </div>
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
      <div className="section-heading" id="course-outline">
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
            {m.part && m.part !== track.modules[i - 1]?.part ? (
              <div className="course-unit-heading" id={`unit-${m.part}`}>
                <span className="eyebrow">UNIT {m.part}</span>
                <h3>
                  {track.parts?.find((part) => part.id === m.part)?.title}
                </h3>
                <p>
                  <MarkdownRenderer
                    content={
                      track.parts?.find((part) => part.id === m.part)
                        ?.description ?? ""
                    }
                    inline
                  />
                </p>
                <UnitCases track={track} part={m.part} />
              </div>
            ) : null}
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
                <h3>
                  <MarkdownRenderer content={m.title} inline />
                </h3>
                <p>
                  <MarkdownRenderer content={m.subtitle} inline />
                </p>
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
      {track.funnel_cta ? (
        <section
          className="funnel-cta-section"
          style={{
            marginTop: "3rem",
            padding: "2rem",
            borderRadius: "14px",
            background:
              "linear-gradient(135deg, rgba(24, 24, 27, 0.95), rgba(39, 39, 42, 0.75))",
            border: "1px solid rgba(255, 255, 255, 0.1)",
          }}
        >
          <span
            className="eyebrow"
            style={{
              textTransform: "uppercase",
              fontSize: "0.75rem",
              letterSpacing: "0.08em",
              color: "#38bdf8",
              fontWeight: 600,
            }}
          >
            Recommended Next Step
          </span>
          <h2 style={{ margin: "0.5rem 0 1rem", fontSize: "1.35rem" }}>
            Where to go after {track.title}
          </h2>
          <div
            style={{
              display: "flex",
              gap: "1rem",
              flexWrap: "wrap",
              alignItems: "center",
            }}
          >
            <Link
              className="button primary"
              to={
                track.funnel_cta.target_course_id
                  ? track.funnel_cta.target_course_id === "curriculum"
                    ? "/curriculum"
                    : `/curriculum/${track.funnel_cta.target_course_id}`
                  : track.funnel_cta.target_url || "/curriculum"
              }
            >
              {track.funnel_cta.label} <ArrowRight size={16} />
            </Link>
            {track.funnel_cta.secondary_label ? (
              <Link
                className="button secondary"
                to={
                  track.funnel_cta.secondary_target_course_id
                    ? track.funnel_cta.secondary_target_course_id ===
                      "certifications"
                      ? "/certifications"
                      : `/curriculum/${track.funnel_cta.secondary_target_course_id}`
                    : track.funnel_cta.secondary_target_url || "/curriculum"
                }
              >
                {track.funnel_cta.secondary_label}
              </Link>
            ) : null}
          </div>
        </section>
      ) : null}
    </div>
  );
}
