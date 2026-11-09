// Contract for the research registry API (/api/v1/research). It mirrors the
// backend's services/experiments.py and domain/research/pipeline.py output.
import type { Params as DatasetParams } from "@/features/research/model/types";
import { api, ApiError, post } from "@/shared/api/client";

export type RiskLevel = "LOW" | "MEDIUM" | "HIGH";
export type LifecycleStatus =
  | "CONFIGURED"
  | "RUNNING"
  | "FAILED"
  | "PASSED"
  | "WARNINGS"
  | "DOCUMENTED"
  | "REPRODUCIBLE";
export type RunStatus =
  "queued" | "running" | "completed" | "failed" | "interrupted";
export type Decision = "trust" | "reject" | "inconclusive" | "";

export type GridParameter = { name: string; values: number[] };

export type ExperimentSpec = {
  dataset: { kind: "synthetic" | "historical"; params: DatasetParams };
  strategy: {
    name: string;
    code: string;
    parameters: GridParameter[];
    base: Record<string, number>;
  };
  costs: { capital: number; commission_bps: number; slippage_bps: number };
  validation: {
    split: number;
    walk_forward: boolean;
    train_bars: number;
    test_bars: number;
    anchored: boolean;
    permutations: number;
    seed_paths: number;
  };
};

export type StrategyTemplate = {
  id: string;
  label: string;
  description: string;
  code: string;
  parameters: GridParameter[];
  base: Record<string, number>;
};

export type ResearchOptions = {
  defaults: ExperimentSpec;
  limits: {
    parameters: number;
    values: number;
    configurations: number;
    code: number;
    title: number;
    hypothesis_min: number;
    hypothesis_max: number;
    notebook: number;
  };
  synthetic: {
    models: { id: string; label: string }[];
    scenarios: { id: string; label: string }[];
  };
  historical: {
    symbol: string;
    versions: { version: number; sha256: string; created_at: string }[];
  }[];
  indicators: { name: string; signature: string; description: string }[];
  templates: StrategyTemplate[];
};

export type MetricSet = {
  total_return: number | null;
  cagr: number | null;
  sharpe: number | null;
  sortino: number | null;
  max_drawdown: number | null;
  calmar: number | null;
  volatility: number | null;
  turnover: number | null;
  win_rate: number | null;
  profit_factor: number | null;
  exposure: number | null;
  trades: number | null;
  final_equity: number | null;
};

export type HeadlineMetrics = MetricSet & {
  alpha: number | null;
  beta: number | null;
  var_95: number | null;
  cvar_95: number | null;
  round_trips: number;
};

export type CurvePoint = {
  time: string;
  equity: number;
  benchmark: number;
  drawdown: number;
};

export type Span = { start: string; end: string; bars: number };
export type Skipped = { status: "skipped" | "undefined"; reason: string };
export type Params = Record<string, number>;

export type SplitArm = {
  index: number;
  params: Params;
  in_sample: MetricSet;
  out_of_sample: MetricSet;
  decay: number | null;
};

export type TrainTest =
  | Skipped
  | {
      status: "completed";
      split: number;
      in_sample: Span;
      out_of_sample: Span;
      base: SplitArm;
      selected: SplitArm;
    };

export type Fold = {
  fold: number;
  train: Span;
  test: Span;
  chosen: number;
  params: Params;
  in_sample_sharpe: number | null;
  out_of_sample_sharpe: number | null;
  out_of_sample_return: number | null;
  base_out_of_sample_sharpe: number | null;
  base_out_of_sample_return: number | null;
};

export type WalkForward =
  | Skipped
  | {
      status: "completed";
      mode: "rolling" | "anchored";
      train_bars: number;
      test_bars: number;
      folds: Fold[];
      out_of_sample: Span;
      aggregate: {
        mean_in_sample_sharpe: number | null;
        out_of_sample: MetricSet;
        base_out_of_sample: MetricSet;
        decay: number | null;
        positive_folds: number;
        distinct_choices: number;
      };
      equity_curve: CurvePoint[];
    };

export type Stability = {
  score: number | null;
  class: "robust" | "sensitive" | "fragile" | "untested" | "no-edge";
  neighbors: number;
  reason: string;
};

export type Surface = {
  configurations: number;
  parameters: GridParameter[];
  points: ({ index: number; params: Params } & MetricSet)[];
  base: number;
  best: number;
  median: number;
  worst: number;
  base_rank: number;
  positive_share: number;
  sharpe_distribution: {
    min: number | null;
    median: number | null;
    max: number | null;
    std: number | null;
  };
  influence: {
    name: string;
    values: number[];
    mean_sharpe: (number | null)[];
    spread: number;
  }[];
  stability: Stability;
  best_stability: Stability;
};

export type CostStress = {
  levels: {
    cost_bps: number;
    sharpe: number | null;
    cagr: number | null;
    total_return: number | null;
    final_equity: number | null;
  }[];
  current_bps: number;
  break_even_bps: number | null;
  break_even_above?: number;
  margin?: number | null;
  reason?: string;
};

export type SeedPath = {
  seed: number;
  strategy: MetricSet;
  benchmark: MetricSet;
};
export type SeedDispersion =
  | Skipped
  | {
      status: "completed";
      original: SeedPath;
      paths: SeedPath[];
      beats_benchmark_share: number;
      original_beats_benchmark: boolean;
      mean_sharpe: number | null;
      std_sharpe: number | null;
      positive_share: number;
      original_z: number | null;
    };

export type DeflatedSharpe =
  | Skipped
  | {
      status: "completed";
      dsr: number;
      psr: number;
      sharpe: number;
      expected_max_sharpe: number;
      trial_sharpe_std: number;
      trials: number;
      observations: number;
      skewness: number;
      kurtosis: number;
    };

export type Overfitting =
  | Skipped
  | {
      status: "completed";
      pbo: number;
      blocks: number;
      combinations: number;
      configurations: number;
      median_logit: number;
      oos_below_risk_free: number;
      in_sample_sharpe_median: number | null;
      out_of_sample_sharpe_median: number | null;
    };

export type RandomTiming =
  | Skipped
  | {
      status: "completed";
      p_value: number;
      permutations: number;
      seed: number;
      actual_sharpe: number;
      percentile: number;
      null_median: number | null;
      null_p05: number | null;
      null_p95: number | null;
    };

export type Concentration =
  | Skipped
  | {
      status: "completed";
      best_year: string;
      best_year_pnl: number;
      share: number;
      years: number;
      losing_years: number;
    };

export type CheckStatus = "pass" | "warn" | "fail" | "skip";
export type RedTeamCheck = {
  id: string;
  title: string;
  status: CheckStatus;
  severity: "medium" | "high" | null;
  finding: string;
  evidence: Record<string, unknown>;
  lesson: string | null;
};

export type RiskSummary = {
  level: RiskLevel;
  passed: number;
  warnings: number;
  high: number;
  failed: number;
  skipped: number;
};

export type Trade = {
  time: string;
  side: "BUY" | "SELL";
  price: number;
  quantity: number;
  commission: number;
  pnl: number | null;
};

export type Results = {
  valid: boolean;
  seeds: {
    dataset: number | null;
    random_timing: number;
    alternative_paths: number[];
  };
  dataset: {
    bars: number;
    start: string;
    end: string;
    quality: {
      checks: {
        id: string;
        label: string;
        status: "pass" | "warn" | "info";
        detail: string | null;
      }[];
      issues: number;
    };
  };
  configurations: Params[];
  base_index: number;
  headline: {
    params: Params;
    metrics: HeadlineMetrics;
    equity_curve: CurvePoint[];
    yearly: { year: string; pnl: number; return: number | null }[];
    trades: Trade[];
    trades_total: number;
    stdout: string;
  };
  benchmarks: {
    rows: {
      id: "strategy" | "buy_hold" | "trend" | "cash";
      label: string;
      metrics: MetricSet;
    }[];
  };
  lookahead: {
    status: "pass" | "fail";
    checks: {
      bars: number;
      time: string;
      match: boolean;
      first_difference?: string;
      error?: string;
    }[];
  };
  validation: { train_test: TrainTest; walk_forward: WalkForward };
  robustness: { surface: Surface; costs: CostStress; seeds: SeedDispersion };
  diagnostics: {
    trials: { run: number; strategy_configurations: number };
    deflated_sharpe: DeflatedSharpe;
    pbo: Overfitting;
    random_timing: RandomTiming;
    concentration: Concentration;
  };
  redteam: { checks: RedTeamCheck[]; risk: RiskSummary };
};

export type Provenance = {
  quanta_version: string;
  engine: { name: string; version: string; sha256: string };
  environment: {
    python: string;
    implementation: string;
    numpy: string;
    platform: string;
    sha256: string;
  };
  runtime: string;
  git_commit: string | null;
  dataset: {
    kind: "synthetic" | "historical";
    key: string;
    label: string;
    source: string;
    version: number;
    version_sha256: string;
    sha256: string;
    bars: number;
    start: string;
    end: string;
  };
  strategy: StrategyRef;
  config_sha256: string;
  seeds: Record<string, number | number[] | null>;
  configurations: number;
  result_sha256: string;
};

export type Reproduction = {
  verdict: "identical" | "equivalent" | "different";
  inputs: {
    id: string;
    label: string;
    same: boolean;
    original: string;
    rerun: string;
  }[];
  changed_inputs: string[];
  output_identical: boolean;
  metric_differences: {
    metric: string;
    original: number | string | null;
    rerun: number | string | null;
  }[];
  largest_relative_difference: number;
};

export type StrategyRef = {
  id: string;
  name: string;
  version: number;
  sha256: string;
};

export type RunSummary = {
  id: string;
  experiment_id: string;
  number: number;
  kind: "run" | "rerun";
  rerun_of: string | null;
  status: RunStatus;
  stage: string | null;
  progress: { done: number; total: number | null };
  summary: {
    risk?: RiskLevel;
    valid?: boolean;
    configurations?: number;
    metrics?: Pick<
      MetricSet,
      "cagr" | "sharpe" | "max_drawdown" | "turnover" | "total_return"
    >;
  };
  reproduction: Reproduction | null;
  strategy: StrategyRef;
  error: string | null;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
  duration_ms: number | null;
};

export type RunDetail = RunSummary & {
  spec: { experiment: ExperimentSpec; strategy: StrategyRef };
  provenance: Provenance | Record<string, never>;
  results: Results | null;
};

export type Notebook = {
  conclusion?: string;
  limitations?: string;
  decision?: Decision;
};

export type QualityComponent = {
  id: string;
  label: string;
  weight: number;
  score: number;
  note: string;
};

export type ExperimentSummary = {
  id: string;
  number: number;
  title: string;
  strategy: string;
  dataset: string;
  status: LifecycleStatus;
  risk: RiskLevel | null;
  metrics: Pick<
    MetricSet,
    "cagr" | "sharpe" | "max_drawdown" | "turnover" | "total_return"
  > | null;
  run_count: number;
  active: boolean;
  created_at: string;
  updated_at: string;
};

export type ExperimentDetail = ExperimentSummary & {
  hypothesis: string;
  hypothesis_registered_at: string;
  hypothesis_locked: boolean;
  spec: ExperimentSpec;
  notebook: Notebook;
  lifecycle: {
    status: LifecycleStatus;
    steps: { id: string; label: string; done: boolean }[];
  };
  quality: { score: number | null; components: QualityComponent[] };
  spec_changed: boolean;
  strategy_versions: { version: number; sha256: string; created_at: string }[];
  runs: RunSummary[];
  active_run: RunSummary | null;
  current: RunDetail | null;
  reproduction: Reproduction | null;
};

export type ExperimentCreate = {
  title: string;
  hypothesis: string;
  spec: ExperimentSpec;
  run?: boolean;
};

export type ExperimentUpdate = {
  title?: string;
  hypothesis?: string;
  spec?: ExperimentSpec;
  notebook?: Notebook;
};

export type ReportFormat = "markdown" | "html";

const base = "/research";

export const researchApi = {
  options: () => api<ResearchOptions>(`${base}/options`),
  list: () => api<{ experiments: ExperimentSummary[] }>(`${base}/experiments`),
  create: (body: ExperimentCreate) =>
    post<ExperimentDetail>(`${base}/experiments`, body),
  get: (id: string) => api<ExperimentDetail>(`${base}/experiments/${id}`),
  update: (id: string, body: ExperimentUpdate) =>
    api<ExperimentDetail>(`${base}/experiments/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  remove: (id: string) =>
    api<{ ok: boolean }>(`${base}/experiments/${id}`, { method: "DELETE" }),
  run: (id: string) => post<RunSummary>(`${base}/experiments/${id}/runs`, {}),
  getRun: (id: string) => api<RunDetail>(`${base}/runs/${id}`),
  rerun: (runId: string) => post<RunSummary>(`${base}/runs/${runId}/rerun`, {}),
  reportUrl: (id: string, format: ReportFormat) =>
    `/api/v1${base}/experiments/${id}/report?format=${format}`,
  async downloadReport(id: string, format: ReportFormat) {
    let response: Response;
    try {
      response = await fetch(researchApi.reportUrl(id, format), {
        credentials: "same-origin",
        signal: AbortSignal.timeout(20000),
      });
    } catch {
      throw new ApiError("The API is unavailable.", 0);
    }
    if (!response.ok) {
      const body = await response.json().catch(() => null);
      throw new ApiError(
        typeof body?.detail === "string"
          ? body.detail
          : "The research note could not be exported.",
        response.status,
      );
    }
    const name =
      /filename="([^"]+)"/.exec(
        response.headers.get("Content-Disposition") || "",
      )?.[1] || `quanta-experiment.${format === "html" ? "html" : "md"}`;
    const url = URL.createObjectURL(await response.blob());
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = name;
    anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  },
};

export const activeStatuses: RunStatus[] = ["queued", "running"];
export const isActive = (run: Pick<RunSummary, "status"> | null | undefined) =>
  !!run && activeStatuses.includes(run.status);
