import { dollars } from "@/features/simulator/model/format";
import "@/features/simulator/simulator.css";
import { Modal } from "@/shared/components/ui";

import type { TerminalView } from "../model/view";

export default function OrderDialogs({
  terminal,
}: {
  terminal: Pick<
    TerminalView,
    | "root"
    | "preview"
    | "setPreview"
    | "ticket"
    | "prefs"
    | "feedback"
    | "run"
    | "estimate"
    | "blocked"
    | "complete"
    | "submitOrder"
    | "busy"
    | "amendment"
    | "setAmendment"
    | "perform"
    | "pending"
    | "journal"
    | "setJournal"
  >;
}) {
  const {
    root,
    preview,
    setPreview,
    ticket,
    prefs,
    feedback,
    run,
    estimate,
    blocked,
    complete,
    submitOrder,
    busy,
    amendment,
    setAmendment,
    perform,
    pending,
    journal,
    setJournal,
  } = terminal;
  return (
    <>
      <Modal
        container={root.current}
        open={preview}
        onOpenChange={setPreview}
        title={`Preview ${ticket.side} order`}
        description={`${prefs.symbol} · ${ticket.kind.replace("_", "-")} · ${ticket.tif}`}
      >
        {feedback}
        <div className="sim-preview">
          <strong>
            {ticket.quantity} shares of {prefs.symbol}
          </strong>
          <p>
            {ticket.kind === "market"
              ? "Fill at the next eligible market price"
              : `Limit ${ticket.limit || "—"} · Stop ${ticket.stop || "—"}`}
          </p>
          <p>
            Commission: {dollars(run.config.commission)} per order. Cash and
            shares are reserved when accepted. Fills depend on the next bar and
            available liquidity.
          </p>
          <dl className="sim-preview-estimates">
            <div>
              <dt>Estimated notional</dt>
              <dd>{dollars(estimate.notional)}</dd>
            </div>
            <div>
              <dt>Estimated {ticket.side === "buy" ? "debit" : "proceeds"}</dt>
              <dd>{dollars(estimate.total)}</dd>
            </div>
            <div>
              <dt>Available cash / reserved</dt>
              <dd>
                {dollars(run.available)} / {dollars(run.reserved)}
              </dd>
            </div>
            <div>
              <dt>Available shares</dt>
              <dd>{estimate.availableShares}</dd>
            </div>
            <div>
              <dt>Position after full fill</dt>
              <dd>{estimate.after} shares</dd>
            </div>
          </dl>
          {ticket.note ? <blockquote>{ticket.note}</blockquote> : null}
        </div>
        <button
          className={`sim-submit ${ticket.side}`}
          disabled={blocked || complete}
          onClick={() => void submitOrder()}
        >
          {busy ? "Submitting…" : `Place ${ticket.side} order`}
        </button>
      </Modal>
      <Modal
        container={root.current}
        open={!!amendment}
        onOpenChange={(v) => {
          if (!v) setAmendment(null);
        }}
        title="Confirm order amendment"
        description="The existing order remains unchanged until the amendment is accepted."
      >
        {feedback}
        {amendment ? (
          <form
            onSubmit={async (e) => {
              e.preventDefault();
              const result = await perform(
                `orders/${amendment.order.id}/amend`,
                {
                  ...(amendment.order.limit_price
                    ? { limit_price: amendment.limit }
                    : {}),
                  ...(amendment.order.stop_price
                    ? { stop_price: amendment.stop }
                    : {}),
                },
                "POST",
                "Order amendment confirmed.",
              );
              if (result) setAmendment(null);
            }}
          >
            {amendment.order.limit_price ? (
              <label className="sim-field">
                New limit price
                <input
                  type="number"
                  min="0.01"
                  step="0.01"
                  required
                  value={amendment.limit}
                  onChange={(e) =>
                    setAmendment({ ...amendment, limit: e.target.value })
                  }
                />
              </label>
            ) : null}
            {amendment.order.stop_price ? (
              <label className="sim-field">
                New stop price
                <input
                  type="number"
                  min="0.01"
                  step="0.01"
                  required
                  value={amendment.stop}
                  onChange={(e) =>
                    setAmendment({ ...amendment, stop: e.target.value })
                  }
                />
              </label>
            ) : null}
            <button className="sim-submit buy" disabled={busy || !!pending}>
              Confirm amendment
            </button>
          </form>
        ) : null}
      </Modal>
      <Modal
        container={root.current}
        open={!!journal}
        onOpenChange={(v) => {
          if (!v) setJournal(null);
        }}
        title="Trade journal"
        description={
          journal
            ? `${journal.side.toUpperCase()} ${journal.quantity} ${journal.symbol}`
            : ""
        }
      >
        {feedback}
        {journal ? (
          <form
            onSubmit={async (e) => {
              e.preventDefault();
              const result = await perform(
                `orders/${journal.id}/journal`,
                { note: journal.note, lesson: journal.lesson },
                "PUT",
                "Trade journal saved.",
              );
              if (result) setJournal(null);
            }}
          >
            <label className="sim-field">
              Trade thesis
              <textarea
                rows={6}
                maxLength={2000}
                value={journal.note}
                onChange={(e) =>
                  setJournal({ ...journal, note: e.target.value })
                }
              />
            </label>
            <label className="sim-field">
              Linked lesson
              <select
                value={journal.lesson}
                onChange={(e) =>
                  setJournal({ ...journal, lesson: e.target.value })
                }
              >
                <option value="">No lesson</option>
                {["0.4", "0.5", "0.7", "0.8"].map((id) => (
                  <option key={id}>{id}</option>
                ))}
              </select>
            </label>
            <button className="sim-submit buy" disabled={blocked}>
              Save journal
            </button>
          </form>
        ) : null}
      </Modal>
    </>
  );
}
