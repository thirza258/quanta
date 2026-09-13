import { useEffect, useRef, useState } from "react";
import {
  AreaSeries,
  CandlestickSeries,
  ColorType,
  createChart,
  LineSeries,
} from "lightweight-charts";
import type { Time } from "lightweight-charts";
import type { Result } from "../lib/types";
export default function FinancialChart({
  result,
  kind,
}: {
  result: Result;
  kind: "equity" | "drawdown" | "candles";
}) {
  const ref = useRef<HTMLDivElement>(null),
    [dark, setDark] = useState(
      document.documentElement.dataset.theme === "dark",
    );
  useEffect(() => {
    const observer = new MutationObserver(() =>
      setDark(document.documentElement.dataset.theme === "dark"),
    );
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-theme"],
    });
    return () => observer.disconnect();
  }, []);
  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, {
      height: 260,
      autoSize: true,
      layout: {
        background: {
          type: ColorType.Solid,
          color: dark ? "#19221f" : "#ffffff",
        },
        textColor: dark ? "#8fa19a" : "#8a918d",
        fontFamily: "JetBrains Mono, monospace",
        fontSize: 10,
        attributionLogo: true,
      },
      grid: {
        vertLines: { visible: false },
        horzLines: { color: dark ? "#293630" : "#f0f2f0" },
      },
      rightPriceScale: { borderVisible: false },
      timeScale: {
        borderVisible: false,
        fixLeftEdge: true,
        fixRightEdge: true,
      },
      crosshair: {
        vertLine: { color: "#8caaa0", labelBackgroundColor: "#285b4b" },
        horzLine: { color: "#8caaa0", labelBackgroundColor: "#285b4b" },
      },
    });
    if (kind === "candles") {
      chart
        .addSeries(CandlestickSeries, {
          upColor: "#4a8b72",
          downColor: "#c76e78",
          borderVisible: false,
          wickUpColor: "#4a8b72",
          wickDownColor: "#c76e78",
        })
        .setData(result.bars.map((b) => ({ ...b, time: b.time as Time })));
    } else if (kind === "drawdown") {
      chart
        .addSeries(AreaSeries, {
          lineColor: "#bd6070",
          topColor: "#bd607022",
          bottomColor: "#bd607000",
          lineWidth: 2,
          priceFormat: { type: "percent" },
        })
        .setData(
          result.equity_curve.map((p) => ({
            time: p.time as Time,
            value: p.drawdown * 100,
          })),
        );
    } else {
      chart
        .addSeries(AreaSeries, {
          lineColor: "#3d8069",
          topColor: "#3d80691c",
          bottomColor: "#3d806900",
          lineWidth: 2,
          lastValueVisible: false,
          priceLineVisible: false,
        })
        .setData(
          result.equity_curve.map((p) => ({
            time: p.time as Time,
            value: p.equity,
          })),
        );
      chart
        .addSeries(LineSeries, {
          color: dark ? "#8d9691" : "#a4afa8",
          lineWidth: 1,
          lineStyle: 2,
          lastValueVisible: false,
          priceLineVisible: false,
        })
        .setData(
          result.equity_curve.map((p) => ({
            time: p.time as Time,
            value: p.benchmark,
          })),
        );
    }
    chart.timeScale().fitContent();
    return () => chart.remove();
  }, [result, kind, dark]);
  return (
    <div
      ref={ref}
      className="financial-chart"
      aria-label={`${kind} chart from ${result.equity_curve[0]?.time} to ${result.equity_curve.at(-1)?.time}`}
    />
  );
}
