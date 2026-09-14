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
              Random seed
              <input
                type="number"
                min={0}
                max={1000000}
                required
                value={newConfig.seed}
                onChange={(e) =>
                  setNewConfig({ ...newConfig, seed: e.target.value })
                }
              />
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
            simplification. Historical corporate-action treatment comes from the
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
        description="Exports include confirmed history and observed market data only."
      >
        <button
          className="sim-outline"
          onClick={() =>
            download(`quanta-simulation-${run.id}.json`, {
              ...run,
              preferences: prefs,
              bars,
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
