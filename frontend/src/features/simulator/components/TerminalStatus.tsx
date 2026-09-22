import { price } from "@/features/simulator/model/format";
import "@/features/simulator/simulator.css";
import {
  Activity,
  ArrowUp,
  Download,
  Layers,
  List,
  Newspaper,
  PanelBottomOpen,
} from "lucide-react";
import type { TerminalView } from "../model/view";

export default function TerminalStatus({
  terminal,
}: {
  terminal: Pick<
    TerminalView,
    | "connectionError"
    | "run"
    | "setHelpOpen"
    | "saveStatus"
    | "busy"
    | "pending"
    | "setPlaying"
    | "load"
    | "boot"
    | "setExportOpen"
    | "prefs"
    | "setPrefs"
    | "quote"
    | "ticket"
    | "setSideTab"
    | "setMobileTab"
    | "mobileTab"
  >;
}) {
  const {
    connectionError,
    run,
    setHelpOpen,
    saveStatus,
    busy,
    pending,
    setPlaying,
    load,
    boot,
    setExportOpen,
    prefs,
    setPrefs,
    quote,
    ticket,
    setSideTab,
    setMobileTab,
    mobileTab,
  } = terminal;
  return (
    <>
      <footer className="sim-statusbar">
        <span className="sim-status-dot" />
        {connectionError
          ? "Disconnected"
          : run.guest
            ? "Guest · saved for this browser"
            : "Account synced"}
        <span className="sim-status-separator">|</span>
        <span title={run.disclosure}>
          {run.config.mode === "synthetic"
            ? `Simulated market · ${run.quotes.length} fictional companies · seed ${run.config.seed}`
            : "Imported historical"}
        </span>
        <button className="sim-text-button" onClick={() => setHelpOpen(true)}>
          Execution model
        </button>
        <span className="sim-footer-spacer" />
        <span>{saveStatus}</span>
        <select
          aria-label="Simulation run history"
          disabled={busy || !!pending}
          value={run.id}
          onChange={(e) => {
            setPlaying(false);
            void load(e.target.value);
          }}
        >
          {boot?.runs.map((r, i) => (
            <option key={r.id} value={r.id}>
              {i === 0 ? "Current" : "Archived"} ·{" "}
              {new Date(r.created_at).toLocaleString()}
            </option>
          ))}
        </select>
        <button
          className="sim-icon"
          aria-label="Export simulation"
          onClick={() => setExportOpen(true)}
        >
          <Download size={14} />
        </button>
        {!prefs.bottomOpen ? (
          <button
            className="sim-icon"
            aria-label="Open trading panel"
            onClick={() => setPrefs({ bottomOpen: true })}
          >
            <PanelBottomOpen size={16} />
          </button>
        ) : null}
      </footer>
      <div className="sim-mobile-trade-entry">
        <span>
          {prefs.symbol} · {quote ? price(quote.close) : "Unavailable"}
        </span>
        {(["buy", "sell"] as const).map((side) => (
          <button
            key={side}
            className={side}
            onClick={() => {
              setPrefs({ rightOpen: true, ticket: { ...ticket, side } });
              setSideTab("Trade");
              setMobileTab("Trade");
            }}
          >
            {side === "buy" ? "Buy" : "Sell"}
          </button>
        ))}
      </div>
      <nav className="sim-mobile-nav" aria-label="Simulator navigation">
        {[
          { name: "Chart", icon: Activity },
          { name: "Watchlist", icon: List },
          { name: "News", icon: Newspaper },
          { name: "Trade", icon: ArrowUp },
          { name: "Portfolio", icon: Layers },
        ].map(({ name, icon: Icon }) => (
          <button
            key={name}
            className={mobileTab === name ? "active" : ""}
            onClick={() => {
              setMobileTab(name);
              if (name === "Trade" || name === "Watchlist" || name === "News") {
                setPrefs({ rightOpen: true });
                setSideTab(name);
              }
              if (name === "Portfolio") setPrefs({ bottomOpen: true });
            }}
          >
            <Icon size={17} />
            {name}
          </button>
        ))}
      </nav>
    </>
  );
}
