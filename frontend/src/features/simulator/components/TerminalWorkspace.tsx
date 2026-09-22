import DeskPanel from "@/features/simulator/components/DeskPanel";
import DrawingsPanel from "@/features/simulator/components/DrawingsPanel";
import NewsPanel from "@/features/simulator/components/NewsPanel";
import OrderTicket from "@/features/simulator/components/OrderTicket";
import PortfolioPanel from "@/features/simulator/components/PortfolioPanel";
import SimChart from "@/features/simulator/components/SimChart";
import { clock, price, stamp } from "@/features/simulator/model/format";
import "@/features/simulator/simulator.css";
import {
  ArrowUp,
  CircleHelp,
  Crosshair,
  Minus,
  Pause,
  Play,
  Plus,
  Redo2,
  RefreshCw,
  Ruler,
  SkipForward,
  Square,
  TrendingUp,
  Type,
  Undo2,
  X,
} from "lucide-react";
import type { TerminalView } from "../model/view";

const tools = [
  { id: "cursor", label: "Crosshair / select", icon: Crosshair },
  { id: "trend", label: "Trend line", icon: TrendingUp },
  { id: "horizontal", label: "Horizontal line", icon: Minus },
  { id: "rectangle", label: "Rectangle", icon: Square },
  { id: "text", label: "Text annotation", icon: Type },
  { id: "measure", label: "Price measurement", icon: Ruler },
] as const;
export default function TerminalWorkspace({
  terminal,
}: {
  terminal: Pick<
    TerminalView,
    | "prefs"
    | "tool"
    | "archived"
    | "setTool"
    | "history"
    | "undo"
    | "historyVersion"
    | "setWalkthrough"
    | "setHelpOpen"
    | "bars"
    | "drawings"
    | "changeDrawings"
    | "selectedDrawing"
    | "setSelectedDrawing"
    | "setSideTab"
    | "setPrefs"
    | "run"
    | "dark"
    | "tradeAt"
    | "blocked"
    | "setPlaying"
    | "setAmendment"
    | "chartAction"
    | "playing"
    | "complete"
    | "perform"
    | "speed"
    | "setSpeed"
    | "marketClosed"
    | "setResetOpen"
    | "resize"
    | "sideTab"
    | "setMobileTab"
    | "setAddSymbol"
    | "setQuery"
    | "setSearchOpen"
    | "chooseSymbol"
    | "quote"
    | "ticket"
    | "ticketProps"
    | "tab"
    | "setTab"
    | "closePosition"
    | "setJournal"
    | "news"
    | "overlays"
    | "desk"
    | "deskError"
    | "calendar"
    | "analytics"
    | "fundamentals"
    | "fundamentalsError"
    | "jump"
  >;
}) {
  const {
    prefs,
    tool,
    archived,
    setTool,
    history,
    undo,
    historyVersion,
    setWalkthrough,
    setHelpOpen,
    bars,
    drawings,
    changeDrawings,
    selectedDrawing,
    setSelectedDrawing,
    setSideTab,
    setPrefs,
    run,
    dark,
    tradeAt,
    blocked,
    setPlaying,
    setAmendment,
    chartAction,
    playing,
    complete,
    perform,
    speed,
    setSpeed,
    marketClosed,
    setResetOpen,
    resize,
    sideTab,
    setMobileTab,
    setAddSymbol,
    setQuery,
    setSearchOpen,
    chooseSymbol,
    quote,
    ticket,
    ticketProps,
    tab,
    setTab,
    closePosition,
    setJournal,
    news,
    overlays,
    desk,
    deskError,
    calendar,
    analytics,
    fundamentals,
    fundamentalsError,
    jump,
  } = terminal;
  // A minute market steps by clock time; a daily replay steps by sessions.
  const jumps: [string, number, string][] =
    run.config.base_interval === "1D"
      ? [
          ["1D", 1, "by one session"],
          ["1W", 5, "by one week"],
          ["1M", 21, "by one month"],
          ["1Q", 63, "by one quarter"],
        ]
      : [
          ["15m", 15, "by fifteen minutes"],
          ["1h", 60, "by one hour"],
          ["1D", 390, "by one session"],
          ["1W", 1950, "by one week"],
        ];
  const tape = (news?.items ?? []).slice(0, 12);
  return (
    <>
      {tape.length ? (
        <div className="sim-tape" aria-label="Latest simulated headlines">
          <span className="sim-tape-badge">SIM NEWS</span>
          <div className="sim-tape-track">
            {tape.map((item) => (
              <button
                key={item.id}
                className={`sim-tape-item ${item.sentiment}`}
                onClick={() => {
                  if (item.symbol) chooseSymbol(item.symbol);
                  setSideTab("News");
                  setPrefs({ rightOpen: true });
                }}
              >
                <span className="sim-tape-time">{clock(item.time)}</span>
                {item.symbol ? <strong>{item.symbol}</strong> : null}
                {item.headline}
              </button>
            ))}
          </div>
        </div>
      ) : null}
      <div
        className={`sim-main-grid ${prefs.rightOpen ? "" : "right-collapsed"} ${prefs.bottomOpen ? "" : "bottom-collapsed"}`}
      >
        <nav className="sim-drawing-toolbar" aria-label="Chart tools">
          {tools.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              className={tool === id ? "active" : ""}
              aria-label={label}
              title={label}
              disabled={archived && id !== "cursor"}
              onClick={() => setTool(id)}
            >
              <Icon size={19} />
            </button>
          ))}
          <span className="sim-tool-divider" />
          <button
            aria-label="Undo drawing"
            title="Undo drawing"
            disabled={!history.current.past.length || archived}
            onClick={() => undo()}
            data-version={historyVersion}
          >
            <Undo2 size={18} />
          </button>
          <button
            aria-label="Redo drawing"
            title="Redo drawing"
            disabled={!history.current.future.length || archived}
            onClick={() => undo(true)}
          >
            <Redo2 size={18} />
          </button>
          <div className="sim-tools-bottom">
            <button
              aria-label="Simulator walkthrough"
              title="Help"
              onClick={() => {
                setWalkthrough(0);
                setHelpOpen(true);
              }}
            >
              <CircleHelp size={18} />
            </button>
          </div>
        </nav>
        <div className="sim-chart-region">
          <SimChart
            bars={bars}
            symbol={prefs.symbol}
            interval={prefs.interval}
            chartType={prefs.chartType}
            indicators={prefs.indicators}
            overlays={overlays}
            drawings={drawings}
            onDrawings={changeDrawings}
            tool={tool}
            setTool={setTool}
            selected={selectedDrawing}
            onSelect={(id) => {
              setSelectedDrawing(id);
              if (id) {
                setSideTab("Drawings");
                setPrefs({ rightOpen: true });
              }
            }}
            run={run}
            dark={dark}
            onTrade={tradeAt}
            onAmend={(id, field, value) => {
              const order = run.orders.find((o) => o.id === id);
              if (order && !blocked) {
                setPlaying(false);
                setAmendment({
                  order,
                  limit:
                    field === "limit_price"
                      ? value.toFixed(2)
                      : (order.limit_price ?? ""),
                  stop:
                    field === "stop_price"
                      ? value.toFixed(2)
                      : (order.stop_price ?? ""),
                });
              }
            }}
            action={chartAction}
          />
          <div className="sim-replay-bar">
            <button
              className="sim-play-button"
              aria-label={playing ? "Pause replay" : "Play replay"}
              disabled={blocked || complete}
              onClick={() => setPlaying(!playing)}
            >
              {playing ? <Pause size={15} /> : <Play size={15} />}
            </button>
            <button
              className="sim-icon"
              aria-label="Next replay bar"
              title="Next replay bar"
              disabled={blocked || complete}
              onClick={() => {
                setPlaying(false);
                void perform(
                  "advance",
                  { steps: 1 },
                  "POST",
                  "Replay advanced by one bar.",
                );
              }}
            >
              <SkipForward size={17} />
            </button>
            <span className="sim-jumps" role="group" aria-label="Jump replay">
              {jumps.map(([label, steps, description]) => (
                <button
                  key={label}
                  disabled={blocked || complete}
                  title={`Jump forward ${description}`}
                  aria-label={`Jump forward ${description}`}
                  onClick={() => void jump(steps, description)}
                >
                  {label}
                </button>
              ))}
            </span>
            <select
              aria-label="Replay speed"
              value={speed}
              onChange={(e) => setSpeed(Number(e.target.value))}
            >
              <option value={1}>1×</option>
              <option value={5}>5×</option>
              <option value={30}>30×</option>
              <option value={390}>390×</option>
            </select>
            <span className="sim-clock">
              <span className={playing ? "sim-pulse" : ""} />
              {complete
                ? "Replay complete"
                : playing
                  ? "Playing"
                  : "Paused"} · {stamp(run.clock)}
              {marketClosed && !complete
                ? " · Market closed · next session on step"
                : ""}
            </span>
            <progress
              max={run.total_bars - 1}
              value={run.cursor}
              aria-label="Replay progress"
            />
            <span className="sim-replay-count">
              {run.cursor + 1} / {run.total_bars}
            </span>
            <button
              className="sim-icon"
              aria-label="New simulation run"
              title="New simulation run"
              onClick={() => {
                setPlaying(false);
                setResetOpen(true);
              }}
            >
              <RefreshCw size={15} />
            </button>
          </div>
        </div>
        {prefs.rightOpen ? (
          <>
            <div
              className="sim-right-resize"
              role="separator"
              aria-label="Watchlist width"
              aria-valuenow={prefs.rightWidth}
              aria-valuemin={250}
              aria-valuemax={420}
              aria-orientation="vertical"
              tabIndex={0}
              onPointerDown={(e) => resize(e, "right")}
              onKeyDown={(e) => {
                if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
                  e.preventDefault();
                  setPrefs({
                    rightWidth: Math.max(
                      250,
                      Math.min(
                        420,
                        prefs.rightWidth + (e.key === "ArrowLeft" ? 20 : -20),
                      ),
                    ),
                  });
                }
              }}
            />
            <aside className="sim-right-panel">
              <div className="sim-sidebar-tabs">
                {["Watchlist", "News", "Desk", "Trade", "Drawings"].map((t) => (
                  <button
                    key={t}
                    className={sideTab === t ? "active" : ""}
                    onClick={() => {
                      setSideTab(t);
                      if (t === "Watchlist") setMobileTab("Watchlist");
                    }}
                  >
                    {t}
                  </button>
                ))}
              </div>
              <div
                className={`sim-watchlist ${sideTab === "Watchlist" ? "show" : ""}`}
              >
                <div className="sim-section-title">
                  <strong>Watchlist</strong>
                  <button
                    className="sim-icon"
                    aria-label="Add stock to watchlist"
                    onClick={() => {
                      setAddSymbol(true);
                      setQuery("");
                      setSearchOpen(true);
                    }}
                  >
                    <Plus size={16} />
                  </button>
                </div>
                <div className="sim-watchlist-head">
                  <span>Symbol</span>
                  <span>Last</span>
                  <span>Change %</span>
                </div>
                {prefs.watchlist.map((symbol, index) => {
                  const q = run.quotes.find((q) => q.symbol === symbol);
                  return (
                    <div
                      key={symbol}
                      className={`sim-watchlist-row ${symbol === prefs.symbol ? "selected" : ""}`}
                    >
                      <button onClick={() => chooseSymbol(symbol)}>
                        <strong>
                          <span className={`sim-symbol-logo logo-${index % 4}`}>
                            {symbol[0]}
                          </span>
                          {symbol}
                        </strong>
                        <span>
                          {q ? price(q.close) : "—"}
                          {q ? (
                            <small className="sim-absolute-change">
                              {q.change >= 0 ? "+" : ""}
                              {price(q.change)}
                            </small>
                          ) : null}
                        </span>
                        <span
                          className={
                            q && q.change_pct >= 0 ? "sim-up" : "sim-down"
                          }
                        >
                          {q
                            ? `${q.change_pct >= 0 ? "+" : ""}${q.change_pct.toFixed(2)}%`
                            : "—"}
                        </span>
                      </button>
                      <div className="sim-watchlist-edit">
                        <button
                          aria-label={`Move ${symbol} up`}
                          disabled={index === 0}
                          onClick={() => {
                            const list = [...prefs.watchlist];
                            [list[index - 1], list[index]] = [
                              list[index],
                              list[index - 1],
                            ];
                            setPrefs({ watchlist: list });
                          }}
                        >
                          <ArrowUp size={12} />
                        </button>
                        <button
                          aria-label={`Remove ${symbol} from watchlist`}
                          onClick={() =>
                            setPrefs({
                              watchlist: prefs.watchlist.filter(
                                (s) => s !== symbol,
                              ),
                            })
                          }
                        >
                          <X size={12} />
                        </button>
                      </div>
                    </div>
                  );
                })}
                {!prefs.watchlist.length ? (
                  <p className="sim-small">
                    Your watchlist is empty. Add a stock to follow its price.
                  </p>
                ) : null}
                <div className="sim-symbol-details">
                  <div className="sim-section-title">
                    <strong>{quote?.name ?? prefs.symbol}</strong>
                    <span>{prefs.symbol}</span>
                  </div>
                  <div className="sim-large-price">
                    {quote ? price(quote.close) : "Unavailable"}{" "}
                    <small>USD</small>
                  </div>
                  {quote ? (
                    <p className={quote.change >= 0 ? "sim-up" : "sim-down"}>
                      {quote.change >= 0 ? "+" : ""}
                      {price(quote.change)} ({quote.change_pct.toFixed(2)}%){" "}
                      <span>vs. prior session</span>
                    </p>
                  ) : null}
                  <p className="sim-small">
                    {run.config.mode !== "synthetic"
                      ? "Historical replay · imported prices"
                      : run.universe
                        ? "Simulated market · fictional company"
                        : "Seeded synthetic · fictional price path"}
                    <br />
                    {stamp(run.clock)}
                  </p>
                  <div className="sim-quick-trade">
                    <button
                      className="buy"
                      onClick={() => {
                        setPrefs({ ticket: { ...ticket, side: "buy" } });
                        setSideTab("Trade");
                        setMobileTab("Trade");
                      }}
                    >
                      Buy
                    </button>
                    <button
                      className="sell"
                      onClick={() => {
                        setPrefs({ ticket: { ...ticket, side: "sell" } });
                        setSideTab("Trade");
                        setMobileTab("Trade");
                      }}
                    >
                      Sell
                    </button>
                  </div>
                </div>
              </div>
              <NewsPanel
                feed={news}
                symbol={prefs.symbol}
                scope={prefs.newsScope ?? "all"}
                onScope={(newsScope) => setPrefs({ newsScope })}
                onSymbol={chooseSymbol}
                show={sideTab === "News"}
              />
              <DeskPanel
                desk={desk}
                error={deskError}
                analytics={analytics}
                onSymbol={chooseSymbol}
                show={sideTab === "Desk"}
              />
              {sideTab === "Drawings" ? (
                <DrawingsPanel
                  drawings={drawings}
                  onChange={changeDrawings}
                  selected={selectedDrawing}
                  onSelect={setSelectedDrawing}
                  bars={bars}
                  disabled={archived}
                />
              ) : null}
              <div
                className={`sim-ticket-wrap ${sideTab === "Trade" ? "show" : ""}`}
              >
                <OrderTicket {...ticketProps} />
              </div>
            </aside>
          </>
        ) : null}
        {prefs.bottomOpen ? (
          <>
            <div
              className="sim-bottom-resize"
              role="separator"
              aria-label="Trading panel height"
              aria-valuenow={prefs.bottomHeight}
              aria-valuemin={130}
              aria-valuemax={420}
              aria-orientation="horizontal"
              tabIndex={0}
              onPointerDown={(e) => resize(e, "bottom")}
              onKeyDown={(e) => {
                if (e.key === "ArrowUp" || e.key === "ArrowDown") {
                  e.preventDefault();
                  setPrefs({
                    bottomHeight: Math.max(
                      130,
                      Math.min(
                        420,
                        prefs.bottomHeight + (e.key === "ArrowUp" ? 20 : -20),
                      ),
                    ),
                  });
                }
              }}
            />
            <div className="sim-bottom-panel">
              <PortfolioPanel
                run={run}
                tab={tab}
                setTab={setTab}
                fundamentals={fundamentals}
                fundamentalsError={fundamentalsError}
                desk={desk}
                deskError={deskError}
                calendar={calendar}
                statement={prefs.statement ?? "ratios"}
                setStatement={(statement) => setPrefs({ statement })}
                onSymbol={chooseSymbol}
                onClose={closePosition}
                onCancel={(id) => {
                  setPlaying(false);
                  void perform(
                    `orders/${id}/cancel`,
                    {},
                    "POST",
                    "Order remainder canceled.",
                  );
                }}
                onAmend={(order) => {
                  setPlaying(false);
                  setAmendment({
                    order,
                    limit: order.limit_price ?? "",
                    stop: order.stop_price ?? "",
                  });
                }}
                onJournal={setJournal}
                onCollapse={() => setPrefs({ bottomOpen: false })}
                disabled={blocked}
              />
            </div>
          </>
        ) : null}
      </div>
    </>
  );
}
