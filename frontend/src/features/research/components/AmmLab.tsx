import { decimal, money, percent } from "@/shared/lib/format";
import { ArrowDownUp } from "lucide-react";
import { useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useCalculation } from "../hooks/useCalculation";
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
