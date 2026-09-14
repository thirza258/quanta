import { dollars } from "@/features/simulator/model/format";
import type { Interval, Preferences } from "@/features/simulator/model/types";
import "@/features/simulator/simulator.css";
import {
  Activity,
  ArrowLeft,
  ChevronDown,
  ChevronRight,
  Expand,
  Layers,
  Maximize2,
  PanelRightClose,
  PanelRightOpen,
  Search,
  SlidersHorizontal,
} from "lucide-react";
import { Link } from "react-router-dom";
import type { TerminalView } from "../model/view";

export default function TerminalToolbar({
  terminal,
}: {
  terminal: Pick<
    TerminalView,
    | "run"
    | "setAddSymbol"
    | "setQuery"
    | "setSearchOpen"
    | "prefs"
    | "setPrefs"
    | "setIndicatorOpen"
    | "setSideTab"
    | "setMobileTab"
    | "setChartAction"
    | "root"
  >;
}) {
  const {
    run,
    setAddSymbol,
    setQuery,
    setSearchOpen,
    prefs,
    setPrefs,
    setIndicatorOpen,
    setSideTab,
    setMobileTab,
    setChartAction,
    root,
  } = terminal;
  return (
    <>
      <header className="sim-account-bar">
        <div className="sim-brand">
          <Activity size={20} />
          <strong>
            quanta<span> / trade</span>
          </strong>
          <span className="sim-paper-badge">PAPER TRADING</span>
        </div>
        <div className="sim-account-metrics">
          <span>
            Equity <strong>{dollars(run.equity)}</strong>
          </span>
          <span>
            Cash <strong>{dollars(run.cash)}</strong>
          </span>
          <span>
            Realized P&L{" "}
            <strong
              className={Number(run.realized) >= 0 ? "sim-up" : "sim-down"}
            >
              {dollars(run.realized)}
            </strong>
          </span>
        </div>
        <Link to="/" className="sim-back">
          <ArrowLeft size={14} /> Learning workspace
        </Link>
      </header>
      <div className="sim-workspace-toolbar">
        <button
          className="sim-symbol-trigger"
          onClick={() => {
            setAddSymbol(false);
            setQuery("");
            setSearchOpen(true);
          }}
        >
          <Search size={15} />
          <strong>{prefs.symbol}</strong>
          <ChevronDown size={12} />
        </button>
        <div
          className="sim-timeframes"
          role="group"
          aria-label="Chart timeframe"
        >
          {(["1m", "5m", "15m", "1h", "1D"] as Interval[]).map((value) => (
            <button
              key={value}
              disabled={run.config.base_interval === "1D" && value !== "1D"}
              title={
                run.config.base_interval === "1D" && value !== "1D"
                  ? "This dataset contains daily bars only"
                  : value
              }
              className={prefs.interval === value ? "active" : ""}
              onClick={() => setPrefs({ interval: value })}
            >
              {value}
            </button>
          ))}
        </div>
        <select
          aria-label="Chart type"
          className="sim-chart-type"
          value={prefs.chartType}
          onChange={(e) =>
            setPrefs({ chartType: e.target.value as Preferences["chartType"] })
          }
        >
          <option value="candles">Candles</option>
          <option value="bars">OHLC bars</option>
          <option value="line">Line</option>
        </select>
        <button
          className="sim-toolbar-button"
          onClick={() => setIndicatorOpen(true)}
        >
          <SlidersHorizontal size={16} />
          <span>Indicators</span>
        </button>
        <button
          className="sim-toolbar-button"
          onClick={() => {
            setPrefs({ rightOpen: true });
            setSideTab("Drawings");
            setMobileTab("Trade");
          }}
        >
          <Layers size={16} />
          <span>Objects</span>
        </button>
        <div className="sim-toolbar-spacer" />
        <button
          className="sim-icon"
          aria-label="Fit chart"
          title="Fit chart"
          onClick={() => setChartAction({ kind: "fit", seq: Date.now() })}
        >
          <Expand size={17} />
        </button>
        <button
          className="sim-icon"
          aria-label="Return to latest bar"
          title="Return to latest bar"
          onClick={() => setChartAction({ kind: "latest", seq: Date.now() })}
        >
          <ChevronRight size={18} />
        </button>
        <button
          className="sim-icon"
          aria-label="Fullscreen chart workspace"
          title="Fullscreen workspace"
          onClick={() => {
            if (document.fullscreenElement) void document.exitFullscreen();
            else void root.current?.requestFullscreen();
          }}
        >
          <Maximize2 size={16} />
        </button>
        <button
          className="sim-icon"
          aria-label={prefs.rightOpen ? "Collapse watchlist" : "Open watchlist"}
          onClick={() => setPrefs({ rightOpen: !prefs.rightOpen })}
        >
          {prefs.rightOpen ? (
            <PanelRightClose size={16} />
          ) : (
            <PanelRightOpen size={16} />
          )}
        </button>
      </div>
    </>
  );
}
