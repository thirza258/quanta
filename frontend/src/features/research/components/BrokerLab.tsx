import { post } from "@/shared/api/client";
import { Modal } from "@/shared/components/ui";

import { decimal, money } from "@/shared/lib/format";
import { ArrowDownUp, ArrowRight, RotateCcw } from "lucide-react";
import { useState } from "react";
type PaperState = {
  cash: number;
  quantity: number;
  initial_equity: number;
  halted: boolean;
};
type Order = {
  id: string;
  status: string;
  reason: string | null;
  side: string;
  filled: number;
  remaining: number;
  price: number;
  commission: number;
  state: PaperState;
};
const newPaper = (): PaperState => ({
  cash: 100000,
  quantity: 0,
  initial_equity: 100000,
  halted: false,
});
export function BrokerLab() {
  const [account, setAccount] = useState<PaperState>(newPaper),
    [orders, setOrders] = useState<Order[]>([]),
    [input, setInput] = useState({
      side: "buy",
      quantity: 10,
      price: 100,
      volume: 1000,
      slippage_bps: 3,
      commission_bps: 5,
      spread_bps: 5,
      data_age_seconds: 0,
    }),
    [busy, setBusy] = useState(false),
    [error, setError] = useState(""),
    [reset, setReset] = useState(false);
  const place = async (quantity = input.quantity) => {
    setBusy(true);
    setError("");
    try {
      const order = await post<Order>("/broker/order", {
        ...input,
        quantity,
        state: account,
      });
      setAccount(order.state);
      setOrders((old) => [order, ...old]);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  };
  return (
    <div className="broker-layout">
      <div className="paper-stats">
        <div>
          <label>CASH AVAILABLE</label>
          <strong>{money(account.cash)}</strong>
        </div>
        <div>
          <label>SHARES HELD</label>
          <strong>{decimal(account.quantity)}</strong>
        </div>
        <div>
          <label>MARKED EQUITY</label>
          <strong>
            {money(account.cash + account.quantity * input.price)}
          </strong>
        </div>
        <div>
          <label>RISK STATE</label>
          <strong className={account.halted ? "negative" : "positive"}>
            {account.halted ? "Halted" : "Active"}
          </strong>
        </div>
      </div>
      <div className="tool-layout">
        <section className="tool-card">
          <div className="tool-card-heading">
            <span className="eyebrow">QUANTA MOCK BROKER</span>
            <h2>Place a paper order.</h2>
            <p>Inspect fill behavior with explicit market assumptions.</p>
          </div>
          <div className="segmented">
            <button
              className={input.side === "buy" ? "active" : ""}
              onClick={() => setInput({ ...input, side: "buy" })}
            >
              Buy
            </button>
            <button
              className={input.side === "sell" ? "active" : ""}
              onClick={() => setInput({ ...input, side: "sell" })}
            >
              Sell
            </button>
          </div>
          <div className="input-grid">
            {[
              ["quantity", "Order quantity"],
              ["price", "Reference price ($)"],
              ["volume", "Available bar volume"],
              ["spread_bps", "Bid-ask spread (bps)"],
              ["slippage_bps", "Slippage (bps)"],
              ["commission_bps", "Commission (bps)"],
              ["data_age_seconds", "Price age (seconds)"],
            ].map(([key, label]) => (
              <label className="field" key={key}>
                {label}
                <input
                  type="number"
                  min={["price", "quantity"].includes(key) ? 0.01 : 0}
                  step="1"
                  value={input[key as "quantity"]}
                  onChange={(e) =>
                    setInput({ ...input, [key]: Number(e.target.value) })
                  }
                />
              </label>
            ))}
          </div>
          <button
            className="button primary full-width"
            disabled={busy}
            onClick={() => void place()}
          >
            {busy ? "Simulating fill…" : `Submit ${input.side} order`}
            <ArrowRight size={16} />
          </button>
          {error ? <p className="error-message">{error}</p> : null}
          <p className="fine-print">
            10% volume participation cap · 100 bps spread guard · 60s
            stale-price guard · 2.5% loss breaker relative to initial account
            equity. This single-session paper account has no live brokerage
            connection.
          </p>
        </section>
        <section className="tool-card">
          <div className="tool-card-heading row">
            <div>
              <span className="eyebrow">ORDER AUDIT LOG</span>
              <h2>Every fill has a story.</h2>
            </div>
            <button
              className="icon-button"
              aria-label="Reset paper account"
              onClick={() => setReset(true)}
            >
              <RotateCcw size={17} />
            </button>
          </div>
          {!orders.length ? (
            <div className="empty-state">
              <ArrowDownUp size={26} />
              <h3>Waiting for your first order.</h3>
              <p>
                Try increasing the order size beyond 10% of available volume to
                observe a partial fill.
              </p>
            </div>
          ) : (
            <div className="order-log">
              {orders.map((o) => (
                <article key={o.id}>
                  <div>
                    <span className={`order-side ${o.side}`}>
                      {o.side.toUpperCase()}
                    </span>
                    <strong>{o.status.replaceAll("_", " ")}</strong>
                    <span className="mono">{o.filled} filled</span>
                  </div>
                  {o.reason ? (
                    <p className="negative">{o.reason}</p>
                  ) : (
                    <p>
                      {money(o.price)} / share · {money(o.commission)}{" "}
                      commission
                      {o.remaining > 0 ? ` · ${o.remaining} unfilled` : ""}
                    </p>
                  )}
                  <small className="mono">{o.id.slice(0, 12)}</small>
                  {o.remaining > 0 && o.status === "partially_filled" ? (
                    <p className="fine-print">
                      Unfilled quantity remains unexecuted. Submit a new order
                      after updating market conditions to simulate a later fill.
                    </p>
                  ) : null}
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
      <Modal
        open={reset}
        onOpenChange={setReset}
        title="Reset the paper account?"
        description="This starts a fresh $100,000 simulation and clears this session’s order log."
      >
        <div className="dialog-actions">
          <button className="button secondary" onClick={() => setReset(false)}>
            Keep account
          </button>
          <button
            className="button primary"
            onClick={() => {
              setAccount(newPaper());
              setOrders([]);
              setReset(false);
            }}
          >
            Reset simulation
          </button>
        </div>
      </Modal>
    </div>
  );
}
