import { ExternalLink } from "@/shared/components/ui";
import { ShieldCheck, FileText, Server, Cpu, AlertTriangle } from "lucide-react";
import { useState } from "react";
import { useLocation, Link } from "react-router-dom";

export default function LegalPage() {
  const location = useLocation();
  const isTermsInitial = location.pathname.includes("terms");
  const [tab, setTab] = useState<"privacy" | "terms">(
    isTermsInitial ? "terms" : "privacy",
  );

  return (
    <div className="page legal-page" style={{ maxWidth: 860, margin: "0 auto", paddingBottom: "4rem" }}>
      <div className="page-eyebrow">COMPLIANCE & TRANSPARENCY</div>
      <h1>Legal &amp; Data Policies</h1>
      <p className="page-subtitle">
        Information about Quanta&apos;s self-hosted architecture, local data storage, and external AI processing.
      </p>

      <div style={{ display: "flex", gap: "0.75rem", margin: "1.5rem 0 2rem" }}>
        <button
          className={`button ${tab === "privacy" ? "primary" : "secondary"}`}
          onClick={() => setTab("privacy")}
        >
          <ShieldCheck size={16} style={{ marginRight: 6 }} />
          Privacy Policy
        </button>
        <button
          className={`button ${tab === "terms" ? "primary" : "secondary"}`}
          onClick={() => setTab("terms")}
        >
          <FileText size={16} style={{ marginRight: 6 }} />
          Terms of Service
        </button>
      </div>

      {tab === "privacy" ? (
        <div className="legal-content" style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
          <section className="tool-card" style={{ padding: "1.75rem" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "1rem" }}>
              <Server size={22} className="text-accent" />
              <h2 style={{ margin: 0, fontSize: "1.25rem" }}>1. 100% Self-Hosted &amp; Private Infrastructure</h2>
            </div>
            <p style={{ lineHeight: 1.6, color: "var(--text-secondary, #ccc)" }}>
              Quanta is designed and operated as a fully self-hosted quantitative finance and investment research platform.
              All trading simulations, quantitative strategies, research notebooks, market datasets, curriculum progress,
              exam scores, and user accounts reside entirely within your private containerized environment.
            </p>
            <p style={{ lineHeight: 1.6, color: "var(--text-secondary, #ccc)", marginTop: "0.75rem" }}>
              We do not track your activity, collect telemetry, profile your investment decisions, or monetize your research.
              Your data is never transmitted to advertisers, data brokers, or commercial finance companies.
            </p>
          </section>

          <section className="tool-card" style={{ padding: "1.75rem" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "1rem" }}>
              <Cpu size={22} className="text-accent" />
              <h2 style={{ margin: 0, fontSize: "1.25rem" }}>2. AI Capabilities via OpenRouter</h2>
            </div>
            <p style={{ lineHeight: 1.6, color: "var(--text-secondary, #ccc)" }}>
              For intelligent code explanation, interactive quant tutoring, formula breakdowns, and notebook strategy assistance,
              Quanta connects to leading foundation models through <strong>OpenRouter</strong>.
            </p>
            <p style={{ lineHeight: 1.6, color: "var(--text-secondary, #ccc)", marginTop: "0.75rem" }}>
              When you prompt an AI assistant or request an automated code review, only the specific prompt and contextual snippet
              necessary for inference are dispatched to OpenRouter. For full transparency regarding how OpenRouter processes and handles API transmissions, please consult:
            </p>
            <ul style={{ margin: "1rem 0 0 1.5rem", lineHeight: 1.8, color: "var(--text-secondary, #ccc)" }}>
              <li>
                <ExternalLink href="https://openrouter.ai/privacy">
                  OpenRouter Privacy Policy
                </ExternalLink>
              </li>
              <li>
                <ExternalLink href="https://openrouter.ai/terms">
                  OpenRouter Terms of Service
                </ExternalLink>
              </li>
            </ul>
          </section>

          <section className="tool-card" style={{ padding: "1.75rem" }}>
            <h2 style={{ margin: "0 0 1rem", fontSize: "1.25rem" }}>3. Data Retention &amp; Local Ownership</h2>
            <p style={{ lineHeight: 1.6, color: "var(--text-secondary, #ccc)" }}>
              All database records, strategy code files, backtest logs, and user credentials are stored in your private PostgreSQL and Redis databases
              or local filesystem volumes. You retain complete ownership, with full authority to backup, inspect, export, or delete any and all records at will.
            </p>
          </section>

          <section className="tool-card" style={{ padding: "1.75rem" }}>
            <h2 style={{ margin: "0 0 1rem", fontSize: "1.25rem" }}>4. Privacy Contact</h2>
            <p style={{ lineHeight: 1.6, color: "var(--text-secondary, #ccc)" }}>
              For any questions, requests, or privacy concerns regarding this policy or your data, please contact us at:{" "}
              <a href="mailto:nevatalapp@gmail.com" className="text-link" style={{ fontWeight: 600 }}>
                nevatalapp@gmail.com
              </a>
            </p>
          </section>
        </div>
      ) : (
        <div className="legal-content" style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
          <section className="tool-card" style={{ padding: "1.75rem" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "1rem" }}>
              <AlertTriangle size={22} className="text-accent" />
              <h2 style={{ margin: 0, fontSize: "1.25rem" }}>1. Financial &amp; Investment Disclaimer</h2>
            </div>
            <p style={{ lineHeight: 1.6, color: "var(--text-secondary, #ccc)" }}>
              Quanta is strictly an educational, mathematical, and algorithmic research software platform. It does not provide investment,
              financial, tax, accounting, or legal advice.
            </p>
            <p style={{ lineHeight: 1.6, color: "var(--text-secondary, #ccc)", marginTop: "0.75rem" }}>
              All market simulators, historical backtests, pricing formulas, and quantitative models are hypothetical approximations.
              Past performance, backtested returns, and paper-trading metrics do not guarantee real-world results. Users are solely responsible
              for evaluating any trading strategy or financial instrument before committing capital.
            </p>
          </section>

          <section className="tool-card" style={{ padding: "1.75rem" }}>
            <h2 style={{ margin: "0 0 1rem", fontSize: "1.25rem" }}>2. OpenRouter AI Service Terms</h2>
            <p style={{ lineHeight: 1.6, color: "var(--text-secondary, #ccc)" }}>
              By using AI-assisted features (strategy explanations, question assistance, code hints), you acknowledge that queries are processed
              via OpenRouter&apos;s API infrastructure and agree to their terms of use:
            </p>
            <ul style={{ margin: "1rem 0 0 1.5rem", lineHeight: 1.8, color: "var(--text-secondary, #ccc)" }}>
              <li>
                <ExternalLink href="https://openrouter.ai/terms">
                  OpenRouter Terms of Service
                </ExternalLink>
              </li>
              <li>
                <ExternalLink href="https://openrouter.ai/privacy">
                  OpenRouter Privacy Policy
                </ExternalLink>
              </li>
            </ul>
          </section>

          <section className="tool-card" style={{ padding: "1.75rem" }}>
            <h2 style={{ margin: "0 0 1rem", fontSize: "1.25rem" }}>3. Software License &amp; Limitation of Liability</h2>
            <p style={{ lineHeight: 1.6, color: "var(--text-secondary, #ccc)" }}>
              Quanta is provided &ldquo;as is&rdquo;, without warranty of any kind, express or implied. Under no circumstances shall the authors,
              developers, or maintainers be liable for any direct, indirect, incidental, or consequential damages resulting from data errors,
              computational inaccuracies, network disruptions, or investment decisions made in connection with this software.
            </p>
          </section>

          <section className="tool-card" style={{ padding: "1.75rem" }}>
            <h2 style={{ margin: "0 0 1rem", fontSize: "1.25rem" }}>4. Inquiries &amp; Support Contact</h2>
            <p style={{ lineHeight: 1.6, color: "var(--text-secondary, #ccc)" }}>
              For legal inquiries, terms clarification, or notices, contact:{" "}
              <a href="mailto:nevatalapp@gmail.com" className="text-link" style={{ fontWeight: 600 }}>
                nevatalapp@gmail.com
              </a>
            </p>
          </section>
        </div>
      )}

      <div style={{ marginTop: "3rem", paddingTop: "1.5rem", borderTop: "1px solid var(--border-color, #333)" }}>
        <Link to="/" className="text-link">
          &larr; Return to Quanta Overview
        </Link>
      </div>
    </div>
  );
}
