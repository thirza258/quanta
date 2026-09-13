import { Link, useLocation } from "react-router-dom";
import {
  ArrowUpRight,
  BookOpen,
  Code2,
  Database,
  FlaskConical,
  Server,
} from "lucide-react";
import { ExternalLink } from "./ui";
const references = [
  [
    "Security Analysis",
    "Benjamin Graham & David Dodd",
    "The foundations of intrinsic value, earning power, senior claims, and margin of safety. Quanta’s lessons are original explanations, not reproductions of the textbook.",
    "Tracks 01 & 04",
    "https://www.mheducation.com/highered.html",
  ],
  [
    "Quantitative Investment Analysis",
    "CFA Institute · DeFusco and coauthors",
    "Probability, estimation, regression, time series, portfolio construction, and quantitative risk management.",
    "Tracks 02 & 03",
    "https://www.cfainstitute.org/insights/professional-learning/refresher-readings",
  ],
  [
    "Fama–French Data Library",
    "Kenneth R. French · Dartmouth",
    "Primary source for factor definitions, construction methods, and research datasets. Inspect coverage and methodology before use.",
    "Factor research",
    "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
  ],
  [
    "EDGAR Company Filings",
    "U.S. Securities and Exchange Commission",
    "Company filings with public availability timestamps. Distinguish reporting-period dates from actual filing dates.",
    "Fundamental data",
    "https://www.sec.gov/edgar/search/",
  ],
  [
    "Uniswap Protocol Documentation",
    "Uniswap Labs",
    "Pool invariants, concentrated liquidity, swaps, and protocol mechanics.",
    "Track 06",
    "https://docs.uniswap.org/",
  ],
];
export default function Library() {
  const { pathname } = useLocation();
  return pathname === "/methodology" ? (
    <Methodology />
  ) : (
    <div className="page">
      <div className="page-eyebrow">GO TO THE SOURCE</div>
      <h1>Reference library</h1>
      <p className="page-subtitle">
        A small, considered collection for deeper study.
      </p>
      <div className="reference-list">
        {references.map(([title, author, description, tag, href]) => (
          <article className="reference-card" key={title}>
            <span className="reference-icon">
              <BookOpen size={23} />
            </span>
            <div>
              <span className="eyebrow">{tag}</span>
              <h2>{title}</h2>
              <span className="reference-author">{author}</span>
              <p>{description}</p>
            </div>
            <ExternalLink href={href}>Visit source</ExternalLink>
          </article>
        ))}
      </div>
      <p className="fine-print">
        Source links may lead to publisher catalogs or external documentation.
        Quanta does not bundle copyrighted textbooks or restricted market
        datasets.
      </p>
    </div>
  );
}
function Methodology() {
  return (
    <div className="page methodology-page">
      <div className="page-eyebrow">SUBSTANCE OVER DECORATION</div>
      <h1>A workspace for thinking carefully.</h1>
      <p className="page-subtitle">
        How the lessons, models, and research tools fit together.
      </p>
      <div className="methodology-grid">
        <section className="tool-card">
          <BookOpen size={23} />
          <h2>Read, then reproduce.</h2>
          <p>
            Each of the 29 modules contains an original explanation, a
            mathematical relationship, a worked example, and an exercise.
            Complete the exercise to mark the module done. Use reading, split,
            or sandbox view to match the task.
          </p>
          <Link to="/curriculum" className="text-link">
            Explore the curriculum
            <ArrowUpRight size={14} />
          </Link>
        </section>
        <section className="tool-card">
          <FlaskConical size={23} />
          <h2>Make assumptions visible.</h2>
          <p>
            The sandbox uses seeded synthetic markets by default. A signal
            observed at a close fills at the next bar’s open, with configured
            commissions and slippage. The benchmark buys and holds the same
            asset, paying entry costs.
          </p>
          <p>
            Annualized risk metrics use 252 observations and a 3% risk-free
            rate. Open trades are marked to the last close and excluded from
            closed-trade win rate and profit factor.
          </p>
        </section>
        <section className="tool-card">
          <Code2 size={23} />
          <h2>Two execution environments.</h2>
          <p>
            The default guided Python interpreter supports arithmetic,
            functions, bounded loops, lists, and numeric series. Available data:
            close, open, high, low, volume, returns, sma_50, and sma_200. The
            window slider adjusts sma_50.
          </p>
          <p>
            Return Boolean long/cash signals from strategy(data). Selected math
            and NumPy functions are available. Code runs in a fresh process with
            a two-second limit. The optional Docker runtime enables NumPy,
            Pandas, Polars, SciPy, and Statsmodels.
          </p>
          <pre className="inline-code">
            {'def strategy(data):\n    return data["close"] > data["sma_50"]'}
          </pre>
        </section>
        <section className="tool-card">
          <Database size={23} />
          <h2>Know where the data came from.</h2>
          <p>
            Named synthetic scenarios illustrate a stress mechanism; they are
            not reconstructions of historical episodes. Simulated calendars omit
            weekends but do not model exchange holidays.
          </p>
          <p>
            To use historical data, supply a licensed CSV with time, open, high,
            low, close, and volume. The importer validates the bars and stores
            Parquet for DuckDB queries. Corporate actions, filing dates, and
            delisted-universe coverage remain the data provider’s
            responsibility.
          </p>
          <pre className="inline-code">
            backend/.venv/bin/python scripts/import_data.py prices.csv SPY
          </pre>
        </section>
        <section className="tool-card">
          <Server size={23} />
          <h2>Keep your workspace.</h2>
          <p>
            Guest progress, drafts, notes, and experiments save in this browser.
            Create an account to copy your guest work into a persistent API
            workspace. Signed-in changes sync to SQLite locally or PostgreSQL in
            Docker.
          </p>
          <p>
            Export notes and experiments for portable copies. If account sync
            fails, your local edits stay on this device. Avoid editing the same
            account in two tabs at once; version checks prevent silent
            overwrites.
          </p>
          <pre className="inline-code">docker compose up --build -d</pre>
        </section>
        <section className="tool-card">
          <Database size={23} />
          <h2>Understand the boundaries.</h2>
          <p>
            The paper broker and AMM panels simulate execution. No real funds,
            wallets, brokerage accounts, or AI providers are connected. The
            broker account is scoped to its current panel session.
          </p>
          <p>
            OAuth, live feeds, autonomous deployment, external notifications,
            and production model evaluation need additional provider
            configuration and operational work. See the repository
            implementation notes for the full scope.
          </p>
        </section>
      </div>
    </div>
  );
}
