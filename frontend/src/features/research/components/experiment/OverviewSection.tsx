import type {
  ExperimentDetail,
  Results,
  RunDetail,
} from "@/features/research/model/registry";
import {
  BENCHMARK_METRICS,
  downsample,
  formatBps,
  formatCount,
  formatDay,
  formatMetric,
  formatParams,
  formatTimes,
} from "@/features/research/model/experiment";
import { decimal, money, percent } from "@/shared/lib/format";
import { lazy, memo, Suspense } from "react";
import { HypothesisQuote } from "./NotebookSection";
import { ChartFallback, ChartLegend, SectionHeading, Stat } from "./ui";

const EquityChart = lazy(() => import("./charts/EquityChart"));
const DrawdownChart = lazy(() => import("./charts/DrawdownChart"));

const moneyOrDash = (value: number | null | undefined) =>
  value == null || !Number.isFinite(value) ? "—" : money(value);

export const OverviewSection = memo(function OverviewSection({
  experiment,
  run,
  results,
}: {
  experiment: ExperimentDetail;
  run: RunDetail;
  results: Results;
}) {
  const metrics = results.headline.metrics;
  const curve = results.headline.equity_curve;
  const buyHold = results.benchmarks.rows.find((r) => r.id === "buy_hold");
  const order = experiment.spec.strategy.parameters.map((p) => p.name);
  const first = curve[0],
    last = curve.at(-1);
  const deepest = curve.reduce<(typeof curve)[number] | null>(
    (worst, point) =>
      !worst || point.drawdown < worst.drawdown ? point : worst,
    null,
  );
  const summary =
    first && last
      ? `From ${formatDay(first.time)} to ${formatDay(last.time)} the strategy moved from ${moneyOrDash(first.equity)} to ${moneyOrDash(last.equity)} (${percent(metrics.total_return)}), while buy-and-hold ended at ${moneyOrDash(last.benchmark)}. The deepest drawdown was ${percent(metrics.max_drawdown)}${deepest ? `, on ${formatDay(deepest.time)}` : ""}.`
      : "The run produced no equity curve.";
  const table = downsample(curve, 60);
  const vsBuyHold = (value: string) =>
    buyHold ? `Buy & hold ${value}` : undefined;
  return (
    <section
      id="overview"
      className="xd-section"
      aria-labelledby="overview-title"
    >
      <SectionHeading
        id="overview"
        eyebrow="OVERVIEW"
        title="What the backtest shows"
        description={
          <>
            Run #{run.number} · base configuration{" "}
            <code>{formatParams(results.headline.params, order)}</code> ·{" "}
            {formatCount(results.dataset.bars)} bars from{" "}
            {formatDay(results.dataset.start)} to{" "}
            {formatDay(results.dataset.end)}.
          </>
        }
      />
      <HypothesisQuote experiment={experiment} />
      <div className="xd-kpis" role="list" aria-label="Headline metrics">
        <div role="listitem">
          <Stat
            label="CAGR"
            value={percent(metrics.cagr)}
            sub={vsBuyHold(percent(buyHold?.metrics.cagr))}
          />
        </div>
        <div role="listitem">
          <Stat
            label="Sharpe ratio"
            value={decimal(metrics.sharpe)}
            sub={vsBuyHold(decimal(buyHold?.metrics.sharpe))}
          />
        </div>
        <div role="listitem">
          <Stat
            label="Max drawdown"
            value={percent(metrics.max_drawdown)}
            sub={vsBuyHold(percent(buyHold?.metrics.max_drawdown))}
          />
        </div>
        <div role="listitem">
          <Stat
            label="Turnover"
            value={formatTimes(metrics.turnover)}
            sub="Traded value ÷ average equity, per year"
          />
        </div>
        <div role="listitem">
          <Stat
            label="Trades"
            value={formatCount(metrics.trades)}
            sub={`${formatCount(metrics.round_trips)} round ${metrics.round_trips === 1 ? "trip" : "trips"}`}
          />
        </div>
        <div role="listitem">
          <Stat
            label="Exposure"
            value={percent(metrics.exposure)}
            sub="Share of bars in the market"
          />
        </div>
      </div>
      <figure className="xd-card xd-figure" aria-labelledby="equity-caption">
        <div className="xd-card-head">
          <h3>Equity curve</h3>
          <ChartLegend
            items={[
              { label: "Strategy", tone: "strategy" },
              { label: "Buy & hold", tone: "context" },
            ]}
          />
        </div>
        <Suspense fallback={<ChartFallback height={260} />}>
          <EquityChart
            points={curve}
            height={260}
            syncId="xd-headline"
            title="Equity curve: strategy against buy-and-hold"
            description={summary}
          />
        </Suspense>
        <h4 className="xd-subhead">Drawdown from the previous peak</h4>
        <Suspense fallback={<ChartFallback height={130} />}>
          <DrawdownChart
            points={curve}
            height={130}
            syncId="xd-headline"
            title="Strategy drawdown"
            description={`Deepest drawdown ${percent(metrics.max_drawdown)}.`}
          />
        </Suspense>
        <figcaption id="equity-caption" className="xd-figcaption">
          {summary} Results include{" "}
          {formatBps(
            run.spec.experiment.costs.commission_bps +
              run.spec.experiment.costs.slippage_bps,
          )}{" "}
          of costs per fill.
        </figcaption>
        <details className="xd-details">
          <summary>Show the equity data as a table</summary>
          <div className="table-scroll xd-table">
            <table>
              <caption className="sr-only">
                Equity and drawdown, sampled to {table.length} dates
              </caption>
              <thead>
                <tr>
                  <th scope="col">Date</th>
                  <th scope="col" className="num">
                    Strategy
                  </th>
                  <th scope="col" className="num">
                    Buy & hold
                  </th>
                  <th scope="col" className="num">
                    Drawdown
                  </th>
                </tr>
              </thead>
              <tbody>
                {table.map((point) => (
                  <tr key={point.time}>
                    <th scope="row">{formatDay(point.time)}</th>
                    <td className="num">{moneyOrDash(point.equity)}</td>
                    <td className="num">{moneyOrDash(point.benchmark)}</td>
                    <td className="num">{percent(point.drawdown)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </details>
      </figure>
      <div className="xd-card">
        <div className="xd-card-head">
          <h3>Against simple alternatives</h3>
          <p className="xd-hint">
            A strategy has to beat doing nothing clever.
          </p>
        </div>
        <div className="table-scroll xd-table xd-table-full">
          <table>
            <caption className="sr-only">
              Strategy metrics compared with buy-and-hold, a trend baseline and
              cash
            </caption>
            <thead>
              <tr>
                <th scope="col">Metric</th>
                {results.benchmarks.rows.map((row) => (
                  <th
                    scope="col"
                    key={row.id}
                    className={`num${row.id === "strategy" ? " is-strategy" : ""}`}
                  >
                    {row.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {BENCHMARK_METRICS.map((metric) => (
                <tr key={metric.key}>
                  <th scope="row">{metric.label}</th>
                  {results.benchmarks.rows.map((row) => (
                    <td
                      key={row.id}
                      className={`num${row.id === "strategy" ? " is-strategy" : ""}`}
                    >
                      {formatMetric(row.metrics[metric.key], metric.format)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="fine-print">
          Ratios use a 3% annual risk-free rate; “—” marks a ratio that is
          undefined (for example no losing trades or no volatility), not zero.
        </p>
      </div>
    </section>
  );
});
