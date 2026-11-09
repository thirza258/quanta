import type { Fold } from "@/features/research/model/registry";
import {
  formatDay,
  formatNumber,
  niceScale,
} from "@/features/research/model/experiment";
import { decimal } from "@/shared/lib/format";
import {
  Bar,
  BarChart,
  CartesianGrid,
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

const sharpe = (value: number | null) => decimal(value, 2);

const FoldTooltip = makeTooltip({
  label: (_, datum) =>
    `Fold ${datum.fold} · ${formatDay(String(datum.start))} – ${formatDay(String(datum.end))}`,
  rows: [
    {
      key: "oos",
      name: "Out-of-sample Sharpe",
      tone: "strategy",
      format: sharpe,
    },
    { key: "is", name: "In-sample Sharpe", tone: "context", format: sharpe },
  ],
});

/** In-sample vs out-of-sample Sharpe for each walk-forward fold. */
export default function FoldSharpeChart({
  folds,
  height = 220,
}: {
  folds: Fold[];
  height?: number;
}) {
  const data = folds.map((fold) => ({
    label: `F${fold.fold}`,
    fold: fold.fold,
    start: fold.test.start,
    end: fold.test.end,
    is: fold.in_sample_sharpe,
    oos: fold.out_of_sample_sharpe,
  }));
  const scale = niceScale(
    data.flatMap((d) => [d.is, d.oos]),
    4,
  );
  return (
    <div className="xd-chart" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          title="In-sample and out-of-sample Sharpe ratio by walk-forward fold"
          desc="Grouped bars: grey is the Sharpe ratio on each fold's training window, green the Sharpe ratio on the following unseen test window."
          margin={{ top: 8, right: 12, bottom: 0, left: 0 }}
          barGap={2}
          barCategoryGap="28%"
        >
          <CartesianGrid vertical={false} stroke={gridStroke} />
          <XAxis
            dataKey="label"
            tick={axisTick}
            axisLine={false}
            tickLine={false}
            interval="preserveStartEnd"
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
            content={FoldTooltip}
            cursor={barCursor}
            isAnimationActive={false}
          />
          <ReferenceLine y={0} stroke={zeroStroke} />
          <Bar
            dataKey="is"
            name="In-sample Sharpe"
            fill="var(--xd-context)"
            maxBarSize={24}
            radius={[4, 4, 0, 0]}
            isAnimationActive={false}
          />
          <Bar
            dataKey="oos"
            name="Out-of-sample Sharpe"
            fill="var(--xd-strategy)"
            maxBarSize={24}
            radius={[4, 4, 0, 0]}
            isAnimationActive={false}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
