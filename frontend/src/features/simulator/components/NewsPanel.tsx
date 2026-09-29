import { clock, percent } from "@/features/simulator/model/format";
import type { NewsFeed, NewsItem } from "@/features/simulator/model/types";
import "@/features/simulator/simulator.css";

const SCOPE_LABEL: Record<string, string> = {
  company: "CO",
  sector: "SEC",
  macro: "ECO",
  market: "MKT",
};

function Gauge({ score, label }: { score: number; label: string }) {
  // Score runs -1…+1; the bar fills from the centre in the direction of the tone.
  const width = Math.min(50, Math.abs(score) * 50);
  return (
    <div className="sim-gauge">
      <span className="sim-gauge-label">{label}</span>
      <div className="sim-gauge-track" aria-hidden="true">
        <span
          className={score >= 0 ? "up" : "down"}
          style={{
            width: `${width}%`,
            left: score >= 0 ? "50%" : `${50 - width}%`,
          }}
        />
      </div>
      <span className={`sim-gauge-value ${score >= 0 ? "sim-up" : "sim-down"}`}>
        {score >= 0 ? "+" : ""}
        {score.toFixed(2)}
      </span>
    </div>
  );
}

export default function NewsPanel({
  feed,
  symbol,
  scope,
  onScope,
  onSymbol,
  show,
}: {
  feed: NewsFeed | null;
  symbol: string;
  scope: "all" | "symbol";
  onScope: (next: "all" | "symbol") => void;
  onSymbol: (symbol: string) => void;
  show: boolean;
}) {
  const items: NewsItem[] = feed?.items ?? [];
  const reading = feed?.sentiment;
  return (
    <section
      className={`sim-news ${show ? "show" : ""}`}
      aria-label="Simulated news feed"
    >
      <div className="sim-section-title">
        <strong>Newsroom</strong>
        <span className="sim-sim-badge">SIMULATED</span>
      </div>
      <div className="sim-news-scope" role="group" aria-label="News scope">
        {(
          [
            ["all", "All markets"],
            ["symbol", symbol],
          ] as const
        ).map(([value, label]) => (
          <button
            key={value}
            className={scope === value ? "active" : ""}
            aria-pressed={scope === value}
            onClick={() => onScope(value)}
          >
            {label}
          </button>
        ))}
      </div>
      {reading ? (
        <div className="sim-sentiment">
          <Gauge score={reading.session.score} label="Session" />
          <Gauge score={reading.week.score} label="5 sessions" />
          <p className="sim-small">
            {reading.session.items} items this session ·{" "}
            <span className="sim-up">{reading.session.positive} positive</span>{" "}
            ·{" "}
            <span className="sim-down">
              {reading.session.negative} negative
            </span>{" "}
            · {reading.session.neutral} neutral · market tone{" "}
            {percent(reading.market.score, 0)}
          </p>
        </div>
      ) : null}
      {feed && !feed.available ? (
        <p className="sim-small" role="status">
          {feed.notice}
        </p>
      ) : null}
      <ol className="sim-news-list">
        {items.map((item) => (
          <li key={item.id} className={`sim-news-item ${item.sentiment}`}>
            <div className="sim-news-meta">
              <span className="sim-news-time">{clock(item.time)}</span>
              <span className={`sim-news-scope-tag ${item.scope}`}>
                {SCOPE_LABEL[item.scope] ?? "MKT"}
              </span>
              {item.symbol ? (
                <button
                  className="sim-news-ticker"
                  onClick={() => onSymbol(item.symbol!)}
                  title={`Open ${item.symbol}`}
                >
                  {item.symbol}
                </button>
              ) : null}
              <span
                className={`sim-news-impact impact-${item.impact}`}
                title={`Modeled impact: ${item.impact}`}
              >
                {item.impact === "none" ? "·" : item.impact[0].toUpperCase()}
              </span>
            </div>
            <p className="sim-news-headline">{item.headline}</p>
            <p className="sim-news-source">
              {item.source} · {item.category}
              {item.points ? (
                <span
                  className={`sim-news-points ${item.points > 0 ? "up" : "down"}`}
                  title={`Scored ${item.points} points. One point is one basis point of modeled price move: ${(item.points / 100).toFixed(2)}% in total, 58% of it on this bar and the rest drifting.`}
                >
                  {item.points > 0 ? "+" : ""}
                  {item.points} pts
                </span>
              ) : (
                <span
                  className="sim-news-points flat"
                  title="No modeled price effect"
                >
                  0 pts
                </span>
              )}
            </p>
          </li>
        ))}
      </ol>
      {feed && feed.available && !items.length ? (
        <p className="sim-small">
          No headlines have been released at this point in the replay yet.
        </p>
      ) : null}
      <p className="sim-small sim-news-disclosure">
        {feed?.disclosure ??
          "Simulated market · fictional companies, fictional headlines"}
      </p>
    </section>
  );
}
