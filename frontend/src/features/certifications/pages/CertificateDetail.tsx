import {
  certificateDate,
  matchesCourse,
  verificationPath,
} from "../model/certificates";
import { useVerification } from "../model/useCertificates";
import { tracks } from "@/features/learning/model/catalog";
import { Loading } from "@/shared/components/ui";
import { ArrowLeft, Award, CheckCircle2, Copy, Printer } from "lucide-react";
import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import "../certifications.css";

export default function CertificateDetail() {
  const { certificateId } = useParams();
  return <CertificateView key={certificateId} id={certificateId ?? ""} />;
}

export function CertificateView({
  id,
  publicView = false,
}: {
  id: string;
  publicView?: boolean;
}) {
  const { certificate, loading, error, retry } = useVerification(id);
  const [copyStatus, setCopyStatus] = useState("");
  if (loading)
    return <Loading label="Checking the certificate issuer record…" />;
  if (error)
    return (
      <div className="page">
        <h1>Verification unavailable</h1>
        <p role="alert" className="page-subtitle">
          {error}
        </p>
        <button className="button secondary" onClick={retry}>
          Try again
        </button>
      </div>
    );
  if (!certificate)
    return (
      <div className="page">
        <h1>Certificate not found</h1>
        <p className="page-subtitle">
          No issued certificate matches this ID. Check the ID on the certificate
          and try again.
        </p>
        <Link className="text-link back-link" to="/verify">
          Verify another certificate
        </Link>
      </div>
    );
  const track = tracks.find((item) => item.id === certificate.trackId);
  const earlierCourse = track && !matchesCourse(certificate, track);
  const verificationUrl = `${window.location.origin}${verificationPath(certificate.id)}`;
  return (
    <div className="page certificate-detail-page">
      <div className="certificate-toolbar">
        <Link
          className="text-link"
          to={publicView ? "/verify" : "/certifications"}
        >
          <ArrowLeft size={15} />{" "}
          {publicView ? "Verify another certificate" : "All certifications"}
        </Link>
        <button
          className="button secondary"
          onClick={async () => {
            try {
              await navigator.clipboard.writeText(verificationUrl);
              setCopyStatus("Verification link copied.");
            } catch {
              setCopyStatus(
                "Copy the verification link shown on the certificate below.",
              );
            }
          }}
        >
          <Copy size={16} /> Copy verification link
        </button>
        <button className="button primary" onClick={() => window.print()}>
          <Printer size={16} /> Print / save PDF
        </button>
      </div>
      <div className="verification-banner" role="status">
        <CheckCircle2 size={20} />
        <div>
          <strong>Issuer record verified</strong>
          <p>
            Quanta issued this certificate. The name, course, and issue date
            below match the original record.
          </p>
        </div>
      </div>
      {copyStatus ? (
        <p className="certificate-print-help" role="status">
          {copyStatus}
        </p>
      ) : null}
      <article
        className="certificate-document"
        aria-label="Course completion certificate"
      >
        <div className="certificate-brand">
          quanta<span>.</span>
        </div>
        <div className="certificate-seal">
          <Award size={42} strokeWidth={1.3} aria-hidden="true" />
        </div>
        <p className="certificate-kicker">A MILESTONE IN YOUR LEARNING</p>
        <h1>Certificate of completion</h1>
        <p className="certificate-intro">Awarded to</p>
        <h2 className="certificate-recipient">{certificate.recipientName}</h2>
        <p>for completing the Quanta course</p>
        <h3 className="certificate-course-title">{certificate.courseTitle}</h3>
        <p>
          {certificate.lessonIds.length} modules completed ·{" "}
          {Object.keys(certificate.examVersions).length} exams passed
          <br />
          {certificate.studyMinutes} minutes of guided study
        </p>
        <div className="certificate-details">
          <div>
            <span>ISSUED</span>
            <strong>
              <time dateTime={certificate.issuedAt}>
                {certificateDate(certificate.issuedAt)}
              </time>
            </strong>
          </div>
          <div>
            <span>ISSUED BY</span>
            <strong>Quanta Learning</strong>
          </div>
        </div>
        <p className="certificate-identifier">
          Certificate ID: {certificate.id}
        </p>
        <p className="certificate-verification-link">
          Verify: <a href={verificationUrl}>{verificationUrl}</a>
        </p>
        <p className="certificate-disclosure">
          A record of self-directed study and open-book assessments based on
          recorded module completion and exam answers checked by Quanta. The
          learner name is self-reported. This is not an accredited qualification
          or professional license.
        </p>
      </article>
      <p className="fine-print certificate-print-help">
        Choose “Save as PDF” in the print dialog to download a copy. Share the
        verification link so others can check the original issuer record without
        signing in.
      </p>
      {earlierCourse ? (
        <p className="fine-print certificate-print-help">
          This certificate records an earlier edition of the course.{" "}
          <Link className="text-link" to={`/certifications/course/${track.id}`}>
            View current requirements
          </Link>
        </p>
      ) : null}
    </div>
  );
}
