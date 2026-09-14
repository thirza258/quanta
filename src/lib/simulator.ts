import { ApiError, api } from "./api";
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
export const emptyTicket = (): Ticket => ({
  side: "buy",
  kind: "market",
  quantity: "10",
  limit: "",
  stop: "",
  tif: "GTC",
  note: "",
  lesson: "",
});
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
export const defaultPreferences = (): Preferences => ({
  symbol: "AAPL",
  interval: "1m",
  chartType: "candles",
  watchlist: ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "META"],
  indicators: [
    {
      id: "volume",
      kind: "Volume",
      period: 20,
      slow: 26,
      signal: 9,
      visible: true,
    },
    { id: "sma", kind: "SMA", period: 20, slow: 26, signal: 9, visible: true },
  ],
  drawings: {},
  rightWidth: 300,
  bottomHeight: 230,
  rightOpen: true,
  bottomOpen: true,
});
export function normalizePreferences(
  raw: Partial<Preferences> | undefined,
  symbols: string[],
  base: string,
): Preferences {
  const defaults = defaultPreferences();
  const p = { ...defaults, ...raw };
  p.symbol = symbols.includes(p.symbol) ? p.symbol : symbols[0];
  p.watchlist = Array.isArray(p.watchlist)
    ? [...new Set(p.watchlist.filter((s) => symbols.includes(s)))]
    : symbols;
  if (!p.watchlist.length && !raw?.watchlist) p.watchlist = symbols;
  p.interval =
    base === "1D"
      ? "1D"
      : ["1m", "5m", "15m", "1h", "1D"].includes(p.interval)
        ? p.interval
        : "1m";
  p.chartType = ["candles", "bars", "line"].includes(p.chartType)
    ? p.chartType
    : "candles";
  p.indicators = Array.isArray(p.indicators)
    ? p.indicators
        .filter(
          (i) =>
            i &&
            ["SMA", "EMA", "RSI", "MACD", "Volume"].includes(i.kind) &&
            Number.isFinite(i.period),
        )
        .slice(0, 8)
    : defaults.indicators;
  p.indicators = p.indicators.map((i) => ({
    ...i,
    period: Math.max(2, Math.min(200, Math.floor(i.period))),
    slow: Math.max(2, Math.min(200, Math.floor(Number(i.slow) || 26))),
    signal: Math.max(2, Math.min(200, Math.floor(Number(i.signal) || 9))),
  }));
  p.drawings = Object.fromEntries(
    Object.entries(
      p.drawings && typeof p.drawings === "object" && !Array.isArray(p.drawings)
        ? p.drawings
        : {},
    )
      .filter(([symbol]) => symbols.includes(symbol))
      .map(([symbol, objects]) => [
        symbol,
        Array.isArray(objects)
          ? objects
              .filter(
                (d) =>
                  d &&
                  typeof d.id === "string" &&
                  [
                    "trend",
                    "horizontal",
                    "rectangle",
                    "text",
                    "measure",
                  ].includes(d.kind) &&
                  [d.t1, d.t2, d.p1, d.p2].every(Number.isFinite) &&
                  d.p1 > 0 &&
                  d.p2 > 0 &&
                  typeof d.text === "string" &&
                  /^#[0-9a-f]{6}$/i.test(d.color),
              )
              .slice(0, 500)
          : [],
      ]),
  );
  p.rightWidth = Math.min(420, Math.max(250, Number(p.rightWidth) || 300));
  p.bottomHeight = Math.min(420, Math.max(130, Number(p.bottomHeight) || 230));
  return p;
}
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
export const working = (o: SimOrder) =>
  ["working", "partially_filled"].includes(o.status);
export const dollars = (value: string | number) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  }).format(Number(value));
export const price = (value: string | number) =>
  Number(value).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
export const stamp = (time: number | null) =>
  time
    ? new Date(time * 1000).toLocaleString("en-US", {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        timeZone: "America/New_York",
      }) + " ET"
    : "Opening balance";
export function csv(rows: Record<string, unknown>[]) {
  if (!rows.length) return "";
  const keys = [...new Set(rows.flatMap((row) => Object.keys(row)))];
  const cell = (v: unknown) => {
    const raw = String(v ?? "");
    // Preserve ledger amounts as numbers while escaping executable journal text.
    const safe =
      /^[\s]*[=+@\-]/.test(raw) && !/^-?\d+(\.\d+)?$/.test(raw)
        ? "' " + raw
        : raw;
    return '"' + safe.replaceAll('"', '""') + '"';
  };
  return [
    keys.map(cell).join(","),
    ...rows.map((row) => keys.map((k) => cell(row[k])).join(",")),
  ].join("\r\n");
}
export async function simApi<T>(
  path: string,
  method = "GET",
  body?: unknown,
): Promise<T> {
  try {
    return await api<T>("/simulator" + path, {
      method,
      ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
    });
  } catch (error) {
    if (error instanceof ApiError && error.status === 0)
      throw new ApiError(
        "Connection lost. Your confirmed trades are saved. Reconnect to recover before retrying.",
        0,
      );
    throw error;
  }
}
export function sma(values: number[], period: number): (number | null)[] {
  let sum = 0;
  return values.map((value, i) => {
    sum += value;
    if (i >= period) sum -= values[i - period];
    return i >= period - 1 ? sum / period : null;
  });
}
export function ema(values: number[], period: number): (number | null)[] {
  let previous: number | null = null;
  let sum = 0;
  const alpha = 2 / (period + 1);
  return values.map((v, i) => {
    sum += v;
    if (i < period - 1) return null;
    previous =
      previous === null ? sum / period : alpha * v + (1 - alpha) * previous;
    return previous;
  });
}
export function rsi(values: number[], period: number): (number | null)[] {
  let gain = 0,
    loss = 0;
  return values.map((v, i) => {
    if (i === 0) return null;
    const diff = v - values[i - 1];
    if (i <= period) {
      gain += Math.max(diff, 0) / period;
      loss += Math.max(-diff, 0) / period;
    } else {
      gain = (gain * (period - 1) + Math.max(diff, 0)) / period;
      loss = (loss * (period - 1) + Math.max(-diff, 0)) / period;
    }
    return i < period
      ? null
      : loss === 0
        ? gain === 0
          ? 50
          : 100
        : 100 - 100 / (1 + gain / loss);
  });
}
export function macd(
  values: number[],
  fast: number,
  slow: number,
  signal: number,
) {
  const a = ema(values, fast),
    b = ema(values, slow),
    line = a.map((v, i) => (v !== null && b[i] !== null ? v - b[i]! : null));
  const valid = line.filter((v): v is number => v !== null);
  const offset = line.length - valid.length;
  const sig = [
    ...Array<number | null>(offset).fill(null),
    ...ema(valid, signal),
  ];
  return {
    line,
    signal: sig,
    histogram: line.map((v, i) =>
      v !== null && sig[i] !== null ? v - sig[i]! : null,
    ),
  };
}

export function orderEstimate(run: SimRun, symbol: string, ticket: Ticket) {
  const mark = run.quotes.find((q) => q.symbol === symbol)?.close ?? 0;
  const position = run.positions.find((p) => p.symbol === symbol);
  const buy = ticket.side === "buy",
    quantity = Number(ticket.quantity) || 0;
  const friction =
    (Number(run.config.slippage_bps) + Number(run.config.spread_bps) / 2) /
    10000;
  const hasLimit = ticket.kind === "limit" || ticket.kind === "stop_limit";
  const base =
    ticket.kind === "stop"
      ? buy
        ? Math.max(mark, Number(ticket.stop))
        : Math.min(mark, Number(ticket.stop))
      : mark;
  const price = hasLimit
    ? Number(ticket.limit)
    : buy
      ? Math.ceil(base * (1 + friction) * 100) / 100
      : Math.round(base * (1 - friction) * 100) / 100;
  const notional = quantity * price,
    fee = Number(run.config.commission);
  return {
    price,
    notional,
    total: notional + (buy ? fee : -fee),
    availableShares: position?.available ?? 0,
    after: (position?.quantity ?? 0) + (buy ? quantity : -quantity),
  };
}
