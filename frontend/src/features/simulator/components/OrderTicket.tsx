import { dollars, price } from "@/features/simulator/model/format";
import { orderEstimate } from "@/features/simulator/model/orders";
import type { SimRun, Ticket } from "@/features/simulator/model/types";
import { ArrowDownLeft, ArrowUpRight } from "lucide-react";
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
    needsStop = ticket.kind === "stop" || ticket.kind === "stop_limit",
    needsTrail = ticket.kind === "trailing_stop";
  const calculation = orderEstimate(run, symbol, ticket);
  const estimate = calculation.price,
    cost = calculation.total;
  // Exits can only be attached to an entry: there is nothing for them to
  // protect on an order that is closing a position.
  const canBracket = ticket.side === "buy" && ticket.kind !== "trailing_stop";
  const bracket = canBracket && ticket.bracket;
  const trail = Number(ticket.trail),
    target = Number(ticket.takeProfit),
    loss = Number(ticket.stopLoss),
    lossTrail = Number(ticket.stopTrail);
  // The price the exits are measured against is the one this entry would pay.
  const reference = needsLimit ? limit : needsStop ? stop : estimate;
  const problem = !quote
    ? "No quote available."
    : !Number.isInteger(quantity) || quantity <= 0
      ? "Enter a positive whole number of shares."
      : needsLimit && (!Number.isFinite(limit) || limit <= 0)
        ? "Enter a positive limit price."
        : needsStop && (!Number.isFinite(stop) || stop <= 0)
          ? "Enter a positive stop price."
          : needsTrail && (!(trail > 0) || trail > 50)
            ? "Enter a trail between 0 and 50 percent."
            : needsTrail && ticket.side === "buy"
              ? "A trailing stop is an exit. Sell to use one."
              : bracket &&
                  !ticket.takeProfit &&
                  !ticket.stopLoss &&
                  !ticket.stopTrail
                ? "Set a target, a stop, or both."
                : bracket && ticket.takeProfit && !(target > reference)
                  ? "A take-profit has to sit above the entry it protects."
                  : bracket && ticket.stopLoss && !(loss < reference)
                    ? "A stop-loss has to sit below the entry it protects."
                    : bracket && ticket.stopLoss && ticket.stopTrail
                      ? "Choose a fixed stop or a trailing one, not both."
                      : bracket &&
                          ticket.stopTrail &&
                          !(lossTrail > 0 && lossTrail <= 50)
                        ? "Enter a trail between 0 and 50 percent."
                        : ticket.side === "buy" && cost > Number(run.available)
                          ? "Insufficient available cash, including working orders and fees."
                          : ticket.side === "sell" &&
                              quantity > (position?.available ?? 0)
                            ? "Insufficient available shares. This account is long-only."
                            : "";
  const risk =
    bracket && loss > 0 && reference > 0 ? (reference - loss) * quantity : null;
  const reward =
    bracket && target > 0 && reference > 0
      ? (target - reference) * quantity
      : null;
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
            <option value="trailing_stop">Trailing stop</option>
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
        {needsTrail ? (
          <label className="sim-field">
            Trail (% below the high)
            <input
              type="number"
              step="0.25"
              min="0.25"
              max="50"
              value={ticket.trail}
              onChange={(e) => change("trail", e.target.value)}
              aria-describedby="sim-ticket-problem"
              required
            />
          </label>
        ) : null}
        {canBracket ? (
          <fieldset className="sim-bracket">
            <label className="sim-check">
              <input
                type="checkbox"
                checked={ticket.bracket}
                onChange={(e) =>
                  setTicket({ ...ticket, bracket: e.target.checked })
                }
              />
              Attach exits to this entry
            </label>
            {bracket ? (
              <>
                <div className="sim-field-pair">
                  <label className="sim-field">
                    Take profit
                    <input
                      type="number"
                      step="0.01"
                      min="0.01"
                      value={ticket.takeProfit}
                      onChange={(e) => change("takeProfit", e.target.value)}
                      aria-describedby="sim-ticket-problem"
                    />
                  </label>
                  <label className="sim-field">
                    Stop loss
                    <input
                      type="number"
                      step="0.01"
                      min="0.01"
                      value={ticket.stopLoss}
                      onChange={(e) => change("stopLoss", e.target.value)}
                      aria-describedby="sim-ticket-problem"
                      disabled={!!ticket.stopTrail}
                    />
                  </label>
                </div>
                <label className="sim-field">
                  Or trail the stop (%)
                  <input
                    type="number"
                    step="0.25"
                    min="0.25"
                    max="50"
                    value={ticket.stopTrail}
                    onChange={(e) => change("stopTrail", e.target.value)}
                    aria-describedby="sim-ticket-problem"
                    disabled={!!ticket.stopLoss}
                  />
                </label>
                {risk !== null || reward !== null ? (
                  <p className="sim-small">
                    {risk !== null ? `Risking ${dollars(risk)}` : "No stop set"}
                    {reward !== null
                      ? ` to make ${dollars(reward)}`
                      : ", no target set"}
                    {risk !== null && reward !== null && risk > 0
                      ? ` · ${(reward / risk).toFixed(2)}:1`
                      : ""}
                    . Both exits are placed with the entry and wait, held, until
                    it fills; whichever triggers first cancels the other.
                  </p>
                ) : null}
              </>
            ) : null}
          </fieldset>
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
        {/* A mission that asks for a written reason should not hide the box. */}
        <details className="sim-journal-fields" open={!!run.config.mission}>
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
