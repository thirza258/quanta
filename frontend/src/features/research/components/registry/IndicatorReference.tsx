import type { ResearchOptions } from "@/features/research/model/registry";
import { BookOpenText, ChevronDown } from "lucide-react";

// The series the guided runtime passes as `data` (execution/sandbox_worker.py).
const columns = [
  "open",
  "high",
  "low",
  "close",
  "volume",
  "returns",
  "sma_50",
  "sma_200",
];

export function IndicatorReference({
  indicators,
}: {
  indicators: ResearchOptions["indicators"];
}) {
  return (
    <details className="registry-reference">
      <summary>
        <BookOpenText size={15} aria-hidden="true" />
        <span>
          Indicator reference
          <small>
            {columns.length} data columns · {indicators.length} helpers
          </small>
        </span>
        <ChevronDown size={14} aria-hidden="true" />
      </summary>
      <div className="registry-reference-body">
        <p>
          <strong>data["…"]</strong>{" "}
          {columns.map((column) => (
            <code key={column}>{column}</code>
          ))}
        </p>
        <dl>
          {indicators.map((indicator) => (
            <div key={indicator.name}>
              <dt>
                <code>{indicator.signature}</code>
              </dt>
              <dd>{indicator.description}</dd>
            </div>
          ))}
        </dl>
        <p className="registry-hint">
          Return a true/false series. A signal at a close is traded at the next
          open, and the red team truncates the data to check that no value
          depends on a later bar.
        </p>
      </div>
    </details>
  );
}
