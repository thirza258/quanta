import { multiple, percent, price } from "@/features/simulator/model/format";
import type {
  DeskView,
  MoverRow,
  SymbolAnalytics,
} from "@/features/simulator/model/types";
import "@/features/simulator/simulator.css";

function Movers({
  title,
  rows,
  onSymbol,
}: {
  title: string;
  rows: MoverRow[];
  onSymbol: (symbol: string) => void;
}) {
  return (
    <>
      <h4>{title}</h4>
      <table className="sim-desk-table">
        <thead>
          <tr>
            <th scope="col">Symbol</th>
            <th scope="col">Last</th>
            <th scope="col">Change</th>
            <th scope="col">Tone</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.symbol}>
              <td>
                <button onClick={() => onSymbol(row.symbol)} title={row.name}>
                  {row.symbol}
                </button>
              </td>
              <td>{price(row.close)}</td>
              <td className={row.change_pct >= 0 ? "sim-up" : "sim-down"}>
                {row.change_pct >= 0 ? "+" : ""}
                {row.change_pct.toFixed(2)}%
              </td>
              <td className={(row.sentiment ?? 0) >= 0 ? "sim-up" : "sim-down"}>
                {row.sentiment === null ? "—" : row.sentiment.toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

export default function DeskPanel({
  desk,
  error,
  analytics,
  onSymbol,
  show,
}: {
  desk: DeskView | null;
  error: string;
  analytics: SymbolAnalytics | null;
  onSymbol: (symbol: string) => void;
  show: boolean;
}) {
  // A warming-up indicator has no value yet; it is not a price of zero.
  const level = (value: number | null) => (value === null ? "—" : price(value));
  return (
    <section
      className={`sim-desk ${show ? "show" : ""}`}
      aria-label="Desk analytics"
    >
      <div className="sim-section-title">
        <strong>Desk</strong>
        <span className="sim-sim-badge">API CALCULATED</span>
      </div>
      {analytics ? (
        <>
          <h4>{analytics.symbol} quant sheet</h4>
          <dl className="sim-desk-stats">
            {(
              [
                ["Last", price(analytics.close)],
                ["SMA 20", level(analytics.indicators.sma_20)],
                ["SMA 50", level(analytics.indicators.sma_50)],
                ["EMA 20", level(analytics.indicators.ema_20)],
                [
                  "RSI 14",
                  analytics.indicators.rsi_14 === null
                    ? "—"
                    : analytics.indicators.rsi_14.toFixed(1),
                ],
                [
                  "MACD hist.",
                  analytics.indicators.macd
                    ? analytics.indicators.macd.histogram.toFixed(3)
                    : "—",
                ],
                ["Volatility (ann.)", percent(analytics.risk.volatility_short)],
                ["Beta", multiple(analytics.risk.beta, 2)],
                ["Correlation", multiple(analytics.risk.correlation, 2)],
                [
                  "Session move",
                  analytics.momentum.session === null
                    ? "—"
                    : `${analytics.momentum.session.toFixed(2)}%`,
                ],
                ["Since open", `${analytics.momentum.since_open.toFixed(2)}%`],
                [
                  "Relative volume",
                  analytics.liquidity.average_volume_20
                    ? multiple(
                        analytics.liquidity.volume /
                          analytics.liquidity.average_volume_20,
                        2,
                      )
                    : "—",
                ],
              ] as [string, string][]
            ).map(([label, value]) => (
              <div key={label}>
                <dt>{label}</dt>
                <dd>{value}</dd>
              </div>
            ))}
          </dl>
        </>
      ) : null}
      {desk ? (
        <>
          <Movers
            title="Top gainers"
            rows={desk.movers.gainers}
            onSymbol={onSymbol}
          />
          <Movers
            title="Top losers"
            rows={desk.movers.losers}
            onSymbol={onSymbol}
          />
          <Movers
            title="Most active"
            rows={desk.movers.active}
            onSymbol={onSymbol}
          />
          <h4>Sectors</h4>
          <table className="sim-desk-table">
            <thead>
              <tr>
                <th scope="col">Sector</th>
                <th scope="col">Change</th>
                <th scope="col">Tone</th>
              </tr>
            </thead>
            <tbody>
              {desk.movers.sectors.map((row) => (
                <tr key={row.sector}>
                  <td>{row.sector}</td>
                  <td className={row.change_pct >= 0 ? "sim-up" : "sim-down"}>
                    {row.change_pct >= 0 ? "+" : ""}
                    {row.change_pct.toFixed(2)}%
                  </td>
                  <td>
                    {row.sentiment === null ? "—" : row.sentiment.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="sim-small">
            Breadth: {desk.movers.breadth.advancing} advancing ·{" "}
            {desk.movers.breadth.declining} declining · average{" "}
            {desk.movers.breadth.average_change_pct.toFixed(2)}%
          </p>
          <p className="sim-small sim-news-disclosure">{desk.disclosure}</p>
        </>
      ) : (
        <p className="sim-small" role={error ? "alert" : "status"}>
          {error || "Loading desk analytics…"}
        </p>
      )}
    </section>
  );
}
