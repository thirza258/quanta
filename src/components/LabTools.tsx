import { useEffect, useState } from "react";
import {
  AlertCircle,
  ArrowDownUp,
  ArrowRight,
  Check,
  RotateCcw,
} from "lucide-react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { post, decimal, money, percent } from "../lib/api";
import { Modal } from "./ui";
function useCalculation<T>(path: string, input: unknown) {
  const [result, setResult] = useState<T | null>(null),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(true);
  const key = JSON.stringify(input);
  useEffect(() => {
    let active = true;
    setBusy(true);
    const timer = setTimeout(() => {
      post<T>(path, JSON.parse(key))
        .then((value) => {
          if (active) {
            setResult(value);
            setError("");
          }
        })
        .catch((e) => {
          if (active) setError(e.message);
        })
        .finally(() => {
          if (active) setBusy(false);
        });
    }, 250);
    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [path, key]);
  return { result, error, busy };
}
export function ValuationLab() {
  const [input, setInput] = useState({
    cash: 40,
    receivables: 60,
    inventory: 80,
    liabilities: 70,
    shares: 10,
    receivable_recovery: 0.85,
    inventory_recovery: 0.6,
    eps: 4,
    growth: 5,
    bond_yield: 4.4,
    price: 6,
  });
  const { result, error, busy } = useCalculation<{
    ncav: number;
    adjusted_ncav: number;
    screen_price: number;
    graham_value: number;
    margin_of_safety: number | null;
    passes_screen: boolean;
  }>("/analytics/valuation", input);
  return (
    <div className="tool-layout">
      <section className="tool-card">
        <div className="tool-card-heading">
          <span className="eyebrow">BALANCE SHEET INPUTS</span>
          <h2>What is the asset cushion?</h2>
          <p>Enter amounts in millions, except per-share values.</p>
        </div>
        <div className="input-grid">
          {[
            ["cash", "Cash & equivalents"],
            ["receivables", "Accounts receivable"],
            ["inventory", "Inventory"],
            ["liabilities", "Total liabilities"],
            ["shares", "Diluted shares"],
            ["price", "Market price / share"],
          ].map(([key, label]) => (
            <label className="field" key={key}>
              {label}
              <input
                type="number"
                min={key === "shares" || key === "price" ? 0.01 : 0}
                step="0.1"
                value={input[key as "cash"]}
                onChange={(e) =>
                  setInput({ ...input, [key]: Number(e.target.value) })
                }
              />
            </label>
          ))}
        </div>
        <h3 className="small-heading">Liquidation assumptions</h3>
        {[
          ["receivable_recovery", "Receivables recovered"],
          ["inventory_recovery", "Inventory recovered"],
        ].map(([key, label]) => (
          <label className="slider-field" key={key}>
            <span>
              {label}
              <strong>{percent(input[key as "cash"], 0)}</strong>
            </span>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={input[key as "cash"]}
              onChange={(e) =>
                setInput({ ...input, [key]: Number(e.target.value) })
              }
            />
          </label>
        ))}
        <h3 className="small-heading">Graham formula inputs</h3>
        <div className="input-grid three">
          {[
            ["eps", "EPS ($)"],
            ["growth", "Growth (%)"],
            ["bond_yield", "Bond yield (%)"],
          ].map(([key, label]) => (
            <label className="field" key={key}>
              {label}
              <input
                type="number"
                step="0.1"
                min={
                  key === "bond_yield" ? 0.1 : key === "growth" ? -4 : -10000
                }
                value={input[key as "cash"]}
                onChange={(e) =>
                  setInput({ ...input, [key]: Number(e.target.value) })
                }
              />
            </label>
          ))}
        </div>
      </section>
      <section className="tool-card valuation-result" aria-live="polite">
        <span className="eyebrow">
          VALUATION WORKSHEET{busy ? " · UPDATING" : ""}
        </span>
        <h2>Value, with room for uncertainty.</h2>
        {error ? <p className="error-message">{error}</p> : null}
        {result ? (
          <>
            <div className="valuation-hero-number">
              <span>ADJUSTED NCAV / SHARE</span>
              <strong>{money(result.adjusted_ncav)}</strong>
              <small>After your receivable and inventory haircuts</small>
            </div>
            <div className="value-comparison">
              <span
                style={{
                  width: `${Math.min(100, (input.price / Math.max(input.price, result.ncav)) * 100)}%`,
                }}
              />
              <div>
                <span>Market price</span>
                <strong>{money(input.price)}</strong>
              </div>
            </div>
            <div className="value-comparison intrinsic">
              <span
                style={{
                  width: `${Math.max(0, (result.adjusted_ncav / Math.max(input.price, result.ncav)) * 100)}%`,
                }}
              />
              <div>
                <span>Adjusted asset value</span>
                <strong>{money(result.adjusted_ncav)}</strong>
              </div>
            </div>
            <div className="valuation-metrics">
              <div>
                <span>Unadjusted NCAV</span>
                <strong>{money(result.ncav)}</strong>
              </div>
              <div>
                <span>Two-thirds screen price</span>
                <strong>{money(result.screen_price)}</strong>
              </div>
              <div>
                <span>Margin of safety · adjusted NCAV</span>
                <strong
                  className={
                    (result.margin_of_safety || 0) > 0 ? "positive" : "negative"
                  }
                >
                  {percent(result.margin_of_safety)}
                </strong>
              </div>
              <div>
                <span>Graham heuristic value</span>
                <strong>{money(result.graham_value)}</strong>
              </div>
            </div>
            <div
              className={`screen-status ${result.passes_screen ? "passes" : ""}`}
            >
              {result.passes_screen ? (
                <Check size={18} />
              ) : (
                <AlertCircle size={18} />
              )}
              <span>
                {result.passes_screen
                  ? "Passes the unadjusted two-thirds NCAV screen."
                  : "Does not pass the unadjusted two-thirds NCAV screen."}
              </span>
            </div>
            <p className="fine-print">
              A screen is a starting point for investigation. The Graham
              heuristic and asset-based estimates answer different questions;
              neither guarantees realizable value.
            </p>
          </>
        ) : null}
      </section>
    </div>
  );
}
export function AmmLab() {
  const [input, setInput] = useState({
    x: 10,
    y: 20000,
    trade: 1,
    fee: 0.003,
    price_ratio: 2,
    lower_ratio: 0.5,
    upper_ratio: 2,
  });
  const { result, error, busy } = useCalculation<{
    output: number;
    spot_price: number;
    execution_price: number;
    price_impact: number;
    impermanent_loss: number;
    concentrated_loss: number;
    in_range: boolean;
    fee_x: number;
  }>("/analytics/amm", input);
  const chart = Array.from({ length: 70 }, (_, i) => {
    const ratio = 0.1 + i * 0.07;
    return { ratio, loss: ((2 * Math.sqrt(ratio)) / (1 + ratio) - 1) * 100 };
  });
  return (
    <div className="tool-layout">
      <section className="tool-card">
        <div className="tool-card-heading">
          <span className="eyebrow">CONSTANT-PRODUCT POOL</span>
          <h2>Follow the reserves.</h2>
          <p>Explore an ETH / USDC pool with x · y = k.</p>
        </div>
        <div className="input-grid">
          {[
            ["x", "ETH reserves"],
            ["y", "USDC reserves"],
            ["trade", "ETH to swap"],
            ["fee", "Swap fee (decimal)"],
          ].map(([key, label]) => (
            <label className="field" key={key}>
              {label}
              <input
                type="number"
                min={key === "fee" || key === "trade" ? 0 : 0.001}
                step={key === "fee" ? 0.001 : 0.1}
                max={key === "fee" ? 0.1 : 1000000000000}
                value={input[key as "x"]}
                onChange={(e) =>
                  setInput({ ...input, [key]: Number(e.target.value) })
                }
              />
            </label>
          ))}
        </div>
        <div className="swap-output">
          <span>
            <ArrowDownUp size={17} />
            Estimated swap output
          </span>
          <strong>
            {result ? decimal(result.output) : "—"} <small>USDC</small>
          </strong>
        </div>
        <label className="slider-field">
          <span>
            Future price / initial price
            <strong>{input.price_ratio.toFixed(2)}×</strong>
          </span>
          <input
            type="range"
            min="0.1"
            max="5"
            step="0.05"
            value={input.price_ratio}
            onChange={(e) =>
              setInput({ ...input, price_ratio: Number(e.target.value) })
            }
          />
        </label>
        <h3 className="small-heading">Concentrated liquidity range</h3>
        <div className="input-grid">
          <label className="field">
            Lower price ratio
            <input
              type="number"
              min="0.01"
              max="0.99"
              step="0.05"
              value={input.lower_ratio}
              onChange={(e) =>
                setInput({ ...input, lower_ratio: Number(e.target.value) })
              }
            />
          </label>
          <label className="field">
            Upper price ratio
            <input
              type="number"
              min="1.01"
              step="0.1"
              value={input.upper_ratio}
              onChange={(e) =>
                setInput({ ...input, upper_ratio: Number(e.target.value) })
              }
            />
          </label>
        </div>
        <p className="fine-print">
          Initial price is normalized to 1 for the range calculation.
          Concentrated positions use piecewise reserve accounting; fees and gas
          are excluded from LP relative returns.
        </p>
      </section>
      <section className="tool-card">
        <span className="eyebrow">
          LIQUIDITY PROVIDER ANALYSIS{busy ? " · UPDATING" : ""}
        </span>
        <h2>The cost of price movement.</h2>
        <div className="tool-chart">
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={chart}>
              <defs>
                <linearGradient id="loss-gradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#b96874" stopOpacity={0.02} />
                  <stop offset="100%" stopColor="#b96874" stopOpacity={0.18} />
                </linearGradient>
              </defs>
              <CartesianGrid vertical={false} stroke="var(--border)" />
              <XAxis
                dataKey="ratio"
                tickFormatter={(v) => `${Number(v).toFixed(1)}×`}
                minTickGap={32}
                tick={{ fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                unit="%"
                tick={{ fontSize: 11 }}
                axisLine={false}
                tickLine={false}
                width={40}
              />
              <Tooltip
                formatter={(v) => [`${Number(v).toFixed(2)}%`, "Full-range IL"]}
                labelFormatter={(v) => `Price ratio ${Number(v).toFixed(2)}×`}
              />
              <Area
                type="monotone"
                dataKey="loss"
                stroke="#b96874"
                fill="url(#loss-gradient)"
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        {error ? <p className="error-message">{error}</p> : null}
        {result ? (
          <div className="valuation-metrics">
            <div>
              <span>Full-range impermanent loss</span>
              <strong className="negative">
                {percent(result.impermanent_loss, 2)}
              </strong>
            </div>
            <div>
              <span>Concentrated position vs. holding</span>
              <strong className="negative">
                {percent(result.concentrated_loss, 2)}
              </strong>
            </div>
            <div>
              <span>Position status</span>
              <strong>{result.in_range ? "In range" : "Out of range"}</strong>
            </div>
            <div>
              <span>Execution price</span>
              <strong>{money(result.execution_price)}</strong>
            </div>
            <div>
              <span>Price impact including fee</span>
              <strong>{percent(result.price_impact, 2)}</strong>
            </div>
            <div>
              <span>Fee retained by pool</span>
              <strong>{decimal(result.fee_x, 4)} ETH</strong>
            </div>
          </div>
        ) : null}
      </section>
    </div>
  );
}
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
type FactorResult = {
  coefficients: {
    factor: string;
    coefficient: number;
    standard_error: number;
    t_stat: number;
    p_value: number;
  }[];
  r_squared: number;
  adjusted_r_squared: number;
  observations: number;
  hac_lags: number;
  ridge_oos_r_squared: number | null;
  train_observations: number;
  test_observations: number;
  residuals: { index: number; residual: number }[];
  provenance: string;
};
export function FactorLab() {
  const [input, setInput] = useState({
      model: "ff3",
      observations: 756,
      seed: 42,
      noise: 0.01,
    }),
    [result, setResult] = useState<FactorResult | null>(null),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  return (
    <div className="tool-layout">
      <section className="tool-card">
        <div className="tool-card-heading">
          <span className="eyebrow">FACTOR & REGRESSION STUDIO</span>
          <h2>Explain the exposures.</h2>
          <p>
            Fit a model to synthetic returns with known factor exposures.
            Compare the recovered coefficients.
          </p>
        </div>
        <label className="field">
          Factor specification
          <select
            value={input.model}
            onChange={(e) => setInput({ ...input, model: e.target.value })}
          >
            <option value="capm">CAPM · market only</option>
            <option value="ff3">Fama–French · three factors</option>
            <option value="carhart4">Carhart · four factors</option>
            <option value="ff5">Fama–French · five factors</option>
          </select>
        </label>
        <div className="input-grid">
          <label className="field">
            Observations
            <input
              type="number"
              min="60"
              max="5000"
              value={input.observations}
              onChange={(e) =>
                setInput({ ...input, observations: Number(e.target.value) })
              }
            />
          </label>
          <label className="field">
            Random seed
            <input
              type="number"
              min="0"
              value={input.seed}
              onChange={(e) =>
                setInput({ ...input, seed: Number(e.target.value) })
              }
            />
          </label>
        </div>
        <label className="slider-field">
          <span>
            Idiosyncratic daily volatility
            <strong>{percent(input.noise, 1)}</strong>
          </span>
          <input
            type="range"
            min="0.001"
            max="0.05"
            step="0.001"
            value={input.noise}
            onChange={(e) =>
              setInput({ ...input, noise: Number(e.target.value) })
            }
          />
        </label>
        <button
          className="button primary full-width"
          disabled={busy}
          onClick={async () => {
            setBusy(true);
            setError("");
            try {
              setResult(await post<FactorResult>("/analytics/factors", input));
            } catch (e) {
              setError((e as Error).message);
            } finally {
              setBusy(false);
            }
          }}
        >
          {busy ? "Fitting model…" : "Fit factor model"}
          <ArrowRight size={16} />
        </button>
        <div className="lesson-objective">
          <span className="eyebrow">KNOWN DATA-GENERATING PROCESS</span>
          <p>
            Daily alpha: 0.0001. Factor exposures in order: 1.10, 0.25, 0.40,
            0.15, −0.10. Added noise obscures the signal. These are generated
            observations, not historical factor returns.
          </p>
        </div>
        <p className="fine-print">
          The API also accepts uploaded excess-return observations. Standard
          errors use Newey–West HAC. A chronological ridge model fits the first
          75% and tests on the remaining 25%.
        </p>
      </section>
      <section className="tool-card">
        <span className="eyebrow">MODEL DIAGNOSTICS</span>
        <h2>Signal, noise, and uncertainty.</h2>
        {error ? (
          <p className="error-message" role="alert">
            {error}
          </p>
        ) : null}
        {result ? (
          <>
            <div className="metrics-grid factor-metrics">
              <div>
                <span>R² · OLS</span>
                <strong>{decimal(result.r_squared, 3)}</strong>
              </div>
              <div>
                <span>ADJUSTED R²</span>
                <strong>{decimal(result.adjusted_r_squared, 3)}</strong>
              </div>
              <div>
                <span>TEST R² · RIDGE</span>
                <strong>{decimal(result.ridge_oos_r_squared, 3)}</strong>
              </div>
            </div>
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>Factor</th>
                    <th>β</th>
                    <th>SE · HAC</th>
                    <th>p-value</th>
                  </tr>
                </thead>
                <tbody>
                  {result.coefficients.map((c) => (
                    <tr key={c.factor}>
                      <td>{c.factor}</td>
                      <td>{decimal(c.coefficient, 4)}</td>
                      <td>{decimal(c.standard_error, 4)}</td>
                      <td>{decimal(c.p_value, 4)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <h3 className="small-heading">OLS residuals</h3>
            <div className="tool-chart">
              <ResponsiveContainer width="100%" height={190}>
                <LineChart data={result.residuals}>
                  <CartesianGrid vertical={false} stroke="var(--border)" />
                  <XAxis dataKey="index" hide />
                  <YAxis tick={{ fontSize: 10 }} width={45} />
                  <Tooltip />
                  <Line
                    dataKey="residual"
                    stroke="#51866f"
                    dot={false}
                    strokeWidth={1}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="fine-print">
              {result.observations} observations · {result.hac_lags} HAC lags ·
              ridge training/test split {result.train_observations}/
              {result.test_observations}. A strong fit on generated data does
              not establish market predictability.
            </p>
          </>
        ) : (
          <div className="empty-state">
            <h3>A coefficient needs context.</h3>
            <p>
              Fit a factor model to inspect estimated exposures, uncertainty,
              and performance on unseen observations.
            </p>
          </div>
        )}
      </section>
    </div>
  );
}
