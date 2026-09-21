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
  // A compact sparkline of the equity path the API marked bar by bar.
  const values = p.curve.map((point) => point.equity);
  const low = Math.min(...values, p.opening_equity);
  const high = Math.max(...values, p.opening_equity);
  const span = high - low || 1;
  const path = values
    .map(
      (value, index) =>
        `${(index / Math.max(1, values.length - 1)) * 100},${30 - ((value - low) / span) * 28}`,
    )
    .join(" ");
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
          <h4>Equity path</h4>
          <svg
            className="sim-sparkline"
            viewBox="0 0 100 32"
            preserveAspectRatio="none"
            role="img"
            aria-label={`Equity moved from ${dollars(p.opening_equity)} to ${dollars(p.equity)}`}
          >
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
            {p.bars_observed} observed bars.
          </p>
        </div>
      </div>
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
