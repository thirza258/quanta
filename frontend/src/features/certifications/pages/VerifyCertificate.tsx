import { useState, type FormEvent } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Search } from "lucide-react";
import { verificationPath } from "../model/certificates";
import { CertificateView } from "./CertificateDetail";
import "../certifications.css";

export default function VerifyCertificate() {
  const { certificateId } = useParams();
  return (
    <main className="public-verification">
      <header className="verification-header">
        <Link className="certificate-brand" to="/">
          quanta.
        </Link>
        <Link className="text-link" to="/certifications">
          My certifications
        </Link>
      </header>
      {certificateId ? (
        <CertificateView key={certificateId} id={certificateId} publicView />
      ) : (
        <VerificationSearch />
      )}
    </main>
  );
}

function VerificationSearch() {
  const [id, setId] = useState("");
  const navigate = useNavigate();
  function verify(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (id.trim()) navigate(verificationPath(id.trim().toUpperCase()));
  }
  return (
    <section className="verification-search">
      <div className="page-eyebrow">
        QUANTA LEARNING · CERTIFICATE VERIFICATION
      </div>
      <h1>Verify a certificate</h1>
      <p className="page-subtitle">
        Check a certificate against Quanta’s original issuer record. You’ll see
        the learner’s name, completed course, and issue date.
      </p>
      <form onSubmit={verify}>
        <label className="field">
          Certificate ID
          <input
            value={id}
            onChange={(event) => setId(event.target.value)}
            placeholder="QTA-…"
            maxLength={100}
            required
            autoComplete="off"
            spellCheck={false}
          />
        </label>
        <button className="button primary" disabled={!id.trim()}>
          <Search size={16} /> Verify certificate
        </button>
      </form>
      <p className="fine-print">
        Verification confirms that Quanta issued the record. Course assessments
        are open book and names are self-reported; it does not verify identity
        or professional accreditation.
      </p>
    </section>
  );
}
