import {
  FlaskConical,
  Lightbulb,
  ListChecks,
  NotebookPen,
  RefreshCw,
  ShieldAlert,
} from "lucide-react";

const steps = [
  { label: "Hypothesis", hint: "Claim it before the data", icon: Lightbulb },
  { label: "Experiment", hint: "Rule, data, grid, costs", icon: FlaskConical },
  { label: "Validate", hint: "Out of sample, walk-forward", icon: ListChecks },
  { label: "Red team", hint: "Try to break it", icon: ShieldAlert },
  { label: "Document", hint: "Conclude and decide", icon: NotebookPen },
  { label: "Reproduce", hint: "Rerun, compare hashes", icon: RefreshCw },
];

/** The six stages every registered experiment moves through. */
export function ResearchLoop() {
  return (
    <ol className="registry-loop" aria-label="The research loop">
      {steps.map(({ label, hint, icon: Icon }, index) => (
        <li key={label} className={label === "Red team" ? "is-key" : undefined}>
          <span className="registry-loop-icon">
            <Icon size={15} aria-hidden="true" />
          </span>
          <span>
            <strong>
              <span className="mono">{index + 1}</span> {label}
            </strong>
            <small>{hint}</small>
          </span>
        </li>
      ))}
    </ol>
  );
}
