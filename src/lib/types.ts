export type Exercise = {
  question: string;
  options: string[];
  answer: number;
  explanation: string;
};
export type Lesson = {
  id: string;
  title: string;
  subtitle: string;
  minutes: number;
  content: string;
  formula: string;
  exercise: Exercise;
  code: string;
  kind: string;
  objective?: string;
  exercises?: Exercise[];
  terms?: { term: string; definition: string }[];
  part?: string;
  reading?: string;
  references?: { title: string; url: string }[];
  assignment?: { prompt: string; solution: string };
};
export type ExamQuestion = Exercise & { id: string; lessonId: string };
export type Exam = {
  id: string;
  title: string;
  kind: string;
  version: number;
  description: string;
  minutes: number;
  passingScore: number;
  moduleIds: string[];
  questions: ExamQuestion[];
};
export type ExamDraft = {
  id: string;
  version: number;
  startedAt: string;
  answers: Record<string, number>;
};
export type ExamAttempt = ExamDraft & {
  examId: string;
  submittedAt: string;
  correctCount: number;
  total: number;
  score: number;
  passed: boolean;
  grading: "server" | "device";
};
export type Track = {
  id: string;
  number: number;
  title: string;
  description: string;
  source: string;
  level: string;
  icon: string;
  modules: Lesson[];
  outcomes?: string[];
  prerequisites?: string;
  readingGuide?: string;
  studyType?: string;
  resources?: { title: string; url: string }[];
  references?: { title: string; url: string }[];
  parts?: { id: string; title: string; description: string }[];
  exams: Exam[];
};
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
export type Note = {
  id: string;
  title: string;
  body: string;
  lessonId?: string;
  updatedAt: string;
};
export type WorkspaceState = {
  completed: string[];
  lastLesson: string;
  drafts: Record<string, string>;
  notes: Note[];
  experiments: Experiment[];
  submissions: Record<string, { answer: number; correct: boolean }>;
  examDrafts: Record<string, ExamDraft>;
  examAttempts: Record<string, ExamAttempt[]>;
  runs: number;
};
export type User = { id: string; name: string; email: string };
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
