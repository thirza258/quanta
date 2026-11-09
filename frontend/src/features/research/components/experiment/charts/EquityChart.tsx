import type { CurvePoint } from "@/features/research/model/registry";
import {
  compactMoney,
  formatDay,
  formatMonth,
} from "@/features/research/model/experiment";
import { money } from "@/shared/lib/format";
import { useMemo } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  activeDot,
  axisTick,
  baselineStroke,
  gridStroke,
  lineCursor,
  makeTooltip,
} from "./theme";

const asMoney = (value: number | null) => (value == null ? "—" : money(value));

/** Strategy equity (emphasis) against buy-and-hold (context grey). */
export default function EquityChart({
  points,
  height = 260,
  syncId,
  title,
  description,
  strategyLabel = "Strategy",
  benchmarkLabel = "Buy & hold",
}: {
  points: CurvePoint[];
  height?: number;
  syncId?: string;
  title: string;
  description: string;
  strategyLabel?: string;
  benchmarkLabel?: string;
}) {
  const content = useMemo(
    () =>
      makeTooltip({
        label: (label) => formatDay(String(label ?? "")),
        rows: [
          {
            key: "equity",
            name: strategyLabel,
            tone: "strategy",
            format: asMoney,
          },
          {
            key: "benchmark",
            name: benchmarkLabel,
            tone: "context",
            format: asMoney,
          },
        ],
      }),
    [strategyLabel, benchmarkLabel],
  );
  return (
    <div className="xd-chart" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={points}
          syncId={syncId}
          title={title}
          desc={description}
          margin={{ top: 8, right: 12, bottom: 0, left: 0 }}
        >
          <CartesianGrid vertical={false} stroke={gridStroke} />
          <XAxis
            dataKey="time"
            tickFormatter={(value) => formatMonth(String(value))}
            minTickGap={56}
            tick={axisTick}
            axisLine={{ stroke: baselineStroke }}
            tickLine={false}
          />
          <YAxis
            tickFormatter={(value) => compactMoney(Number(value))}
            tick={axisTick}
            axisLine={false}
            tickLine={false}
            width={58}
            domain={["auto", "auto"]}
          />
          <Tooltip
            content={content}
            cursor={lineCursor}
            isAnimationActive={false}
          />
          <Line
            dataKey="benchmark"
            name={benchmarkLabel}
            stroke="var(--xd-context)"
            strokeWidth={2}
            dot={false}
            activeDot={{ ...activeDot, fill: "var(--xd-context)" }}
            isAnimationActive={false}
          />
          <Line
            dataKey="equity"
            name={strategyLabel}
            stroke="var(--xd-strategy)"
            strokeWidth={2}
            dot={false}
            activeDot={{ ...activeDot, fill: "var(--xd-strategy)" }}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
