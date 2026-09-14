import { useEffect, useMemo, useRef, useState } from "react";
import {
  BarSeries,
  CandlestickSeries,
  ColorType,
  createChart,
  createSeriesMarkers,
  HistogramSeries,
  LineSeries,
  LineStyle,
  TickMarkType,
} from "lightweight-charts";
import type {
  IChartApi,
  ISeriesApi,
  ISeriesMarkersPluginApi,
  SeriesType,
  Time,
  UTCTimestamp,
} from "lightweight-charts";
import { ema, macd, price, rsi, sma, working } from "../../lib/simulator";
import type {
  Candle,
  Drawing,
  DrawingKind,
  Indicator,
  Interval,
  SimRun,
} from "../../lib/simulator";

type Props = {
  bars: Candle[];
  symbol: string;
  interval: Interval;
  chartType: "candles" | "bars" | "line";
  indicators: Indicator[];
  drawings: Drawing[];
  onDrawings: (d: Drawing[]) => void;
  tool: DrawingKind | "cursor";
  setTool: (t: DrawingKind | "cursor") => void;
  selected: string | null;
  onSelect: (id: string | null) => void;
  run: SimRun;
  dark: boolean;
  onTrade: (p: number) => void;
  onAmend: (
    id: string,
    field: "limit_price" | "stop_price",
    value: number,
  ) => void;
  action: { kind: "fit" | "latest"; seq: number };
};
const colors = ["#e3a63f", "#599bf3", "#ba83f3", "#43b4a0", "#e485ad"];
export default function SimChart(props: Props) {
  const host = useRef<HTMLDivElement>(null),
    chart = useRef<IChartApi | null>(null),
    series = useRef<ISeriesApi<SeriesType> | null>(null),
    markers = useRef<ISeriesMarkersPluginApi<UTCTimestamp> | null>(null);
  const indicatorSeries = useRef<
    { indicator: Indicator; series: ISeriesApi<SeriesType>[] }[]
  >([]);
  const live = useRef(props);
  live.current = props;
  const [hover, setHover] = useState<Candle | null>(null),
    [epoch, setEpoch] = useState(0),
    [draft, setDraft] = useState<Drawing | null>(null);
  const start = useRef<{ time: number; value: number } | null>(null),
    drag = useRef<{
      drawing: Drawing;
      start: { time: number; value: number };
    } | null>(null);
  const [orderDrag, setOrderDrag] = useState<{
    id: string;
    field: "limit_price" | "stop_price";
    price: number;
  } | null>(null);
  const orderDragRef = useRef(orderDrag);
  orderDragRef.current = orderDrag;
  const refresh = useRef<number | null>(null);
  const indicatorKey = JSON.stringify(props.indicators);
  useEffect(() => {
    if (!host.current) return;
    const chartApi = createChart(host.current, {
      autoSize: true,
      layout: {
        background: {
          type: ColorType.Solid,
          color: props.dark ? "#101722" : "#ffffff",
        },
        textColor: props.dark ? "#8592a6" : "#68778b",
        fontFamily: "Inter, sans-serif",
        fontSize: 11,
        attributionLogo: true,
        panes: {
          separatorColor: props.dark ? "#253042" : "#e3e7ed",
          separatorHoverColor: "#4778bc",
          enableResize: true,
        },
      },
      grid: {
        vertLines: { color: props.dark ? "#192232" : "#f0f3f7" },
        horzLines: { color: props.dark ? "#192232" : "#f0f3f7" },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
        borderColor: props.dark ? "#263044" : "#e2e6ed",
        rightOffset: 8,
        tickMarkFormatter: (time: Time, kind: TickMarkType) =>
          typeof time !== "number"
            ? null
            : new Date(time * 1000).toLocaleString("en-US", {
                timeZone: "America/New_York",
                ...(kind === TickMarkType.Time ||
                kind === TickMarkType.TimeWithSeconds
                  ? { hour: "2-digit", minute: "2-digit", hour12: false }
                  : kind === TickMarkType.Year
                    ? { year: "numeric" }
                    : kind === TickMarkType.Month
                      ? { month: "short", year: "2-digit" }
                      : { month: "short", day: "numeric" }),
              }),
      },
      rightPriceScale: { borderColor: props.dark ? "#263044" : "#e2e6ed" },
      crosshair: {
        mode: 0,
        vertLine: { color: "#758499", labelBackgroundColor: "#354763" },
        horzLine: { color: "#758499", labelBackgroundColor: "#354763" },
      },
      handleScroll: { vertTouchDrag: false, horzTouchDrag: true },
      localization: {
        locale: "en-US",
        timeFormatter: (time: Time) =>
          typeof time === "number"
            ? new Date(time * 1000).toLocaleString("en-US", {
                timeZone: "America/New_York",
              }) + " ET"
            : String(time),
      },
    });
    chart.current = chartApi;
    setHover(null);
    const definition =
      props.chartType === "candles"
        ? CandlestickSeries
        : props.chartType === "bars"
          ? BarSeries
          : LineSeries;
    const base = chartApi.addSeries(definition, {
      upColor: "#20a78d",
      downColor: "#e76676",
      borderVisible: false,
      wickUpColor: "#20a78d",
      wickDownColor: "#e76676",
      color: "#5b91e5",
      lineWidth: 2,
    });
    series.current = base;
    markers.current = createSeriesMarkers(
      base as ISeriesApi<SeriesType, UTCTimestamp>,
      [],
    );
    let pane = 1;
    indicatorSeries.current = props.indicators
      .filter((i) => i.visible)
      .map((indicator, i) => {
        if (indicator.kind === "Volume") {
          const volume = chartApi.addSeries(HistogramSeries, {
            priceFormat: { type: "volume" },
            priceScaleId: "volume",
            lastValueVisible: false,
            priceLineVisible: false,
          });
          volume.priceScale().applyOptions({
            scaleMargins: { top: 0.83, bottom: 0 },
            visible: false,
          });
          return { indicator, series: [volume] };
        }
        const separate = indicator.kind === "RSI" || indicator.kind === "MACD";
        const index = separate ? pane++ : 0;
        const line = chartApi.addSeries(
          LineSeries,
          {
            color: colors[i % colors.length],
            lineWidth: 1,
            priceLineVisible: false,
            lastValueVisible: false,
            title: indicator.kind,
          },
          index,
        );
        const list: ISeriesApi<SeriesType>[] = [line];
        if (indicator.kind === "MACD") {
          list.push(
            chartApi.addSeries(
              LineSeries,
              {
                color: "#eb9a4e",
                lineWidth: 1,
                priceLineVisible: false,
                lastValueVisible: false,
              },
              index,
            ),
          );
          list.push(
            chartApi.addSeries(
              HistogramSeries,
              { priceLineVisible: false, lastValueVisible: false },
              index,
            ),
          );
        }
        if (indicator.kind === "RSI")
          for (const value of [30, 70])
            line.createPriceLine({
              price: value,
              color: "#8491a3",
              lineWidth: 1,
              lineStyle: LineStyle.Dashed,
              axisLabelVisible: false,
              title: "",
            });
        return { indicator, series: list };
      });
    for (const p of chartApi.panes().slice(1)) p.setHeight(95);
    function redraw() {
      if (refresh.current === null)
        refresh.current = requestAnimationFrame(() => {
          refresh.current = null;
          setEpoch((v) => v + 1);
        });
    }
    chartApi.timeScale().subscribeVisibleLogicalRangeChange(redraw);
    chartApi.timeScale().subscribeSizeChange(redraw);
    chartApi.subscribeCrosshairMove((param) => {
      setHover(
        param.time
          ? (live.current.bars.find((b) => b.time === Number(param.time)) ??
              null)
          : null,
      );
      redraw();
    });
    setEpoch((v) => v + 1);
    return () => {
      if (refresh.current !== null) cancelAnimationFrame(refresh.current);
      refresh.current = null;
      markers.current = null;
      chartApi.remove();
      chart.current = null;
      series.current = null;
      start.current = null;
    };
    // Rebuild only structural changes; replay updates series in place.
  }, [props.symbol, props.interval, props.chartType, indicatorKey, props.dark]);
  useEffect(() => {
    if (!series.current || !props.bars.length) return;
    const data = props.bars.map((b) => ({
      ...b,
      time: b.time as UTCTimestamp,
    }));
    series.current.setData(
      props.chartType === "line"
        ? data.map((b) => ({ time: b.time, value: b.close }))
        : data,
    );
    const values = props.bars.map((b) => b.close);
    const points = (v: (number | null)[]) =>
      v.flatMap((value, i) =>
        value === null ? [] : [{ time: data[i].time, value }],
      );
    for (const entry of indicatorSeries.current) {
      const { indicator: i, series: list } = entry;
      if (i.kind === "Volume")
        list[0].setData(
          data.map((b) => ({
            time: b.time,
            value: b.volume,
            color: b.close >= b.open ? "#20a78d35" : "#e7667635",
          })),
        );
      if (i.kind === "SMA") list[0].setData(points(sma(values, i.period)));
      if (i.kind === "EMA") list[0].setData(points(ema(values, i.period)));
      if (i.kind === "RSI") list[0].setData(points(rsi(values, i.period)));
      if (i.kind === "MACD") {
        const m = macd(values, i.period, i.slow, i.signal);
        list[0].setData(points(m.line));
        list[1].setData(points(m.signal));
        list[2].setData(
          points(m.histogram).map((p) => ({
            ...p,
            color: p.value >= 0 ? "#20a78d70" : "#e7667670",
          })),
        );
      }
    }
    if (chart.current?.timeScale().getVisibleLogicalRange() === null)
      chart.current?.timeScale().fitContent();
    setEpoch((v) => v + 1);
  }, [
    props.bars,
    props.chartType,
    indicatorKey,
    props.symbol,
    props.interval,
    props.dark,
  ]);
  useEffect(() => {
    if (!markers.current) return;
    const times = props.bars.map((b) => b.time);
    const entries = props.run.fills
      .filter((f) => f.symbol === props.symbol)
      .flatMap((f) => {
        const time = [...times].reverse().find((t) => t <= f.time);
        return time
          ? [
              {
                time: time as UTCTimestamp,
                position:
                  f.side === "buy"
                    ? ("belowBar" as const)
                    : ("aboveBar" as const),
                color: f.side === "buy" ? "#20a78d" : "#e76676",
                shape:
                  f.side === "buy"
                    ? ("arrowUp" as const)
                    : ("arrowDown" as const),
                text: `${f.side.toUpperCase()} ${f.quantity} @ ${f.price}`,
              },
            ]
          : [];
      });
    markers.current.setMarkers(entries);
  }, [
    props.bars,
    props.run.fills,
    props.symbol,
    props.interval,
    props.chartType,
    props.dark,
    indicatorKey,
  ]);
  useEffect(() => {
    if (props.action.kind === "fit") chart.current?.timeScale().fitContent();
    else chart.current?.timeScale().scrollToRealTime();
  }, [props.action]);
  useEffect(() => {
    if (props.tool === "cursor") {
      start.current = null;
      setDraft(null);
    }
  }, [props.tool]);
  const geometry = useMemo(() => {
    const x = (t: number) => {
      // Anchor across aggregated timeframes and session gaps.
      let low = 0,
        high = props.bars.length - 1;
      while (low < high) {
        const mid = Math.ceil((low + high) / 2);
        if (props.bars[mid].time <= t) low = mid;
        else high = mid - 1;
      }
      const time = props.bars[low]?.time;
      return time === undefined
        ? null
        : (chart.current?.timeScale().timeToCoordinate(time as UTCTimestamp) ??
            null);
    };
    const y = (p: number) => series.current?.priceToCoordinate(p) ?? null;
    return [
      ...props.drawings.filter((d) => d.id !== draft?.id),
      ...(draft ? [draft] : []),
    ].map((d) => ({
      ...d,
      x1: x(d.t1),
      x2: x(d.t2),
      y1: y(d.p1),
      y2: y(d.p2),
    }));
  }, [props.drawings, props.bars, draft, epoch]);
  const point = (event: React.PointerEvent | React.MouseEvent) => {
    const rect = host.current?.getBoundingClientRect();
    if (!rect) return null;
    const time = chart.current
      ?.timeScale()
      .coordinateToTime(event.clientX - rect.left);
    const value = series.current?.coordinateToPrice(event.clientY - rect.top);
    return time && value != null
      ? { time: Number(time), value: Number(value.toFixed(2)) }
      : null;
  };
  const clickStart = useRef({ x: 0, y: 0 });
  function placeDrawing(point: { time: number; value: number }) {
    if (props.tool === "cursor") return;
    if (!start.current && !["horizontal", "text"].includes(props.tool)) {
      start.current = point;
      setDraft({
        id: "draft",
        kind: props.tool,
        t1: point.time,
        t2: point.time,
        p1: point.value,
        p2: point.value,
        text: "",
        color: "#668de8",
        locked: false,
      });
      return;
    }
    const first = start.current ?? point;
    const drawing: Drawing = {
      id: crypto.randomUUID(),
      kind: props.tool,
      t1: first.time,
      t2: point.time,
      p1: first.value,
      p2: point.value,
      text: props.tool === "text" ? "Chart note" : "",
      color: "#668de8",
      locked: false,
    };
    props.onDrawings([...props.drawings, drawing]);
    props.onSelect(drawing.id);
    props.setTool("cursor");
    start.current = null;
    setDraft(null);
  }
  const shown = hover ?? props.bars.at(-1);
  return (
    <div
      className={`sim-chart-container ${props.tool !== "cursor" ? "drawing-active" : ""}`}
      onPointerDownCapture={(e) => {
        clickStart.current = { x: e.clientX, y: e.clientY };
      }}
      onClick={(e) => {
        if (
          props.tool === "cursor" ||
          !(e.target as Element).closest(".sim-chart-canvas")
        )
          return;
        if (
          Math.abs(e.clientX - clickStart.current.x) +
            Math.abs(e.clientY - clickStart.current.y) >
          5
        )
          return;
        const top = host.current?.getBoundingClientRect().top ?? 0;
        if (e.clientY - top > (chart.current?.panes()[0]?.getHeight() ?? 0))
          return;
        const p = point(e);
        if (p) placeDrawing(p);
      }}
      onPointerMove={(e) => {
        if (start.current && props.tool !== "cursor") {
          const p = point(e);
          if (p)
            setDraft((d) => (d ? { ...d, t2: p.time, p2: p.value } : null));
        }
      }}
      onContextMenu={(e) => {
        e.preventDefault();
        const p = point(e);
        if (p) props.onTrade(p.value);
      }}
    >
      <div className="sim-chart-readout" aria-live="off">
        <strong>{props.symbol}</strong>
        <span>
          · {props.interval} · ET ·{" "}
          {props.run.config.mode === "synthetic" ? "SYNTHETIC" : "HISTORICAL"}
        </span>
        {shown ? (
          <span className={shown.close >= shown.open ? "sim-up" : "sim-down"}>
            O {price(shown.open)} &nbsp;H {price(shown.high)} &nbsp;L{" "}
            {price(shown.low)} &nbsp;C {price(shown.close)}{" "}
            <span className="sim-volume-readout">
              &nbsp;Vol {shown.volume.toLocaleString()}
            </span>
          </span>
        ) : null}
      </div>
      <div className="sim-indicator-legend">
        {props.indicators
          .filter((i) => i.visible)
          .map((i, n) => (
            <span key={i.id} style={{ color: colors[n % colors.length] }}>
              {i.kind} {i.kind === "Volume" ? "" : i.period}
              {props.bars.length <
              (i.kind === "Volume"
                ? 1
                : i.kind === "RSI"
                  ? i.period + 1
                  : i.kind === "MACD"
                    ? Math.max(i.period, i.slow) + i.signal - 1
                    : i.period)
                ? " · warming up"
                : ""}
            </span>
          ))}
      </div>
      <div
        ref={host}
        className="sim-chart-canvas"
        aria-label={`${props.symbol} ${props.interval} price chart`}
        role="img"
      />
      <svg
        className="sim-drawing-overlay"
        aria-label="Chart drawings"
        onPointerMove={(e) => {
          const p = point(e);
          if (!p) return;
          if (drag.current) {
            const d = drag.current.drawing;
            const delta = p.time - drag.current.start.time;
            const change = p.value - drag.current.start.value;
            setDraft({
              ...d,
              t1: d.t1 + delta,
              t2: d.t2 + delta,
              p1: d.p1 + change,
              p2: d.p2 + change,
            });
          }
          if (orderDragRef.current)
            setOrderDrag({ ...orderDragRef.current, price: p.value });
        }}
        onPointerUp={(e) => {
          if (drag.current && draft) {
            props.onDrawings(
              props.drawings.map((d) => (d.id === draft.id ? draft : d)),
            );
            drag.current = null;
            setDraft(null);
          }
          const move = orderDragRef.current;
          if (move) {
            const p = point(e);
            props.onAmend(move.id, move.field, p?.value ?? move.price);
            setOrderDrag(null);
          }
        }}
      >
        {geometry.map((d) => {
          if (d.y1 === null || (d.kind !== "horizontal" && d.x1 === null))
            return null;
          const x1 = d.x1 ?? 0,
            x2 = d.x2 ?? x1,
            y1 = d.y1,
            y2 = d.y2 ?? y1;
          const selected = props.selected === d.id;
          const common = { stroke: d.color, strokeWidth: selected ? 2.5 : 1.5 };
          return (
            <g
              key={d.id}
              className={`sim-drawing ${selected ? "selected" : ""}`}
              style={{ pointerEvents: d.id === "draft" ? "none" : "all" }}
              onPointerDown={(e) => {
                e.stopPropagation();
                props.onSelect(d.id);
                const p = point(e);
                if (!d.locked && p) {
                  drag.current = { drawing: d, start: p };
                  setDraft(d);
                  e.currentTarget.setPointerCapture(e.pointerId);
                }
              }}
            >
              {d.kind === "horizontal" ? (
                <>
                  <line x1={0} x2="100%" y1={y1} y2={y1} {...common} />
                  <text x={12} y={y1 - 6} fill={d.color}>
                    {d.text || price(d.p1)}
                  </text>
                </>
              ) : d.kind === "rectangle" ? (
                <rect
                  x={Math.min(x1, x2)}
                  y={Math.min(y1, y2)}
                  width={Math.max(3, Math.abs(x2 - x1))}
                  height={Math.max(3, Math.abs(y2 - y1))}
                  fill={d.color + "18"}
                  {...common}
                />
              ) : d.kind === "text" ? (
                <text x={x1} y={y1} fill={d.color}>
                  {d.text || "Chart note"}
                </text>
              ) : (
                <>
                  <line x1={x1} y1={y1} x2={x2} y2={y2} {...common} />
                  {d.kind === "measure" ? (
                    <text
                      x={(x1 + x2) / 2 + 5}
                      y={(y1 + y2) / 2 - 8}
                      fill={d.color}
                    >
                      {price(d.p2 - d.p1)} (
                      {((d.p2 / d.p1 - 1) * 100).toFixed(2)}%)
                    </text>
                  ) : null}
                </>
              )}
              {selected && d.kind !== "horizontal" ? (
                <circle cx={x1} cy={y1} r={4} fill={d.color} />
              ) : null}
            </g>
          );
        })}
        {props.run.positions
          .filter((p) => p.symbol === props.symbol)
          .map((p) => {
            const y = series.current?.priceToCoordinate(Number(p.average));
            return y != null ? (
              <g key={p.symbol}>
                <line
                  x1={0}
                  x2="100%"
                  y1={y}
                  y2={y}
                  stroke="#20a78d"
                  strokeDasharray="5 4"
                />
                <text x={12} y={y - 6} fill="#20a78d">
                  LONG {p.quantity} · average {p.average}
                </text>
              </g>
            ) : null;
          })}
        {props.run.orders
          .filter((o) => o.symbol === props.symbol && working(o))
          .flatMap((o) =>
            (["limit_price", "stop_price"] as const).map((field) => {
              if (!o[field]) return null;
              const value =
                orderDrag?.id === o.id && orderDrag.field === field
                  ? orderDrag.price
                  : Number(o[field]);
              const y = series.current?.priceToCoordinate(value);
              if (y == null) return null;
              return (
                <g
                  key={o.id + field}
                  className="sim-order-line"
                  style={{ pointerEvents: "all" }}
                  onPointerDown={(e) => {
                    e.stopPropagation();
                    setOrderDrag({ id: o.id, field, price: value });
                    e.currentTarget.setPointerCapture(e.pointerId);
                  }}
                >
                  <line
                    x1={0}
                    x2="100%"
                    y1={y}
                    y2={y}
                    stroke="#d6a352"
                    strokeWidth={2}
                    strokeDasharray="6 4"
                  />
                  <rect
                    x={80}
                    y={y - 18}
                    width={200}
                    height={19}
                    rx={3}
                    fill={props.dark ? "#3e3320" : "#fff0cf"}
                  />
                  <text
                    x={87}
                    y={y - 5}
                    fill={props.dark ? "#ebbd72" : "#805300"}
                  >
                    {o.side.toUpperCase()} {o.quantity - o.filled} ·{" "}
                    {field === "limit_price" ? "LIMIT" : "STOP"} {price(value)}
                  </text>
                </g>
              );
            }),
          )}
      </svg>
      {!props.bars.length ? (
        <div className="sim-chart-empty">
          Loading available market observations…
        </div>
      ) : null}
      {props.tool !== "cursor" ? (
        <div className="sim-drawing-hint">
          {start.current
            ? "Click the second point"
            : props.tool === "horizontal" || props.tool === "text"
              ? "Click the chart to place your drawing"
              : "Click two points on the chart"}{" "}
          · Esc to cancel
        </div>
      ) : null}
    </div>
  );
}
