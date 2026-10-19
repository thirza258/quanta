import { orderEstimate } from "@/features/simulator/model/orders";
import type { Ticket } from "@/features/simulator/model/types";
import "@/features/simulator/simulator.css";
import { Loading } from "@/shared/components/ui";

import { X } from "lucide-react";
import type { CSSProperties } from "react";
import HelpDialog from "../components/HelpDialog";
import MissionBar from "../components/MissionBar";
import MarketDialogs from "../components/MarketDialogs";
import OrderDialogs from "../components/OrderDialogs";
import RunDialogs from "../components/RunDialogs";
import TerminalStatus from "../components/TerminalStatus";
import TerminalToolbar from "../components/TerminalToolbar";
import TerminalWorkspace from "../components/TerminalWorkspace";
import { useTradingTerminal } from "../hooks/useTradingTerminal";
export default function TradingSimulator() {
  const terminal = useTradingTerminal();
  const {
    loading,
    run,
    error,
    load,
    busy,
    pending,
    archived,
    marketError,
    connectionError,
    bars,
    prefs,
    ticket,
    setPrefs,
    setPlaying,
    setPreview,
    root,
    dark,
    mobileTab,
    notice,
    retryPending,
    setMarketRetry,
    setError,
    setNotice,
  } = terminal;
  if (loading) return <Loading label="Opening your paper trading terminal…" />;
  if (!run)
    return (
      <div className="page">
        <h1>Trading simulator</h1>
        <p role="alert">{error}</p>
        <button className="button primary" onClick={() => void load()}>
          Reconnect
        </button>
      </div>
    );
  const blocked =
    busy ||
    !!pending ||
    archived ||
    !!marketError ||
    !!connectionError ||
    !bars.length;
  // A generated market produces the next session as the clock reaches it, so only
  // a bounded import can finish.
  const complete = !run.endless && run.cursor >= run.total_bars - 1;
  // A stop holds the clock but not the ticket: trading is one of the two ways
  // of answering it, so only the replay controls are disabled.
  const stopped = !!run.interrupted;
  const estimate = orderEstimate(run, prefs.symbol, ticket);
  const marketClosed =
    run.config.base_interval === "1D" ||
    new Date(run.clock * 1000).toLocaleTimeString("en-GB", {
      timeZone: "America/New_York",
      hour: "2-digit",
      minute: "2-digit",
    }) === "15:59";
  const feedback = error ? (
    <p className="sim-validation" role="alert">
      {error}
      {pending
        ? " Close this dialog to reconnect and retry the saved action."
        : ""}
    </p>
  ) : null;
  const ticketProps = {
    run,
    symbol: prefs.symbol,
    ticket,
    setTicket: (next: Ticket) => setPrefs({ ticket: next }),
    onPreview: () => {
      setPlaying(false);
      setPreview(true);
    },
    disabled: blocked || complete,
  };
  const view = {
    ...terminal,
    run,
    blocked,
    complete,
    stopped,
    estimate,
    marketClosed,
    feedback,
    ticketProps,
  };
  return (
    <div
      ref={root}
      className={`trading-terminal ${dark ? "dark" : ""} mobile-${mobileTab.toLowerCase()}`}
      style={
        {
          "--sim-right-width": `${prefs.rightWidth}px`,
          "--sim-bottom-height": `${prefs.bottomHeight}px`,
        } as CSSProperties
      }
      data-testid="trading-terminal"
    >
      <TerminalToolbar terminal={view} />
      <MissionBar mission={terminal.mission} />

      {error ||
      pending ||
      connectionError ||
      marketError ||
      (notice && notice !== "Replay advancing") ? (
        <div
          className={`sim-notice ${error || marketError || connectionError ? "error" : ""}`}
          role={error || marketError || connectionError ? "alert" : "status"}
        >
          <span>
            {error || marketError || connectionError || notice}
            {pending
              ? " Unconfirmed action saved; recover it before placing another trade."
              : ""}
          </span>
          {pending ? (
            <button onClick={() => void retryPending()} disabled={busy}>
              Reconnect & retry action
            </button>
          ) : marketError ? (
            <button onClick={() => setMarketRetry((v) => v + 1)}>
              Retry data
            </button>
          ) : (
            <button
              className="sim-icon"
              aria-label="Dismiss trading notice"
              onClick={() => {
                setError("");
                setNotice("");
              }}
            >
              <X size={14} />
            </button>
          )}
        </div>
      ) : null}
      {archived ? (
        <div className="sim-archive-banner">
          Archived run · review and export only{" "}
          <button
            onClick={() => {
              setPlaying(false);
              void load();
            }}
          >
            Return to current run
          </button>
        </div>
      ) : null}
      <TerminalWorkspace terminal={view} />
      <TerminalStatus terminal={view} />

      <MarketDialogs terminal={view} />
      <OrderDialogs terminal={view} />

      <RunDialogs terminal={view} />
      <HelpDialog terminal={view} />
    </div>
  );
}
