import {
  clock,
  millions,
  percent,
  price,
} from "@/features/simulator/model/format";
import { MONITOR_TOOLS } from "@/features/simulator/model/preferences";
import type {
  MonitorTool,
  MonitorView,
  NewsFeed,
} from "@/features/simulator/model/types";
import "@/features/simulator/simulator.css";

/** A tone between -1 and 1 mapped to a background a whole grid can be read from. */
function heat(change: number) {
  const scale = Math.max(-1, Math.min(1, change / 2));
  const alpha = 0.12 + Math.abs(scale) * 0.55;
  return scale >= 0
    ? `rgba(32, 167, 141, ${alpha.toFixed(3)})`
    : `rgba(231, 102, 118, ${alpha.toFixed(3)})`;
}

function Tape({ view }: { view: NonNullable<MonitorView["tools"]["tape"]> }) {
  return (
    <div className="sim-monitor-body">
      <p className="sim-monitor-summary">
        {view.prints.length} prints · {view.volume.toLocaleString("en-US")}{" "}
        shares ·{" "}
        {view.buy_share === null
          ? "—"
          : `${(view.buy_share * 100).toFixed(0)}% lifted the offer`}
      </p>
      <table className="sim-monitor-table sim-tape-table">
        <thead>
          <tr>
            <th scope="col">Time</th>
            <th scope="col">Price</th>
            <th scope="col">Size</th>
          </tr>
        </thead>
        <tbody>
          {view.prints.map((print, index) => (
            <tr key={`${print.time}:${index}`}>
              <td>{clock(print.time)}</td>
              <td
                className={
                  print.side === "buy"
                    ? "sim-up"
                    : print.side === "sell"
                      ? "sim-down"
                      : ""
                }
              >
                ${price(print.price)}
              </td>
              <td>{print.size.toLocaleString("en-US")}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="sim-monitor-note">{view.notice}</p>
    </div>
  );
}

function Book({ view }: { view: NonNullable<MonitorView["tools"]["book"]> }) {
  const deepest = Math.max(
    ...view.bids.map((level) => level.size),
    ...view.asks.map((level) => level.size),
    1,
  );
  return (
    <div className="sim-monitor-body">
      <p className="sim-monitor-summary">
        ${price(view.bid)} / ${price(view.ask)} · spread ${price(view.spread)} ·{" "}
        {view.imbalance === null
          ? "—"
          : `${(view.imbalance * 100).toFixed(0)}% of size on the bid`}
      </p>
      <div className="sim-book">
        {["bids", "asks"].map((sideKey) => {
          const side = sideKey as "bids" | "asks";
          return (
            <table className="sim-monitor-table" key={side}>
              <thead>
                <tr>
                  <th scope="col">{side === "bids" ? "Bid" : "Ask"}</th>
                  <th scope="col">Size</th>
                </tr>
              </thead>
              <tbody>
                {view[side].map((level) => (
                  <tr key={level.price}>
                    <td className={side === "bids" ? "sim-up" : "sim-down"}>
                      ${price(level.price)}
                    </td>
                    <td>
                      <span
                        className="sim-book-bar"
                        style={{ width: `${(level.size / deepest) * 100}%` }}
                      />
                      {level.size.toLocaleString("en-US")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          );
        })}
      </div>
      <p className="sim-monitor-note">{view.notice}</p>
    </div>
  );
}

function Heatmap({
  view,
  onSymbol,
}: {
  view: NonNullable<MonitorView["tools"]["heatmap"]>;
  onSymbol: (symbol: string) => void;
}) {
  return (
    <div className="sim-monitor-body">
      <p className="sim-monitor-summary">
        {view.companies} companies · best {view.best.toFixed(2)}% · worst{" "}
        {view.worst.toFixed(2)}% · weighted by {view.weighting}
      </p>
      <div className="sim-heatmap">
        {view.sectors.map((sector) => (
          <div className="sim-heat-sector" key={sector.sector}>
            <h5>
              {sector.sector}
              <span className={sector.change_pct >= 0 ? "sim-up" : "sim-down"}>
                {sector.change_pct >= 0 ? "+" : ""}
                {sector.change_pct.toFixed(2)}%
              </span>
            </h5>
            <div className="sim-heat-grid">
              {sector.companies.map((company) => (
                <button
                  key={company.symbol}
                  className="sim-heat-cell"
                  style={{ background: heat(company.change_pct) }}
                  onClick={() => onSymbol(company.symbol)}
                  title={`${company.name} · $${price(company.close)} · ${millions(
                    company.notional,
                  )} traded`}
                >
                  <strong>{company.symbol}</strong>
                  <span>
                    {company.change_pct >= 0 ? "+" : ""}
                    {company.change_pct.toFixed(2)}%
                  </span>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function Screener({
  view,
  screen,
  onScreen,
  onSymbol,
}: {
  view: NonNullable<MonitorView["tools"]["screener"]>;
  screen: string;
  onScreen: (screen: string) => void;
  onSymbol: (symbol: string) => void;
}) {
  return (
    <div className="sim-monitor-body">
      <div className="sim-monitor-controls">
        <label>
          Screen
          <select value={screen} onChange={(e) => onScreen(e.target.value)}>
            {view.screens.map((option) => (
              <option key={option.id} value={option.id}>
                {option.label}
              </option>
            ))}
          </select>
        </label>
        <span className="sim-monitor-summary">
          {view.matches} match{view.matches === 1 ? "" : "es"} ·{" "}
          {view.description}
        </span>
      </div>
      <table className="sim-monitor-table">
        <thead>
          <tr>
            <th scope="col">Symbol</th>
            <th scope="col">Last</th>
            <th scope="col">Chg</th>
            <th scope="col">RSI</th>
            <th scope="col">Rel vol</th>
            <th scope="col">P/E</th>
            <th scope="col">Vol</th>
          </tr>
        </thead>
        <tbody>
          {view.rows.map((row) => (
            <tr key={row.symbol}>
              <td>
                <button onClick={() => onSymbol(row.symbol)}>
                  {row.symbol}
                </button>
              </td>
              <td>${price(row.close)}</td>
              <td className={row.change_pct >= 0 ? "sim-up" : "sim-down"}>
                {row.change_pct >= 0 ? "+" : ""}
                {row.change_pct.toFixed(2)}%
              </td>
              <td>{row.rsi === null ? "—" : row.rsi.toFixed(0)}</td>
              <td>
                {row.relative_volume === null
                  ? "—"
                  : `${row.relative_volume.toFixed(2)}×`}
              </td>
              <td>{row.multiple === null ? "—" : row.multiple.toFixed(1)}</td>
              <td>{percent(row.volatility, 0)}</td>
            </tr>
          ))}
          {!view.rows.length ? (
            <tr>
              <td colSpan={7}>Nothing matches this screen on this bar.</td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </div>
  );
}

function Sessions({
  view,
}: {
  view: NonNullable<MonitorView["tools"]["sessions"]>;
}) {
  return (
    <div className="sim-monitor-body">
      <p className="sim-monitor-summary">
        {view.symbol} · prior close ${price(view.prior_close)} · volatility{" "}
        {percent(view.volatility, 0)}
      </p>
      <table className="sim-monitor-table">
        <thead>
          <tr>
            <th scope="col">Session</th>
            <th scope="col">Open</th>
            <th scope="col">High</th>
            <th scope="col">Low</th>
            <th scope="col">Close</th>
            <th scope="col">Chg</th>
          </tr>
        </thead>
        <tbody>
          {[...view.sessions].reverse().map((row) => (
            <tr key={row.time}>
              <td>
                {new Date(row.time * 1000).toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                })}
              </td>
              <td>${price(row.open)}</td>
              <td>${price(row.high)}</td>
              <td>${price(row.low)}</td>
              <td>${price(row.close)}</td>
              <td className={row.change_pct >= 0 ? "sim-up" : "sim-down"}>
                {row.change_pct >= 0 ? "+" : ""}
                {row.change_pct.toFixed(2)}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Quotes({
  view,
  onSymbol,
}: {
  view: NonNullable<MonitorView["tools"]["quotes"]>;
  onSymbol: (symbol: string) => void;
}) {
  return (
    <div className="sim-monitor-body">
      <table className="sim-monitor-table">
        <thead>
          <tr>
            <th scope="col">Symbol</th>
            <th scope="col">Last</th>
            <th scope="col">Chg</th>
            <th scope="col">Volume</th>
          </tr>
        </thead>
        <tbody>
          {view.rows.map((row) => (
            <tr key={row.symbol}>
              <td>
                <button onClick={() => onSymbol(row.symbol)}>
                  {row.symbol}
                </button>
              </td>
              <td>${price(row.close)}</td>
              <td className={row.change_pct >= 0 ? "sim-up" : "sim-down"}>
                {row.change_pct >= 0 ? "+" : ""}
                {row.change_pct.toFixed(2)}%
              </td>
              <td>{row.volume.toLocaleString("en-US")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Headlines({ feed }: { feed: NewsFeed | null }) {
  if (!feed?.items.length)
    return (
      <div className="sim-monitor-body">
        <p className="sim-monitor-summary">
          {feed?.notice || "No headlines released yet on this bar."}
        </p>
      </div>
    );
  return (
    <div className="sim-monitor-body">
      <ul className="sim-monitor-headlines">
        {feed.items.map((item, index) => (
          <li key={`${item.index}:${index}`}>
            <span className="sim-monitor-time">{clock(item.time)}</span>
            <span
              className={
                item.points > 0 ? "sim-up" : item.points < 0 ? "sim-down" : ""
              }
            >
              {item.points > 0 ? "+" : ""}
              {item.points}
            </span>
            {item.headline}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function MonitorPane({
  slot,
  tool,
  view,
  error,
  news,
  screen,
  onScreen,
  onTool,
  onSymbol,
}: {
  slot: number;
  tool: MonitorTool;
  view: MonitorView | null;
  error: string;
  news: NewsFeed | null;
  screen: string;
  onScreen: (screen: string) => void;
  onTool: (slot: number, tool: MonitorTool) => void;
  onSymbol: (symbol: string) => void;
}) {
  const tools = view?.tools ?? {};
  const label =
    MONITOR_TOOLS.find((entry) => entry.id === tool)?.label ?? "Tool";
  const ready = tool === "news" || Boolean(tools[tool]);
  return (
    <section
      className="sim-monitor-pane"
      aria-label={`Monitor ${slot + 2}: ${label}`}
    >
      <header className="sim-monitor-head">
        <label>
          <span className="sim-monitor-index">{slot + 2}</span>
          <select
            aria-label={`Tool for monitor ${slot + 2}`}
            value={tool}
            onChange={(e) => onTool(slot, e.target.value as MonitorTool)}
          >
            {MONITOR_TOOLS.map((entry) => (
              <option key={entry.id} value={entry.id}>
                {entry.label}
              </option>
            ))}
          </select>
        </label>
      </header>
      {error && tool !== "news" ? (
        <p className="sim-monitor-summary" role="alert">
          {error}
        </p>
      ) : !ready ? (
        <p className="sim-monitor-summary" role="status">
          Loading {label.toLowerCase()}…
        </p>
      ) : tool === "tape" ? (
        <Tape view={tools.tape!} />
      ) : tool === "book" ? (
        <Book view={tools.book!} />
      ) : tool === "heatmap" ? (
        <Heatmap view={tools.heatmap!} onSymbol={onSymbol} />
      ) : tool === "screener" ? (
        <Screener
          view={tools.screener!}
          screen={screen}
          onScreen={onScreen}
          onSymbol={onSymbol}
        />
      ) : tool === "sessions" ? (
        <Sessions view={tools.sessions!} />
      ) : tool === "quotes" ? (
        <Quotes view={tools.quotes!} onSymbol={onSymbol} />
      ) : (
        <Headlines feed={news} />
      )}
    </section>
  );
}
