import { certificateDate, matchesCourse } from "../model/certificates";
import { useCertificates } from "../model/useCertificates";
import { trackLabel, tracks } from "@/features/learning/model/catalog";
import { trackProgress } from "@/features/learning/model/progress";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import { EmptyState, Loading } from "@/shared/components/ui";
import { ArrowRight, Award, BookOpen, CheckCircle2 } from "lucide-react";
import { Link } from "react-router-dom";
import "../certifications.css";

export default function Certifications() {
  const { state, user } = useWorkspace();
  const { certificates, loading, error, retry } = useCertificates(user?.id);
  const available = tracks.filter(
    (track) =>
      !certificates.some((certificate) => matchesCourse(certificate, track)),
  );
  const ready = available.filter(
    (track) => trackProgress(track, state).complete,
  ).length;
  return (
    <div className="page certifications-page">
      <div className="page-eyebrow">
        <Award size={15} /> RECOGNIZE YOUR PROGRESS
      </div>
      <div className="page-title-row">
        <div>
          <h1>Certifications</h1>
          <p className="page-subtitle">
            Turn the work you put in into a record of what you’ve learned.
            Complete a course, claim your certificate, and keep a copy.
          </p>
        </div>
        <div className="certification-heading-actions">
          <Link to="/verify" className="button secondary">
            <Award size={16} /> Verify a certificate
          </Link>
          <Link to="/curriculum" className="button secondary">
            <BookOpen size={16} /> Browse courses
          </Link>
        </div>
      </div>
      <div
        className="certification-summary"
        aria-label="Certification progress"
      >
        <div>
          <strong>{loading || error ? "—" : certificates.length}</strong>
          <span>Certificates earned</span>
        </div>
        <div>
          <strong>{ready}</strong>
          <span>Ready to claim</span>
        </div>
        <p>
          Complete every module and pass every current exam in a course to earn
          its certificate.
        </p>
      </div>
      <section aria-labelledby="earned-heading">
        <div className="section-heading">
          <h2 id="earned-heading">Your certificates</h2>
        </div>
        {loading ? (
          <Loading label="Loading your certificates…" />
        ) : error ? (
          <div role="alert">
            <p>{error}</p>
            <button className="button secondary" onClick={retry}>
              Try again
            </button>
          </div>
        ) : certificates.length ? (
          <div className="certification-grid">
            {certificates.map((certificate) => (
              <article
                className="certification-card earned"
                key={certificate.id}
              >
                <div className="certification-card-top">
                  <Award size={28} />
                  <span className="certification-status">Earned</span>
                </div>
                <h3>{certificate.courseTitle}</h3>
                <p>{certificate.recipientName}</p>
                <p className="muted">
                  Issued {certificateDate(certificate.issuedAt)}
                </p>
                <Link
                  className="button secondary"
                  to={`/certifications/${certificate.id}`}
                >
                  View certificate <ArrowRight size={15} />
                </Link>
              </article>
            ))}
          </div>
        ) : (
          <EmptyState
            icon={<Award size={25} />}
            title="Your first certificate starts with a course"
            description={
              ready
                ? "You’ve completed a course. Claim your certificate below."
                : "Your earned certificates will appear here, ready to print or save as a PDF."
            }
          />
        )}
      </section>
      {available.length ? (
        <section aria-labelledby="available-heading">
          <div className="section-heading">
            <div>
              <h2 id="available-heading">Earn a certificate</h2>
              <p>One course. A new milestone.</p>
            </div>
          </div>
          <div className="certification-grid">
            {available.map((track) => {
              const progress = trackProgress(track, state);
              return (
                <article className="certification-card" key={track.id}>
                  <div className="certification-card-top">
                    <span className="eyebrow">{trackLabel(track)}</span>
                    <span className="certification-status">
                      {progress.complete ? (
                        <>
                          <CheckCircle2 size={14} /> Ready to claim
                        </>
                      ) : (
                        `${progress.percent}% complete`
                      )}
                    </span>
                  </div>
                  <h3>{track.title}</h3>
                  <p>
                    {progress.modules} of {track.modules.length} modules
                    completed
                    <br />
                    {progress.exams} of {track.exams.length} exams passed
                  </p>
                  <progress
                    className="certification-progress"
                    value={progress.percent}
                    max={100}
                    aria-label={`${track.title} completion`}
                  >
                    {progress.percent}%
                  </progress>
                  <Link
                    className={`button ${progress.complete ? "primary" : "secondary"}`}
                    to={`/certifications/course/${track.id}`}
                  >
                    {progress.complete
                      ? "Claim certificate"
                      : "View requirements"}
                    <ArrowRight size={15} />
                  </Link>
                </article>
              );
            })}
          </div>
        </section>
      ) : null}
      <p className="fine-print certification-note">
        Quanta issues course completion certificates for self-directed study and
        open-book assessments. These are learning records, not accredited
        qualifications or professional licenses.
      </p>
    </div>
  );
}
