import type { CurvePoint } from "@/features/research/model/registry";
import { formatDay, formatMonth } from "@/features/research/model/experiment";
import { percent } from "@/shared/lib/format";
import {
  Area,
  AreaChart,
  CartesianGrid,
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

const DrawdownTooltip = makeTooltip({
  label: (label) => formatDay(String(label ?? "")),
  rows: [
    {
      key: "drawdown",
      name: "Below the previous peak",
      tone: "loss",
      format: (value) => percent(value, 1),
    },
  ],
});

/** Strategy drawdown from its running peak (values are ≤ 0). */
export default function DrawdownChart({
  points,
  height = 130,
  syncId,
  title,
  description,
}: {
  points: CurvePoint[];
  height?: number;
  syncId?: string;
  title: string;
  description: string;
}) {
  return (
    <div className="xd-chart" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={points}
          syncId={syncId}
          title={title}
          desc={description}
          margin={{ top: 6, right: 12, bottom: 0, left: 0 }}
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
            tickFormatter={(value) => percent(Number(value), 0)}
            tick={axisTick}
            axisLine={false}
            tickLine={false}
            width={58}
            domain={["dataMin", 0]}
          />
          <Tooltip
            content={DrawdownTooltip}
            cursor={lineCursor}
            isAnimationActive={false}
          />
          <Area
            dataKey="drawdown"
            name="Drawdown"
            type="linear"
            stroke="var(--xd-loss)"
            strokeWidth={2}
            fill="var(--xd-loss)"
            fillOpacity={0.1}
            activeDot={{ ...activeDot, fill: "var(--xd-loss)" }}
            isAnimationActive={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
