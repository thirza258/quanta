import { ArrowDownLeft, ArrowUpRight } from "lucide-react";
import { dollars, price, orderEstimate } from "../../lib/simulator";
import type { SimRun, Ticket } from "../../lib/simulator";
export default function OrderTicket({
  run,
  symbol,
  ticket,
  setTicket,
  onPreview,
  disabled,
}: {
  run: SimRun;
  symbol: string;
  ticket: Ticket;
  setTicket: (t: Ticket) => void;
  onPreview: () => void;
  disabled: boolean;
}) {
  const quote = run.quotes.find((q) => q.symbol === symbol),
    position = run.positions.find((p) => p.symbol === symbol);
  const quantity = Number(ticket.quantity),
    limit = Number(ticket.limit),
    stop = Number(ticket.stop);
  const needsLimit = ticket.kind === "limit" || ticket.kind === "stop_limit",
    needsStop = ticket.kind === "stop" || ticket.kind === "stop_limit";
  const calculation = orderEstimate(run, symbol, ticket);
  const estimate = calculation.price,
    cost = calculation.total;
  const problem = !quote
    ? "No quote available."
    : !Number.isInteger(quantity) || quantity <= 0
      ? "Enter a positive whole number of shares."
      : needsLimit && (!Number.isFinite(limit) || limit <= 0)
        ? "Enter a positive limit price."
        : needsStop && (!Number.isFinite(stop) || stop <= 0)
          ? "Enter a positive stop price."
          : ticket.side === "buy" && cost > Number(run.available)
            ? "Insufficient available cash, including working orders and fees."
            : ticket.side === "sell" && quantity > (position?.available ?? 0)
              ? "Insufficient available shares. This account is long-only."
              : "";
  const change = (key: keyof Ticket, value: string) =>
    setTicket({ ...ticket, [key]: value });
  return (
    <section className="sim-ticket" aria-label="Order ticket">
      <div className="sim-ticket-heading">
        <strong>{symbol}</strong>
        <span>Order ticket</span>
      </div>
      <div className="sim-side-tabs">
        <button
          className={ticket.side === "buy" ? "active buy" : ""}
          aria-pressed={ticket.side === "buy"}
          onClick={() => change("side", "buy")}
        >
          <ArrowUpRight size={15} /> Buy
        </button>
        <button
          className={ticket.side === "sell" ? "active sell" : ""}
          aria-pressed={ticket.side === "sell"}
          onClick={() => change("side", "sell")}
        >
          <ArrowDownLeft size={15} /> Sell
        </button>
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (!problem && !disabled) onPreview();
        }}
      >
        <label className="sim-field">
          Order type
          <select
            value={ticket.kind}
            onChange={(e) => change("kind", e.target.value)}
          >
            <option value="market">Market</option>
            <option value="limit">Limit</option>
            <option value="stop">Stop</option>
            <option value="stop_limit">Stop-limit</option>
          </select>
        </label>
        <div className="sim-field-pair">
          <label className="sim-field">
            Shares
            <input
              type="number"
              min="1"
              max="1000000"
              step="1"
              value={ticket.quantity}
              onChange={(e) => change("quantity", e.target.value)}
              aria-describedby="sim-ticket-problem"
              required
            />
          </label>
          <label className="sim-field">
            Duration
            <select
              value={ticket.tif}
              onChange={(e) => change("tif", e.target.value)}
            >
              <option>GTC</option>
              <option>DAY</option>
            </select>
          </label>
        </div>
        {needsLimit ? (
          <label className="sim-field">
            Limit price
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={ticket.limit}
              onChange={(e) => change("limit", e.target.value)}
              aria-describedby="sim-ticket-problem"
              required
            />
          </label>
        ) : null}
        {needsStop ? (
          <label className="sim-field">
            Stop price
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={ticket.stop}
              onChange={(e) => change("stop", e.target.value)}
              aria-describedby="sim-ticket-problem"
              required
            />
          </label>
        ) : null}
        <div className="sim-order-estimates">
          <div>
            <span>Reserved cash</span>
            <strong>{dollars(run.reserved)}</strong>
          </div>
          <div>
            <span>Last price</span>
            <strong>{quote ? price(quote.close) : "Unavailable"}</strong>
          </div>
          <div>
            <span>Estimated value</span>
            <strong>
              {Number.isFinite(quantity * estimate)
                ? dollars(quantity * estimate)
                : "—"}
            </strong>
          </div>
          <div>
            <span>Commission / order</span>
            <strong>{dollars(run.config.commission)}</strong>
          </div>
          <div>
            <span>
              {ticket.side === "buy" ? "Available cash" : "Available shares"}
            </span>
            <strong>
              {ticket.side === "buy"
                ? dollars(run.available)
                : (position?.available ?? 0)}
            </strong>
          </div>
          <div>
            <span>Position after full fill</span>
            <strong>
              {Math.max(
                0,
                (position?.quantity ?? 0) +
                  (ticket.side === "buy" ? quantity : -quantity),
              )}{" "}
              shares
            </strong>
          </div>
        </div>
        <details className="sim-journal-fields">
          <summary>Trade thesis & lesson</summary>
          <label className="sim-field">
            Trade thesis
            <textarea
              rows={3}
              maxLength={2000}
              value={ticket.note}
              onChange={(e) => change("note", e.target.value)}
              placeholder="Why this trade? What would change your view?"
            />
          </label>
          <label className="sim-field">
            Linked lesson
            <select
              value={ticket.lesson}
              onChange={(e) => change("lesson", e.target.value)}
            >
              <option value="">No lesson</option>
              <option value="0.4">0.4 · Quotes and orders</option>
              <option value="0.5">0.5 · Returns and costs</option>
              <option value="0.7">0.7 · Risk and sizing</option>
              <option value="0.8">0.8 · Trading plan</option>
            </select>
          </label>
        </details>
        {problem ? (
          <p className="sim-validation" role="status" id="sim-ticket-problem">
            {problem}
          </p>
        ) : null}
        <button
          className={`sim-submit ${ticket.side}`}
          disabled={!!problem || disabled}
        >
          Preview {ticket.side} order
        </button>
        <p className="sim-small">
          Orders become eligible on the next replay bar. Estimated prices and
          stop triggers are not guaranteed fills.
        </p>
      </form>
    </section>
  );
}
