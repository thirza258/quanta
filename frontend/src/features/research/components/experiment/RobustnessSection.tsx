import type { Results, Stability } from "@/features/research/model/registry";
import type { SurfacePoint } from "@/features/research/model/experiment";
import {
  formatCount,
  formatNumber,
  formatParams,
  isSkipped,
  pointAt,
  STABILITY,
} from "@/features/research/model/experiment";
import { decimal, percent } from "@/shared/lib/format";
import { memo } from "react";
import { CostStressCard } from "./CostStressCard";
import { ParameterSurface } from "./ParameterSurface";
import { SeedPaths } from "./SeedPaths";
import {
  ChartLegend,
  SectionHeading,
  SkippedNote,
  Stat,
  StatusBadge,
} from "./ui";

function StabilityBlock({
  title,
  point,
  stability,
  order,
}: {
  title: string;
  point: SurfacePoint | undefined;
  stability: Stability;
  order: string[];
}) {
  const meta = STABILITY[stability.class];
  return (
    <div className="xd-stability">
      <h4>{title}</h4>
      {point ? (
        <p className="xd-mono-line">
          {formatParams(point.params, order)} · Sharpe {decimal(point.sharpe)}
        </p>
      ) : null}
      <div className="xd-stability-score">
        <StatusBadge tone={meta.tone} label={meta.label} />
        <span>
          <strong>{stability.score ?? "—"}</strong>
          {stability.score != null ? " / 100" : ""}
        </span>
      </div>
      <p>{stability.reason}</p>
      <p className="xd-hint">
        Compared with {stability.neighbors} neighbouring{" "}
        {stability.neighbors === 1 ? "configuration" : "configurations"}.
      </p>
    </div>
  );
}

export const RobustnessSection = memo(function RobustnessSection({
  results,
}: {
  results: Results;
}) {
  const { surface, costs, seeds } = results.robustness;
  const order = surface.parameters.map((p) => p.name);
  const rows = [
    { label: "Best", index: surface.best },
    { label: "Median", index: surface.median },
    { label: "Worst", index: surface.worst },
    { label: "Base", index: surface.base },
  ];
  const spreadMax = surface.influence.reduce(
    (max, item) => Math.max(max, item.spread),
    0,
  );
  const distribution = surface.sharpe_distribution;
  return (
    <section
      id="robustness"
      className="xd-section"
      aria-labelledby="robustness-title"
    >
      <SectionHeading
        id="robustness"
        eyebrow="ROBUSTNESS"
        title="Does it survive small changes?"
        description="A real effect should not depend on one lucky setting, on today's cost assumption, or on one draw of the market."
      />
      <div className="xd-card">
        <div className="xd-card-head">
          <h3>Parameter surface</h3>
          <p className="xd-hint">
            {formatCount(surface.configurations)}{" "}
            {surface.configurations === 1 ? "configuration" : "configurations"}{" "}
            tested
          </p>
        </div>
        <ParameterSurface surface={surface} />
        {surface.configurations > 1 ? (
          <>
            <div className="xd-kpis xd-kpis-compact">
              <Stat
                label="Positive Sharpe"
                value={percent(surface.positive_share, 0)}
                sub="of configurations"
              />
              <Stat
                label="Base rank"
                value={`#${surface.base_rank}`}
                sub={`of ${formatCount(surface.configurations)} by Sharpe`}
              />
              <Stat
                label="Sharpe range"
                value={`${decimal(distribution.min)} to ${decimal(distribution.max)}`}
                sub={`Median ${decimal(distribution.median)} · s.d. ${decimal(distribution.std)}`}
              />
            </div>
            <div className="xd-grid-2">
              <StabilityBlock
                title="Base configuration"
                point={pointAt(surface, surface.base)}
                stability={surface.stability}
                order={order}
              />
              <StabilityBlock
                title="Best configuration"
                point={pointAt(surface, surface.best)}
                stability={surface.best_stability}
                order={order}
              />
            </div>
            <h4 className="xd-subhead">
              Best, median and worst configurations
            </h4>
            <div className="table-scroll xd-table xd-table-full">
              <table>
                <caption className="sr-only">
                  Best, median, worst and base configurations by Sharpe ratio
                </caption>
                <thead>
                  <tr>
                    <th scope="col">Configuration</th>
                    <th scope="col">Parameters</th>
                    <th scope="col" className="num">
                      Sharpe
                    </th>
                    <th scope="col" className="num">
                      CAGR
                    </th>
                    <th scope="col" className="num">
                      Max drawdown
                    </th>
                    <th scope="col" className="num">
                      Trades
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row) => {
                    const point = pointAt(surface, row.index);
                    return (
                      <tr key={row.label}>
                        <th scope="row">{row.label}</th>
                        <td>
                          {point ? formatParams(point.params, order) : "—"}
                        </td>
                        <td className="num">{decimal(point?.sharpe)}</td>
                        <td className="num">{percent(point?.cagr)}</td>
                        <td className="num">{percent(point?.max_drawdown)}</td>
                        <td className="num">{formatCount(point?.trades)}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            {surface.influence.length ? (
              <>
                <h4 className="xd-subhead">Parameter influence</h4>
                <p className="xd-hint">
                  Spread between the best and worst mean Sharpe across each
                  parameter's values. A large spread means the result leans on
                  that setting.
                </p>
                <ul className="xd-influence">
                  {surface.influence.map((item) => (
                    <li key={item.name}>
                      <code>{item.name}</code>
                      <span className="xd-influence-bar" aria-hidden="true">
                        <span
                          style={{
                            width: `${spreadMax > 0 ? (item.spread / spreadMax) * 100 : 0}%`,
                          }}
                        />
                      </span>
                      <strong>Δ {decimal(item.spread)}</strong>
                      <span className="xd-influence-values">
                        {item.values
                          .map(
                            (value, i) =>
                              `${formatNumber(value)}: ${decimal(item.mean_sharpe[i])}`,
                          )
                          .join(" · ")}
                      </span>
                    </li>
                  ))}
                </ul>
              </>
            ) : null}
          </>
        ) : null}
      </div>
      <CostStressCard costs={costs} />
      <div className="xd-card">
        <div className="xd-card-head">
          <h3>Alternative market paths</h3>
          {!isSkipped(seeds) ? (
            <ChartLegend
              items={[
                { label: "Strategy", tone: "strategy", mark: "dot" },
                { label: "Buy & hold", tone: "context", mark: "dot" },
              ]}
            />
          ) : null}
        </div>
        {isSkipped(seeds) ? (
          <SkippedNote value={seeds} what="alternative paths" />
        ) : (
          <>
            <p className="xd-lede">
              The same rule on {seeds.paths.length} other draws of the same
              synthetic market. The original path{" "}
              {seeds.original_beats_benchmark ? "beat" : "did not beat"}{" "}
              buy-and-hold; the alternatives show whether that was the market or
              the rule.
            </p>
            <SeedPaths seeds={seeds} />
          </>
        )}
      </div>
    </section>
  );
});
