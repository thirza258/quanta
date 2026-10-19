import { stamp } from "@/features/simulator/model/format";
import type { SimRun, StopEvent } from "@/features/simulator/model/types";
import "@/features/simulator/simulator.css";
import { Pause, X } from "lucide-react";

/** What each stop is for, in the learner's terms rather than the engine's. */
export const STOP_EVENTS: { id: StopEvent; label: string; hint: string }[] = [
  {
    id: "fill",
    label: "My order fills",
    hint: "Stop on the bar an order of yours trades.",
  },
  {
    id: "bracket",
    label: "An exit triggers",
    hint: "Stop when a take-profit or stop-loss leg trades.",
  },
  {
    id: "earnings",
    label: "A company I hold reports",
    hint: "Stop on the bar a held or ordered company prints its quarter.",
  },
  {
    id: "news",
    label: "High-impact news on a position",
    hint: "Stop on a high-impact scored headline touching a position of yours.",
  },
  {
    id: "margin_call",
    label: "The account is called",
    hint: "Stop when equity falls under the maintenance requirement.",
  },
];

export default function DecisionCard({
  run,
  onDismiss,
  onTrade,
  onHold,
  busy,
}: {
  run: SimRun;
  onDismiss: () => void;
  onTrade: () => void;
  onHold: () => void;
  busy: boolean;
}) {
  const stop = run.interrupted;
  if (!stop) return null;
  return (
    <aside className="sim-decision" role="alert" aria-label="Replay stopped">
      <Pause size={16} />
      <div className="sim-decision-body">
        <strong>{stop.reason}</strong>
        <span className="sim-small">
          The clock stopped here, {stamp(run.clock)}, after{" "}
          {(stop.ran ?? 1).toLocaleString("en-US")} of the{" "}
          {stop.of.toLocaleString("en-US")} bars you asked for, with{" "}
          {Math.max(0, stop.of - (stop.ran ?? 1)).toLocaleString("en-US")} still
          to run. Decide now, while the outcome is still unknown.
        </span>
      </div>
      <div className="sim-decision-actions">
        <button className="sim-submit buy" disabled={busy} onClick={onTrade}>
          Trade
        </button>
        <button className="sim-text-button" disabled={busy} onClick={onHold}>
          Hold, and say why
        </button>
        <button
          className="sim-icon"
          aria-label="Hold without a reason"
          title="Hold without giving a reason. It still counts as answered, but
          a campaign objective that asks for reasons will not count it."
          disabled={busy}
          onClick={onDismiss}
        >
          <X size={15} />
        </button>
      </div>
    </aside>
  );
}
