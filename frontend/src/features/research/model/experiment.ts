// Pure helpers for the experiment result page (/research/:experimentId).
// No DOM access: everything here is unit-tested in node.
import type {
  CheckStatus,
  CostStress,
  ExperimentDetail,
  ExperimentSpec,
  GridParameter,
  LifecycleStatus,
  MetricSet,
  Notebook,
  Params,
  Provenance,
  QualityComponent,
  RedTeamCheck,
  RiskLevel,
  RunDetail,
  RunStatus,
  RunSummary,
  Skipped,
  Stability,
  Surface,
} from "@/features/research/model/registry";
import { decimal, percent } from "@/shared/lib/format";

export const NOTEBOOK_LIMIT = 8000;

export const SECTIONS = [
  { id: "overview", label: "Overview" },
  { id: "validation", label: "Validation" },
  { id: "robustness", label: "Robustness" },
  { id: "red-team", label: "Red team" },
  { id: "notebook", label: "Notebook" },
  { id: "provenance", label: "Provenance" },
] as const;
export type SectionId = (typeof SECTIONS)[number]["id"];

/** Visual tone of a status; always rendered with an icon and a text label. */
export type Tone = "pass" | "warn" | "fail" | "neutral" | "active";

export function isSkipped(value: { status: string }): value is Skipped {
  return value.status === "skipped" || value.status === "undefined";
}

export function hasProvenance(
  value: RunDetail["provenance"] | null | undefined,
): value is Provenance {
  return (
    !!value && typeof (value as Partial<Provenance>).result_sha256 === "string"
  );
}

const ACTIVE: RunStatus[] = ["queued", "running"];
export const isRunActive = (status: RunStatus | null | undefined) =>
  !!status && ACTIVE.includes(status);

// ---------------------------------------------------------------- numbers

/** Trim float noise from grid values: 0.30000000000000004 -> "0.3". */
export function formatNumber(value: number | null | undefined): string {
  if (value == null || !Number.isFinite(value)) return "—";
  if (Number.isInteger(value)) return String(value);
  return String(Number(value.toPrecision(6)));
}

export const formatCount = (value: number | null | undefined) =>
  value == null || !Number.isFinite(value)
    ? "—"
    : new Intl.NumberFormat("en-US").format(value);

export function formatBps(value: number | null | undefined): string {
  if (value == null || !Number.isFinite(value)) return "—";
  return `${formatNumber(Math.round(value * 100) / 100)} bps`;
}

export const formatTimes = (value: number | null | undefined, digits = 2) =>
  value == null || !Number.isFinite(value) ? "—" : `${value.toFixed(digits)}×`;

export function formatPValue(value: number | null | undefined): string {
  if (value == null || !Number.isFinite(value)) return "—";
  return value < 0.001 ? "< 0.001" : value.toFixed(3);
}

/** Compact money for axis ticks: $10K, $1.2M. */
export function compactMoney(value: number | null | undefined): string {
  if (value == null || !Number.isFinite(value)) return "—";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}

export type MetricFormat = "percent" | "ratio" | "times" | "count";

export function formatMetric(
  value: number | null | undefined,
  format: MetricFormat,
): string {
  if (value == null || !Number.isFinite(value)) return "—";
  switch (format) {
    case "percent":
      return percent(value, 1);
    case "ratio":
      return decimal(value, 2);
    case "times":
      return formatTimes(value, 2);
    case "count":
      return formatCount(value);
  }
}

export const BENCHMARK_METRICS: {
  key: Exclude<keyof MetricSet, "final_equity">;
  label: string;
  format: MetricFormat;
}[] = [
  { key: "cagr", label: "CAGR", format: "percent" },
  { key: "total_return", label: "Total return", format: "percent" },
  { key: "sharpe", label: "Sharpe", format: "ratio" },
  { key: "sortino", label: "Sortino", format: "ratio" },
  { key: "max_drawdown", label: "Max drawdown", format: "percent" },
  { key: "calmar", label: "Calmar", format: "ratio" },
  { key: "volatility", label: "Volatility", format: "percent" },
  { key: "turnover", label: "Turnover", format: "times" },
  { key: "win_rate", label: "Win rate", format: "percent" },
  { key: "profit_factor", label: "Profit factor", format: "ratio" },
  { key: "exposure", label: "Exposure", format: "percent" },
  { key: "trades", label: "Trades", format: "count" },
];

/** Decay is 1 − OOS/IS (a share of the in-sample Sharpe that was lost). */
export function formatDecay(decay: number | null | undefined): string {
  if (decay == null || !Number.isFinite(decay)) return "—";
  if (decay < 0) return `${percent(-decay, 0)} better out of sample`;
  return `${percent(decay, 0)} lost`;
}

// ------------------------------------------------------------------ dates

const DAY = /^\d{4}-\d{2}-\d{2}$/;

function parseDate(value: string): Date | null {
  const date = new Date(DAY.test(value) ? `${value}T00:00:00Z` : value);
  return Number.isNaN(date.getTime()) ? null : date;
}

/** A bar date ("2019-01-02" or an ISO timestamp) as "Jan 2, 2019", in UTC. */
export function formatDay(value: string | null | undefined): string {
  if (!value) return "—";
  const date = parseDate(value);
  if (!date) return value;
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  }).format(date);
}

/** Axis tick for a bar date: "Jan 2019". */
export function formatMonth(value: string | null | undefined): string {
  if (!value) return "";
  const date = parseDate(value);
  if (!date) return value;
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  }).format(date);
}

/** A server timestamp in the reader's time zone: "Nov 9, 2026, 2:03 PM". */
export function formatTimestamp(value: string | null | undefined): string {
  if (!value) return "—";
  const date = parseDate(value);
  if (!date) return value;
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(date);
}

export const formatSpan = (span: {
  start: string;
  end: string;
  bars: number;
}) =>
  `${formatDay(span.start)} – ${formatDay(span.end)} · ${formatCount(span.bars)} bars`;

/** Elapsed wall time: "42s", "3m 05s", "1h 02m". */
export function formatElapsed(ms: number | null | undefined): string {
  if (ms == null || !Number.isFinite(ms) || ms < 0) return "—";
  const seconds = Math.floor(ms / 1000);
  if (seconds < 60) return `${seconds}s`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60)
    return `${minutes}m ${String(seconds % 60).padStart(2, "0")}s`;
  return `${Math.floor(minutes / 60)}h ${String(minutes % 60).padStart(2, "0")}m`;
}

/** A run duration: "820 ms", "4.2s", "3m 05s". */
export function formatDuration(ms: number | null | undefined): string {
  if (ms == null || !Number.isFinite(ms) || ms < 0) return "—";
  if (ms < 1000) return `${Math.round(ms)} ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  return formatElapsed(ms);
}

/** Milliseconds since a run started (or was queued), never negative. */
export function runElapsed(
  run: Pick<RunSummary, "started_at" | "created_at">,
  now: number,
): number | null {
  const start = parseDate(run.started_at ?? run.created_at);
  return start ? Math.max(0, now - start.getTime()) : null;
}

// --------------------------------------------------------------- statuses

export const LIFECYCLE_LABEL: Record<LifecycleStatus, string> = {
  CONFIGURED: "Configured",
  RUNNING: "Running",
  FAILED: "Failed",
  PASSED: "Passed",
  WARNINGS: "Warnings",
  DOCUMENTED: "Documented",
  REPRODUCIBLE: "Reproducible",
};

export const LIFECYCLE_TONE: Record<LifecycleStatus, Tone> = {
  CONFIGURED: "neutral",
  RUNNING: "active",
  FAILED: "fail",
  PASSED: "pass",
  WARNINGS: "warn",
  DOCUMENTED: "pass",
  REPRODUCIBLE: "pass",
};

export type StepState = "done" | "current" | "pending";

/** Lifecycle steps with the first unfinished one marked as current. */
export function lifecycleSteps(lifecycle: ExperimentDetail["lifecycle"]) {
  const open = lifecycle.steps.findIndex((step) => !step.done);
  return lifecycle.steps.map((step, index) => ({
    ...step,
    state: (step.done
      ? "done"
      : index === open
        ? "current"
        : "pending") as StepState,
  }));
}

export function riskTone(level: RiskLevel | null | undefined): Tone {
  return level === "LOW"
    ? "pass"
    : level === "MEDIUM"
      ? "warn"
      : level === "HIGH"
        ? "fail"
        : "neutral";
}

export const CHECK_STATUS: Record<CheckStatus, { label: string; tone: Tone }> =
  {
    pass: { label: "Passed", tone: "pass" },
    warn: { label: "Warning", tone: "warn" },
    fail: { label: "Failed", tone: "fail" },
    skip: { label: "Not applicable", tone: "neutral" },
  };

export const RUN_STATUS: Record<RunStatus, { label: string; tone: Tone }> = {
  queued: { label: "Queued", tone: "active" },
  running: { label: "Running", tone: "active" },
  completed: { label: "Completed", tone: "pass" },
  failed: { label: "Failed", tone: "fail" },
  interrupted: { label: "Interrupted", tone: "warn" },
};

export const STABILITY: Record<
  Stability["class"],
  { label: string; tone: Tone }
> = {
  robust: { label: "Robust", tone: "pass" },
  sensitive: { label: "Sensitive", tone: "warn" },
  fragile: { label: "Fragile", tone: "fail" },
  untested: { label: "Untested", tone: "neutral" },
  "no-edge": { label: "No edge", tone: "neutral" },
};

export const REPRODUCTION: Record<
  "identical" | "equivalent" | "different",
  { label: string; tone: Tone; text: string }
> = {
  identical: {
    label: "Identical",
    tone: "pass",
    text: "The rerun reproduced every output exactly.",
  },
  equivalent: {
    label: "Equivalent",
    tone: "pass",
    text: "The rerun matched within numerical tolerance.",
  },
  different: {
    label: "Different",
    tone: "fail",
    text: "The rerun did not match the original run.",
  },
};

const STAGES: Record<string, string> = {
  strategies: "Running the parameter grid",
  validation: "Validating out of sample",
  robustness: "Stress-testing robustness",
  diagnostics: "Measuring overfitting risk",
  "red team": "Red-teaming the result",
  completed: "Writing the results",
};

export function stageLabel(stage: string | null, status: RunStatus): string {
  if (status === "queued") return "Waiting in the queue";
  if (!stage) return "Starting the run";
  return STAGES[stage] ?? stage.charAt(0).toUpperCase() + stage.slice(1);
}

/** Share of the work done, or null when the total is unknown. */
export function progressFraction(progress: RunSummary["progress"]) {
  if (!progress.total || progress.total <= 0) return null;
  return Math.min(1, Math.max(0, progress.done / progress.total));
}

/** The most recent run, whatever order the API returns them in. */
export function latestRun(runs: RunSummary[]): RunSummary | null {
  return runs.reduce<RunSummary | null>(
    (latest, run) => (!latest || run.number > latest.number ? run : latest),
    null,
  );
}

export type RunNotice =
  | { kind: "never" }
  | { kind: "failed"; run: RunSummary }
  | { kind: "interrupted"; run: RunSummary }
  | null;

/** What to say about the latest attempt when it did not produce results. */
export function runNotice(runs: RunSummary[]): RunNotice {
  const latest = latestRun(runs);
  if (!latest) return { kind: "never" };
  if (latest.status === "failed") return { kind: "failed", run: latest };
  if (latest.status === "interrupted")
    return { kind: "interrupted", run: latest };
  return null;
}

export type ActionKind = "run" | "rerun" | "save" | "delete" | "export";
const GENERIC_ERROR = "The request could not be completed.";

/** A readable message for a failed action, by HTTP status. */
export function describeActionError(
  status: number,
  message: string,
  action: ActionKind,
): string {
  const detail = message && message !== GENERIC_ERROR ? message : "";
  const withDetail = (text: string) =>
    detail && detail !== text ? `${text} ${detail}` : text;
  const starting = action === "run" || action === "rerun";
  switch (status) {
    case 409:
      return (
        detail ||
        (starting
          ? "A run is already in progress for this experiment. Wait for it to finish."
          : "The experiment changed in the meantime. Reload the page and try again.")
      );
    case 429:
      return withDetail(
        starting
          ? "Too many runs were started recently. Wait a minute and try again."
          : "Too many requests. Wait a minute and try again.",
      );
    case 503:
      return withDetail(
        "The research runner is busy or unavailable. Try again shortly.",
      );
    case 404:
      return detail || "This experiment or run no longer exists.";
    default:
      return detail || message || GENERIC_ERROR;
  }
}

// ------------------------------------------------------------- parameters

/** "fast=20 · slow=50", in grid order when the grid is known. */
export function formatParams(params: Params, order?: string[]): string {
  const keys = order?.length
    ? [
        ...order.filter((key) => key in params),
        ...Object.keys(params).filter((key) => !order.includes(key)),
      ]
    : Object.keys(params);
  return keys.length
    ? keys.map((key) => `${key}=${formatNumber(params[key])}`).join(" · ")
    : "Single configuration";
}

export const configurationCount = (parameters: GridParameter[]) =>
  parameters.reduce((total, p) => total * Math.max(1, p.values.length), 1);

export type SurfacePoint = Surface["points"][number];

export type SurfaceCell = {
  value: number;
  point: SurfacePoint | null;
  base: boolean;
  best: boolean;
};

export type SurfaceSlice = {
  name: string;
  values: number[];
  selected: number;
};

export type SurfaceGrid =
  | { kind: "single"; point: SurfacePoint | null }
  | { kind: "line"; parameter: GridParameter; cells: SurfaceCell[] }
  | {
      kind: "grid";
      rows: GridParameter;
      columns: GridParameter;
      slices: SurfaceSlice[];
      cells: SurfaceCell[][];
    };

export const pointAt = (surface: Surface, index: number) =>
  surface.points.find((point) => point.index === index);

const same = (a: number | undefined, b: number) =>
  a !== undefined && Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(b));

/**
 * Lay the surface out for display. The first two parameters form the grid;
 * every further parameter is fixed by a slice selector, defaulting to the
 * base configuration's value so the base cell is visible. Points are placed
 * by their parameter values, never by their position in the list.
 */
export function surfaceGrid(
  surface: Surface,
  selection: Record<string, number> = {},
): SurfaceGrid {
  const parameters = surface.parameters;
  const base = pointAt(surface, surface.base);
  const find = (fixed: [string, number][]) =>
    surface.points.find((point) =>
      fixed.every(([name, value]) => same(point.params[name], value)),
    ) ?? null;
  const cell = (value: number, fixed: [string, number][]): SurfaceCell => {
    const point = find(fixed);
    return {
      value,
      point,
      base: !!point && point.index === surface.base,
      best: !!point && point.index === surface.best,
    };
  };
  if (!parameters.length)
    return { kind: "single", point: base ?? surface.points[0] ?? null };
  if (parameters.length === 1) {
    const [parameter] = parameters;
    return {
      kind: "line",
      parameter,
      cells: parameter.values.map((value) =>
        cell(value, [[parameter.name, value]]),
      ),
    };
  }
  const [rows, columns, ...rest] = parameters;
  const slices = rest.map((parameter) => {
    const wanted = selection[parameter.name] ?? base?.params[parameter.name];
    const selected =
      parameter.values.find((value) => same(wanted, value)) ??
      parameter.values[0];
    return { name: parameter.name, values: parameter.values, selected };
  });
  const fixed: [string, number][] = slices.map((s) => [s.name, s.selected]);
  return {
    kind: "grid",
    rows,
    columns,
    slices,
    cells: rows.values.map((row) =>
      columns.values.map((column) =>
        cell(column, [[rows.name, row], [columns.name, column], ...fixed]),
      ),
    ),
  };
}

export const DIVERGING_STEPS = 4;
const MIN_EXTENT = 0.5;

/** Symmetric colour extent for Sharpe: the largest |value|, at least 0.5. */
export function sharpeExtent(values: (number | null | undefined)[]): number {
  const defined = values.filter(
    (v): v is number => v != null && Number.isFinite(v),
  );
  const largest = defined.reduce((max, v) => Math.max(max, Math.abs(v)), 0);
  return Math.max(MIN_EXTENT, largest);
}

/**
 * Diverging bin for a value: 0 is the neutral midpoint, ±1..±steps grow with
 * |value| / extent. Null for an undefined value.
 */
export function divergingBin(
  value: number | null | undefined,
  extent: number,
  steps = DIVERGING_STEPS,
): number | null {
  if (value == null || !Number.isFinite(value)) return null;
  if (Math.abs(value) < 0.005 || extent <= 0) return 0;
  const share = Math.min(1, Math.abs(value) / extent);
  const step = Math.max(1, Math.ceil(share * steps - 1e-9));
  return value > 0 ? step : -step;
}

export const binClass = (bin: number | null) =>
  bin == null
    ? "xd-bin-na"
    : bin === 0
      ? "xd-bin-0"
      : `xd-bin-${bin > 0 ? "p" : "n"}${Math.abs(bin)}`;

// -------------------------------------------------------- cost & scales

export type BreakEven =
  | { kind: "value"; bps: number; inRange: boolean; margin: number | null }
  | { kind: "above"; bps: number; reason: string | null }
  | { kind: "none"; reason: string };

export function breakEven(costs: CostStress): BreakEven {
  const top = costs.levels.reduce((max, l) => Math.max(max, l.cost_bps), 0);
  if (costs.break_even_bps != null)
    return {
      kind: "value",
      bps: costs.break_even_bps,
      inRange: costs.break_even_bps <= top,
      margin: costs.margin ?? null,
    };
  if (costs.break_even_above != null)
    return {
      kind: "above",
      bps: costs.break_even_above,
      reason: costs.reason ?? null,
    };
  return {
    kind: "none",
    reason: costs.reason ?? "The break-even cost could not be determined.",
  };
}

/** A padded [min, max] covering the values (and zero, when asked). */
export function extent(
  values: (number | null | undefined)[],
  includeZero = true,
): [number, number] {
  const defined = values.filter(
    (v): v is number => v != null && Number.isFinite(v),
  );
  if (includeZero) defined.push(0);
  if (!defined.length) return [0, 1];
  let low = Math.min(...defined),
    high = Math.max(...defined);
  if (low === high) {
    low -= 0.5;
    high += 0.5;
  }
  const pad = (high - low) * 0.08;
  return [low - pad, high + pad];
}

/** Position of a value in a domain, as a 0–100 percentage (clamped). */
export function position(value: number, [low, high]: [number, number]) {
  if (high === low) return 50;
  return Math.min(100, Math.max(0, ((value - low) / (high - low)) * 100));
}

/** Round tick values inside a domain (about `count` of them). */
function niceStep(raw: number): number {
  const power = 10 ** Math.floor(Math.log10(raw));
  return (
    [1, 2, 2.5, 5, 10].map((m) => m * power).find((s) => s >= raw - 1e-12) ??
    10 * power
  );
}

const round = (value: number) => Number(value.toFixed(10)) + 0;

export function niceTicks([low, high]: [number, number], count = 5): number[] {
  if (!(high > low)) return [low];
  const step = niceStep((high - low) / Math.max(1, count));
  const ticks: number[] = [];
  for (let t = Math.ceil(low / step - 1e-9) * step; t <= high + 1e-9; t += step)
    ticks.push(round(t));
  return ticks;
}

/**
 * A domain snapped outward to round steps, with its ticks, for a value axis
 * (zero included unless asked otherwise).
 */
export function niceScale(
  values: (number | null | undefined)[],
  count = 5,
  includeZero = true,
): { domain: [number, number]; ticks: number[] } {
  const defined = values.filter(
    (v): v is number => v != null && Number.isFinite(v),
  );
  if (includeZero) defined.push(0);
  if (!defined.length) return { domain: [0, 1], ticks: [0, 1] };
  let low = Math.min(...defined),
    high = Math.max(...defined);
  if (low === high) {
    low -= 0.5;
    high += 0.5;
  }
  const step = niceStep((high - low) / Math.max(1, count));
  const start = Math.floor(low / step + 1e-9) * step;
  const end = Math.ceil(high / step - 1e-9) * step;
  const ticks: number[] = [];
  for (let t = start; t <= end + step * 1e-6; t += step) ticks.push(round(t));
  return { domain: [ticks[0], ticks[ticks.length - 1]], ticks };
}

/** Keep at most `max` items, evenly spaced, always including the last. */
export function downsample<T>(items: T[], max: number): T[] {
  if (items.length <= max || max < 2) return items;
  const step = (items.length - 1) / (max - 1);
  return Array.from({ length: max }, (_, i) => items[Math.round(i * step)]);
}

// --------------------------------------------------------------- notebook

export function normalizeNotebook(notebook: Notebook | null | undefined) {
  return {
    conclusion: notebook?.conclusion ?? "",
    limitations: notebook?.limitations ?? "",
    decision: notebook?.decision ?? "",
  } satisfies Required<Notebook>;
}

export function notebookDirty(saved: Notebook, draft: Notebook): boolean {
  const a = normalizeNotebook(saved),
    b = normalizeNotebook(draft);
  return (
    a.conclusion !== b.conclusion ||
    a.limitations !== b.limitations ||
    a.decision !== b.decision
  );
}

export type SuggestedLimitation = {
  id: string;
  title: string;
  status: CheckStatus;
  severity: RedTeamCheck["severity"];
  text: string;
};

/** Warn/fail red-team findings, failures and high severity first. */
export function suggestedLimitations(
  checks: RedTeamCheck[],
): SuggestedLimitation[] {
  const rank = (c: RedTeamCheck) =>
    c.status === "fail" ? 0 : c.severity === "high" ? 1 : 2;
  return checks
    .filter((c) => c.status === "warn" || c.status === "fail")
    .sort((a, b) => rank(a) - rank(b))
    .map((c) => ({
      id: c.id,
      title: c.title,
      status: c.status,
      severity: c.severity,
      text: `${c.title}: ${c.finding}`,
    }));
}

/** Append a limitation as a bullet unless it is already written down. */
export function appendLimitation(current: string, text: string): string {
  if (current.includes(text)) return current;
  const line = `- ${text}`;
  return current.trim() ? `${current.replace(/\s+$/, "")}\n${line}` : line;
}

const MODELS: Record<string, string> = {
  gbm: "geometric Brownian motion",
  merton: "Merton jump-diffusion",
  heston: "Heston stochastic volatility",
  regime: "Markov regime-switching",
};

const SCENARIOS: Record<string, string> = {
  pure_random_walk: "pure random walk",
  "1929_crash": "deflationary crash (1929-inspired)",
  "1970s_stagflation": "stagflation (1970s-inspired)",
  "2008_liquidity_crisis": "liquidity crisis (2008-inspired)",
  flash_crash: "flash crash (−50%)",
};

/** A plain-language method section generated from the specification. */
export function methodSummary(
  spec: ExperimentSpec,
  datasetLabel?: string | null,
): { label: string; text: string }[] {
  const { dataset, strategy, costs, validation } = spec;
  const p = dataset.params;
  const synthetic = dataset.kind === "synthetic";
  const scenario =
    synthetic && p.scenario && p.scenario !== "custom"
      ? `, ${SCENARIOS[p.scenario] ?? p.scenario.replaceAll("_", " ")} scenario`
      : "";
  const data = synthetic
    ? `Synthetic ${MODELS[p.model] ?? p.model} market, ${formatNumber(p.years)} ${p.years === 1 ? "year" : "years"}, seed ${p.seed}${scenario}.`
    : `Historical ${p.symbol ?? "dataset"}${datasetLabel ? ` (${datasetLabel})` : ""}.`;
  const count = configurationCount(strategy.parameters);
  const grid = strategy.parameters.length
    ? `${strategy.parameters
        .map((g) => `${g.name} ∈ {${g.values.map(formatNumber).join(", ")}}`)
        .join(
          " × ",
        )} — ${count} ${count === 1 ? "configuration" : "configurations"}; base ${formatParams(
        strategy.base,
        strategy.parameters.map((g) => g.name),
      )}.`
    : "One configuration, no parameter grid.";
  const total = costs.commission_bps + costs.slippage_bps;
  const walk = validation.walk_forward
    ? `${validation.anchored ? "Anchored" : "Rolling"} walk-forward with ${formatCount(validation.train_bars)} training and ${formatCount(validation.test_bars)} test bars per fold.`
    : "Walk-forward analysis switched off.";
  const paths = !synthetic
    ? "Alternative paths do not apply to historical data."
    : validation.seed_paths > 0
      ? `${validation.seed_paths} alternative synthetic paths.`
      : "Alternative synthetic paths switched off.";
  return [
    { label: "Dataset", text: data },
    { label: "Strategy", text: `${strategy.name}: ${grid}` },
    {
      label: "Costs",
      text: `Commission ${formatNumber(costs.commission_bps)} bps + slippage ${formatNumber(costs.slippage_bps)} bps = ${formatNumber(total)} bps per fill, on ${new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(costs.capital)} starting capital.`,
    },
    {
      label: "Validation",
      text: `Chronological train/test split at ${percent(validation.split, 0)} in sample. ${walk} ${formatCount(validation.permutations)} random-timing permutations. ${paths}`,
    },
  ];
}

/** Quality components with each one's share of the total weight. */
export function qualityBreakdown(components: QualityComponent[]) {
  const total = components.reduce((sum, c) => sum + Math.max(0, c.weight), 0);
  return components.map((c) => {
    const share = total > 0 ? Math.max(0, c.weight) / total : 0;
    // Points (out of 100) this component adds to the overall score.
    return { ...c, share, points: share * c.score, maxPoints: share * 100 };
  });
}

// ------------------------------------------------------------- provenance

export function shortHash(hash: string | null | undefined, length = 12) {
  if (!hash) return "—";
  return hash.length <= length + 1 ? hash : `${hash.slice(0, length)}…`;
}

export function formatSeeds(seeds: Provenance["seeds"]): string {
  const entries = Object.entries(seeds);
  if (!entries.length) return "None";
  return entries
    .map(([key, value]) => {
      const text =
        value == null
          ? "none"
          : Array.isArray(value)
            ? value.length
              ? value.join(", ")
              : "none"
            : String(value);
      return `${key.replaceAll("_", " ")}: ${text}`;
    })
    .join(" · ");
}

export type FingerprintRow = {
  id: string;
  label: string;
  detail: string;
  hash?: string | null;
  hashLabel?: string;
};

export function fingerprintRows(p: Provenance): FingerprintRow[] {
  return [
    {
      id: "dataset",
      label: "Dataset",
      detail: `${p.dataset.key} · version ${p.dataset.version} · ${formatCount(p.dataset.bars)} bars (${formatDay(p.dataset.start)} – ${formatDay(p.dataset.end)})`,
      hash: p.dataset.sha256,
      hashLabel: "dataset SHA-256",
    },
    {
      id: "dataset-version",
      label: "Dataset version",
      detail: `${p.dataset.label} · ${p.dataset.source}`,
      hash: p.dataset.version_sha256,
      hashLabel: "dataset version SHA-256",
    },
    {
      id: "strategy",
      label: "Strategy",
      detail: `${p.strategy.name} · version ${p.strategy.version}`,
      hash: p.strategy.sha256,
      hashLabel: "strategy SHA-256",
    },
    {
      id: "config",
      label: "Configuration",
      detail: `${formatCount(p.configurations)} ${p.configurations === 1 ? "configuration" : "configurations"}`,
      hash: p.config_sha256,
      hashLabel: "configuration SHA-256",
    },
    {
      id: "engine",
      label: "Engine",
      detail: `${p.engine.name} ${p.engine.version}`,
      hash: p.engine.sha256,
      hashLabel: "engine SHA-256",
    },
    {
      id: "environment",
      label: "Environment",
      detail: `${p.environment.implementation} ${p.environment.python} · NumPy ${p.environment.numpy} · ${p.environment.platform}`,
      hash: p.environment.sha256,
      hashLabel: "environment SHA-256",
    },
    { id: "runtime", label: "Runtime", detail: p.runtime || "—" },
    { id: "quanta", label: "Quanta version", detail: p.quanta_version || "—" },
    {
      id: "git",
      label: "Git commit",
      detail: p.git_commit ? "" : "Not recorded",
      hash: p.git_commit,
      hashLabel: "git commit",
    },
    { id: "seeds", label: "Seeds", detail: formatSeeds(p.seeds) },
    {
      id: "result",
      label: "Result",
      detail: "Canonical results",
      hash: p.result_sha256,
      hashLabel: "result SHA-256",
    },
  ];
}
