import "@/features/simulator/simulator.css";
import { Modal } from "@/shared/components/ui";

import { download } from "@/shared/lib/download";
import { Download } from "lucide-react";
import type { TerminalView } from "../model/view";

export default function RunDialogs({
  terminal,
}: {
  terminal: Pick<
    TerminalView,
    | "root"
    | "resetOpen"
    | "setResetOpen"
    | "feedback"
    | "startRun"
    | "newConfig"
    | "setNewConfig"
    | "boot"
    | "busy"
    | "exportOpen"
    | "setExportOpen"
    | "run"
    | "prefs"
    | "bars"
    | "news"
    | "fundamentals"
    | "desk"
    | "calendar"
    | "missionCatalog"
  >;
}) {
  const {
    root,
    resetOpen,
    setResetOpen,
    feedback,
    startRun,
    newConfig,
    setNewConfig,
    boot,
    busy,
    exportOpen,
    setExportOpen,
    run,
    prefs,
    bars,
    news,
    fundamentals,
    desk,
    calendar,
    missionCatalog,
  } = terminal;
  return (
    <>
      <Modal
        container={root.current}
        open={resetOpen}
        onOpenChange={setResetOpen}
        title="Start a new simulation"
        description="Create a fresh $100,000 paper account. This run and its trade history remain available in the run selector."
      >
        {feedback}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            void startRun();
          }}
        >
          <label className="sim-field">
            Practice mission (optional)
            <select
              value={newConfig.mission}
              onChange={(e) =>
                setNewConfig({
                  ...newConfig,
                  mission: e.target.value,
                  mode: e.target.value ? "synthetic" : newConfig.mode,
                })
              }
            >
              <option value="">No mission · free practice</option>
              {missionCatalog?.missions.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.title} · {m.symbol}
                </option>
              ))}
            </select>
            <small className="sim-small">
              A mission fixes the market and the starting point, so everyone
              attempting it meets the same one. Its objectives describe process,
              never profit.
            </small>
          </label>
          <label className="sim-field">
            Account type
            <select
              value={newConfig.mission ? "cash" : newConfig.account}
              disabled={!!newConfig.mission}
              onChange={(e) =>
                setNewConfig({ ...newConfig, account: e.target.value })
              }
            >
              <option value="cash">Cash · long only</option>
              <option value="margin">Margin · may sell short</option>
            </select>
            <small className="sim-small">
              A cash account can only sell what it owns. A margin account can
              borrow stock to sell: half the value is held as initial margin,
              the borrow accrues a fee every session, and the account is bought
              in if equity falls under 30% of what it is carrying. Dividends are
              not modelled, in either direction. Practice missions always run on
              a cash account.
            </small>
          </label>
          <label className="sim-field">
            Market data
            <select
              value={newConfig.mode}
              onChange={(e) =>
                setNewConfig({
                  ...newConfig,
                  mode: e.target.value,
                  symbol: boot?.historical[0]?.symbol ?? "",
                })
              }
            >
              <option value="synthetic">Seeded synthetic market</option>
              <option value="historical" disabled={!boot?.historical.length}>
                Historical replay
                {!boot?.historical.length ? " · no imported datasets" : ""}
              </option>
            </select>
          </label>
          {newConfig.mode === "synthetic" ? (
            <label className="sim-field">
              Market seed (optional)
              <input
                type="number"
                min={0}
                max={1000000}
                placeholder="Automatic"
                value={newConfig.seed}
                onChange={(e) =>
                  setNewConfig({ ...newConfig, seed: e.target.value })
                }
              />
              <small className="sim-small">
                Leave empty for a new generated market and news schedule. Enter
                a number to reproduce the same one.
              </small>
            </label>
          ) : (
            <label className="sim-field">
              Historical stock
              <select
                value={newConfig.symbol}
                onChange={(e) =>
                  setNewConfig({ ...newConfig, symbol: e.target.value })
                }
              >
                {boot?.historical.map((d) => (
                  <option key={d.symbol}>{d.symbol}</option>
                ))}
              </select>
            </label>
          )}
          <div className="sim-field-pair">
            {(
              [
                {
                  key: "commission",
                  label: "Commission / order ($)",
                  step: "0.01",
                  max: 100,
                  min: 0,
                },
                {
                  key: "slippage_bps",
                  label: "Slippage (bps)",
                  step: "0.1",
                  max: 100,
                  min: 0,
                },
                {
                  key: "spread_bps",
                  label: "Spread (bps)",
                  step: "0.1",
                  max: 100,
                  min: 0,
                },
                {
                  key: "participation",
                  label: "Volume participation (0–1)",
                  step: "0.001",
                  max: 1,
                  min: 0.001,
                },
              ] as const
            ).map((f) => (
              <label key={f.key} className="sim-field">
                {f.label}
                <input
                  type="number"
                  step={f.step}
                  min={f.min}
                  max={f.max}
                  required
                  value={newConfig[f.key]}
                  onChange={(e) =>
                    setNewConfig({ ...newConfig, [f.key]: e.target.value })
                  }
                />
              </label>
            ))}
          </div>
          <p className="sim-small">
            Long-only, whole-share practice. Immediate settlement is a teaching
            simplification. Synthetic runs list fictional companies whose prices
            respond to a generated news schedule; nothing in them describes a
            real issuer. Historical corporate-action treatment comes from the
            imported dataset.
          </p>
          <button className="sim-submit buy" disabled={busy}>
            Create new paper account
          </button>
        </form>
      </Modal>
      <Modal
        container={root.current}
        open={exportOpen}
        onOpenChange={setExportOpen}
        title="Export simulation"
        description="Exports include confirmed history, observed market data, and the simulated headlines and statements released so far."
      >
        <button
          className="sim-outline"
          onClick={() =>
            download(`quanta-simulation-${run.id}.json`, {
              ...run,
              preferences: prefs,
              bars,
              simulated_news: news?.items ?? [],
              simulated_sentiment: news?.sentiment ?? null,
              simulated_statements: fundamentals,
              desk_analytics: desk,
              reporting_calendar: calendar,
              disclosure: run.disclosure,
            })
          }
        >
          <Download size={16} /> Run, chart settings & journal (JSON)
        </button>
        <p className="sim-small">
          Use the export icon on each trading-panel tab for its CSV file.
          Archived runs remain available in the run selector.
        </p>
      </Modal>
    </>
  );
}
