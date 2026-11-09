import type { Surface } from "@/features/research/model/registry";
import type { SurfaceCell } from "@/features/research/model/experiment";
import {
  binClass,
  DIVERGING_STEPS,
  divergingBin,
  formatNumber,
  formatParams,
  pointAt,
  sharpeExtent,
  surfaceGrid,
} from "@/features/research/model/experiment";
import { decimal } from "@/shared/lib/format";
import { lazy, Suspense, useMemo, useState } from "react";
import { ChartFallback } from "./ui";

const SharpeByValueChart = lazy(() => import("./charts/SharpeByValueChart"));

const marks = (cell: SurfaceCell) =>
  [cell.base ? "Base" : "", cell.best ? "Best" : ""]
    .filter(Boolean)
    .join(" · ");

function DivergingScale({ extent }: { extent: number }) {
  const bins = Array.from(
    { length: DIVERGING_STEPS * 2 + 1 },
    (_, i) => i - DIVERGING_STEPS,
  );
  return (
    <div className="xd-scale">
      <span className="xd-scale-title">Sharpe ratio</span>
      <span className="xd-scale-end">−{decimal(extent)}</span>
      <span
        className="xd-scale-swatches"
        role="img"
        aria-label={`Colour scale from −${decimal(extent)} in rose, through grey at zero, to +${decimal(extent)} in blue. Every cell also prints its value.`}
      >
        {bins.map((bin) => (
          <i key={bin} className={binClass(bin)} />
        ))}
      </span>
      <span className="xd-scale-end">+{decimal(extent)}</span>
      <span className="xd-scale-keys">
        <i className="xd-scale-key is-base" aria-hidden="true" /> Base
        <i className="xd-scale-key is-best" aria-hidden="true" /> Best
        <i className="xd-scale-key is-na" aria-hidden="true" /> Undefined
      </span>
    </div>
  );
}

/**
 * The parameter-robustness surface: a heatmap for two or more parameters
 * (extra parameters sliced by a selector), bars for one, a note for none.
 */
export function ParameterSurface({ surface }: { surface: Surface }) {
  const [selection, setSelection] = useState<Record<string, number>>({});
  const grid = useMemo(
    () => surfaceGrid(surface, selection),
    [surface, selection],
  );
  const range = useMemo(
    () => sharpeExtent(surface.points.map((p) => p.sharpe)),
    [surface],
  );
  const order = surface.parameters.map((p) => p.name);
  const base = pointAt(surface, surface.base);

  if (grid.kind === "single")
    return (
      <div className="xd-skipped">
        <p>
          <strong>Only one configuration was tested.</strong> There is no
          surface to inspect, so sensitivity to the parameters is unknown
          {grid.point ? ` (Sharpe ${decimal(grid.point.sharpe)})` : ""}. Add a
          parameter grid to the specification to see whether nearby settings
          keep the result.
        </p>
      </div>
    );

  if (grid.kind === "line")
    return (
      <figure className="xd-figure" aria-labelledby="surface-caption">
        <Suspense fallback={<ChartFallback height={230} />}>
          <SharpeByValueChart
            name={grid.parameter.name}
            cells={grid.cells}
            height={230}
          />
        </Suspense>
        <figcaption id="surface-caption" className="xd-figcaption">
          Sharpe ratio for each tested value of{" "}
          <code>{grid.parameter.name}</code>. Blue bars are positive, rose bars
          negative; base and best are labelled under the axis.
        </figcaption>
        <details className="xd-details">
          <summary>Show the values as a table</summary>
          <div className="table-scroll xd-table">
            <table>
              <thead>
                <tr>
                  <th scope="col">{grid.parameter.name}</th>
                  <th scope="col" className="num">
                    Sharpe
                  </th>
                  <th scope="col">Marked</th>
                </tr>
              </thead>
              <tbody>
                {grid.cells.map((cell) => (
                  <tr key={cell.value}>
                    <th scope="row">{formatNumber(cell.value)}</th>
                    <td className="num">
                      {cell.point ? decimal(cell.point.sharpe) : "Not run"}
                    </td>
                    <td>{marks(cell) || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </details>
      </figure>
    );

  const sliceText = grid.slices
    .map((s) => `${s.name} = ${formatNumber(s.selected)}`)
    .join(", ");
  return (
    <div className="xd-surface">
      {grid.slices.length ? (
        <div className="xd-slices">
          {grid.slices.map((slice) => (
            <label className="field xd-slice" key={slice.name}>
              Slice at {slice.name}
              <select
                value={String(slice.selected)}
                onChange={(event) =>
                  setSelection({
                    ...selection,
                    [slice.name]: Number(event.target.value),
                  })
                }
              >
                {slice.values.map((value) => (
                  <option key={value} value={String(value)}>
                    {formatNumber(value)}
                    {base && base.params[slice.name] === value ? " (base)" : ""}
                  </option>
                ))}
              </select>
            </label>
          ))}
        </div>
      ) : null}
      <div className="xd-heatmap-scroll">
        <table className="xd-heatmap">
          <caption>
            Sharpe ratio by <code>{grid.rows.name}</code> (rows) and{" "}
            <code>{grid.columns.name}</code> (columns)
            {sliceText ? `, sliced at ${sliceText}` : ""}
          </caption>
          <thead>
            <tr>
              <td className="xd-corner">
                <span>
                  {grid.rows.name} ↓ · {grid.columns.name} →
                </span>
              </td>
              {grid.columns.values.map((value) => (
                <th scope="col" key={value}>
                  {formatNumber(value)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {grid.cells.map((row, r) => (
              <tr key={grid.rows.values[r]}>
                <th scope="row">{formatNumber(grid.rows.values[r])}</th>
                {row.map((cell) => {
                  const sharpe = cell.point?.sharpe ?? null;
                  const bin = cell.point ? divergingBin(sharpe, range) : null;
                  const mark = marks(cell);
                  const where = cell.point
                    ? formatParams(cell.point.params, order)
                    : `${grid.rows.name}=${formatNumber(grid.rows.values[r])} · ${grid.columns.name}=${formatNumber(cell.value)}`;
                  return (
                    <td
                      key={cell.value}
                      className={[
                        "xd-cell",
                        binClass(bin),
                        cell.base ? "is-base" : "",
                        cell.best ? "is-best" : "",
                      ]
                        .filter(Boolean)
                        .join(" ")}
                      title={`${where}: ${cell.point ? `Sharpe ${decimal(sharpe)}` : "not tested"}${mark ? ` (${mark.toLowerCase()})` : ""}`}
                    >
                      <span className="xd-cell-value">
                        {cell.point ? decimal(sharpe) : "n/a"}
                      </span>
                      {mark ? (
                        <span className="xd-cell-tag">{mark}</span>
                      ) : null}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <DivergingScale extent={range} />
    </div>
  );
}
