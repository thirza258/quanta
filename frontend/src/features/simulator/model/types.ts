export type Candle = {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
};

export type Interval = "1m" | "5m" | "15m" | "1h" | "1D";

export type OrderKind =
  "market" | "limit" | "stop" | "stop_limit" | "trailing_stop";

export type SimOrder = {
  id: string;
  symbol: string;
  side: "buy" | "sell";
  kind: OrderKind;
  quantity: number;
  limit_price: string | null;
  stop_price: string | null;
  trail_percent?: string | null;
  trail_anchor?: string | null;
  tif: "DAY" | "GTC";
  /** Set on an exit attached to an entry, naming the entry it protects. */
  parent_id?: string | null;
  oco_group?: string | null;
  role?: "target" | "stop" | null;
  /** The bar an armed bracket leg can first trade on. */
  activates?: number | null;
  filled: number;
  status: string;
  average: string;
  time: number;
  reason: string;
  note: string;
  lesson: string;
};

export type Fill = {
  id: string;
  order_id: string;
  symbol: string;
  side: string;
  quantity: number;
  price: string;
  fee: string;
  realized: string;
  time: number;
  note: string;
  lesson: string;
};

export type Position = {
  symbol: string;
  quantity: number;
  cost: string;
  average: string;
  mark: string;
  market_value: string;
  unrealized: string;
  available: number;
  /** Shares a close acts on, whichever way the position faces. */
  closable: number;
  short: boolean;
};

export type DrawingKind =
  "trend" | "horizontal" | "rectangle" | "text" | "measure";

export type Drawing = {
  id: string;
  kind: DrawingKind;
  t1: number;
  t2: number;
  p1: number;
  p2: number;
  text: string;
  color: string;
  locked: boolean;
};

export type Indicator = {
  id: string;
  kind: "SMA" | "EMA" | "RSI" | "MACD" | "Volume";
  period: number;
  slow: number;
  signal: number;
  visible: boolean;
};

export type Ticket = {
  side: "buy" | "sell";
  kind: OrderKind;
  quantity: string;
  limit: string;
  stop: string;
  /** Trail for a trailing stop, as a percentage of the best price reached. */
  trail: string;
  /** Exits attached to an entry, sent with it and held until it fills. */
  bracket: boolean;
  takeProfit: string;
  stopLoss: string;
  /** A trailing stop leg instead of a fixed one, as a percentage. */
  stopTrail: string;
  tif: "DAY" | "GTC";
  note: string;
  lesson: string;
};

export type Preferences = {
  symbol: string;
  interval: Interval;
  chartType: "candles" | "bars" | "line";
  watchlist: string[];
  indicators: Indicator[];
  drawings: Record<string, Drawing[]>;
  rightWidth: number;
  bottomHeight: number;
  rightOpen: boolean;
  bottomOpen: boolean;
  theme?: string;
  ticket?: Ticket;
  walkthrough?: boolean;
  newsScope?: "all" | "symbol";
  statement?: "income" | "balance" | "cash" | "ratios" | "peers";
  /** How many windows the chart region is split into: 1, 2 or 3. */
  monitors?: 1 | 2 | 3;
  /** The tool shown in the second and third windows. */
  panes?: MonitorTool[];
  /** Whether scored headlines are marked on the price chart. */
  newsMarkers?: boolean;
  /** Events that cut a jump short so a decision has to be made. */
  stopOn?: StopEvent[];
};

export type NewsMarker = {
  time: number;
  /** Net basis points of modeled impact on this bar, summed across its items. */
  points: number;
  count: number;
  headline: string;
  items: {
    headline: string;
    points: number;
    scope: string;
    impact: string;
  }[];
};

export type StopEvent =
  | "fill"
  | "bracket"
  | "margin_call"
  | "earnings"
  | "news";

export type MonitorTool =
  | "tape"
  | "book"
  | "heatmap"
  | "screener"
  | "sessions"
  | "quotes"
  | "crowd"
  | "news";

export type TapePrint = {
  time: number;
  price: number;
  size: number;
  side: "buy" | "sell" | "—";
  index: number;
};

export type MonitorTools = {
  tape?: {
    symbol: string;
    name: string;
    sector: string | null;
    prints: TapePrint[];
    volume: number;
    buy_share: number | null;
    notice: string;
  };
  book?: {
    symbol: string;
    last: number;
    bid: number;
    ask: number;
    spread: number;
    bids: { price: number; size: number; cumulative: number }[];
    asks: { price: number; size: number; cumulative: number }[];
    imbalance: number | null;
    notice: string;
  };
  heatmap?: {
    sectors: {
      sector: string;
      change_pct: number;
      notional: number;
      companies_count: number;
      companies: {
        symbol: string;
        name: string;
        close: number;
        change_pct: number;
        relative_volume: number | null;
        notional: number;
        sentiment: number | null;
      }[];
    }[];
    companies: number;
    best: number;
    worst: number;
    weighting: string;
  };
  screener?: {
    screen: string;
    label: string;
    description: string;
    screens: { id: string; label: string; description: string }[];
    matches: number;
    rows: {
      symbol: string;
      name: string;
      sector: string | null;
      close: number;
      change_pct: number;
      relative_volume: number | null;
      volatility: number | null;
      sentiment: number | null;
      rsi: number | null;
      above_fast: boolean;
      above_slow: boolean;
      range_position: number | null;
      multiple: number | null;
      window_high: number;
      window_low: number;
    }[];
    window_bars: number;
    session_bars: number;
  };
  sessions?: {
    symbol: string;
    sessions: {
      time: number;
      open: number;
      high: number;
      low: number;
      close: number;
      volume: number;
      change_pct: number;
    }[];
    volatility: number | null;
    prior_close: number;
  };
  crowd?: {
    symbol: string;
    available: boolean;
    notice: string;
    orders: {
      desk: string;
      style: string;
      side: "buy" | "sell";
      kind: "market" | "limit";
      quantity: number;
      limit: number | null;
      placed: number;
      index: number;
      status: "working" | "filled";
      price: number | null;
      filled_at: number | null;
      reason: string;
    }[];
    desks: { id: string; name: string; style: string }[];
    window_bars?: number;
    working?: number;
    filled?: number;
    buy_share?: number | null;
  };
  quotes?: {
    rows: {
      symbol: string;
      name: string;
      sector: string | null;
      close: number;
      change: number;
      change_pct: number;
      volume: number;
      relative_volume: number | null;
      sentiment: number | null;
    }[];
  };
};

export type MonitorView = {
  tools: MonitorTools;
  symbol: string;
  cursor: number;
  version: number;
  disclosure: string;
};

export type SimRun = {
  id: string;
  version: number;
  created_at: string;
  guest: boolean;
  cursor: number;
  total_bars: number;
  /** A generated market keeps producing sessions; an import is bounded. */
  endless: boolean;
  session: number | null;
  clock: number;
  cash: string;
  reserved: string;
  available: string;
  equity: string;
  /** Why the last jump stopped short, if it did. */
  interrupted: { bar: number; reason: string; of: number } | null;
  /** What the account is carrying, counting a short at what it owes. */
  gross_exposure: string;
  /** Cash on a cash account; twice equity less gross on a margin one. */
  buying_power: string;
  account: "cash" | "margin";
  realized: string;
  config: {
    mode: "synthetic" | "historical";
    seed: number;
    universe?: string;
    mission?: string | null;
    symbol: string | null;
    base_interval: string;
    source: string;
    commission: string;
    slippage_bps: string;
    spread_bps: string;
    participation: string;
  };
  universe: string | null;
  disclosure: string;
  quotes: (Candle & {
    symbol: string;
    name: string;
    sector: string | null;
    business: string | null;
    change: number;
    change_pct: number;
  })[];
  positions: Position[];
  orders: SimOrder[];
  fills: Fill[];
  ledger: {
    id: string;
    time: number | null;
    type: string;
    description: string;
    amount: string;
    cash: string;
  }[];
  preferences: Partial<Preferences>;
};

export type Bootstrap = {
  run: SimRun | null;
  runs: { id: string; created_at: string; mode: string }[];
  historical: { symbol: string; source: string }[];
  symbols: {
    symbol: string;
    name: string;
    sector: string | null;
    business: string | null;
    simulated: boolean;
  }[];
  watchlist: string[];
  disclosure: string;
};

/** Overlay series computed by the API from the same observed bars. */
export type MarketIndicator = {
  kind: string;
  values?: (number | null)[];
  line?: (number | null)[];
  signal?: (number | null)[];
  histogram?: (number | null)[];
};

export type MarketIndicators = Record<string, MarketIndicator>;

export type MoverRow = {
  symbol: string;
  name: string;
  sector: string | null;
  close: number;
  change: number;
  change_pct: number;
  volume: number;
  relative_volume: number | null;
  notional: number;
  volatility: number | null;
  window_bars: number;
  window_high: number;
  window_low: number;
  sentiment: number | null;
};

export type DeskView = {
  movers: {
    gainers: MoverRow[];
    losers: MoverRow[];
    active: MoverRow[];
    sectors: {
      sector: string;
      companies: number;
      change_pct: number;
      sentiment: number | null;
    }[];
    breadth: {
      advancing: number;
      declining: number;
      unchanged: number;
      average_change_pct: number;
    };
  };
  performance: {
    curve: { time: number; equity: number }[];
    opening_equity: number;
    equity: number;
    total_return: number;
    max_drawdown: number;
    realized: string;
    unrealized: number;
    average_exposure: number;
    trades: number;
    win_rate: number | null;
    profit_factor: number | null;
    average_win: number | null;
    average_loss: number | null;
    attribution: {
      symbol: string;
      realized: number;
      unrealized: number;
      total: number;
      quantity: number;
      fills: number;
    }[];
    bars_observed: number;
    benchmark: {
      name: string;
      equity: number;
      total_return: number;
      curve: { time: number; equity: number }[];
    };
    sessions: number;
    risk: {
      cagr: number | null;
      sharpe: number | null;
      sortino: number | null;
      calmar: number | null;
      alpha: number | null;
      beta: number | null;
      var_95: number | null;
      cvar_95: number | null;
      max_drawdown: number | null;
    };
    risk_is_meaningful: boolean;
  };
  cursor: number;
  version: number;
  disclosure: string;
};

export type SymbolAnalytics = {
  symbol: string;
  name: string;
  sector: string | null;
  close: number;
  indicators: {
    sma_20: number | null;
    sma_50: number | null;
    ema_20: number | null;
    rsi_14: number | null;
    macd: { line: number; signal: number; histogram: number } | null;
  };
  risk: {
    volatility_short: number | null;
    volatility_long: number | null;
    short_window_bars: number;
    long_window_bars: number;
    beta: number | null;
    correlation: number | null;
    observations: number;
  };
  momentum: {
    session: number | null;
    week: number | null;
    since_open: number;
  };
  range: Record<string, number>;
  liquidity: {
    volume: number;
    average_volume_20: number;
    average_volume_session: number;
  };
  sentiment: { session: SentimentReading; week: SentimentReading } | null;
};

export type MissionProgress = {
  id: string;
  title: string;
  subtitle: string;
  brief: string;
  lessons: string[];
  symbol: string;
  objectives: {
    id: string;
    title: string;
    detail: string;
    met: boolean;
    progress: string;
  }[];
  met: number;
  total: number;
  complete: boolean;
  cursor: number;
  version: number;
  disclosure: string;
};

export type MissionCatalog = {
  missions: {
    id: string;
    title: string;
    subtitle: string;
    lessons: string[];
    brief: string;
    symbol: string;
    name: string;
    objectives: { id: string; title: string; detail: string }[];
  }[];
  disclosure: string;
};

export type RunCalendar = {
  economic: {
    index: number;
    time: number;
    name: string;
    topic: string;
    released: boolean;
    headline: string | null;
    sentiment: "positive" | "negative" | "neutral" | null;
  }[];
  earnings: {
    symbol: string;
    name: string;
    sector: string | null;
    label: string;
    index: number;
    time: number;
    bars_away: number;
    released: boolean;
    // Null until the quarter is scheduled: the date is knowable before the
    // street has published an estimate for it.
    consensus_eps: number | null;
    consensus_revenue: number | null;
    eps?: number;
    revenue?: number;
    eps_surprise?: number | null;
    revenue_surprise?: number;
  }[];
  horizon_bars: number;
  cursor: number;
  version: number;
  disclosure: string;
};

export type PeerRow = {
  symbol: string;
  name: string;
  sector: string | null;
  price: number;
  market_capitalization: number;
  price_earnings: number | null;
  price_sales: number | null;
  price_book: number | null;
  enterprise_ebitda: number | null;
  operating_margin: number | null;
  return_on_equity: number | null;
  revenue_growth: number | null;
  debt_equity: number | null;
  free_cash_flow_yield: number | null;
  reported_quarters: number;
  self: boolean;
};

export type NewsScope = "company" | "sector" | "macro" | "market";

export type NewsItem = {
  id: string;
  index: number;
  time: number;
  scope: NewsScope;
  symbol: string | null;
  sector: string | null;
  category: string;
  headline: string;
  summary: string;
  source: string;
  sentiment: "positive" | "negative" | "neutral";
  impact: "high" | "medium" | "low" | "none";
  /** Signed score. One point is one basis point of modeled price move. */
  points: number;
};

export type SentimentReading = {
  score: number;
  weight: number;
  items: number;
  window_bars: number;
  positive: number;
  negative: number;
  neutral: number;
};

export type NewsFeed = {
  items: NewsItem[];
  available: boolean;
  cursor: number;
  version: number;
  disclosure: string;
  notice: string;
  sentiment: {
    session: SentimentReading;
    week: SentimentReading;
    market: SentimentReading;
  } | null;
};

export type Quarter = {
  label: string;
  index: number;
  released: boolean;
  revenue: number;
  cost_of_revenue: number;
  gross_profit: number;
  research_development: number;
  selling_general_admin: number;
  depreciation: number;
  operating_income: number;
  ebitda: number;
  interest_expense: number;
  pretax_income: number;
  tax_expense: number;
  net_income: number;
  eps: number;
  shares: number;
  cash: number;
  receivables: number;
  inventory: number;
  current_assets: number;
  property_plant_equipment: number;
  goodwill: number;
  total_assets: number;
  payables: number;
  short_term_debt: number;
  current_liabilities: number;
  long_term_debt: number;
  total_debt: number;
  total_liabilities: number;
  equity: number;
  operating_cash_flow: number;
  capital_expenditure: number;
  free_cash_flow: number;
  dividends_paid: number;
  buybacks: number;
  external_financing: number;
  financing_cash_flow: number;
  opening_cash: number;
  consensus_eps?: number;
  consensus_revenue?: number;
  revenue_surprise?: number;
  eps_surprise?: number | null;
};

export type Valuation = {
  price: number;
  market_capitalization: number;
  enterprise_value: number;
  shares: number;
  net_debt: number;
  trailing_revenue: number;
  trailing_net_income: number;
  trailing_ebitda: number;
  trailing_free_cash_flow: number;
  trailing_eps: number;
  price_earnings: number | null;
  price_sales: number | null;
  price_book: number | null;
  enterprise_sales: number | null;
  enterprise_ebitda: number | null;
  free_cash_flow_yield: number | null;
  dividend_yield: number | null;
  payout_ratio: number | null;
  gross_margin: number | null;
  operating_margin: number | null;
  net_margin: number | null;
  return_on_equity: number | null;
  return_on_assets: number | null;
  revenue_growth: number | null;
  earnings_growth: number | null;
  current_ratio: number | null;
  quick_ratio: number | null;
  working_capital: number;
  debt_equity: number | null;
  net_debt_ebitda: number | null;
  interest_coverage: number | null;
  net_current_asset_value: number;
  graham_number: number | null;
  book_value_per_share: number;
  prior_year_quarter: string | null;
};

export type Fundamentals = {
  symbol: string;
  name: string;
  sector: string;
  business: string;
  currency: string;
  units: string;
  // Descriptive facts only; the parameters that generate a quarter stay server-side.
  structure: {
    shares: number;
    employees: number;
    fiscal_year_end: string;
    development_stage: boolean;
  };
  quarters: Quarter[];
  upcoming: {
    label: string;
    time: number;
    bars_away: number;
    consensus_eps: number;
    consensus_revenue: number;
  } | null;
  valuation: Valuation;
  peers: {
    sector: string | null;
    rows: PeerRow[];
    median: Record<string, number | null>;
  };
  cursor: number;
  version: number;
  disclosure: string;
};
