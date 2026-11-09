import type { CostStress } from "@/features/research/model/registry";
import {
  breakEven,
  formatBps,
  formatNumber,
  niceScale,
} from "@/features/research/model/experiment";
import { decimal, percent } from "@/shared/lib/format";
import type { LabelProps } from "recharts";
import {
  CartesianGrid,
  Line,
  LineChart,
  ReferenceDot,
  ReferenceLine,
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
  zeroStroke,
} from "./theme";

const CostTooltip = makeTooltip({
  label: (label) => `${formatBps(Number(label))} per fill`,
  rows: [
    {
      key: "sharpe",
      name: "Sharpe ratio",
      tone: "strategy",
      format: (value) => decimal(value, 2),
    },
    {
      key: "cagr",
      name: "CAGR",
      tone: "context",
      format: (value) => percent(value, 1),
    },
  ],
});

/** A direct label beside a vertical marker; flips left near the right edge. */
function markerLabel(text: string, anchor: "start" | "end", row: number) {
  return function MarkerLabel(props: LabelProps) {
    const box = (props.viewBox ?? {}) as { x?: number; y?: number };
    const x = box.x ?? 0,
      y = box.y ?? 0;
    return (
      <text
        x={anchor === "start" ? x + 6 : x - 6}
        y={y + 12 + row * 15}
        textAnchor={anchor}
        fill="var(--secondary)"
        fontSize={11}
      >
        {text}
      </text>
    );
  };
}

/** Sharpe ratio as the one-way cost per fill rises, with the break-even. */
export default function CostStressChart({
  costs,
  height = 240,
}: {
  costs: CostStress;
  height?: number;
}) {
  const top = costs.levels.reduce((max, l) => Math.max(max, l.cost_bps), 0);
  const domainMax = Math.max(top, costs.current_bps, 1);
  const even = breakEven(costs);
  const scale = niceScale(
    costs.levels.map((l) => l.sharpe),
    4,
  );
  const evenAt = even.kind === "value" && even.inRange ? even.bps : null;
  const anchor = (value: number) =>
    value > domainMax * 0.6 ? ("end" as const) : ("start" as const);
  const close =
    evenAt != null && Math.abs(evenAt - costs.current_bps) < domainMax * 0.22;
  return (
    <div className="xd-chart" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={costs.levels}
          title="Sharpe ratio against transaction cost"
          desc="Sharpe ratio of the base configuration at one-way costs from 0 basis points per fill upward, with the assumed cost and the break-even cost marked."
          margin={{ top: 8, right: 32, bottom: 0, left: 0 }}
        >
          <CartesianGrid vertical={false} stroke={gridStroke} />
          <XAxis
            dataKey="cost_bps"
            type="number"
            domain={[0, domainMax]}
            tickFormatter={(value) => `${value}`}
            tick={axisTick}
            axisLine={{ stroke: baselineStroke }}
            tickLine={false}
            allowDecimals={false}
            unit=" bps"
          />
          <YAxis
            tickFormatter={(value) => formatNumber(Number(value))}
            tick={axisTick}
            axisLine={false}
            tickLine={false}
            width={40}
            domain={scale.domain}
            ticks={scale.ticks}
          />
          <Tooltip
            content={CostTooltip}
            cursor={lineCursor}
            isAnimationActive={false}
          />
          <ReferenceLine y={0} stroke={zeroStroke} />
          <ReferenceLine
            x={costs.current_bps}
            stroke="var(--muted)"
            strokeDasharray="4 3"
            label={markerLabel(
              `Assumed ${formatBps(costs.current_bps)}`,
              anchor(costs.current_bps),
              0,
            )}
          />
          {evenAt != null ? (
            <ReferenceLine
              x={evenAt}
              stroke="var(--xd-loss)"
              strokeDasharray="4 3"
              label={markerLabel(
                `Break-even ${formatBps(evenAt)}`,
                anchor(evenAt),
                close ? 1 : 0,
              )}
            />
          ) : null}
          <Line
            dataKey="sharpe"
            name="Sharpe ratio"
            stroke="var(--xd-strategy)"
            strokeWidth={2}
            dot={{
              r: 4,
              fill: "var(--xd-strategy)",
              stroke: "var(--bg)",
              strokeWidth: 2,
            }}
            activeDot={{ ...activeDot, r: 5, fill: "var(--xd-strategy)" }}
            isAnimationActive={false}
          />
          {evenAt != null ? (
            <ReferenceDot
              x={evenAt}
              y={0}
              r={5}
              fill="var(--xd-loss)"
              stroke="var(--bg)"
              strokeWidth={2}
            />
          ) : null}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
