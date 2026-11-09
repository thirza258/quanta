import type { Results, SplitArm } from "@/features/research/model/registry";
import {
  formatCount,
  formatDay,
  formatDecay,
  formatParams,
  formatSpan,
  isSkipped,
} from "@/features/research/model/experiment";
import { decimal, percent } from "@/shared/lib/format";
import { lazy, memo, Suspense } from "react";
import {
  ChartFallback,
  ChartLegend,
  SectionHeading,
  SkippedNote,
  Stat,
} from "./ui";

const FoldSharpeChart = lazy(() => import("./charts/FoldSharpeChart"));
const EquityChart = lazy(() => import("./charts/EquityChart"));

function ArmRow({
  label,
  arm,
  order,
}: {
  label: string;
  arm: SplitArm;
  order: string[];
}) {
  return (
    <tr>
      <th scope="row">{label}</th>
      <td>{formatParams(arm.params, order)}</td>
      <td className="num">{decimal(arm.in_sample.sharpe)}</td>
      <td className="num">{decimal(arm.out_of_sample.sharpe)}</td>
      <td className="num">{formatDecay(arm.decay)}</td>
      <td className="num">{percent(arm.out_of_sample.total_return)}</td>
    </tr>
  );
}

export const ValidationSection = memo(function ValidationSection({
  results,
  order,
}: {
  results: Results;
  order: string[];
}) {
  const split = results.validation.train_test;
  const walk = results.validation.walk_forward;
  return (
    <section
      id="validation"
      className="xd-section"
      aria-labelledby="validation-title"
    >
      <SectionHeading
        id="validation"
        eyebrow="VALIDATION"
        title="Does it hold on data it never saw?"
        description="Parameters are chosen on the past and judged on what came next. Decay is the share of the in-sample Sharpe ratio lost out of sample; it is undefined when the in-sample Sharpe is not positive. IS = in sample, OOS = out of sample."
      />
      <div className="xd-card">
        <div className="xd-card-head">
          <h3>Train / test split</h3>
        </div>
        {isSkipped(split) ? (
          <SkippedNote value={split} what="train / test split" />
        ) : (
          <>
            <div
              className="xd-split"
              role="img"
              aria-label={`${percent(split.split, 0)} of bars in sample, the rest out of sample`}
            >
              <span
                className="is-in"
                style={{ flexGrow: split.in_sample.bars }}
              />
              <span
                className="is-out"
                style={{ flexGrow: split.out_of_sample.bars }}
              />
            </div>
            <dl className="xd-pairs">
              <div>
                <dt>
                  <i
                    className="xd-key xd-key-bar is-context"
                    aria-hidden="true"
                  />
                  In sample · {percent(split.split, 0)}
                </dt>
                <dd>{formatSpan(split.in_sample)}</dd>
              </div>
              <div>
                <dt>
                  <i
                    className="xd-key xd-key-bar is-strategy"
                    aria-hidden="true"
                  />
                  Out of sample · {percent(1 - split.split, 0)}
                </dt>
                <dd>{formatSpan(split.out_of_sample)}</dd>
              </div>
            </dl>
            <div className="table-scroll xd-table xd-table-full">
              <table>
                <caption className="sr-only">
                  Sharpe ratio in and out of sample for the base configuration
                  and the configuration that was best in sample
                </caption>
                <thead>
                  <tr>
                    <th scope="col">Arm</th>
                    <th scope="col">Parameters</th>
                    <th scope="col" className="num">
                      <abbr title="In-sample">IS</abbr> Sharpe
                    </th>
                    <th scope="col" className="num">
                      <abbr title="Out-of-sample">OOS</abbr> Sharpe
                    </th>
                    <th scope="col" className="num">
                      Decay
                    </th>
                    <th scope="col" className="num">
                      <abbr title="Out-of-sample">OOS</abbr> return
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <ArmRow
                    label="Base configuration"
                    arm={split.base}
                    order={order}
                  />
                  <ArmRow
                    label="Best in sample"
                    arm={split.selected}
                    order={order}
                  />
                </tbody>
              </table>
            </div>
            {split.base.index === split.selected.index ? (
              <p className="fine-print">
                The best in-sample configuration is the base configuration.
              </p>
            ) : (
              <p className="fine-print">
                “Best in sample” is what an optimiser would have picked on the
                training data; its out-of-sample Sharpe is the honest estimate.
              </p>
            )}
          </>
        )}
      </div>
      <div className="xd-card">
        <div className="xd-card-head">
          <h3>Walk-forward</h3>
          {!isSkipped(walk) ? (
            <p className="xd-hint">
              {walk.mode === "anchored" ? "Anchored" : "Rolling"} windows ·{" "}
              {formatCount(walk.train_bars)} training /{" "}
              {formatCount(walk.test_bars)} test bars · {walk.folds.length}{" "}
              {walk.folds.length === 1 ? "fold" : "folds"}
            </p>
          ) : null}
        </div>
        {isSkipped(walk) ? (
          <SkippedNote value={walk} what="walk-forward" />
        ) : (
          <>
            <div className="xd-kpis xd-kpis-compact">
              <Stat
                label="Mean in-sample Sharpe"
                value={decimal(walk.aggregate.mean_in_sample_sharpe)}
              />
              <Stat
                label="Stitched out-of-sample Sharpe"
                value={decimal(walk.aggregate.out_of_sample.sharpe)}
                sub={`Base configuration ${decimal(walk.aggregate.base_out_of_sample.sharpe)}`}
              />
              <Stat label="Decay" value={formatDecay(walk.aggregate.decay)} />
              <Stat
                label="Positive folds"
                value={`${walk.aggregate.positive_folds} / ${walk.folds.length}`}
                sub="Out-of-sample Sharpe above zero"
              />
              <Stat
                label="Configurations chosen"
                value={formatCount(walk.aggregate.distinct_choices)}
                sub={`Distinct winners across ${walk.folds.length} ${walk.folds.length === 1 ? "fold" : "folds"}`}
              />
            </div>
            <figure className="xd-figure" aria-labelledby="folds-caption">
              <div className="xd-card-head">
                <h4 className="xd-subhead">Sharpe ratio by fold</h4>
                <ChartLegend
                  items={[
                    { label: "In sample", tone: "context", mark: "bar" },
                    { label: "Out of sample", tone: "strategy", mark: "bar" },
                  ]}
                />
              </div>
              <Suspense fallback={<ChartFallback height={220} />}>
                <FoldSharpeChart folds={walk.folds} height={220} />
              </Suspense>
              <figcaption id="folds-caption" className="xd-figcaption">
                Each fold re-optimises on its training window and is scored on
                the next {formatCount(walk.test_bars)} bars. The table below
                lists every value.
              </figcaption>
            </figure>
            <div className="table-scroll xd-table xd-table-full">
              <table>
                <caption className="sr-only">Walk-forward folds</caption>
                <thead>
                  <tr>
                    <th scope="col">Fold</th>
                    <th scope="col">Test window</th>
                    <th scope="col">Chosen parameters</th>
                    <th scope="col" className="num">
                      <abbr title="In-sample">IS</abbr> Sharpe
                    </th>
                    <th scope="col" className="num">
                      <abbr title="Out-of-sample">OOS</abbr> Sharpe
                    </th>
                    <th scope="col" className="num">
                      <abbr title="Out-of-sample">OOS</abbr> return
                    </th>
                    <th scope="col" className="num">
                      Base <abbr title="out-of-sample">OOS</abbr> Sharpe
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {walk.folds.map((fold) => (
                    <tr key={fold.fold}>
                      <th scope="row">{fold.fold}</th>
                      <td>
                        {formatDay(fold.test.start)} –{" "}
                        {formatDay(fold.test.end)}
                      </td>
                      <td>{formatParams(fold.params, order)}</td>
                      <td className="num">{decimal(fold.in_sample_sharpe)}</td>
                      <td className="num">
                        {decimal(fold.out_of_sample_sharpe)}
                      </td>
                      <td className="num">
                        {percent(fold.out_of_sample_return)}
                      </td>
                      <td className="num">
                        {decimal(fold.base_out_of_sample_sharpe)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {walk.equity_curve.length ? (
              <figure className="xd-figure" aria-labelledby="oos-caption">
                <div className="xd-card-head">
                  <h4 className="xd-subhead">Stitched out-of-sample equity</h4>
                  <ChartLegend
                    items={[
                      { label: "Walk-forward strategy", tone: "strategy" },
                      { label: "Buy & hold", tone: "context" },
                    ]}
                  />
                </div>
                <Suspense fallback={<ChartFallback height={220} />}>
                  <EquityChart
                    points={walk.equity_curve}
                    height={220}
                    title="Stitched out-of-sample equity"
                    description="Equity from chaining every fold's test window, against buy-and-hold over the same windows."
                    strategyLabel="Walk-forward strategy"
                  />
                </Suspense>
                <figcaption id="oos-caption" className="xd-figcaption">
                  Only test windows are chained here (
                  {formatSpan(walk.out_of_sample)}
                  ), so every point was traded with parameters chosen on earlier
                  data. Stitched out-of-sample return{" "}
                  {percent(walk.aggregate.out_of_sample.total_return)}, max
                  drawdown {percent(walk.aggregate.out_of_sample.max_drawdown)}.
                </figcaption>
              </figure>
            ) : null}
          </>
        )}
      </div>
    </section>
  );
});
