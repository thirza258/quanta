export type Candle = {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
};

export type Interval = "1m" | "5m" | "15m" | "1h" | "1D";

export type OrderKind = "market" | "limit" | "stop" | "stop_limit";

export type SimOrder = {
  id: string;
  symbol: string;
  side: "buy" | "sell";
  kind: OrderKind;
  quantity: number;
  limit_price: string | null;
  stop_price: string | null;
  tif: "DAY" | "GTC";
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
};

export type SimRun = {
  id: string;
  version: number;
  created_at: string;
  guest: boolean;
  cursor: number;
  total_bars: number;
  clock: number;
  cash: string;
  reserved: string;
  available: string;
  equity: string;
  realized: string;
  config: {
    mode: "synthetic" | "historical";
    seed: number;
    symbol: string | null;
    base_interval: string;
    source: string;
    commission: string;
    slippage_bps: string;
    spread_bps: string;
    participation: string;
  };
  quotes: (Candle & {
    symbol: string;
    name: string;
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
  symbols: { symbol: string; name: string }[];
};
