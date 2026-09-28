import { dollars, percent, signed } from "@/features/simulator/model/format";
import type { DeskView } from "@/features/simulator/model/types";
import "@/features/simulator/simulator.css";

export default function PerformancePanel({
  desk,
  error,
  onSymbol,
}: {
  desk: DeskView | null;
  error: string;
  onSymbol: (symbol: string) => void;
}) {
  if (!desk)
    return (
      <p className="sim-small" role={error ? "alert" : "status"}>
        {error || "Loading account analytics…"}
      </p>
    );
  const p = desk.performance;
  // A compact sparkline of the equity path the API marked bar by bar, drawn
  // against the index on one shared scale so the two are actually comparable.
  const values = p.curve.map((point) => point.equity);
  const market = p.benchmark.curve.map((point) => point.equity);
  const low = Math.min(...values, ...market, p.opening_equity);
  const high = Math.max(...values, ...market, p.opening_equity);
  const span = high - low || 1;
  const plot = (series: number[]) =>
    series
      .map(
        (value, index) =>
          `${(index / Math.max(1, series.length - 1)) * 100},${30 - ((value - low) / span) * 28}`,
      )
      .join(" ");
  const path = plot(values);
  const excess = p.total_return - p.benchmark.total_return;
  const figure = (value: number | null, digits = 2) =>
    value === null ? "—" : value.toFixed(digits);
  return (
    <section className="sim-company" aria-label="Account performance">
      <div className="sim-ratio-grid">
        <div>
          <h4>Result</h4>
          <dl>
            {(
              [
                ["Equity", dollars(p.equity)],
                ["Total return", signed(p.total_return, 2)],
                ["Max drawdown", percent(p.max_drawdown, 2)],
                ["Realized P&L", dollars(p.realized)],
                ["Unrealized P&L", dollars(p.unrealized)],
              ] as [string, string][]
            ).map(([label, value]) => (
              <div key={label}>
                <dt>{label}</dt>
                <dd>{value}</dd>
              </div>
            ))}
          </dl>
        </div>
        <div>
          <h4>Execution</h4>
          <dl>
            {(
              [
                ["Closing trades", String(p.trades)],
                ["Win rate", percent(p.win_rate, 0)],
                [
                  "Profit factor",
                  p.profit_factor === null ? "—" : p.profit_factor.toFixed(2),
                ],
                [
                  "Average win",
                  p.average_win === null ? "—" : dollars(p.average_win),
                ],
                [
                  "Average loss",
                  p.average_loss === null ? "—" : dollars(p.average_loss),
                ],
                ["Average exposure", percent(p.average_exposure, 0)],
                ["Bars observed", String(p.bars_observed)],
                ["Sessions", String(p.sessions)],
              ] as [string, string][]
            ).map(([label, value]) => (
              <div key={label}>
                <dt>{label}</dt>
                <dd>{value}</dd>
              </div>
            ))}
          </dl>
        </div>
        <div>
          <h4>Equity path vs {p.benchmark.name}</h4>
          <svg
            className="sim-sparkline"
            viewBox="0 0 100 32"
            preserveAspectRatio="none"
            role="img"
            aria-label={`Equity moved from ${dollars(p.opening_equity)} to ${dollars(p.equity)}`}
          >
            <polyline
              points={plot(market)}
              fill="none"
              stroke="#8a93a6"
              strokeWidth="1"
              strokeDasharray="3 2"
              vectorEffect="non-scaling-stroke"
            />
            <polyline
              points={path}
              fill="none"
              stroke={p.total_return >= 0 ? "#20a78d" : "#e76676"}
              strokeWidth="1"
              vectorEffect="non-scaling-stroke"
            />
          </svg>
          <p className="sim-small">
            {dollars(p.opening_equity)} → {dollars(p.equity)} over{" "}
            {p.bars_observed} observed bars. The dashed line is{" "}
            {p.benchmark.name} rebased to the same opening balance.
          </p>
        </div>
      </div>
      <h4>Against the market</h4>
      <div className="sim-ratio-grid">
        <div>
          <dl>
            {(
              [
                ["Your return", signed(p.total_return, 2)],
                [
                  `${p.benchmark.name} return`,
                  signed(p.benchmark.total_return, 2),
                ],
                ["Excess return", signed(excess, 2)],
                ["Beta", figure(p.risk.beta)],
                [
                  "Alpha (annualized)",
                  p.risk.alpha === null ? "—" : signed(p.risk.alpha, 2),
                ],
              ] as [string, string][]
            ).map(([label, value]) => (
              <div key={label}>
                <dt>{label}</dt>
                <dd>{value}</dd>
              </div>
            ))}
          </dl>
        </div>
        <div>
          <dl>
            {(
              [
                ["Sharpe", figure(p.risk.sharpe)],
                ["Sortino", figure(p.risk.sortino)],
                ["Calmar", figure(p.risk.calmar)],
                ["CAGR", p.risk.cagr === null ? "—" : signed(p.risk.cagr, 2)],
              ] as [string, string][]
            ).map(([label, value]) => (
              <div key={label}>
                <dt>{label}</dt>
                <dd>{value}</dd>
              </div>
            ))}
          </dl>
        </div>
        <div>
          <dl>
            {(
              [
                ["Daily VaR 95%", percent(p.risk.var_95 ?? null, 2)],
                ["Daily CVaR 95%", percent(p.risk.cvar_95, 2)],
                ["Max drawdown", percent(p.risk.max_drawdown, 2)],
              ] as [string, string][]
            ).map(([label, value]) => (
              <div key={label}>
                <dt>{label}</dt>
                <dd>{value}</dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
      <p className="sim-small" role="note">
        {p.risk_is_meaningful
          ? `Ratios are computed from ${p.sessions} session closes and annualized at 252 sessions a year.`
          : `Only ${p.sessions} session${p.sessions === 1 ? "" : "s"} have closed. Annualizing that few returns produces a number, not a measurement — advance the clock before reading these.`}
      </p>
      <h4>Attribution by company</h4>
      <table className="sim-desk-table sim-attribution">
        <thead>
          <tr>
            <th scope="col">Symbol</th>
            <th scope="col">Shares</th>
            <th scope="col">Fills</th>
            <th scope="col">Realized</th>
            <th scope="col">Unrealized</th>
            <th scope="col">Total</th>
          </tr>
        </thead>
        <tbody>
          {p.attribution.map((row) => (
            <tr key={row.symbol}>
              <td>
                <button onClick={() => onSymbol(row.symbol)}>
                  {row.symbol}
                </button>
              </td>
              <td>{row.quantity}</td>
              <td>{row.fills}</td>
              <td className={row.realized >= 0 ? "sim-up" : "sim-down"}>
                {dollars(row.realized)}
              </td>
              <td className={row.unrealized >= 0 ? "sim-up" : "sim-down"}>
                {dollars(row.unrealized)}
              </td>
              <td className={row.total >= 0 ? "sim-up" : "sim-down"}>
                {dollars(row.total)}
              </td>
            </tr>
          ))}
          {!p.attribution.length ? (
            <tr>
              <td colSpan={6}>No fills yet in this run.</td>
            </tr>
          ) : null}
        </tbody>
      </table>
      <p className="sim-small">{desk.disclosure}</p>
    </section>
  );
}
