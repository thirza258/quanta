import type { CSSProperties } from "react";
import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import {
  Activity,
  ArrowLeft,
  ArrowUp,
  Check,
  ChevronDown,
  ChevronRight,
  CircleHelp,
  Crosshair,
  Download,
  Expand,
  Eye,
  EyeOff,
  Layers,
  List,
  Maximize2,
  Minus,
  PanelBottomOpen,
  PanelRightClose,
  PanelRightOpen,
  Pause,
  Play,
  Plus,
  Redo2,
  RefreshCw,
  Ruler,
  Search,
  SkipForward,
  SlidersHorizontal,
  Square,
  TrendingUp,
  Type,
  Undo2,
  X,
} from "lucide-react";
import { ApiError, download } from "../../lib/api";
import { useWorkspace } from "../../lib/workspace";
import { Modal, Loading } from "../ui";
import SimChart from "./SimChart";
import OrderTicket from "./OrderTicket";
import PortfolioPanel from "./PortfolioPanel";
import type { TradingTab } from "./PortfolioPanel";
import DrawingsPanel from "./DrawingsPanel";
import {
  defaultPreferences,
  dollars,
  emptyTicket,
  normalizePreferences,
  price,
  simApi,
  stamp,
  orderEstimate,
} from "../../lib/simulator";
import type {
  Bootstrap,
  Candle,
  Drawing,
  DrawingKind,
  Indicator,
  Interval,
  Preferences,
  SimOrder,
  SimRun,
  Ticket,
} from "../../lib/simulator";
import "../../simulator.css";

type Pending = {
  path: string;
  method: string;
  body: Record<string, unknown>;
  runId: string;
  message: string;
};
const tools = [
  { id: "cursor", label: "Crosshair / select", icon: Crosshair },
  { id: "trend", label: "Trend line", icon: TrendingUp },
  { id: "horizontal", label: "Horizontal line", icon: Minus },
  { id: "rectangle", label: "Rectangle", icon: Square },
  { id: "text", label: "Text annotation", icon: Type },
  { id: "measure", label: "Price measurement", icon: Ruler },
] as const;
export default function TradingSimulator() {
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
    seed: "42",
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
    simApi<{ bars: Candle[] }>(
      `/runs/${run.id}/market?symbol=${encodeURIComponent(prefs.symbol)}&interval=${prefs.interval}&cursor=${run.cursor}`,
    )
      .then((data) => {
        if (active) setBars(data.bars);
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
  }, [run?.id, run?.cursor, prefs.symbol, prefs.interval, marketRetry]);
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
        seed: Number(newConfig.seed),
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
  if (loading) return <Loading label="Opening your paper trading terminal…" />;
  if (!run)
    return (
      <div className="page">
        <h1>Trading simulator</h1>
        <p role="alert">{error}</p>
        <button className="button primary" onClick={() => void load()}>
          Reconnect
        </button>
      </div>
    );
  const blocked =
    busy ||
    !!pending ||
    archived ||
    !!marketError ||
    !!connectionError ||
    !bars.length;
  const complete = run.cursor >= run.total_bars - 1;
  const estimate = orderEstimate(run, prefs.symbol, ticket);
  const marketClosed =
    run.config.base_interval === "1D" ||
    new Date(run.clock * 1000).toLocaleTimeString("en-GB", {
      timeZone: "America/New_York",
      hour: "2-digit",
      minute: "2-digit",
    }) === "15:59";
  const feedback = error ? (
    <p className="sim-validation" role="alert">
      {error}
      {pending
        ? " Close this dialog to reconnect and retry the saved action."
        : ""}
    </p>
  ) : null;
  const ticketProps = {
    run,
    symbol: prefs.symbol,
    ticket,
    setTicket: (next: Ticket) => setPrefs({ ticket: next }),
    onPreview: () => {
      setPlaying(false);
      setPreview(true);
    },
    disabled: blocked || complete,
  };
  return (
    <div
      ref={root}
      className={`trading-terminal ${dark ? "dark" : ""} mobile-${mobileTab.toLowerCase()}`}
      style={
        {
          "--sim-right-width": `${prefs.rightWidth}px`,
          "--sim-bottom-height": `${prefs.bottomHeight}px`,
        } as CSSProperties
      }
      data-testid="trading-terminal"
    >
      <header className="sim-account-bar">
        <div className="sim-brand">
          <Activity size={20} />
          <strong>
            quanta<span> / trade</span>
          </strong>
          <span className="sim-paper-badge">PAPER TRADING</span>
        </div>
        <div className="sim-account-metrics">
          <span>
            Equity <strong>{dollars(run.equity)}</strong>
          </span>
          <span>
            Cash <strong>{dollars(run.cash)}</strong>
          </span>
          <span>
            Realized P&L{" "}
            <strong
              className={Number(run.realized) >= 0 ? "sim-up" : "sim-down"}
            >
              {dollars(run.realized)}
            </strong>
          </span>
        </div>
        <Link to="/" className="sim-back">
          <ArrowLeft size={14} /> Learning workspace
        </Link>
      </header>
      <div className="sim-workspace-toolbar">
        <button
          className="sim-symbol-trigger"
          onClick={() => {
            setAddSymbol(false);
            setQuery("");
            setSearchOpen(true);
          }}
        >
          <Search size={15} />
          <strong>{prefs.symbol}</strong>
          <ChevronDown size={12} />
        </button>
        <div
          className="sim-timeframes"
          role="group"
          aria-label="Chart timeframe"
        >
          {(["1m", "5m", "15m", "1h", "1D"] as Interval[]).map((value) => (
            <button
              key={value}
              disabled={run.config.base_interval === "1D" && value !== "1D"}
              title={
                run.config.base_interval === "1D" && value !== "1D"
                  ? "This dataset contains daily bars only"
                  : value
              }
              className={prefs.interval === value ? "active" : ""}
              onClick={() => setPrefs({ interval: value })}
            >
              {value}
            </button>
          ))}
        </div>
        <select
          aria-label="Chart type"
          className="sim-chart-type"
          value={prefs.chartType}
          onChange={(e) =>
            setPrefs({ chartType: e.target.value as Preferences["chartType"] })
          }
        >
          <option value="candles">Candles</option>
          <option value="bars">OHLC bars</option>
          <option value="line">Line</option>
        </select>
        <button
          className="sim-toolbar-button"
          onClick={() => setIndicatorOpen(true)}
        >
          <SlidersHorizontal size={16} />
          <span>Indicators</span>
        </button>
        <button
          className="sim-toolbar-button"
          onClick={() => {
            setPrefs({ rightOpen: true });
            setSideTab("Drawings");
            setMobileTab("Trade");
          }}
        >
          <Layers size={16} />
          <span>Objects</span>
        </button>
        <div className="sim-toolbar-spacer" />
        <button
          className="sim-icon"
          aria-label="Fit chart"
          title="Fit chart"
          onClick={() => setChartAction({ kind: "fit", seq: Date.now() })}
        >
          <Expand size={17} />
        </button>
        <button
          className="sim-icon"
          aria-label="Return to latest bar"
          title="Return to latest bar"
          onClick={() => setChartAction({ kind: "latest", seq: Date.now() })}
        >
          <ChevronRight size={18} />
        </button>
        <button
          className="sim-icon"
          aria-label="Fullscreen chart workspace"
          title="Fullscreen workspace"
          onClick={() => {
            if (document.fullscreenElement) void document.exitFullscreen();
            else void root.current?.requestFullscreen();
          }}
        >
          <Maximize2 size={16} />
        </button>
        <button
          className="sim-icon"
          aria-label={prefs.rightOpen ? "Collapse watchlist" : "Open watchlist"}
          onClick={() => setPrefs({ rightOpen: !prefs.rightOpen })}
        >
          {prefs.rightOpen ? (
            <PanelRightClose size={16} />
          ) : (
            <PanelRightOpen size={16} />
          )}
        </button>
      </div>
      {error ||
      pending ||
      connectionError ||
      marketError ||
      (notice && notice !== "Replay advancing") ? (
        <div
          className={`sim-notice ${error || marketError || connectionError ? "error" : ""}`}
          role={error || marketError || connectionError ? "alert" : "status"}
        >
          <span>
            {error || marketError || connectionError || notice}
            {pending
              ? " Unconfirmed action saved; recover it before placing another trade."
              : ""}
          </span>
          {pending ? (
            <button onClick={() => void retryPending()} disabled={busy}>
              Reconnect & retry action
            </button>
          ) : marketError ? (
            <button onClick={() => setMarketRetry((v) => v + 1)}>
              Retry data
            </button>
          ) : (
            <button
              className="sim-icon"
              aria-label="Dismiss trading notice"
              onClick={() => {
                setError("");
                setNotice("");
              }}
            >
              <X size={14} />
            </button>
          )}
        </div>
      ) : null}
      {archived ? (
        <div className="sim-archive-banner">
          Archived run · review and export only{" "}
          <button
            onClick={() => {
              setPlaying(false);
              void load();
            }}
          >
            Return to current run
          </button>
        </div>
      ) : null}
      <div
        className={`sim-main-grid ${prefs.rightOpen ? "" : "right-collapsed"} ${prefs.bottomOpen ? "" : "bottom-collapsed"}`}
      >
        <nav className="sim-drawing-toolbar" aria-label="Chart tools">
          {tools.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              className={tool === id ? "active" : ""}
              aria-label={label}
              title={label}
              disabled={archived && id !== "cursor"}
              onClick={() => setTool(id)}
            >
              <Icon size={19} />
            </button>
          ))}
          <span className="sim-tool-divider" />
          <button
            aria-label="Undo drawing"
            title="Undo drawing"
            disabled={!history.current.past.length || archived}
            onClick={() => undo()}
            data-version={historyVersion}
          >
            <Undo2 size={18} />
          </button>
          <button
            aria-label="Redo drawing"
            title="Redo drawing"
            disabled={!history.current.future.length || archived}
            onClick={() => undo(true)}
          >
            <Redo2 size={18} />
          </button>
          <div className="sim-tools-bottom">
            <button
              aria-label="Simulator walkthrough"
              title="Help"
              onClick={() => {
                setWalkthrough(0);
                setHelpOpen(true);
              }}
            >
              <CircleHelp size={18} />
            </button>
          </div>
        </nav>
        <div className="sim-chart-region">
          <SimChart
            bars={bars}
            symbol={prefs.symbol}
            interval={prefs.interval}
            chartType={prefs.chartType}
            indicators={prefs.indicators}
            drawings={drawings}
            onDrawings={changeDrawings}
            tool={tool}
            setTool={setTool}
            selected={selectedDrawing}
            onSelect={(id) => {
              setSelectedDrawing(id);
              if (id) {
                setSideTab("Drawings");
                setPrefs({ rightOpen: true });
              }
            }}
            run={run}
            dark={dark}
            onTrade={tradeAt}
            onAmend={(id, field, value) => {
              const order = run.orders.find((o) => o.id === id);
              if (order && !blocked) {
                setPlaying(false);
                setAmendment({
                  order,
                  limit:
                    field === "limit_price"
                      ? value.toFixed(2)
                      : (order.limit_price ?? ""),
                  stop:
                    field === "stop_price"
                      ? value.toFixed(2)
                      : (order.stop_price ?? ""),
                });
              }
            }}
            action={chartAction}
          />
          <div className="sim-replay-bar">
            <button
              className="sim-play-button"
              aria-label={playing ? "Pause replay" : "Play replay"}
              disabled={blocked || complete}
              onClick={() => setPlaying(!playing)}
            >
              {playing ? <Pause size={15} /> : <Play size={15} />}
            </button>
            <button
              className="sim-icon"
              aria-label="Next replay bar"
              title="Next replay bar"
              disabled={blocked || complete}
              onClick={() => {
                setPlaying(false);
                void perform(
                  "advance",
                  { steps: 1 },
                  "POST",
                  "Replay advanced by one bar.",
                );
              }}
            >
              <SkipForward size={17} />
            </button>
            <select
              aria-label="Replay speed"
              value={speed}
              onChange={(e) => setSpeed(Number(e.target.value))}
            >
              <option value={1}>1×</option>
              <option value={5}>5×</option>
              <option value={30}>30×</option>
              <option value={390}>390×</option>
            </select>
            <span className="sim-clock">
              <span className={playing ? "sim-pulse" : ""} />
              {complete
                ? "Replay complete"
                : playing
                  ? "Playing"
                  : "Paused"} · {stamp(run.clock)}
              {marketClosed && !complete
                ? " · Market closed · next session on step"
                : ""}
            </span>
            <progress
              max={run.total_bars - 1}
              value={run.cursor}
              aria-label="Replay progress"
            />
            <span className="sim-replay-count">
              {run.cursor + 1} / {run.total_bars}
            </span>
            <button
              className="sim-icon"
              aria-label="New simulation run"
              title="New simulation run"
              onClick={() => {
                setPlaying(false);
                setResetOpen(true);
              }}
            >
              <RefreshCw size={15} />
            </button>
          </div>
        </div>
        {prefs.rightOpen ? (
          <>
            <div
              className="sim-right-resize"
              role="separator"
              aria-label="Watchlist width"
              aria-valuenow={prefs.rightWidth}
              aria-valuemin={250}
              aria-valuemax={420}
              aria-orientation="vertical"
              tabIndex={0}
              onPointerDown={(e) => resize(e, "right")}
              onKeyDown={(e) => {
                if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
                  e.preventDefault();
                  setPrefs({
                    rightWidth: Math.max(
                      250,
                      Math.min(
                        420,
                        prefs.rightWidth + (e.key === "ArrowLeft" ? 20 : -20),
                      ),
                    ),
                  });
                }
              }}
            />
            <aside className="sim-right-panel">
              <div className="sim-sidebar-tabs">
                {["Watchlist", "Trade", "Drawings"].map((t) => (
                  <button
                    key={t}
                    className={sideTab === t ? "active" : ""}
                    onClick={() => {
                      setSideTab(t);
                      if (t === "Watchlist") setMobileTab("Watchlist");
                    }}
                  >
                    {t}
                  </button>
                ))}
              </div>
              <div
                className={`sim-watchlist ${sideTab === "Watchlist" ? "show" : ""}`}
              >
                <div className="sim-section-title">
                  <strong>Watchlist</strong>
                  <button
                    className="sim-icon"
                    aria-label="Add stock to watchlist"
                    onClick={() => {
                      setAddSymbol(true);
                      setQuery("");
                      setSearchOpen(true);
                    }}
                  >
                    <Plus size={16} />
                  </button>
                </div>
                <div className="sim-watchlist-head">
                  <span>Symbol</span>
                  <span>Last</span>
                  <span>Change %</span>
                </div>
                {prefs.watchlist.map((symbol, index) => {
                  const q = run.quotes.find((q) => q.symbol === symbol);
                  return (
                    <div
                      key={symbol}
                      className={`sim-watchlist-row ${symbol === prefs.symbol ? "selected" : ""}`}
                    >
                      <button onClick={() => chooseSymbol(symbol)}>
                        <strong>
                          <span className={`sim-symbol-logo logo-${index % 4}`}>
                            {symbol[0]}
                          </span>
                          {symbol}
                        </strong>
                        <span>
                          {q ? price(q.close) : "—"}
                          {q ? (
                            <small className="sim-absolute-change">
                              {q.change >= 0 ? "+" : ""}
                              {price(q.change)}
                            </small>
                          ) : null}
                        </span>
                        <span
                          className={
                            q && q.change_pct >= 0 ? "sim-up" : "sim-down"
                          }
                        >
                          {q
                            ? `${q.change_pct >= 0 ? "+" : ""}${q.change_pct.toFixed(2)}%`
                            : "—"}
                        </span>
                      </button>
                      <div className="sim-watchlist-edit">
                        <button
                          aria-label={`Move ${symbol} up`}
                          disabled={index === 0}
                          onClick={() => {
                            const list = [...prefs.watchlist];
                            [list[index - 1], list[index]] = [
                              list[index],
                              list[index - 1],
                            ];
                            setPrefs({ watchlist: list });
                          }}
                        >
                          <ArrowUp size={12} />
                        </button>
                        <button
                          aria-label={`Remove ${symbol} from watchlist`}
                          onClick={() =>
                            setPrefs({
                              watchlist: prefs.watchlist.filter(
                                (s) => s !== symbol,
                              ),
                            })
                          }
                        >
                          <X size={12} />
                        </button>
                      </div>
                    </div>
                  );
                })}
                {!prefs.watchlist.length ? (
                  <p className="sim-small">
                    Your watchlist is empty. Add a stock to follow its price.
                  </p>
                ) : null}
                <div className="sim-symbol-details">
                  <div className="sim-section-title">
                    <strong>{quote?.name ?? prefs.symbol}</strong>
                    <span>{prefs.symbol}</span>
                  </div>
                  <div className="sim-large-price">
                    {quote ? price(quote.close) : "Unavailable"}{" "}
                    <small>USD</small>
                  </div>
                  {quote ? (
                    <p className={quote.change >= 0 ? "sim-up" : "sim-down"}>
                      {quote.change >= 0 ? "+" : ""}
                      {price(quote.change)} ({quote.change_pct.toFixed(2)}%){" "}
                      <span>vs. prior session</span>
                    </p>
                  ) : null}
                  <p className="sim-small">
                    {run.config.mode === "synthetic"
                      ? "Synthetic market · fictional prices"
                      : "Historical replay · imported prices"}
                    <br />
                    {stamp(run.clock)}
                  </p>
                  <div className="sim-quick-trade">
                    <button
                      className="buy"
                      onClick={() => {
                        setPrefs({ ticket: { ...ticket, side: "buy" } });
                        setSideTab("Trade");
                        setMobileTab("Trade");
                      }}
                    >
                      Buy
                    </button>
                    <button
                      className="sell"
                      onClick={() => {
                        setPrefs({ ticket: { ...ticket, side: "sell" } });
                        setSideTab("Trade");
                        setMobileTab("Trade");
                      }}
                    >
                      Sell
                    </button>
                  </div>
                </div>
              </div>
              {sideTab === "Drawings" ? (
                <DrawingsPanel
                  drawings={drawings}
                  onChange={changeDrawings}
                  selected={selectedDrawing}
                  onSelect={setSelectedDrawing}
                  bars={bars}
                  disabled={archived}
                />
              ) : null}
              <div
                className={`sim-ticket-wrap ${sideTab === "Trade" ? "show" : ""}`}
              >
                <OrderTicket {...ticketProps} />
              </div>
            </aside>
          </>
        ) : null}
        {prefs.bottomOpen ? (
          <>
            <div
              className="sim-bottom-resize"
              role="separator"
              aria-label="Trading panel height"
              aria-valuenow={prefs.bottomHeight}
              aria-valuemin={130}
              aria-valuemax={420}
              aria-orientation="horizontal"
              tabIndex={0}
              onPointerDown={(e) => resize(e, "bottom")}
              onKeyDown={(e) => {
                if (e.key === "ArrowUp" || e.key === "ArrowDown") {
                  e.preventDefault();
                  setPrefs({
                    bottomHeight: Math.max(
                      130,
                      Math.min(
                        420,
                        prefs.bottomHeight + (e.key === "ArrowUp" ? 20 : -20),
                      ),
                    ),
                  });
                }
              }}
            />
            <div className="sim-bottom-panel">
              <PortfolioPanel
                run={run}
                tab={tab}
                setTab={setTab}
                onSymbol={chooseSymbol}
                onClose={closePosition}
                onCancel={(id) => {
                  setPlaying(false);
                  void perform(
                    `orders/${id}/cancel`,
                    {},
                    "POST",
                    "Order remainder canceled.",
                  );
                }}
                onAmend={(order) => {
                  setPlaying(false);
                  setAmendment({
                    order,
                    limit: order.limit_price ?? "",
                    stop: order.stop_price ?? "",
                  });
                }}
                onJournal={setJournal}
                onCollapse={() => setPrefs({ bottomOpen: false })}
                disabled={blocked}
              />
            </div>
          </>
        ) : null}
      </div>
      <footer className="sim-statusbar">
        <span className="sim-status-dot" />
        {connectionError
          ? "Disconnected"
          : run.guest
            ? "Guest · saved for this browser"
            : "Account synced"}
        <span className="sim-status-separator">|</span>
        <span>
          {run.config.mode === "synthetic"
            ? "Seeded synthetic · " + run.config.seed
            : "Imported historical"}
        </span>
        <button className="sim-text-button" onClick={() => setHelpOpen(true)}>
          Execution model
        </button>
        <span className="sim-footer-spacer" />
        <span>{saveStatus}</span>
        <select
          aria-label="Simulation run history"
          disabled={busy || !!pending}
          value={run.id}
          onChange={(e) => {
            setPlaying(false);
            void load(e.target.value);
          }}
        >
          {boot?.runs.map((r, i) => (
            <option key={r.id} value={r.id}>
              {i === 0 ? "Current" : "Archived"} ·{" "}
              {new Date(r.created_at).toLocaleString()}
            </option>
          ))}
        </select>
        <button
          className="sim-icon"
          aria-label="Export simulation"
          onClick={() => setExportOpen(true)}
        >
          <Download size={14} />
        </button>
        {!prefs.bottomOpen ? (
          <button
            className="sim-icon"
            aria-label="Open trading panel"
            onClick={() => setPrefs({ bottomOpen: true })}
          >
            <PanelBottomOpen size={16} />
          </button>
        ) : null}
      </footer>
      <div className="sim-mobile-trade-entry">
        <span>
          {prefs.symbol} · {quote ? price(quote.close) : "Unavailable"}
        </span>
        {(["buy", "sell"] as const).map((side) => (
          <button
            key={side}
            className={side}
            onClick={() => {
              setPrefs({ rightOpen: true, ticket: { ...ticket, side } });
              setSideTab("Trade");
              setMobileTab("Trade");
            }}
          >
            {side === "buy" ? "Buy" : "Sell"}
          </button>
        ))}
      </div>
      <nav className="sim-mobile-nav" aria-label="Simulator navigation">
        {[
          { name: "Chart", icon: Activity },
          { name: "Watchlist", icon: List },
          { name: "Trade", icon: ArrowUp },
          { name: "Portfolio", icon: Layers },
        ].map(({ name, icon: Icon }) => (
          <button
            key={name}
            className={mobileTab === name ? "active" : ""}
            onClick={() => {
              setMobileTab(name);
              if (name === "Trade" || name === "Watchlist") {
                setPrefs({ rightOpen: true });
                setSideTab(name);
              }
              if (name === "Portfolio") setPrefs({ bottomOpen: true });
            }}
          >
            <Icon size={17} />
            {name}
          </button>
        ))}
      </nav>
      <Modal
        container={root.current}
        open={searchOpen}
        onOpenChange={setSearchOpen}
        title={addSymbol ? "Add to watchlist" : "Find a stock"}
        description="Available symbols in this simulation. Prices follow the selected replay clock."
      >
        <label className="sim-search">
          <Search size={18} />
          <input
            autoFocus
            aria-label="Search stocks"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ticker or company name"
          />
        </label>
        {!run.quotes.some((q) =>
          `${q.symbol} ${q.name}`.toLowerCase().includes(query.toLowerCase()),
        ) ? (
          <p className="sim-small">
            No matching stock is available in this run.
          </p>
        ) : null}
        <div className="sim-search-results">
          {run.quotes
            .filter((q) =>
              `${q.symbol} ${q.name}`
                .toLowerCase()
                .includes(query.toLowerCase()),
            )
            .map((q) => (
              <button
                key={q.symbol}
                onClick={() => {
                  if (addSymbol) {
                    setPrefs({
                      watchlist: [...new Set([...prefs.watchlist, q.symbol])],
                    });
                    setSearchOpen(false);
                  } else chooseSymbol(q.symbol);
                }}
              >
                <strong>{q.symbol}</strong>
                <span>{q.name}</span>
                <span>{price(q.close)}</span>
                {addSymbol && prefs.watchlist.includes(q.symbol) ? (
                  <Check size={15} />
                ) : (
                  <ChevronRight size={15} />
                )}
              </button>
            ))}
        </div>
      </Modal>
      <Modal
        container={root.current}
        open={preview}
        onOpenChange={setPreview}
        title={`Preview ${ticket.side} order`}
        description={`${prefs.symbol} · ${ticket.kind.replace("_", "-")} · ${ticket.tif}`}
      >
        {feedback}
        <div className="sim-preview">
          <strong>
            {ticket.quantity} shares of {prefs.symbol}
          </strong>
          <p>
            {ticket.kind === "market"
              ? "Fill at the next eligible market price"
              : `Limit ${ticket.limit || "—"} · Stop ${ticket.stop || "—"}`}
          </p>
          <p>
            Commission: {dollars(run.config.commission)} per order. Cash and
            shares are reserved when accepted. Fills depend on the next bar and
            available liquidity.
          </p>
          <dl className="sim-preview-estimates">
            <div>
              <dt>Estimated notional</dt>
              <dd>{dollars(estimate.notional)}</dd>
            </div>
            <div>
              <dt>Estimated {ticket.side === "buy" ? "debit" : "proceeds"}</dt>
              <dd>{dollars(estimate.total)}</dd>
            </div>
            <div>
              <dt>Available cash / reserved</dt>
              <dd>
                {dollars(run.available)} / {dollars(run.reserved)}
              </dd>
            </div>
            <div>
              <dt>Available shares</dt>
              <dd>{estimate.availableShares}</dd>
            </div>
            <div>
              <dt>Position after full fill</dt>
              <dd>{estimate.after} shares</dd>
            </div>
          </dl>
          {ticket.note ? <blockquote>{ticket.note}</blockquote> : null}
        </div>
        <button
          className={`sim-submit ${ticket.side}`}
          disabled={blocked || complete}
          onClick={() => void submitOrder()}
        >
          {busy ? "Submitting…" : `Place ${ticket.side} order`}
        </button>
      </Modal>
      <Modal
        container={root.current}
        open={!!amendment}
        onOpenChange={(v) => {
          if (!v) setAmendment(null);
        }}
        title="Confirm order amendment"
        description="The existing order remains unchanged until the amendment is accepted."
      >
        {feedback}
        {amendment ? (
          <form
            onSubmit={async (e) => {
              e.preventDefault();
              const result = await perform(
                `orders/${amendment.order.id}/amend`,
                {
                  ...(amendment.order.limit_price
                    ? { limit_price: amendment.limit }
                    : {}),
                  ...(amendment.order.stop_price
                    ? { stop_price: amendment.stop }
                    : {}),
                },
                "POST",
                "Order amendment confirmed.",
              );
              if (result) setAmendment(null);
            }}
          >
            {amendment.order.limit_price ? (
              <label className="sim-field">
                New limit price
                <input
                  type="number"
                  min="0.01"
                  step="0.01"
                  required
                  value={amendment.limit}
                  onChange={(e) =>
                    setAmendment({ ...amendment, limit: e.target.value })
                  }
                />
              </label>
            ) : null}
            {amendment.order.stop_price ? (
              <label className="sim-field">
                New stop price
                <input
                  type="number"
                  min="0.01"
                  step="0.01"
                  required
                  value={amendment.stop}
                  onChange={(e) =>
                    setAmendment({ ...amendment, stop: e.target.value })
                  }
                />
              </label>
            ) : null}
            <button className="sim-submit buy" disabled={busy || !!pending}>
              Confirm amendment
            </button>
          </form>
        ) : null}
      </Modal>
      <Modal
        container={root.current}
        open={!!journal}
        onOpenChange={(v) => {
          if (!v) setJournal(null);
        }}
        title="Trade journal"
        description={
          journal
            ? `${journal.side.toUpperCase()} ${journal.quantity} ${journal.symbol}`
            : ""
        }
      >
        {feedback}
        {journal ? (
          <form
            onSubmit={async (e) => {
              e.preventDefault();
              const result = await perform(
                `orders/${journal.id}/journal`,
                { note: journal.note, lesson: journal.lesson },
                "PUT",
                "Trade journal saved.",
              );
              if (result) setJournal(null);
            }}
          >
            <label className="sim-field">
              Trade thesis
              <textarea
                rows={6}
                maxLength={2000}
                value={journal.note}
                onChange={(e) =>
                  setJournal({ ...journal, note: e.target.value })
                }
              />
            </label>
            <label className="sim-field">
              Linked lesson
              <select
                value={journal.lesson}
                onChange={(e) =>
                  setJournal({ ...journal, lesson: e.target.value })
                }
              >
                <option value="">No lesson</option>
                {["0.4", "0.5", "0.7", "0.8"].map((id) => (
                  <option key={id}>{id}</option>
                ))}
              </select>
            </label>
            <button className="sim-submit buy" disabled={blocked}>
              Save journal
            </button>
          </form>
        ) : null}
      </Modal>
      <Modal
        container={root.current}
        open={indicatorOpen}
        onOpenChange={setIndicatorOpen}
        title="Indicators"
        description="Calculated only from bars already available in replay. At most eight indicators."
      >
        {prefs.indicators.map((i) => (
          <div className="sim-indicator-editor" key={i.id}>
            <strong>{i.kind}</strong>
            <button
              className="sim-icon"
              aria-label={`${i.visible ? "Hide" : "Show"} ${i.kind}`}
              onClick={() =>
                setPrefs({
                  indicators: prefs.indicators.map((item) =>
                    item.id === i.id ? { ...item, visible: !i.visible } : item,
                  ),
                })
              }
            >
              {i.visible ? <Eye size={16} /> : <EyeOff size={16} />}
            </button>
            <button
              className="sim-icon"
              aria-label={`Remove ${i.kind}`}
              onClick={() =>
                setPrefs({
                  indicators: prefs.indicators.filter(
                    (item) => item.id !== i.id,
                  ),
                })
              }
            >
              <X size={16} />
            </button>
            {i.kind !== "Volume" ? (
              <label className="sim-field">
                {i.kind === "MACD" ? "Fast period" : "Period"}
                <input
                  type="number"
                  min={2}
                  max={200}
                  value={i.period}
                  onChange={(e) => {
                    const period = Number(e.target.value);
                    if (
                      Number.isInteger(period) &&
                      period >= 2 &&
                      period <= 200
                    )
                      setPrefs({
                        indicators: prefs.indicators.map((item) =>
                          item.id === i.id ? { ...item, period } : item,
                        ),
                      });
                  }}
                />
              </label>
            ) : null}
            {i.kind === "MACD"
              ? (["slow", "signal"] as const).map((field) => (
                  <label className="sim-field" key={field}>
                    {field} period
                    <input
                      type="number"
                      min={2}
                      max={200}
                      value={i[field]}
                      onChange={(e) => {
                        const n = Number(e.target.value);
                        if (Number.isInteger(n) && n >= 2 && n <= 200)
                          setPrefs({
                            indicators: prefs.indicators.map((item) =>
                              item.id === i.id ? { ...item, [field]: n } : item,
                            ),
                          });
                      }}
                    />
                  </label>
                ))
              : null}
          </div>
        ))}
        <label className="sim-field">
          Add indicator
          <select
            value=""
            disabled={prefs.indicators.length >= 8}
            onChange={(e) => {
              const kind = e.target.value as Indicator["kind"];
              setPrefs({
                indicators: [
                  ...prefs.indicators,
                  {
                    id: crypto.randomUUID(),
                    kind,
                    period: kind === "RSI" ? 14 : kind === "MACD" ? 12 : 20,
                    slow: 26,
                    signal: 9,
                    visible: true,
                  },
                ],
              });
            }}
          >
            <option value="" disabled>
              Select an indicator
            </option>
            {["SMA", "EMA", "Volume", "RSI", "MACD"].map((k) => (
              <option key={k}>{k}</option>
            ))}
          </select>
        </label>
      </Modal>
      <Modal
        container={root.current}
        open={resetOpen}
        onOpenChange={setResetOpen}
        title="Start a new simulation"
        description="Create a fresh $100,000 paper account. This run and its trade history remain available in the run selector."
      >
        {feedback}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            void startRun();
          }}
        >
          <label className="sim-field">
            Market data
            <select
              value={newConfig.mode}
              onChange={(e) =>
                setNewConfig({
                  ...newConfig,
                  mode: e.target.value,
                  symbol: boot?.historical[0]?.symbol ?? "",
                })
              }
            >
              <option value="synthetic">Seeded synthetic market</option>
              <option value="historical" disabled={!boot?.historical.length}>
                Historical replay
                {!boot?.historical.length ? " · no imported datasets" : ""}
              </option>
            </select>
          </label>
          {newConfig.mode === "synthetic" ? (
            <label className="sim-field">
              Random seed
              <input
                type="number"
                min={0}
                max={1000000}
                required
                value={newConfig.seed}
                onChange={(e) =>
                  setNewConfig({ ...newConfig, seed: e.target.value })
                }
              />
            </label>
          ) : (
            <label className="sim-field">
              Historical stock
              <select
                value={newConfig.symbol}
                onChange={(e) =>
                  setNewConfig({ ...newConfig, symbol: e.target.value })
                }
              >
                {boot?.historical.map((d) => (
                  <option key={d.symbol}>{d.symbol}</option>
                ))}
              </select>
            </label>
          )}
          <div className="sim-field-pair">
            {(
              [
                {
                  key: "commission",
                  label: "Commission / order ($)",
                  step: "0.01",
                  max: 100,
                  min: 0,
                },
                {
                  key: "slippage_bps",
                  label: "Slippage (bps)",
                  step: "0.1",
                  max: 100,
                  min: 0,
                },
                {
                  key: "spread_bps",
                  label: "Spread (bps)",
                  step: "0.1",
                  max: 100,
                  min: 0,
                },
                {
                  key: "participation",
                  label: "Volume participation (0–1)",
                  step: "0.001",
                  max: 1,
                  min: 0.001,
                },
              ] as const
            ).map((f) => (
              <label key={f.key} className="sim-field">
                {f.label}
                <input
                  type="number"
                  step={f.step}
                  min={f.min}
                  max={f.max}
                  required
                  value={newConfig[f.key]}
                  onChange={(e) =>
                    setNewConfig({ ...newConfig, [f.key]: e.target.value })
                  }
                />
              </label>
            ))}
          </div>
          <p className="sim-small">
            Long-only, whole-share practice. Immediate settlement is a teaching
            simplification. Historical corporate-action treatment comes from the
            imported dataset.
          </p>
          <button className="sim-submit buy" disabled={busy}>
            Create new paper account
          </button>
        </form>
      </Modal>
      <Modal
        container={root.current}
        open={helpOpen}
        onOpenChange={setHelpOpen}
        title="A workspace for learning to trade"
        description="Paper money. Real decisions to practice."
      >
        <div className="sim-walkthrough">
          <span className="eyebrow">STEP {walkthrough + 1} OF 4</span>
          <h3>
            {
              [
                "Find your market",
                "Read the chart",
                "Place a paper order",
                "Review your process",
              ][walkthrough]
            }
          </h3>
          <p>
            {
              [
                "Choose a stock from the watchlist or symbol search. Synthetic prices are fictional; historical replay uses an installed dataset. The clock always shows what information is available.",
                "Pan, zoom, change the timeframe, and add indicators. Use the left drawing tools or the Objects form. Two clicks create a trend line; Escape cancels a tool.",
                "Open Buy or Sell, choose an order type, and preview it. Your account starts with $100,000. Advance replay to process orders on the next eligible bar.",
                "Open Positions and Trade history. Link a thesis to your trade, compare the outcome to the plan, and export the run. A profitable result alone does not establish a sound decision.",
              ][walkthrough]
            }
          </p>
          <button
            className="sim-outline"
            onClick={() =>
              walkthrough < 3
                ? setWalkthrough((v) => v + 1)
                : setHelpOpen(false)
            }
          >
            {walkthrough < 3 ? "Next step" : "Start exploring"}
            <ChevronRight size={16} />
          </button>
        </div>
        <details className="sim-model-details">
          <summary>Execution and accounting model</summary>
          <p>
            FIFO order arrival within each symbol; all orders share a{" "}
            {Number(run.config.participation) * 100}% bar-volume cap. Market
            orders fill at the next bar open, plus {run.config.slippage_bps} bps
            slippage and half of the {run.config.spread_bps} bps spread. Limit
            fills never violate the limit; a touch alone does not fill.
          </p>
          <p>
            Stop-market orders can gap beyond the trigger. Stop-limit orders
            activate on a trigger bar and cannot fill until a later bar, because
            OHLC data does not reveal the intrabar path. DAY orders entered
            during a session expire at its final bar; orders entered after the
            close apply to the next session. Daily replay timestamps label the
            completed session, not the exact intraday fill time. Cash settles
            immediately in this teaching model.
          </p>
          <p>
            Weighted-average cost includes the entry fee; realized P&L deducts
            the exit fee. The flat {dollars(run.config.commission)} commission
            is charged once, on the first fill of each order. No Level 2 order
            book is inferred from bars. Synthetic sessions omit exchange
            holidays.
          </p>
          <p>
            {run.config.source}. Historical splits and dividends are not applied
            by this engine; import adjusted OHLC prices, or explicitly account
            for this limitation when reviewing returns.
          </p>
          <Link className="sim-text-button" to="/learn/0.4">
            Review order types
          </Link>{" "}
          ·{" "}
          <Link className="sim-text-button" to="/learn/0.7">
            Review risk and sizing
          </Link>
        </details>
      </Modal>
      <Modal
        container={root.current}
        open={exportOpen}
        onOpenChange={setExportOpen}
        title="Export simulation"
        description="Exports include confirmed history and observed market data only."
      >
        <button
          className="sim-outline"
          onClick={() =>
            download(`quanta-simulation-${run.id}.json`, {
              ...run,
              preferences: prefs,
              bars,
            })
          }
        >
          <Download size={16} /> Run, chart settings & journal (JSON)
        </button>
        <p className="sim-small">
          Use the export icon on each trading-panel tab for its CSV file.
          Archived runs remain available in the run selector.
        </p>
      </Modal>
    </div>
  );
}
