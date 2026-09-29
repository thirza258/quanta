import type { Indicator, MonitorTool, Preferences, Ticket } from "./types";

/** The overlay request the API computes; volume is already on every bar. */
export const indicatorSpec = (i: Indicator) =>
  i.kind === "Volume"
    ? ""
    : i.kind === "MACD"
      ? `MACD:${i.period}:${i.slow}:${i.signal}`
      : `${i.kind}:${i.period}`;

export const emptyTicket = (): Ticket => ({
  side: "buy",
  kind: "market",
  quantity: "10",
  limit: "",
  stop: "",
  trail: "",
  bracket: false,
  takeProfit: "",
  stopLoss: "",
  stopTrail: "",
  tif: "GTC",
  note: "",
  lesson: "",
});

export const defaultPreferences = (): Preferences => ({
  symbol: "NVRA",
  interval: "1m",
  chartType: "candles",
  watchlist: ["NVRA", "CLDS", "VLOC", "HLXB", "MRDN", "TRVT", "ZEPH", "PLSR"],
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
  monitors: 1,
  panes: ["tape", "heatmap"],
});

/** Tools a monitor window can show, in the order the picker offers them. */
export const MONITOR_TOOLS: { id: MonitorTool; label: string }[] = [
  { id: "tape", label: "Time & sales" },
  { id: "book", label: "Order book" },
  { id: "heatmap", label: "Heat map" },
  { id: "screener", label: "Screener" },
  { id: "sessions", label: "Sessions" },
  { id: "quotes", label: "Quotes" },
  { id: "news", label: "News" },
];

export function normalizePreferences(
  raw: Partial<Preferences> | undefined,
  symbols: string[],
  base: string,
  suggested: string[] = [],
): Preferences {
  const defaults = defaultPreferences();
  const p = { ...defaults, ...raw };
  p.symbol = symbols.includes(p.symbol) ? p.symbol : symbols[0];
  // An empty saved list is a deliberate choice and is kept. A list that had
  // entries but filters away to nothing was saved against another universe, so
  // it falls back to this run's suggested names instead of staying empty.
  const saved = Array.isArray(raw?.watchlist) ? raw.watchlist : null;
  p.watchlist = [
    ...new Set(
      (saved ?? defaults.watchlist).filter((s) => symbols.includes(s)),
    ),
  ];
  if (!p.watchlist.length && saved?.length !== 0) {
    const fallback = suggested.filter((s) => symbols.includes(s));
    p.watchlist = fallback.length ? fallback : symbols.slice(0, 8);
  }
  p.interval =
    base === "1D"
      ? "1D"
      : ["1m", "5m", "15m", "1h", "1D"].includes(p.interval)
        ? p.interval
        : "1m";
  p.newsScope = p.newsScope === "symbol" ? "symbol" : "all";
  p.statement = ["income", "balance", "cash", "ratios", "peers"].includes(
    p.statement ?? "",
  )
    ? p.statement
    : "ratios";
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
  // A monitor layout saved on a desktop must not arrive on a phone as three
  // windows in a column too short to read any of them.
  p.monitors = ([1, 2, 3] as const).includes(p.monitors as 1 | 2 | 3)
    ? p.monitors
    : 1;
  const tools = MONITOR_TOOLS.map((tool) => tool.id);
  const panes = Array.isArray(p.panes) ? p.panes : [];
  p.panes = [0, 1].map((slot) =>
    tools.includes(panes[slot]) ? panes[slot] : (defaults.panes ?? [])[slot],
  );
  p.rightWidth = Math.min(420, Math.max(250, Number(p.rightWidth) || 300));
  p.bottomHeight = Math.min(420, Math.max(130, Number(p.bottomHeight) || 230));
  return p;
}
