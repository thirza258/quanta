import { lazy, Suspense, useEffect, useRef, useState } from "react";
import {
  Check,
  ChevronDown,
  Code2,
  Download,
  FlaskConical,
  LoaderCircle,
  Play,
  RotateCcw,
  Save,
  Settings2,
  Terminal,
  X,
} from "lucide-react";
import { api, decimal, download, money, percent, post } from "../lib/api";
import { useWorkspace } from "../lib/workspace";
import { defaultCode, defaultConfig } from "../lib/types";
import type { Config, Result } from "../lib/types";
import { Loading, Modal } from "./ui";
const CodeEditor = lazy(() => import("./CodeEditor"));
const FinancialChart = lazy(() => import("./FinancialChart"));
const scenarios = [
  ["custom", "Custom market"],
  ["pure_random_walk", "Pure random walk"],
  ["1929_crash", "Deflationary crash · 1929-inspired"],
  ["1970s_stagflation", "Stagflation · 1970s-inspired"],
  ["2008_liquidity_crisis", "Liquidity crisis · 2008-inspired"],
  ["flash_crash", "Crypto flash crash · −50%"],
];
export default function Sandbox({
  lessonId,
  initialCode = defaultCode,
  initialConfig = defaultConfig,
  experimentId,
  onExpand,
  expanded = false,
}: {
  lessonId?: string;
  initialCode?: string;
  initialConfig?: Config;
  experimentId?: string;
  onExpand?: () => void;
  expanded?: boolean;
}) {
  const { state, update } = useWorkspace(),
    draftKey = experimentId || lessonId || "free-lab";
  const [code, setCode] = useState(state.drafts[draftKey] ?? initialCode),
    [config, setConfig] = useState<Config>(() =>
      structuredClone(initialConfig),
    ),
    [result, setResult] = useState<Result | null>(null),
    [busy, setBusy] = useState(false),
    [error, setError] = useState(""),
    [mode, setMode] = useState<"code" | "parameters">("code"),
    [tab, setTab] = useState("equity"),
    [settings, setSettings] = useState(false),
    [saveOpen, setSaveOpen] = useState(false),
    [title, setTitle] = useState(""),
    [saved, setSaved] = useState(false),
    [history, setHistory] = useState<{ symbol: string }[]>([]),
    [catalogError, setCatalogError] = useState(""),
    [resultsStale, setResultsStale] = useState(false);
  const runRef = useRef<() => void>(() => {}),
    lock = useRef(false),
    mounted = useRef(true),
    resultInput = useRef<{ code: string; config: Config } | null>(null),
    inputVersion = useRef(0);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  useEffect(() => {
    api<{ datasets: { symbol: string }[] }>("/data/catalog")
      .then((d) => setHistory(d.datasets))
      .catch((e) => setCatalogError(e.message));
  }, []);
  const changeCode = (value: string) => {
    inputVersion.current++;
    setCode(value);
    setSaved(false);
    setResultsStale(!!result);
    update((s) => ({ ...s, drafts: { ...s.drafts, [draftKey]: value } }));
  };
  const changeConfig = (next: Config) => {
    inputVersion.current++;
    setConfig(next);
    setResultsStale(!!result);
    setSaved(false);
  };
  const param = (key: string, value: string | number) =>
    changeConfig({
      ...config,
      dataset_params: { ...config.dataset_params, [key]: value },
    });
  const run = async () => {
    if (lock.current) return;
    lock.current = true;
    setBusy(true);
    setError("");
    setSaved(false);
    const input = { code, config: structuredClone(config) },
      runVersion = inputVersion.current;
    try {
      const output = await post<Result>("/sandbox/execute", {
        code,
        ...config,
      });
      if (mounted.current) {
        setResult(output);
        resultInput.current = input;
        setResultsStale(inputVersion.current !== runVersion);
        setTab(output.stdout.trim() ? "console" : "equity");
      }
      update((s) => ({ ...s, runs: s.runs + 1 }));
    } catch (err) {
      if (mounted.current) setError((err as Error).message);
    } finally {
      lock.current = false;
      if (mounted.current) setBusy(false);
    }
  };
  runRef.current = () => void run();
  const save = () => {
    const id = experimentId || crypto.randomUUID(),
      input =
        resultInput.current && !resultsStale
          ? resultInput.current
          : { code, config };
    const exp = {
      id,
      title: title.trim() || `Experiment ${state.experiments.length + 1}`,
      code: input.code,
      config: structuredClone(input.config),
      metrics: result && !resultsStale ? result.metrics : undefined,
      updatedAt: new Date().toISOString(),
      lessonId,
    };
    update((s) => ({
      ...s,
      experiments: [exp, ...s.experiments.filter((e) => e.id !== id)],
    }));
    setSaveOpen(false);
    setSaved(true);
  };
  return (
    <section
      className={`sandbox ${expanded ? "expanded" : ""}`}
      aria-label="Interactive Python sandbox"
    >
      <div className="sandbox-header">
        <div>
          <span className="sandbox-icon">
            <FlaskConical size={16} />
          </span>
          <strong>Quanta sandbox</strong>
          <span className="sandbox-label">PYTHON</span>
        </div>
        <div>
          <button
            className="icon-button"
            aria-label="Execution settings"
            onClick={() => setSettings(!settings)}
          >
            <Settings2 size={16} />
          </button>
          {onExpand ? (
            <button
              className="icon-button"
              aria-label={expanded ? "Restore split view" : "Expand sandbox"}
              onClick={onExpand}
            >
              {expanded ? <X size={16} /> : <Code2 size={16} />}
            </button>
          ) : null}
        </div>
      </div>
      <div className="sandbox-config">
        <label>
          DATA SOURCE
          <select
            aria-label="Data source"
            value={config.dataset_type}
            onChange={(e) =>
              changeConfig({
                ...config,
                dataset_type: e.target.value as Config["dataset_type"],
              })
            }
          >
            <option value="synthetic">Synthetic market</option>
            <option value="real">Historical data</option>
          </select>
        </label>
        {config.dataset_type === "synthetic" ? (
          <label>
            SCENARIO
            <select
              aria-label="Market scenario"
              value={config.dataset_params.scenario}
              onChange={(e) => param("scenario", e.target.value)}
            >
              {scenarios.map(([v, t]) => (
                <option value={v} key={v}>
                  {t}
                </option>
              ))}
            </select>
          </label>
        ) : (
          <label>
            DATASET
            <select
              aria-label="Historical dataset"
              value={config.dataset_params.symbol || ""}
              onChange={(e) => param("symbol", e.target.value)}
            >
              <option value="">Select imported dataset</option>
              {history.map((d) => (
                <option value={d.symbol} key={d.symbol}>
                  {d.symbol}
                </option>
              ))}
            </select>
          </label>
        )}
      </div>
      {config.dataset_type === "real" && !history.length ? (
        <div className="inline-notice">
          {catalogError ||
            "No historical dataset is installed. Import an OHLCV CSV using the instructions in How Quanta works, or choose a synthetic market."}
        </div>
      ) : null}
      {settings ? (
        <div className="execution-settings">
          <label className="field">
            Starting capital ($)
            <input
              type="number"
              min="100"
              max="1000000000"
              value={config.capital}
              onChange={(e) =>
                changeConfig({ ...config, capital: Number(e.target.value) })
              }
            />
          </label>
          <label className="field">
            Commission (bps)
            <input
              type="number"
              min="0"
              max="500"
              value={config.commission_bps}
              onChange={(e) =>
                changeConfig({
                  ...config,
                  commission_bps: Number(e.target.value),
                })
              }
            />
          </label>
          <label className="field">
            Slippage (bps)
            <input
              type="number"
              min="0"
              max="500"
              value={config.slippage_bps}
              onChange={(e) =>
                changeConfig({
                  ...config,
                  slippage_bps: Number(e.target.value),
                })
              }
            />
          </label>
          <label className="field">
            Seed
            <input
              type="number"
              min="0"
              max="4294967295"
              value={config.dataset_params.seed}
              onChange={(e) => param("seed", Number(e.target.value))}
            />
          </label>
        </div>
      ) : null}
      <div className="editor-tabs">
        <div className="tabs">
          <button
            className={mode === "code" ? "active" : ""}
            onClick={() => setMode("code")}
          >
            <Code2 size={14} />
            strategy.py
          </button>
          <button
            className={mode === "parameters" ? "active" : ""}
            onClick={() => setMode("parameters")}
          >
            <Settings2 size={14} />
            Parameters
          </button>
        </div>
        <button
          className="icon-button"
          aria-label="Restore lesson code"
          title="Restore lesson code"
          onClick={() => changeCode(initialCode)}
        >
          <RotateCcw size={14} />
        </button>
      </div>
      {mode === "code" ? (
        <Suspense fallback={<Loading label="Loading Python editor…" />}>
          <CodeEditor
            code={code}
            onChange={changeCode}
            onRun={() => runRef.current()}
          />
        </Suspense>
      ) : (
        <div className="parameter-panel">
          <div className="parameter-top">
            <label className="field">
              Stochastic process
              <select
                aria-label="Stochastic process"
                value={config.dataset_params.model}
                onChange={(e) => param("model", e.target.value)}
              >
                <option value="gbm">Geometric Brownian motion</option>
                <option value="merton">Merton jump-diffusion</option>
                <option value="heston">Heston stochastic volatility</option>
                <option value="regime">Markov regime switching</option>
              </select>
            </label>
            <label className="field">
              Horizon
              <select
                aria-label="Simulation horizon"
                value={config.dataset_params.years}
                onChange={(e) => param("years", Number(e.target.value))}
              >
                {[1, 3, 5, 10, 20, 30].map((y) => (
                  <option key={y} value={y}>
                    {y} {y === 1 ? "year" : "years"}
                  </option>
                ))}
              </select>
            </label>
          </div>
          {[
            ["mu", "Annual drift", -0.3, 0.4, 0.01, "%"],
            ["sigma", "Annual volatility", 0.01, 0.8, 0.01, "%"],
            ["window", "Moving-average window", 2, 252, 1, " days"],
            ...(config.dataset_params.model === "merton"
              ? [["jump_frequency", "Jumps per year", 0, 20, 0.5, ""]]
              : []),
          ].map(([key, label, min, max, step, unit]) => (
            <label className="slider-field" key={key}>
              <span>
                {label}
                <strong>
                  {unit === "%"
                    ? percent(config.dataset_params[key as "mu"], 0)
                    : `${config.dataset_params[key as "window"]}${unit}`}
                </strong>
              </span>
              <input
                type="range"
                min={min}
                max={max}
                step={step}
                value={config.dataset_params[key as "mu"]}
                onChange={(e) => param(String(key), Number(e.target.value))}
              />
            </label>
          ))}
          {config.dataset_params.model === "heston" ? (
            <div className="heston-fields">
              {[
                ["kappa", "Mean reversion κ", 0.1, 20],
                ["theta", "Long-run variance θ", 0.001, 2],
                ["xi", "Vol of variance ξ", 0, 2],
                ["rho", "Correlation ρ", -1, 1],
              ].map(([key, label, min, max]) => (
                <label className="field" key={key}>
                  {label}
                  <input
                    type="number"
                    step="0.01"
                    min={min}
                    max={max}
                    value={config.dataset_params[key as "kappa"]}
                    onChange={(e) => param(String(key), Number(e.target.value))}
                  />
                </label>
              ))}
            </div>
          ) : null}
          <div className="strategy-presets">
            <span>QUICK STRATEGY</span>
            {[
              ["Trend following", ">"],
              ["Mean reversion", "<"],
              ["Buy & hold", "hold"],
            ].map(([label, op]) => (
              <button
                key={label}
                className="chip"
                onClick={() =>
                  changeCode(
                    op === "hold"
                      ? "def strategy(data):\n    return True\n"
                      : defaultCode.replace(" > ", ` ${op} `),
                  )
                }
              >
                {label}
              </button>
            ))}
          </div>
          <p className="fine-print">
            Named stress scenarios override selected process defaults. The
            window controls the template’s sma_50 series; other indicators
            remain unchanged.
          </p>
        </div>
      )}
      <div className="run-bar">
        <span>
          <span className="green-dot" />
          Guided Python<span className="dot-separator">·</span>2s limit
        </span>
        <button
          className="button primary small"
          onClick={() => void run()}
          disabled={busy || !code.trim()}
        >
          {busy ? (
            <LoaderCircle className="spin" size={14} />
          ) : (
            <Play size={13} fill="currentColor" />
          )}
          {busy ? "Running…" : "Run experiment"}
          <kbd>⌘ ↵</kbd>
        </button>
      </div>
      {error ? (
        <div className="error-message execution-error" role="alert">
          <Terminal size={16} />
          <span>{error}</span>
        </div>
      ) : null}
      <div className="output-header">
        <span className="eyebrow">EXPERIMENT OUTPUT</span>
        {result ? (
          <span className="run-timing">
            <Check size={12} />
            {result.execution_ms} ms{resultsStale ? " · inputs changed" : ""}
          </span>
        ) : (
          <span className="muted">Ready when you are</span>
        )}
      </div>
      {result ? (
        <>
          <div className="metrics-grid">
            {[
              ["CAGR", percent(result.metrics.cagr)],
              ["SHARPE", decimal(result.metrics.sharpe)],
              ["MAX DRAWDOWN", percent(result.metrics.max_drawdown)],
              ["WIN RATE", percent(result.metrics.win_rate)],
            ].map(([label, value]) => (
              <div key={label}>
                <span>{label}</span>
                <strong
                  className={
                    label === "MAX DRAWDOWN"
                      ? "negative"
                      : label === "CAGR" && result.metrics.cagr > 0
                        ? "positive"
                        : ""
                  }
                >
                  {value}
                </strong>
              </div>
            ))}
          </div>
          <div className="output-tabs tabs">
            {[
              ["equity", "Equity curve"],
              ["drawdown", "Drawdown"],
              ["candles", "Market"],
              ["returns", "Returns"],
              ["trades", "Trades"],
              ["console", "Console"],
              ["metrics", "All metrics"],
            ].map(([key, label]) => (
              <button
                key={key}
                className={tab === key ? "active" : ""}
                onClick={() => setTab(key)}
              >
                {label}
              </button>
            ))}
          </div>
          {["equity", "drawdown", "candles"].includes(tab) ? (
            <>
              <div className="chart-legend">
                <span>
                  <i />
                  {tab === "equity"
                    ? "Strategy"
                    : tab === "drawdown"
                      ? "Drawdown from peak"
                      : "OHLC prices"}
                </span>
                {tab === "equity" ? (
                  <span>
                    <i className="benchmark" />
                    Buy & hold
                  </span>
                ) : null}
                <small>
                  {result.dataset_type === "synthetic"
                    ? "SYNTHETIC DATA"
                    : "IMPORTED DATA"}
                </small>
              </div>
              <Suspense fallback={<Loading label="Drawing chart…" />}>
                <FinancialChart
                  result={result}
                  kind={tab as "equity" | "drawdown" | "candles"}
                />
              </Suspense>
            </>
          ) : null}
          {tab === "returns" ? (
            <div className="heatmap">
              <div className="heatmap-labels">
                <span>Year</span>
                {[
                  "J",
                  "F",
                  "M",
                  "A",
                  "M",
                  "J",
                  "J",
                  "A",
                  "S",
                  "O",
                  "N",
                  "D",
                ].map((m, i) => (
                  <span key={i}>{m}</span>
                ))}
              </div>
              {[
                ...new Set(
                  result.monthly_returns.map((r) => r.month.slice(0, 4)),
                ),
              ].map((year) => (
                <div className="heatmap-row" key={year}>
                  <span>{year}</span>
                  {Array.from({ length: 12 }, (_, i) => {
                    const cell = result.monthly_returns.find(
                      (r) =>
                        r.month === `${year}-${String(i + 1).padStart(2, "0")}`,
                    );
                    return (
                      <span
                        key={i}
                        title={
                          cell
                            ? `${cell.month}: ${percent(cell.return, 2)}`
                            : "No observation"
                        }
                        style={
                          cell
                            ? {
                                background:
                                  cell.return >= 0 ? "#4d886b" : "#b96d75",
                                opacity:
                                  0.35 +
                                  Math.min(0.65, Math.abs(cell.return) * 8),
                                color: "#fff",
                              }
                            : {}
                        }
                      >
                        {cell ? percent(cell.return, 0) : "—"}
                      </span>
                    );
                  })}
                </div>
              ))}
            </div>
          ) : null}
          {tab === "trades" ? (
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Side</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Fee</th>
                    <th>P&L</th>
                  </tr>
                </thead>
                <tbody>
                  {result.trades.map((t, i) => (
                    <tr key={i}>
                      <td>{t.time}</td>
                      <td
                        className={t.side === "BUY" ? "positive" : "negative"}
                      >
                        {t.side}
                      </td>
                      <td>{t.quantity.toFixed(2)}</td>
                      <td>{money(t.price)}</td>
                      <td>{money(t.commission)}</td>
                      <td>{t.pnl === null ? "—" : money(t.pnl)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {!result.trades.length ? (
                <p className="fine-print">
                  No signals generated a trade during this experiment.
                </p>
              ) : null}
            </div>
          ) : null}
          {tab === "console" ? (
            <pre className="console-output">
              {result.stdout ||
                "Strategy executed successfully. No print output.\n"}
              <span className="console-summary">
                {"\n"}
                {result.bars.length} bars · {result.trades.length} fills · final
                equity {money(result.metrics.final_equity)}
                {"\n"}Signals execute at the next open. Open positions are
                marked to the last close.
              </span>
            </pre>
          ) : null}
          {tab === "metrics" ? (
            <div className="all-metrics">
              {Object.entries(result.metrics).map(([key, value]) => (
                <div key={key}>
                  <span>{key.replaceAll("_", " ")}</span>
                  <strong>
                    {value == null
                      ? "Undefined"
                      : typeof value === "number"
                        ? decimal(value, 4)
                        : value}
                  </strong>
                </div>
              ))}
              <p className="fine-print">
                Returns, drawdowns and probabilities use decimal units. Ratios
                use 252 sessions/year and a 3% annual risk-free rate. Win rate
                and profit factor use closed round trips; undefined ratios are
                not zero.
              </p>
            </div>
          ) : null}
        </>
      ) : (
        <div className="output-empty">
          <span className="empty-chart">
            <svg viewBox="0 0 200 50" aria-hidden="true">
              <path d="M0 45 15 40 25 43 39 30 49 33 61 26 73 32 88 17 100 22 112 14 124 22 138 10 154 15 167 6 180 10 200 0" />
            </svg>
          </span>
          <h4>A hypothesis is a good start.</h4>
          <p>Run your first experiment to see the evidence.</p>
        </div>
      )}
      <div className="sandbox-footer">
        <span>
          {resultsStale
            ? "Output belongs to the previous run."
            : "Reproducible by design."}
        </span>
        <div>
          <button
            className="text-link"
            onClick={() => {
              setTitle(
                state.experiments.find((e) => e.id === experimentId)?.title ||
                  "",
              );
              setSaveOpen(true);
            }}
          >
            {saved ? <Check size={14} /> : <Save size={14} />}Save
          </button>
          <button
            className="icon-button"
            aria-label="Export experiment"
            onClick={() =>
              download("quanta-experiment.json", {
                code,
                config,
                result: !resultsStale ? result : null,
              })
            }
          >
            <Download size={15} />
          </button>
        </div>
      </div>
      <details className="runtime-notes">
        <summary>
          Runtime & data notes
          <ChevronDown size={12} />
        </summary>
        <p>
          Guided Python supports functions, arithmetic, bounded loops, data
          series, and selected math/NumPy functions. Arbitrary imports and OS
          access are unavailable. A Docker runtime can enable scientific Python.
          Synthetic scenarios illustrate stress mechanisms and do not recreate
          historical events.
        </p>
      </details>
      <Modal
        open={saveOpen}
        onOpenChange={setSaveOpen}
        title="Keep this experiment"
        description="Save the code and exact market parameters so you can return to the same question."
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            save();
          }}
        >
          <label className="field">
            Experiment name
            <input
              autoFocus
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="My first market hypothesis"
              required
              maxLength={120}
            />
          </label>
          <button className="button primary full-width">
            Save experiment
            <Save size={16} />
          </button>
        </form>
      </Modal>
    </section>
  );
}
