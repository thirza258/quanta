import { post } from "@/shared/api/client";
import { decimal, percent } from "@/shared/lib/format";
import { ArrowRight } from "lucide-react";
import { useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
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
