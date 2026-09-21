import {
  millions,
  price,
  signed,
  stamp,
} from "@/features/simulator/model/format";
import type { RunCalendar } from "@/features/simulator/model/types";
import "@/features/simulator/simulator.css";

export default function CalendarPanel({
  calendar,
  error,
  onSymbol,
}: {
  calendar: RunCalendar | null;
  error: string;
  onSymbol: (symbol: string) => void;
}) {
  if (!calendar)
    return (
      <p className="sim-small" role={error ? "alert" : "status"}>
        {error || "Loading the reporting calendar…"}
      </p>
    );
  return (
    <section className="sim-company" aria-label="Reporting calendar">
      <p className="sim-small">
        Scheduled releases for this simulated market. An entry that has not been
        reached carries its appointment and, for company results, the published
        consensus — never the outcome.
      </p>
      <div className="sim-calendar-grid">
        <div>
          <h4>Economic releases</h4>
          <table className="sim-desk-table">
            <thead>
              <tr>
                <th scope="col">When</th>
                <th scope="col">Release</th>
                <th scope="col">Outcome</th>
              </tr>
            </thead>
            <tbody>
              {calendar.economic.map((item) => (
                <tr key={`${item.index}-${item.topic}`}>
                  <td>{stamp(item.time)}</td>
                  <td>{item.name}</td>
                  <td
                    className={
                      item.sentiment === "positive"
                        ? "sim-up"
                        : item.sentiment === "negative"
                          ? "sim-down"
                          : ""
                    }
                  >
                    {item.released ? item.headline : "Scheduled"}
                  </td>
                </tr>
              ))}
              {!calendar.economic.length ? (
                <tr>
                  <td colSpan={3}>No releases within this horizon.</td>
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>
        <div>
          <h4>Company results</h4>
          <table className="sim-desk-table">
            <thead>
              <tr>
                <th scope="col">When</th>
                <th scope="col">Symbol</th>
                <th scope="col">Period</th>
                <th scope="col">Consensus EPS</th>
                <th scope="col">Reported</th>
              </tr>
            </thead>
            <tbody>
              {calendar.earnings.map((item) => (
                <tr key={item.symbol}>
                  <td>{stamp(item.time)}</td>
                  <td>
                    <button onClick={() => onSymbol(item.symbol)}>
                      {item.symbol}
                    </button>
                  </td>
                  <td>{item.label}</td>
                  <td>${price(item.consensus_eps)}</td>
                  <td
                    className={
                      !item.released
                        ? ""
                        : (item.eps_surprise ?? 0) >= 0
                          ? "sim-up"
                          : "sim-down"
                    }
                  >
                    {item.released
                      ? `$${price(item.eps ?? 0)} (${signed(item.eps_surprise)})`
                      : `in ${item.bars_away.toLocaleString("en-US")} bars`}
                  </td>
                </tr>
              ))}
              {!calendar.earnings.length ? (
                <tr>
                  <td colSpan={5}>No results due within this horizon.</td>
                </tr>
              ) : null}
            </tbody>
          </table>
          <p className="sim-small">
            Consensus is a published expectation on invented revenue of{" "}
            {millions(calendar.earnings[0]?.consensus_revenue ?? 0)} and
            similar.
          </p>
        </div>
      </div>
      <p className="sim-small">{calendar.disclosure}</p>
    </section>
  );
}
