import {
  csv,
  dollars,
  stamp,
  live,
  working,
} from "@/features/simulator/model/format";
import type {
  DeskView,
  Fundamentals,
  Preferences,
  RunCalendar,
  SimOrder,
  SimRun,
} from "@/features/simulator/model/types";
import CalendarPanel from "@/features/simulator/components/CalendarPanel";
import PerformancePanel from "@/features/simulator/components/PerformancePanel";
import CompanyPanel from "@/features/simulator/components/CompanyPanel";
import { download } from "@/shared/lib/download";
import { Download, PanelBottomClose } from "lucide-react";
import { Link } from "react-router-dom";
export type TradingTab =
  | "Positions"
  | "Open orders"
  | "Order history"
  | "Trade history"
  | "Account history"
  | "Company"
  | "Performance"
  | "Calendar";
export default function PortfolioPanel({
  run,
  tab,
  setTab,
  onSymbol,
  onClose,
  onCancel,
  onAmend,
  onJournal,
  onCollapse,
  disabled,
  fundamentals,
  fundamentalsError,
  statement,
  setStatement,
  desk,
  deskError,
  calendar,
}: {
  run: SimRun;
  tab: TradingTab;
  setTab: (tab: TradingTab) => void;
  onSymbol: (s: string) => void;
  onClose: (s: string, q: number) => void;
  onCancel: (id: string) => void;
  onAmend: (order: SimOrder) => void;
  onJournal: (order: SimOrder) => void;
  onCollapse: () => void;
  disabled: boolean;
  fundamentals: Fundamentals | null;
  fundamentalsError: string;
  statement: NonNullable<Preferences["statement"]>;
  setStatement: (next: NonNullable<Preferences["statement"]>) => void;
  desk: DeskView | null;
  deskError: string;
  calendar: RunCalendar | null;
}) {
  const orders = tab === "Open orders" ? run.orders.filter(live) : run.orders;
  const exportRows =
    tab === "Positions"
      ? run.positions
      : tab === "Trade history"
        ? run.fills
        : tab === "Account history"
          ? run.ledger
          : tab === "Company"
            ? (fundamentals?.quarters ?? [])
            : tab === "Performance"
              ? (desk?.performance.attribution ?? [])
              : tab === "Calendar"
                ? (calendar?.earnings ?? [])
                : orders;
  return (
    <section className="sim-portfolio" aria-label="Trading panel">
      <div className="sim-panel-tabs">
        <div role="tablist" aria-label="Trading views">
          {(
            [
              "Positions",
              "Open orders",
              "Order history",
              "Trade history",
              "Account history",
              "Company",
              "Performance",
              "Calendar",
            ] as TradingTab[]
          ).map((t) => (
            <button
              key={t}
              role="tab"
              aria-selected={tab === t}
              onClick={() => setTab(t)}
            >
              {t}
              {t === "Positions" ? (
                <span>{run.positions.length}</span>
              ) : t === "Open orders" ? (
                <span>{run.orders.filter(live).length}</span>
              ) : null}
            </button>
          ))}
        </div>
        <div className="sim-panel-actions">
          <button
            className="sim-icon"
            title="Export current table as CSV"
            aria-label="Export table as CSV"
            onClick={() =>
              download(
                `quanta-${tab.toLowerCase().replaceAll(" ", "-")}.csv`,
                csv(exportRows as unknown as Record<string, unknown>[]),
                "text/csv",
              )
            }
          >
            <Download size={15} />
          </button>
          <button
            className="sim-icon"
            aria-label="Collapse trading panel"
            onClick={onCollapse}
          >
            <PanelBottomClose size={16} />
          </button>
        </div>
      </div>
      <div className="sim-table-scroll" role="tabpanel" aria-label={tab}>
        {tab === "Calendar" ? (
          <CalendarPanel
            calendar={calendar}
            error={deskError}
            onSymbol={onSymbol}
          />
        ) : tab === "Performance" ? (
          <PerformancePanel desk={desk} error={deskError} onSymbol={onSymbol} />
        ) : tab === "Company" ? (
          <CompanyPanel
            data={fundamentals}
            error={fundamentalsError}
            statement={statement}
            setStatement={setStatement}
          />
        ) : tab === "Positions" ? (
          <table>
            <thead>
              <tr>
                {[
                  "Symbol",
                  "Shares",
                  "Average cost",
                  "Last",
                  "Market value",
                  "Unrealized P&L",
                  "Action",
                ].map((h) => (
                  <th key={h}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {run.positions.map((p) => (
                <tr key={p.symbol}>
                  <td>
                    <button
                      className="sim-text-button"
                      onClick={() => onSymbol(p.symbol)}
                    >
                      {p.symbol}
                    </button>
                  </td>
                  <td>{p.quantity}</td>
                  <td>{dollars(p.average)}</td>
                  <td>{dollars(p.mark)}</td>
                  <td>{dollars(p.market_value)}</td>
                  <td
                    className={
                      Number(p.unrealized) >= 0 ? "sim-up" : "sim-down"
                    }
                  >
                    {dollars(p.unrealized)}
                  </td>
                  <td>
                    <button
                      className="sim-text-button"
                      disabled={disabled || !p.available}
                      onClick={() => onClose(p.symbol, p.available)}
                    >
                      Close
                    </button>{" "}
                    <button
                      className="sim-text-button"
                      disabled={disabled || !p.available}
                      onClick={() =>
                        onClose(
                          p.symbol,
                          Math.max(1, Math.floor(p.available / 2)),
                        )
                      }
                    >
                      Reduce
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : null}
        {tab === "Open orders" || tab === "Order history" ? (
          <table>
            <thead>
              <tr>
                {[
                  "Time",
                  "Symbol",
                  "Side / type",
                  "Shares / filled",
                  "Price",
                  "Status",
                  "Actions",
                ].map((h) => (
                  <th key={h}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[...orders].reverse().map((o) => (
                <tr key={o.id}>
                  <td>{stamp(o.time)}</td>
                  <td>
                    <button
                      className="sim-text-button"
                      onClick={() => onSymbol(o.symbol)}
                    >
                      {o.symbol}
                    </button>
                  </td>
                  <td className={o.side === "buy" ? "sim-up" : "sim-down"}>
                    {o.side.toUpperCase()} · {o.kind.replaceAll("_", "-")}
                    {o.role ? (
                      <small className="sim-order-reason">
                        {o.role === "target" ? "Take profit" : "Stop loss"} on
                        the entry above
                      </small>
                    ) : null}
                  </td>
                  <td>
                    {o.quantity} / {o.filled}
                    <small className="sim-order-reason">
                      {o.quantity - o.filled} remaining
                    </small>
                  </td>
                  <td>
                    {o.kind === "trailing_stop"
                      ? `${o.stop_price ?? "—"} (${o.trail_percent}% trail)`
                      : (o.limit_price ?? o.stop_price ?? "Market")}
                  </td>
                  <td title={o.reason}>
                    <span className={`sim-order-status ${o.status}`}>
                      {o.status.replaceAll("_", " ")}
                    </span>
                    <small className="sim-order-reason">{o.reason}</small>
                  </td>
                  <td>
                    {working(o) ? (
                      <>
                        <button
                          className="sim-text-button"
                          disabled={disabled}
                          onClick={() => onCancel(o.id)}
                        >
                          Cancel
                        </button>{" "}
                        {o.kind !== "market" && o.kind !== "trailing_stop" ? (
                          <button
                            className="sim-text-button"
                            disabled={disabled}
                            onClick={() => onAmend(o)}
                          >
                            Edit
                          </button>
                        ) : null}
                      </>
                    ) : null}{" "}
                    <button
                      className="sim-text-button"
                      onClick={() => onJournal(o)}
                    >
                      Journal
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : null}
        {tab === "Trade history" ? (
          <table>
            <thead>
              <tr>
                {[
                  "Filled at",
                  "Symbol",
                  "Side",
                  "Shares",
                  "Fill price",
                  "Fee",
                  "Realized P&L",
                  "Journal",
                ].map((h) => (
                  <th key={h}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[...run.fills].reverse().map((f) => (
                <tr key={f.id}>
                  <td>{stamp(f.time)}</td>
                  <td>
                    <button
                      className="sim-text-button"
                      onClick={() => onSymbol(f.symbol)}
                    >
                      {f.symbol}
                    </button>
                  </td>
                  <td className={f.side === "buy" ? "sim-up" : "sim-down"}>
                    {f.side.toUpperCase()}
                  </td>
                  <td>{f.quantity}</td>
                  <td>{dollars(f.price)}</td>
                  <td>{dollars(f.fee)}</td>
                  <td
                    className={Number(f.realized) >= 0 ? "sim-up" : "sim-down"}
                  >
                    {dollars(f.realized)}
                  </td>
                  <td title={f.note}>
                    {f.note.slice(0, 70) || "—"}{" "}
                    {f.lesson ? (
                      <Link
                        className="sim-text-button"
                        to={`/learn/${f.lesson}`}
                      >
                        Lesson {f.lesson}
                      </Link>
                    ) : null}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : null}
        {tab === "Account history" ? (
          <table>
            <thead>
              <tr>
                {["Time", "Event", "Cash change", "Cash balance"].map((h) => (
                  <th key={h}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[...run.ledger].reverse().map((e) => (
                <tr key={e.id}>
                  <td>{stamp(e.time)}</td>
                  <td>{e.description}</td>
                  <td className={Number(e.amount) >= 0 ? "sim-up" : "sim-down"}>
                    {dollars(e.amount)}
                  </td>
                  <td>{dollars(e.cash)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : null}
        {!exportRows.length &&
        !["Company", "Performance", "Calendar"].includes(tab) ? (
          <div className="sim-empty-table">
            <strong>
              {tab === "Positions"
                ? "Your next idea starts on the chart."
                : `No ${tab.toLowerCase()} yet.`}
            </strong>
            <span>
              {tab === "Positions"
                ? "Place a paper order, then advance replay to see its execution."
                : "Confirmed activity will appear here automatically."}
            </span>
          </div>
        ) : null}
      </div>
    </section>
  );
}
