import type { SurfaceCell } from "@/features/research/model/experiment";
import { formatNumber, niceScale } from "@/features/research/model/experiment";
import { decimal } from "@/shared/lib/format";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  axisTick,
  barCursor,
  gridStroke,
  makeTooltip,
  zeroStroke,
} from "./theme";

type Datum = {
  label: string;
  sharpe: number | null;
  marker: string;
};

/** Parameter value on the first line, "base"/"best" on the second. */
function ValueTick(props: {
  x?: number | string;
  y?: number | string;
  payload?: { value?: string; index?: number };
  data: Datum[];
}) {
  const x = Number(props.x ?? 0),
    y = Number(props.y ?? 0);
  const datum = props.data[props.payload?.index ?? -1];
  return (
    <g transform={`translate(${x},${y})`}>
      <text dy={12} textAnchor="middle" fill="var(--muted)" fontSize={11}>
        {props.payload?.value}
      </text>
      {datum?.marker ? (
        <text
          dy={26}
          textAnchor="middle"
          fill="var(--text)"
          fontSize={10}
          fontWeight={600}
        >
          {datum.marker}
        </text>
      ) : null}
    </g>
  );
}

/** One-parameter surface: Sharpe ratio for each tested value. */
export default function SharpeByValueChart({
  name,
  cells,
  height = 230,
}: {
  name: string;
  cells: SurfaceCell[];
  height?: number;
}) {
  const data: Datum[] = cells.map((cell) => ({
    label: formatNumber(cell.value),
    sharpe: cell.point?.sharpe ?? null,
    marker:
      cell.base && cell.best
        ? "BASE · BEST"
        : cell.base
          ? "BASE"
          : cell.best
            ? "BEST"
            : "",
  }));
  const scale = niceScale(
    data.map((d) => d.sharpe),
    4,
  );
  const content = makeTooltip({
    label: (label, datum) =>
      `${name} = ${label}${datum.marker ? ` · ${String(datum.marker).toLowerCase()}` : ""}`,
    rows: [
      {
        key: "sharpe",
        name: "Sharpe ratio",
        tone: "strategy",
        format: (value) => decimal(value, 2),
      },
    ],
  });
  return (
    <div className="xd-chart" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          title={`Sharpe ratio by ${name}`}
          desc={`Bars above zero have a positive Sharpe ratio, bars below zero a negative one. The base and best values are labelled under the axis.`}
          margin={{ top: 8, right: 12, bottom: 18, left: 0 }}
        >
          <CartesianGrid vertical={false} stroke={gridStroke} />
          <XAxis
            dataKey="label"
            tick={(props) => <ValueTick {...props} data={data} />}
            axisLine={false}
            tickLine={false}
            interval={0}
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
            content={content}
            cursor={barCursor}
            isAnimationActive={false}
          />
          <ReferenceLine y={0} stroke={zeroStroke} />
          <Bar
            dataKey="sharpe"
            name="Sharpe ratio"
            maxBarSize={24}
            radius={[4, 4, 0, 0]}
            isAnimationActive={false}
          >
            {data.map((datum, index) => (
              <Cell
                key={index}
                fill={
                  (datum.sharpe ?? 0) >= 0
                    ? "var(--xd-div-p4)"
                    : "var(--xd-div-n4)"
                }
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
