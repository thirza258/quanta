import {
  costRules,
  datasetBars,
  MIN_TEST,
  MIN_TRAIN,
  splitBars,
  validationRules,
  walkForwardFolds,
  type ComposerForm,
} from "@/features/research/model/grid";
import { NumberField, Segmented, Switch } from "./fields";

type Validation = ComposerForm["validation"];
type Costs = ComposerForm["costs"];

export function ValidationFields({
  validation,
  dataset,
  issues,
  onChange,
}: {
  validation: Validation;
  dataset: ComposerForm["dataset"];
  issues: Record<string, string>;
  onChange: (validation: Validation) => void;
}) {
  const set = (patch: Partial<Validation>) =>
    onChange({ ...validation, ...patch });
  const number = (
    key: keyof typeof validationRules,
    label: string,
    extra: { suffix?: string; hint?: string; disabled?: boolean } = {},
  ) => (
    <NumberField
      id={`composer-validation-${key}`}
      label={label}
      value={validation[key]}
      rule={validationRules[key]}
      error={issues[`validation.${key}`]}
      onChange={(value) => set({ [key]: value })}
      {...extra}
    />
  );
  const bars = datasetBars(dataset);
  const about = dataset.kind === "historical" ? "up to " : "";
  const percent = Math.round(validation.split * 100);
  const cut = splitBars(bars, validation.split);
  const folds = walkForwardFolds(
    bars,
    validation.train_bars,
    validation.test_bars,
  );
  const sized =
    Number.isFinite(validation.train_bars) &&
    Number.isFinite(validation.test_bars);
  return (
    <>
      <div className="registry-split">
        <div className="registry-split-head">
          <label htmlFor="composer-validation-split">Train / test split</label>
          <output htmlFor="composer-validation-split" className="mono">
            {percent}% / {100 - percent}%
          </output>
        </div>
        <input
          id="composer-validation-split"
          type="range"
          min={50}
          max={90}
          step={1}
          value={percent}
          aria-valuetext={`${percent}% in-sample, ${100 - percent}% out-of-sample`}
          onChange={(event) => set({ split: Number(event.target.value) / 100 })}
        />
        <div className="registry-split-bar" aria-hidden="true">
          <span style={{ width: `${percent}%` }}>In-sample</span>
          <span>Out-of-sample</span>
        </div>
        {bars ? (
          <p className={cut.ok ? "registry-hint" : "registry-warning"}>
            {cut.ok
              ? `The grid is ranked on ${about}${cut.train} bars; the chosen configuration is then tested on ${about}${cut.test} bars it has never seen.`
              : `This split leaves ${cut.train} training and ${cut.test} test bars; the check needs at least ${MIN_TRAIN} and ${MIN_TEST}, so it would be skipped.`}
          </p>
        ) : null}
      </div>
      <Switch
        id="composer-validation-walk_forward"
        checked={validation.walk_forward}
        onChange={(walk_forward) => set({ walk_forward })}
        label="Walk-forward analysis"
        description="Re-pick the best configuration on each training window, then score it on the next window it has not seen."
      />
      <div
        className={`registry-fields registry-walk-forward${validation.walk_forward ? "" : " is-off"}`}
      >
        {number("train_bars", "Training bars", {
          suffix: "bars",
          disabled: !validation.walk_forward,
        })}
        {number("test_bars", "Test bars", {
          suffix: "bars",
          disabled: !validation.walk_forward,
        })}
        <Segmented
          name="composer-validation-anchored"
          legend="Training window"
          disabled={!validation.walk_forward}
          value={validation.anchored ? "anchored" : "rolling"}
          options={[
            { value: "rolling", label: "Rolling" },
            { value: "anchored", label: "Anchored" },
          ]}
          onChange={(mode) => set({ anchored: mode === "anchored" })}
        />
      </div>
      {validation.walk_forward && bars && sized ? (
        <p className={folds >= 2 ? "registry-hint" : "registry-warning"}>
          {folds >= 2
            ? `${dataset.kind === "historical" ? "Up to " : ""}${folds} test windows of up to ${validation.test_bars} bars. ${validation.anchored ? "Anchored windows grow from the first bar." : "Rolling windows keep the latest training bars."}`
            : `Two test windows need at least ${validation.train_bars + 2 * MIN_TEST} bars; this dataset has ${about}${bars}, so walk-forward would be skipped.`}
        </p>
      ) : null}
      <div className="registry-fields">
        {number("permutations", "Random-timing permutations", {
          hint: "Keeps your exposure but shuffles when it happens, to test whether luck explains the Sharpe. 0 skips it.",
        })}
        {dataset.kind === "synthetic"
          ? number("seed_paths", "Alternative market paths", {
              hint: "Regenerates the market from other seeds: an edge should not depend on one path.",
            })
          : null}
      </div>
    </>
  );
}

export function CostFields({
  costs,
  issues,
  onChange,
}: {
  costs: Costs;
  issues: Record<string, string>;
  onChange: (costs: Costs) => void;
}) {
  const number = (
    key: keyof typeof costRules,
    label: string,
    suffix: string,
    hint?: string,
  ) => (
    <NumberField
      id={`composer-costs-${key}`}
      label={label}
      value={costs[key]}
      rule={costRules[key]}
      suffix={suffix}
      hint={hint}
      error={issues[`costs.${key}`]}
      onChange={(value) => onChange({ ...costs, [key]: value })}
    />
  );
  return (
    <>
      <div className="registry-fields">
        {number("capital", "Starting capital", "USD")}
        {number(
          "commission_bps",
          "Commission",
          "bps",
          "Per fill; 1 bp = 0.01%.",
        )}
        {number("slippage_bps", "Slippage", "bps", "Per fill, against you.")}
      </div>
      <p className="registry-hint">
        Charged on every fill. The red team also reruns the strategy at higher
        costs to find where the edge breaks even.
      </p>
    </>
  );
}
