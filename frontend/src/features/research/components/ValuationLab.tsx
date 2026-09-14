import { money, percent } from "@/shared/lib/format";
import { AlertCircle, Check } from "lucide-react";
import { useState } from "react";
import { useCalculation } from "../hooks/useCalculation";
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
