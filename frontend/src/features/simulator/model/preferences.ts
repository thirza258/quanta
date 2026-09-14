import type { Preferences, Ticket } from "./types";

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
