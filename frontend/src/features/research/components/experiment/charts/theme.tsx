// Shared recharts styling for the experiment page. Colours are CSS variables
// defined on `.xd` (light and dark), so charts follow the theme toggle.
import type { TooltipContentProps } from "recharts";

export const axisTick = { fontSize: 11, fill: "var(--muted)" };
export const gridStroke = "var(--xd-grid)";
export const baselineStroke = "var(--xd-baseline)";
/** The zero line on Sharpe charts: above it the strategy beats cash. */
export const zeroStroke = "var(--xd-zero)";
export const activeDot = {
  r: 4,
  stroke: "var(--bg)",
  strokeWidth: 2,
};
export const lineCursor = { stroke: "var(--muted)", strokeWidth: 1 };
export const barCursor = { fill: "var(--xd-hover)" };

export type TooltipRow = {
  key: string;
  name: string;
  tone: "strategy" | "context" | "loss" | "pos" | "neg";
  format: (value: number | null) => string;
};

/**
 * A tooltip that lists every series at the hovered X, value first and the
 * series name second, keyed with a short line in the series colour.
 */
export function makeTooltip({
  rows,
  label,
}: {
  rows: TooltipRow[];
  label: (
    label: string | number | undefined,
    datum: Record<string, unknown>,
  ) => string;
}) {
  return function ChartTooltip({
    active,
    payload,
    label: raw,
  }: TooltipContentProps) {
    if (!active || !payload?.length) return null;
    const datum = (payload[0]?.payload ?? {}) as Record<string, unknown>;
    return (
      <div className="xd-tooltip">
        <div className="xd-tooltip-label">{label(raw, datum)}</div>
        {rows.map((row) => {
          const value = datum[row.key];
          return (
            <div className="xd-tooltip-row" key={row.key}>
              <i className={`xd-key xd-key-line is-${row.tone}`} />
              <strong>
                {row.format(typeof value === "number" ? value : null)}
              </strong>
              <span>{row.name}</span>
            </div>
          );
        })}
      </div>
    );
  };
}
