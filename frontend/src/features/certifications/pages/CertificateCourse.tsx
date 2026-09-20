import { matchesCourse } from "../model/certificates";
import { useCertificates } from "../model/useCertificates";
import type { Certificate } from "../model/types";
import { tracks } from "@/features/learning/model/catalog";
import { examPassed, trackProgress } from "@/features/learning/model/progress";
import type { Track } from "@/features/learning/model/types";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import AuthModal from "@/features/workspace/components/AuthModal";
import { Loading } from "@/shared/components/ui";
import { post } from "@/shared/api/client";
import {
  ArrowLeft,
  ArrowRight,
  Award,
  CheckCircle2,
  Circle,
} from "lucide-react";
import { useEffect, useRef, useState, type FormEvent } from "react";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import "../certifications.css";

export default function CertificateCourse() {
  const { trackId } = useParams();
  const track = tracks.find((item) => item.id === trackId);
  return track ? (
    <Course key={track.id} track={track} />
  ) : (
    <div className="page">
      <h1>Course not found</h1>
      <Link className="text-link back-link" to="/certifications">
        Return to certifications
      </Link>
    </div>
  );
}

function Course({ track }: { track: Track }) {
  const { state, user, syncWorkspace } = useWorkspace();
  const navigate = useNavigate();
  const [name, setName] = useState(user?.name ?? "");
  const [error, setError] = useState("");
  const [authOpen, setAuthOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const mounted = useRef(true);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  const issued = useCertificates(user?.id);
  const certificate = issued.certificates.find((item) =>
    matchesCourse(item, track),
  );
  const progress = trackProgress(track, state);
  const nextLesson = track.modules.find(
    (lesson) => !state.completed.includes(lesson.id),
  );
  const nextExam = track.exams.find((exam) => !examPassed(exam, state));

  if (certificate)
    return <Navigate replace to={`/certifications/${certificate.id}`} />;

  async function claim(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (busy) return;
    setError("");
    setBusy(true);
    try {
      const workspaceVersion = await syncWorkspace();
      if (!mounted.current) return;
      const certificate = await post<Certificate>("/certificates", {
        trackId: track.id,
        recipientName: name.trim(),
        workspaceVersion,
      });
      if (mounted.current)
        navigate(`/certifications/${certificate.id}`, { replace: true });
    } catch (err) {
      if (mounted.current) setError((err as Error).message);
    } finally {
      if (mounted.current) setBusy(false);
    }
  }

  return (
    <div className="page certification-course-page">
      <Link className="text-link back-link" to="/certifications">
        <ArrowLeft size={15} /> All certifications
      </Link>
      <div className="page-eyebrow">
        <Award size={15} /> COURSE COMPLETION CERTIFICATE
      </div>
      <h1>{track.title}</h1>
      <p className="page-subtitle">
        {progress.complete
          ? "You’ve completed every module and passed every exam. Make this milestone yours."
          : "Complete the modules and pass the exams below to earn your certificate."}
      </p>
      {issued.loading ? (
        <Loading label="Checking issued certificates…" />
      ) : issued.error ? (
        <div role="alert">
          <p>{issued.error}</p>
          <button className="button secondary" onClick={issued.retry}>
            Try again
          </button>
        </div>
      ) : progress.complete && !user ? (
        <section className="certificate-claim">
          <h2>Sign in to claim your certificate</h2>
          <p>
            Your certificate will be saved to your account with a public
            verification link. Creating an account carries over your guest
            progress.
          </p>
          <button className="button primary" onClick={() => setAuthOpen(true)}>
            Sign in or create account
          </button>
        </section>
      ) : progress.complete ? (
        <form className="certificate-claim" onSubmit={claim}>
          <h2>Claim your certificate</h2>
          <label className="field">
            Name on certificate
            <input
              autoComplete="name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              maxLength={80}
              required
              aria-describedby="certificate-name-help"
            />
          </label>
          <p id="certificate-name-help">
            Check the spelling before claiming. This name and the issue date
            will be saved on your certificate.
          </p>
          {error ? (
            <p role="alert" className="negative">
              {error}
            </p>
          ) : null}
          <button
            className="button primary"
            type="submit"
            disabled={busy || !name.trim()}
          >
            <Award size={16} />{" "}
            {busy ? "Issuing certificate…" : "Claim certificate"}
          </button>
          <p className="fine-print">
            Anyone with the verification link can view this name, course, and
            issue date. Your email and exam answers remain private.
          </p>
        </form>
      ) : (
        <div className="certification-next-step">
          <p>
            {progress.modules} of {track.modules.length} modules completed ·{" "}
            {progress.exams} of {track.exams.length} exams passed
          </p>
          <Link
            className="button primary"
            to={
              nextLesson
                ? `/learn/${nextLesson.id}`
                : nextExam
                  ? `/exams/${nextExam.id}`
                  : `/curriculum/${track.id}`
            }
          >
            {nextLesson ? "Continue learning" : "Continue to exam"}
            <ArrowRight size={16} />
          </Link>
        </div>
      )}
      <section aria-labelledby="requirements-heading">
        <div className="section-heading">
          <h2 id="requirements-heading">Course requirements</h2>
        </div>
        <ul className="certification-requirements">
          {[
            ...track.modules.map((lesson) => ({
              id: `lesson-${lesson.id}`,
              title: lesson.title,
              path: `/learn/${lesson.id}`,
              done: state.completed.includes(lesson.id),
              label: "Module",
            })),
            ...track.exams.map((exam) => ({
              id: `exam-${exam.id}`,
              title: exam.title,
              path: `/exams/${exam.id}`,
              done: examPassed(exam, state),
              label: "Exam",
            })),
          ].map((item) => (
            <li key={item.id}>
              <Link to={item.path}>
                {item.done ? (
                  <CheckCircle2
                    size={18}
                    className="positive"
                    aria-hidden="true"
                  />
                ) : (
                  <Circle size={18} aria-hidden="true" />
                )}
                <span>
                  <small>
                    {item.label} · {item.done ? "Complete" : "To complete"}
                  </small>
                  <strong>{item.title}</strong>
                </span>
                <ArrowRight size={15} aria-hidden="true" />
              </Link>
            </li>
          ))}
        </ul>
      </section>
      <p className="fine-print certification-note">
        This certificate records self-directed course completion and open-book
        assessments. It is not an accredited qualification or a professional
        license.
      </p>
      <AuthModal open={authOpen} onOpenChange={setAuthOpen} />
    </div>
  );
}
