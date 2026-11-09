import type {
  SeedDispersion,
  SeedPath,
} from "@/features/research/model/registry";
import {
  formatNumber,
  niceScale,
  position,
} from "@/features/research/model/experiment";
import { decimal, percent } from "@/shared/lib/format";
import { Stat, StatusBadge } from "./ui";

type Completed = Exclude<SeedDispersion, { status: "skipped" | "undefined" }>;

const beats = (path: SeedPath) => {
  const s = path.strategy.sharpe,
    b = path.benchmark.sharpe;
  if (s == null) return false;
  return b == null || s > b;
};

/**
 * Strategy vs buy-and-hold Sharpe on alternative synthetic paths: a dumbbell
 * per seed, with the original path first and highlighted.
 */
export function SeedPaths({ seeds }: { seeds: Completed }) {
  const rows = [
    { path: seeds.original, original: true },
    ...seeds.paths.map((path) => ({ path, original: false })),
  ];
  const { domain, ticks } = niceScale(
    rows.flatMap(({ path }) => [path.strategy.sharpe, path.benchmark.sharpe]),
    4,
  );
  const at = (value: number) => `${position(value, domain)}%`;
  return (
    <>
      <div className="xd-kpis xd-kpis-compact">
        <Stat
          label="Beats buy & hold"
          value={percent(seeds.beats_benchmark_share, 0)}
          sub={`of ${seeds.paths.length} alternative ${seeds.paths.length === 1 ? "path" : "paths"}`}
        />
        <Stat
          label="Mean Sharpe"
          value={decimal(seeds.mean_sharpe)}
          sub={
            seeds.std_sharpe != null
              ? `± ${decimal(seeds.std_sharpe)} across paths`
              : "Spread undefined"
          }
        />
        <Stat
          label="Positive Sharpe"
          value={percent(seeds.positive_share, 0)}
          sub="of alternative paths"
        />
        <Stat
          label="Original path z-score"
          value={decimal(seeds.original_z)}
          sub="Original Sharpe vs the alternatives"
        />
      </div>
      <div className="table-scroll xd-table xd-table-full xd-dumbbell">
        <table>
          <caption className="sr-only">
            Sharpe ratio of the strategy and of buy-and-hold on each synthetic
            path; the first row is the path the experiment was run on
          </caption>
          <thead>
            <tr>
              <th scope="col">Path</th>
              <th scope="col" className="num">
                Strategy
              </th>
              <th scope="col" className="num">
                Buy & hold
              </th>
              <th scope="col" className="xd-dumbbell-head">
                <span className="sr-only">Comparison</span>
                <span className="xd-axis" aria-hidden="true">
                  {ticks.map((tick) => (
                    <span key={tick} style={{ left: at(tick) }}>
                      {formatNumber(tick)}
                    </span>
                  ))}
                </span>
              </th>
              <th scope="col">Result</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(({ path, original }) => {
              const s = path.strategy.sharpe,
                b = path.benchmark.sharpe;
              const won = beats(path);
              return (
                <tr
                  key={`${path.seed}-${original}`}
                  className={original ? "is-marked" : undefined}
                >
                  <th scope="row">
                    Seed {path.seed}
                    {original ? <span className="tag">original</span> : null}
                  </th>
                  <td className="num">{decimal(s)}</td>
                  <td className="num">{decimal(b)}</td>
                  <td className="xd-dumbbell-plot" aria-hidden="true">
                    <span className="xd-track">
                      <span className="xd-track-zero" style={{ left: at(0) }} />
                      {s != null && b != null ? (
                        <span
                          className="xd-track-link"
                          style={{
                            left: at(Math.min(s, b)),
                            width: `${Math.abs(position(s, domain) - position(b, domain))}%`,
                          }}
                        />
                      ) : null}
                      {b != null ? (
                        <span
                          className="xd-dot is-context"
                          style={{ left: at(b) }}
                        />
                      ) : null}
                      {s != null ? (
                        <span
                          className="xd-dot is-strategy"
                          style={{ left: at(s) }}
                        />
                      ) : null}
                    </span>
                  </td>
                  <td>
                    <StatusBadge
                      tone={won ? "pass" : "fail"}
                      label={won ? "Beats" : "Trails"}
                    />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}
