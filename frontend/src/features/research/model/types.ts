export type Params = {
  model: "gbm" | "merton" | "heston" | "regime";
  scenario: string;
  mu: number;
  sigma: number;
  years: number;
  seed: number;
  window: number;
  jump_frequency: number;
  kappa: number;
  theta: number;
  xi: number;
  rho: number;
  symbol?: string;
};

export type Config = {
  dataset_type: "synthetic" | "real";
  dataset_params: Params;
  capital: number;
  commission_bps: number;
  slippage_bps: number;
};

export type Metrics = {
  total_return: number;
  cagr: number;
  sharpe: number | null;
  sortino: number | null;
  max_drawdown: number;
  win_rate: number | null;
  profit_factor: number | null;
  alpha: number | null;
  beta: number | null;
  var_95: number;
  cvar_95: number | null;
  calmar: number | null;
  trades: number;
  final_equity: number;
};

export type Bar = {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
};

export type Trade = {
  time: string;
  side: "BUY" | "SELL";
  price: number;
  quantity: number;
  commission: number;
  pnl: number | null;
};

export type Result = {
  metrics: Metrics;
  equity_curve: {
    time: string;
    equity: number;
    benchmark: number;
    drawdown: number;
  }[];
  monthly_returns: { month: string; return: number }[];
  trades: Trade[];
  bars: Bar[];
  stdout: string;
  stderr: string;
  execution_ms: number;
  dataset_type: string;
  runtime: string;
};

export type Experiment = {
  id: string;
  title: string;
  code: string;
  config: Config;
  metrics?: Metrics;
  updatedAt: string;
  lessonId?: string;
};

export const defaultConfig: Config = {
  dataset_type: "synthetic",
  dataset_params: {
    model: "gbm",
    scenario: "custom",
    mu: 0.08,
    sigma: 0.2,
    years: 3,
    seed: 42,
    window: 50,
    jump_frequency: 1,
    kappa: 2,
    theta: 0.04,
    xi: 0.3,
    rho: -0.7,
  },
  capital: 100000,
  commission_bps: 5,
  slippage_bps: 3,
};

export const defaultCode =
  'def strategy(data):\n    # Signal at the close; execution at the next open.\n    return data["close"] > data["sma_50"]\n';
