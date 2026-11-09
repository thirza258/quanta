import type { CostStress } from "@/features/research/model/registry";
import {
  breakEven,
  formatBps,
  formatTimes,
} from "@/features/research/model/experiment";
import { decimal, percent } from "@/shared/lib/format";
import { lazy, Suspense } from "react";
import { ChartFallback, ChartLegend } from "./ui";

const CostStressChart = lazy(() => import("./charts/CostStressChart"));

function breakEvenText(costs: CostStress): string {
  const even = breakEven(costs);
  const assumed = formatBps(costs.current_bps);
  switch (even.kind) {
    case "value": {
      const margin =
        even.margin != null
          ? ` — ${formatTimes(even.margin, 1)} the assumed ${assumed}`
          : "";
      return even.inRange
        ? `The Sharpe ratio falls to zero at ${formatBps(even.bps)} per fill${margin}.`
        : `The Sharpe ratio falls to zero at ${formatBps(even.bps)} per fill, beyond the plotted range${margin}.`;
    }
    case "above":
      return `The Sharpe ratio stays positive even at ${formatBps(even.bps)} per fill.${even.reason ? ` ${even.reason}` : ""}`;
    case "none":
      return `No break-even cost: ${even.reason}`;
  }
}

/** Sharpe ratio against one-way transaction cost, with the break-even. */
export function CostStressCard({ costs }: { costs: CostStress }) {
  const even = breakEven(costs);
  const text = breakEvenText(costs);
  return (
    <div className="xd-card">
      <div className="xd-card-head">
        <h3>Transaction-cost stress</h3>
        <p className="xd-hint">
          Assumed cost {formatBps(costs.current_bps)} per fill
        </p>
      </div>
      <p className="xd-lede">{text}</p>
      <figure className="xd-figure" aria-labelledby="cost-caption">
        <ChartLegend
          items={[
            { label: "Sharpe ratio", tone: "strategy" },
            { label: "Assumed cost", tone: "marker", mark: "dashed" },
            ...(even.kind === "value" && even.inRange
              ? [
                  {
                    label: "Break-even",
                    tone: "break-even" as const,
                    mark: "dashed" as const,
                  },
                ]
              : []),
          ]}
        />
        <Suspense fallback={<ChartFallback height={240} />}>
          <CostStressChart costs={costs} height={240} />
        </Suspense>
        <figcaption id="cost-caption" className="xd-figcaption">
          Each level sets commission plus slippage to that many basis points per
          fill, split as configured. Sharpe is measured over a 3% risk-free
          rate, so break-even is where the strategy stops beating cash.
        </figcaption>
      </figure>
      <div className="table-scroll xd-table xd-table-compact">
        <table>
          <caption className="sr-only">Metrics at each cost level</caption>
          <thead>
            <tr>
              <th scope="col">Cost per fill</th>
              <th scope="col" className="num">
                Sharpe
              </th>
              <th scope="col" className="num">
                CAGR
              </th>
              <th scope="col" className="num">
                Total return
              </th>
            </tr>
          </thead>
          <tbody>
            {costs.levels.map((level) => {
              const assumed =
                Math.abs(level.cost_bps - costs.current_bps) < 1e-9;
              return (
                <tr
                  key={level.cost_bps}
                  className={assumed ? "is-marked" : undefined}
                >
                  <th scope="row">
                    {formatBps(level.cost_bps)}
                    {assumed ? <span className="tag">assumed</span> : null}
                  </th>
                  <td className="num">{decimal(level.sharpe)}</td>
                  <td className="num">{percent(level.cagr)}</td>
                  <td className="num">{percent(level.total_return)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
