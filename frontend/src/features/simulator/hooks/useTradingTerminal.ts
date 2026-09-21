import { simApi } from "@/features/simulator/api/client";
import type { TradingTab } from "@/features/simulator/components/PortfolioPanel";
import {
  defaultPreferences,
  emptyTicket,
  normalizePreferences,
} from "@/features/simulator/model/preferences";
import type {
  Bootstrap,
  Candle,
  Drawing,
  DrawingKind,
  DeskView,
  Fundamentals,
  MarketIndicators,
  NewsFeed,
  RunCalendar,
  Preferences,
  SimOrder,
  SimRun,
  SymbolAnalytics,
} from "@/features/simulator/model/types";
import { indicatorSpec } from "@/features/simulator/model/preferences";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import { ApiError } from "@/shared/api/client";
import { useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
type Pending = {
  path: string;
  method: string;
  body: Record<string, unknown>;
  runId: string;
  message: string;
};

export function useTradingTerminal() {
  const { user } = useWorkspace();
  const [searchParams] = useSearchParams();
  const namespace = `quanta-simulator:v1:${user?.id ?? "guest"}`;
  const [run, setRun] = useState<SimRun | null>(null),
    runRef = useRef<SimRun | null>(null);
  const [boot, setBoot] = useState<Bootstrap | null>(null),
    [loading, setLoading] = useState(true),
    [error, setError] = useState(""),
    [notice, setNotice] = useState("");
  const [prefs, setPrefsState] = useState(defaultPreferences),
    prefRef = useRef(prefs),
    dirty = useRef(false);
  const [bars, setBars] = useState<Candle[]>([]),
    [marketError, setMarketError] = useState(""),
    [marketRetry, setMarketRetry] = useState(0);
  const [overlays, setOverlays] = useState<MarketIndicators>({});
  const [desk, setDesk] = useState<DeskView | null>(null),
    [calendar, setCalendar] = useState<RunCalendar | null>(null),
    [analytics, setAnalytics] = useState<SymbolAnalytics | null>(null);
  const [news, setNews] = useState<NewsFeed | null>(null),
    [fundamentals, setFundamentals] = useState<Fundamentals | null>(null),
    [fundamentalsError, setFundamentalsError] = useState(""),
    [deskError, setDeskError] = useState("");
  const suggestedWatchlist = useRef<string[]>([]);
  const [connectionError, setConnectionError] = useState("");
  const loadSequence = useRef(0);
  const preferenceWrite = useRef<Promise<void> | null>(null);
  const [busy, setBusy] = useState(false),
    busyRef = useRef(false),
    mounted = useRef(true);
  const [pending, setPendingState] = useState<Pending | null>(null),
    pendingRef = useRef<Pending | null>(null);
  const [playing, setPlaying] = useState(false),
    [speed, setSpeed] = useState(1),
    [saveStatus, setSaveStatus] = useState("Saved");
  const [dark, setDark] = useState(
    document.documentElement.dataset.theme === "dark",
  );
  const [searchOpen, setSearchOpen] = useState(false),
    [query, setQuery] = useState(""),
    [addSymbol, setAddSymbol] = useState(false);
  const [indicatorOpen, setIndicatorOpen] = useState(false),
    [resetOpen, setResetOpen] = useState(false),
    [helpOpen, setHelpOpen] = useState(false),
    [exportOpen, setExportOpen] = useState(false);
  const [preview, setPreview] = useState(false),
    [amendment, setAmendment] = useState<{
      order: SimOrder;
      limit: string;
      stop: string;
    } | null>(null),
    [journal, setJournal] = useState<SimOrder | null>(null);
  const [tab, setTab] = useState<TradingTab>("Positions"),
    [mobileTab, setMobileTab] = useState("Chart"),
    [sideTab, setSideTab] = useState("Watchlist");
  // Statements, screening and quant statistics are only fetched while something
  // is showing them, or while the export dialog is collecting a full snapshot.
  const wantsStatements = tab === "Company" || exportOpen;
  const wantsDesk = sideTab === "Desk" || tab === "Performance" || exportOpen;
  const wantsCalendar = tab === "Calendar" || exportOpen;
  const [tool, setTool] = useState<DrawingKind | "cursor">("cursor"),
    [selectedDrawing, setSelectedDrawing] = useState<string | null>(null);
  const [chartAction, setChartAction] = useState<{
    kind: "fit" | "latest";
    seq: number;
  }>({ kind: "latest", seq: 0 });
  const history = useRef<{ past: Drawing[][]; future: Drawing[][] }>({
    past: [],
    future: [],
  });
  const [historyVersion, setHistoryVersion] = useState(0);
  const [newConfig, setNewConfig] = useState({
    mode: "synthetic",
    seed: "",
    symbol: "",
    commission: "1",
    slippage_bps: "2",
    spread_bps: "2",
    participation: "0.01",
  });
  const [walkthrough, setWalkthrough] = useState(0);
  const root = useRef<HTMLDivElement>(null);
  const archived = !!boot?.runs.length && run?.id !== boot.runs[0].id;
  const ticket = prefs.ticket ?? {
    ...emptyTicket(),
    lesson: searchParams.get("lesson") ?? "",
  };
  const drawings = prefs.drawings[prefs.symbol] ?? [];
  const quote = run?.quotes.find((q) => q.symbol === prefs.symbol);
  const persistPrefs = (next: Preferences, id = runRef.current?.id) => {
    if (!id) return;
    try {
      localStorage.setItem(
        `${namespace}:${id}:view`,
        JSON.stringify({ preferences: next, dirty: dirty.current }),
      );
    } catch {
      setError(
        "Device storage is full. Export your work before closing the terminal.",
      );
    }
  };
  const setPrefs = (change: Partial<Preferences>) => {
    const next = { ...prefRef.current, ...change };
    prefRef.current = next;
    dirty.current = true;
    setPrefsState(next);
    setSaveStatus("Saving layout…");
    persistPrefs(next);
  };
  const setPending = (value: Pending | null) => {
    pendingRef.current = value;
    setPendingState(value);
    try {
      if (value)
        localStorage.setItem(`${namespace}:pending`, JSON.stringify(value));
      else localStorage.removeItem(`${namespace}:pending`);
    } catch {
      setError(
        "Device storage is full. Keep this tab open to recover unconfirmed actions.",
      );
    }
  };
  function accept(value: SimRun, restore = false) {
    if (!mounted.current) return;
    runRef.current = value;
    setRun(value);
    if (restore) {
      let cached: { preferences: Preferences; dirty: boolean } | null = null;
      try {
        cached = JSON.parse(
          localStorage.getItem(`${namespace}:${value.id}:view`) ?? "null",
        );
      } catch {}
      const next = normalizePreferences(
        cached?.dirty ? cached.preferences : value.preferences,
        value.quotes.map((q) => q.symbol),
        value.config.base_interval,
        suggestedWatchlist.current,
      );
      if (searchParams.get("lesson") && !next.ticket)
        next.ticket = { ...emptyTicket(), lesson: searchParams.get("lesson")! };
      prefRef.current = next;
      dirty.current = cached?.dirty ?? false;
      setPrefsState(next);
      if (next.theme === "dark" || next.theme === "light") {
        document.documentElement.dataset.theme = next.theme;
        localStorage.setItem("quanta-theme", next.theme);
        window.dispatchEvent(new Event("quanta-theme-change"));
      }
    }
  }
  async function load(selectedId?: string) {
    const sequence = ++loadSequence.current;
    try {
      const result = await simApi<Bootstrap>("");
      if (!mounted.current || sequence !== loadSequence.current) return;
      setBoot(result);
      suggestedWatchlist.current = result.watchlist ?? [];
      let value = selectedId
        ? await simApi<SimRun>(`/runs/${selectedId}`)
        : result.run;
      if (!value) {
        const key = `${namespace}:initial-run`;
        let id = localStorage.getItem(key);
        if (!id) {
          id = crypto.randomUUID();
          localStorage.setItem(key, id);
        }
        value = await simApi<SimRun>("/runs", "POST", { id });
        if (!mounted.current) return;
        const refreshed = await simApi<Bootstrap>("");
        setBoot(refreshed);
      }
      if (!mounted.current || sequence !== loadSequence.current) return;
      accept(value, true);
      setError("");
      setLoading(false);
      try {
        const saved = JSON.parse(
          localStorage.getItem(`${namespace}:pending`) ?? "null",
        ) as Pending | null;
        setPending(saved && saved.runId === value.id ? saved : null);
      } catch {}
    } catch (e) {
      if (mounted.current) {
        setError((e as Error).message);
        setLoading(false);
      }
    }
  }
  useEffect(() => {
    mounted.current = true;
    void load();
    return () => {
      mounted.current = false;
      loadSequence.current += 1;
    };
  }, []);
  useEffect(() => {
    const observer = new MutationObserver(() => {
      const theme = document.documentElement.dataset.theme === "dark";
      setDark(theme);
      if (
        runRef.current &&
        prefRef.current.theme !== (theme ? "dark" : "light")
      )
        setPrefs({ theme: theme ? "dark" : "light" });
    });
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-theme"],
    });
    return () => observer.disconnect();
  }, []);
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setTool("cursor");
        setPlaying(false);
      }
      if (
        (e.metaKey || e.ctrlKey) &&
        e.key === "z" &&
        !["INPUT", "TEXTAREA"].includes((e.target as HTMLElement).tagName)
      ) {
        e.preventDefault();
        undo(e.shiftKey);
      }
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  });
  useEffect(() => {
    if (!run) return;
    let active = true;
    setMarketError("");
    const specs = prefs.indicators
      .filter((i) => i.visible)
      .map(indicatorSpec)
      .filter(Boolean)
      .join(",");
    simApi<{ bars: Candle[]; indicators: MarketIndicators }>(
      `/runs/${run.id}/market?symbol=${encodeURIComponent(prefs.symbol)}&interval=${prefs.interval}&cursor=${run.cursor}&indicators=${encodeURIComponent(specs)}`,
    )
      .then((data) => {
        if (active) {
          setBars(data.bars);
          setOverlays(data.indicators ?? {});
        }
      })
      .catch((e) => {
        if (active) {
          setMarketError(e.message);
          setPlaying(false);
        }
      });
    return () => {
      active = false;
    };
  }, [
    run?.id,
    run?.cursor,
    prefs.symbol,
    prefs.interval,
    marketRetry,
    JSON.stringify(prefs.indicators),
  ]);
  useEffect(() => {
    if (!run || !wantsDesk) return;
    let active = true;
    const timer = setTimeout(() => {
      void simApi<DeskView>(`/runs/${run.id}/desk`)
        .then((view) => {
          if (active) {
            setDesk(view);
            setDeskError("");
          }
        })
        .catch((e) => {
          if (active) {
            setDesk(null);
            setDeskError((e as Error).message);
          }
        });
      void simApi<SymbolAnalytics>(
        `/runs/${run.id}/analytics?symbol=${encodeURIComponent(prefs.symbol)}`,
      )
        .then((view) => {
          if (active) setAnalytics(view);
        })
        .catch(() => {
          if (active) setAnalytics(null);
        });
    }, 300);
    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [run?.id, run?.cursor, prefs.symbol, wantsDesk]);
  useEffect(() => {
    if (!run || !wantsCalendar) return;
    let active = true;
    const timer = setTimeout(() => {
      void simApi<RunCalendar>(`/runs/${run.id}/calendar`)
        .then((view) => {
          if (active) setCalendar(view);
        })
        .catch(() => {
          if (active) setCalendar(null);
        });
    }, 300);
    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [run?.id, run?.cursor, wantsCalendar]);
  useEffect(() => {
    if (!run) return;
    let active = true;
    const timer = setTimeout(() => {
      const scope = prefs.newsScope === "symbol" ? prefs.symbol : "";
      simApi<NewsFeed>(
        `/runs/${run.id}/news?limit=80${scope ? `&symbol=${encodeURIComponent(scope)}` : ""}`,
      )
        .then((feed) => {
          if (active) setNews(feed);
        })
        .catch(() => {
          if (active) setNews(null);
        });
    }, 260);
    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [run?.id, run?.cursor, prefs.newsScope, prefs.symbol]);
  useEffect(() => {
    if (!run || !wantsStatements) return;
    let active = true;
    if (run.config.mode !== "synthetic" || !run.config.universe) {
      setFundamentals(null);
      setFundamentalsError(
        run.config.mode === "historical"
          ? "Imported historical replays have no generated company accounts."
          : "This run predates the simulator's fictional companies. Start a new run to read generated accounts.",
      );
      return;
    }
    const timer = setTimeout(() => {
      simApi<Fundamentals>(
        `/runs/${run.id}/fundamentals?symbol=${encodeURIComponent(prefs.symbol)}`,
      )
        .then((data) => {
          if (active) {
            setFundamentals(data);
            setFundamentalsError("");
          }
        })
        .catch((e) => {
          if (active) {
            setFundamentals(null);
            setFundamentalsError((e as Error).message);
          }
        });
    }, 260);
    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [run?.id, run?.cursor, prefs.symbol, run?.config.mode, wantsStatements]);
  useEffect(() => {
    setNews(null);
    setDesk(null);
    setCalendar(null);
    setAnalytics(null);
    setFundamentals(null);
    setDeskError("");
    setFundamentalsError("");
  }, [run?.id]);
  useEffect(() => {
    setBars([]);
    setSelectedDrawing(null);
    setTool("cursor");
    history.current = { past: [], future: [] };
    setHistoryVersion((v) => v + 1);
  }, [run?.id, prefs.symbol, prefs.interval]);
  async function perform(
    path: string,
    body: Record<string, unknown> = {},
    method = "POST",
    message = "Saved",
    reuse?: Pending,
  ) {
    // A layout write must not swallow a trade click or race its account version.
    if (preferenceWrite.current) {
      setBusy(true);
      await preferenceWrite.current;
    }
    if (!mounted.current) return null;
    const current = runRef.current;
    if (!current || busyRef.current) return null;
    busyRef.current = true;
    setBusy(true);
    setError("");
    const operation: Pending = reuse ?? {
      path,
      method,
      body: { ...body, id: crypto.randomUUID() },
      runId: current.id,
      message,
    };
    setPending(operation);
    try {
      const result = await simApi<SimRun>(
        `/runs/${operation.runId}/${operation.path}`,
        operation.method,
        { ...operation.body, version: current.version },
      );
      if (!mounted.current) return null;
      accept(result);
      setPending(null);
      setNotice(operation.message);
      return result;
    } catch (e) {
      if (!mounted.current) return null;
      setError((e as Error).message);
      setPlaying(false);
      if (
        e instanceof ApiError &&
        e.status >= 400 &&
        e.status < 500 &&
        e.status !== 409
      )
        setPending(null);
      if (e instanceof ApiError && e.status === 409) {
        try {
          const fresh = await simApi<SimRun>(`/runs/${current.id}`);
          accept(fresh);
          const latest = await simApi<Bootstrap>("");
          setBoot(latest);
          if (latest.run?.id !== current.id) setPending(null);
        } catch {}
      }
      return null;
    } finally {
      busyRef.current = false;
      if (mounted.current) setBusy(false);
    }
  }
  const flushPrefs = useCallback(async () => {
    const current = runRef.current;
    if (!current || !dirty.current || busyRef.current || pendingRef.current)
      return;
    const next = JSON.parse(JSON.stringify(prefRef.current)) as Preferences;
    let release!: () => void;
    preferenceWrite.current = new Promise<void>((resolve) => {
      release = resolve;
    });
    busyRef.current = true;
    try {
      const result = await simApi<SimRun>(
        `/runs/${current.id}/preferences`,
        "PUT",
        {
          id: crypto.randomUUID(),
          version: current.version,
          preferences: next,
        },
      );
      if (!mounted.current || runRef.current?.id !== current.id) return;
      accept(result);
      if (JSON.stringify(next) === JSON.stringify(prefRef.current)) {
        dirty.current = false;
        setSaveStatus("Layout saved");
        persistPrefs(next);
      }
    } catch (e) {
      if (!mounted.current) return;
      setSaveStatus("Layout saved on this device");
      if (e instanceof ApiError && e.status === 409) {
        try {
          const fresh = await simApi<SimRun>(`/runs/${current.id}`);
          if (runRef.current?.id === current.id) accept(fresh);
        } catch {}
      }
    } finally {
      busyRef.current = false;
      preferenceWrite.current = null;
      release();
    }
  }, []);
  useEffect(() => {
    if (archived) return;
    const timer = setInterval(() => void flushPrefs(), 1000);
    return () => clearInterval(timer);
  }, [flushPrefs, archived]);
  useEffect(() => {
    if (!playing) return;
    const timer = setInterval(() => {
      if (busyRef.current || pendingRef.current) return;
      const current = runRef.current;
      if (!current || current.cursor >= current.total_bars - 1) {
        setPlaying(false);
        return;
      }
      void perform("advance", { steps: speed }, "POST", "Replay advancing");
    }, 800);
    return () => clearInterval(timer);
  }, [playing, speed]);
  useEffect(() => {
    if (!run || playing || archived) return;
    let active = true;
    const reconcile = async () => {
      if (busyRef.current) return;
      try {
        const current = runRef.current!;
        const latest = await simApi<Bootstrap>("");
        if (
          !active ||
          !mounted.current ||
          busyRef.current ||
          runRef.current?.id !== current.id
        )
          return;
        setConnectionError("");
        setBoot(latest);
        if (
          latest.run?.id === current.id &&
          latest.run.version > current.version
        )
          accept(latest.run, !dirty.current && !pendingRef.current);
        setMarketRetry((v) => v + 1);
      } catch {
        if (active) {
          setConnectionError(
            "Disconnected · displayed prices may be stale. Reconnect to confirm your account.",
          );
          setPlaying(false);
        }
      }
    };
    const offline = () => {
      setConnectionError(
        "Disconnected · displayed prices may be stale. Your draft is saved.",
      );
      setPlaying(false);
    };
    window.addEventListener("offline", offline);
    window.addEventListener("online", reconcile);
    const timer = setInterval(reconcile, 10000);
    return () => {
      active = false;
      clearInterval(timer);
      window.removeEventListener("offline", offline);
      window.removeEventListener("online", reconcile);
    };
  }, [run?.id, playing, archived]);
  /** Terminal-style entry: a ticker, a function code, or both ("NVRA FA"). */
  const FUNCTIONS: Record<string, string> = {
    GP: "Chart",
    N: "News",
    NEWS: "News",
    MOV: "Desk",
    DESK: "Desk",
    FA: "Company financials",
    DES: "Company financials",
    PORT: "Performance",
    CAL: "Calendar",
    ECO: "Calendar",
    EARN: "Calendar",
    RV: "Peers",
    PEER: "Peers",
    POS: "Positions",
    OMON: "Open orders",
    BLOT: "Trade history",
    W: "Watchlist",
    BUY: "Buy ticket",
    SELL: "Sell ticket",
    HELP: "Execution model",
  };
  function runCommand(raw: string) {
    const parts = raw.trim().toUpperCase().split(/\s+/).filter(Boolean);
    if (!parts.length) return false;
    const listed = new Set(runRef.current?.quotes.map((q) => q.symbol) ?? []);
    const symbol = listed.has(parts[0]) ? parts[0] : "";
    const code = symbol ? (parts[1] ?? "GP") : parts[0];
    if (!symbol && !FUNCTIONS[code]) return false;
    if (symbol) chooseSymbol(symbol);
    const openSide = (name: string) => {
      setSideTab(name);
      setMobileTab(name === "Trade" || name === "Watchlist" ? name : "Chart");
      setPrefs({ rightOpen: true });
    };
    const openBottom = (name: TradingTab) => {
      setTab(name);
      setMobileTab("Portfolio");
      setPrefs({ bottomOpen: true });
    };
    switch (FUNCTIONS[code]) {
      case "News":
        openSide("News");
        setMobileTab("News");
        break;
      case "Desk":
        openSide("Desk");
        break;
      case "Watchlist":
        openSide("Watchlist");
        break;
      case "Buy ticket":
      case "Sell ticket":
        setPrefs({
          rightOpen: true,
          ticket: {
            ...emptyTicket(),
            lesson: ticket.lesson,
            side: code === "SELL" ? "sell" : "buy",
          },
        });
        setSideTab("Trade");
        setMobileTab("Trade");
        break;
      case "Company financials":
        openBottom("Company");
        break;
      case "Performance":
        openBottom("Performance");
        break;
      case "Calendar":
        openBottom("Calendar");
        break;
      case "Peers":
        setPrefs({ statement: "peers" });
        openBottom("Company");
        break;
      case "Positions":
        openBottom("Positions");
        break;
      case "Open orders":
        openBottom("Open orders");
        break;
      case "Trade history":
        openBottom("Trade history");
        break;
      case "Execution model":
        setHelpOpen(true);
        break;
      default:
        setMobileTab("Chart");
    }
    return true;
  }
  async function jump(steps: number, label: string) {
    setPlaying(false);
    await perform("advance", { steps }, "POST", `Replay advanced ${label}.`);
  }
  function chooseSymbol(symbol: string) {
    setPrefs({ symbol, ticket: { ...emptyTicket(), lesson: ticket.lesson } });
    setSearchOpen(false);
    setMobileTab("Chart");
    setSelectedDrawing(null);
  }
  function changeDrawings(next: Drawing[]) {
    if (archived) return;
    history.current.past.push(drawings);
    history.current.past = history.current.past.slice(-50);
    history.current.future = [];
    setHistoryVersion((v) => v + 1);
    setPrefs({
      drawings: { ...prefRef.current.drawings, [prefs.symbol]: next },
    });
  }
  function undo(redo = false) {
    if (archived) return;
    const h = history.current;
    const source = redo ? h.future : h.past;
    const target = redo ? h.past : h.future;
    const next = source.pop();
    if (!next) return;
    target.push(prefRef.current.drawings[prefRef.current.symbol] ?? []);
    setPrefs({
      drawings: { ...prefRef.current.drawings, [prefRef.current.symbol]: next },
    });
    setHistoryVersion((v) => v + 1);
  }
  function tradeAt(value: number) {
    setPrefs({
      rightOpen: true,
      ticket: { ...ticket, kind: "limit", limit: value.toFixed(2) },
    });
    setSideTab("Trade");
    setMobileTab("Trade");
  }
  function closePosition(symbol: string, quantity: number) {
    setPlaying(false);
    setPrefs({
      symbol,
      rightOpen: true,
      ticket: { ...emptyTicket(), side: "sell", quantity: String(quantity) },
    });
    setSideTab("Trade");
    setMobileTab("Trade");
  }
  async function submitOrder() {
    const t = prefRef.current.ticket ?? ticket;
    const result = await perform(
      "orders",
      {
        symbol: prefRef.current.symbol,
        side: t.side,
        kind: t.kind,
        quantity: Number(t.quantity),
        ...(t.kind === "limit" || t.kind === "stop_limit"
          ? { limit_price: t.limit }
          : {}),
        ...(t.kind === "stop" || t.kind === "stop_limit"
          ? { stop_price: t.stop }
          : {}),
        tif: t.tif,
        note: t.note,
        lesson: t.lesson,
      },
      "POST",
      "Order accepted. Advance replay to observe its fill.",
    );
    if (result) {
      setPreview(false);
      setTab("Open orders");
      setPrefs({ bottomOpen: true });
    }
  }
  async function retryPending() {
    const item = pendingRef.current;
    if (!item) return;
    try {
      accept(await simApi<SimRun>(`/runs/${item.runId}`));
      const result = await perform(
        item.path,
        item.body,
        item.method,
        item.message,
        item,
      );
      if (result) setPreview(false);
    } catch (e) {
      setError((e as Error).message);
    }
  }
  async function startRun() {
    if (preferenceWrite.current) {
      setBusy(true);
      await preferenceWrite.current;
    }
    if (!mounted.current || busyRef.current) return;
    setPlaying(false);
    busyRef.current = true;
    setBusy(true);
    try {
      const draftConfig = {
        id: crypto.randomUUID(),
        mode: newConfig.mode,
        ...(newConfig.seed.trim() ? { seed: Number(newConfig.seed) } : {}),
        ...(newConfig.mode === "historical"
          ? { symbol: newConfig.symbol }
          : {}),
        commission: newConfig.commission,
        slippage_bps: newConfig.slippage_bps,
        spread_bps: newConfig.spread_bps,
        participation: newConfig.participation,
      };
      const config =
        JSON.parse(localStorage.getItem(`${namespace}:new-run`) || "null") ||
        draftConfig;
      localStorage.setItem(`${namespace}:new-run`, JSON.stringify(config));
      const result = await simApi<SimRun>("/runs", "POST", config);
      localStorage.removeItem(`${namespace}:new-run`);
      if (!mounted.current) return;
      setPending(null);
      accept(result, true);
      const next = await simApi<Bootstrap>("");
      setBoot(next);
      setResetOpen(false);
      setNotice(
        "New $100,000 paper account ready. Prior runs remain in your run history.",
      );
    } catch (e) {
      if (mounted.current) setError((e as Error).message);
    } finally {
      busyRef.current = false;
      if (mounted.current) setBusy(false);
    }
  }
  function resize(e: React.PointerEvent, side: "right" | "bottom") {
    e.preventDefault();
    const start = e.clientX,
      top = e.clientY,
      initial = side === "right" ? prefs.rightWidth : prefs.bottomHeight;
    const move = (event: PointerEvent) => {
      if (side === "right")
        setPrefs({
          rightWidth: Math.max(
            250,
            Math.min(420, initial + start - event.clientX),
          ),
        });
      else
        setPrefs({
          bottomHeight: Math.max(
            130,
            Math.min(420, initial + top - event.clientY),
          ),
        });
    };
    const up = () => {
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up);
    };
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
  }

  return {
    loading,
    run,
    error,
    load,
    busy,
    pending,
    archived,
    marketError,
    connectionError,
    bars,
    overlays,
    desk,
    deskError,
    calendar,
    analytics,
    news,
    fundamentals,
    fundamentalsError,
    jump,
    runCommand,
    commandFunctions: FUNCTIONS,
    prefs,
    ticket,
    setPrefs,
    setPlaying,
    setPreview,
    root,
    dark,
    mobileTab,
    setAddSymbol,
    setQuery,
    setSearchOpen,
    setIndicatorOpen,
    setSideTab,
    setMobileTab,
    setChartAction,
    notice,
    retryPending,
    setMarketRetry,
    setError,
    setNotice,
    tool,
    setTool,
    history,
    undo,
    historyVersion,
    setWalkthrough,
    setHelpOpen,
    drawings,
    changeDrawings,
    selectedDrawing,
    setSelectedDrawing,
    tradeAt,
    setAmendment,
    chartAction,
    playing,
    perform,
    speed,
    setSpeed,
    setResetOpen,
    resize,
    sideTab,
    chooseSymbol,
    quote,
    tab,
    setTab,
    closePosition,
    setJournal,
    saveStatus,
    boot,
    setExportOpen,
    searchOpen,
    addSymbol,
    query,
    preview,
    submitOrder,
    amendment,
    journal,
    indicatorOpen,
    resetOpen,
    startRun,
    newConfig,
    setNewConfig,
    helpOpen,
    walkthrough,
    exportOpen,
  };
}
export type TerminalController = ReturnType<typeof useTradingTerminal>;
