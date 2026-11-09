import {
  BARS_PER_YEAR,
  datasetBars,
  datasetRules,
  type ComposerForm,
} from "@/features/research/model/grid";
import type { ResearchOptions } from "@/features/research/model/registry";
import type { Params as DatasetParams } from "@/features/research/model/types";
import { Database, Sparkles, TriangleAlert } from "lucide-react";
import { Link } from "react-router-dom";
import { NumberField, Segmented, SelectField } from "./fields";

type Dataset = ComposerForm["dataset"];

const formatDay = (value: string) => {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleDateString();
};

export function DataFields({
  dataset,
  options,
  issues,
  onChange,
}: {
  dataset: Dataset;
  options: ResearchOptions;
  issues: Record<string, string>;
  onChange: (dataset: Dataset) => void;
}) {
  const { kind, params } = dataset;
  const set = (patch: Partial<DatasetParams>) =>
    onChange({ kind, params: { ...params, ...patch } });
  const number = (
    key: keyof typeof datasetRules,
    label: string,
    extra: { suffix?: string; hint?: string; step?: number } = {},
  ) => (
    <NumberField
      id={`composer-dataset-${key}`}
      label={label}
      value={params[key]}
      rule={datasetRules[key]}
      error={issues[`dataset.${key}`]}
      onChange={(value) => set({ [key]: value })}
      {...extra}
    />
  );
  const bars = datasetBars(dataset);
  const imported = options.historical;
  const versions = imported.find((h) => h.symbol === params.symbol)?.versions;
  const latest = versions?.[versions.length - 1];
  return (
    <>
      <Segmented
        name="composer-source"
        legend="Data source"
        hideLegend
        value={kind}
        options={[
          {
            value: "synthetic",
            label: (
              <>
                <Sparkles size={14} aria-hidden="true" />
                Synthetic market
              </>
            ),
          },
          {
            value: "historical",
            label: (
              <>
                <Database size={14} aria-hidden="true" />
                Historical data
              </>
            ),
          },
        ]}
        onChange={(next) => onChange({ kind: next, params })}
      />
      {kind === "synthetic" ? (
        <>
          <div className="registry-fields is-wide">
            <SelectField
              id="composer-dataset-model"
              label="Process"
              value={params.model}
              options={options.synthetic.models}
              onChange={(model) =>
                set({ model: model as DatasetParams["model"] })
              }
            />
            <SelectField
              id="composer-dataset-scenario"
              label="Scenario"
              value={params.scenario}
              options={options.synthetic.scenarios}
              onChange={(scenario) => set({ scenario })}
            />
          </div>
          <div className="registry-fields">
            {number("years", "Horizon", { suffix: "years" })}
            {number("seed", "Seed", { hint: "Same seed, same market." })}
            {number("mu", "Drift μ", { suffix: "% / yr", step: 1 })}
            {number("sigma", "Volatility σ", { suffix: "% / yr", step: 1 })}
            {params.model === "merton"
              ? number("jump_frequency", "Jumps per year", { step: 0.5 })
              : null}
            {params.model === "heston" ? (
              <>
                {number("kappa", "Mean reversion κ", { step: 0.1 })}
                {number("theta", "Long-run variance θ", { step: 0.01 })}
                {number("xi", "Vol of variance ξ", { step: 0.05 })}
                {number("rho", "Correlation ρ", { step: 0.05 })}
              </>
            ) : null}
          </div>
          {params.scenario !== "custom" ? (
            <p className="registry-note">
              Named scenarios fix some settings (the process, drift or
              volatility) to recreate their stress. Your values apply wherever
              the scenario leaves them open.
            </p>
          ) : null}
          {bars ? (
            <p className="registry-hint">
              {params.years} {params.years === 1 ? "year" : "years"} ×{" "}
              {BARS_PER_YEAR} sessions = <span className="mono">{bars}</span>{" "}
              bars, generated from the seed. The red team also regenerates the
              market from other seeds.
            </p>
          ) : null}
        </>
      ) : (
        <>
          <div className="registry-fields">
            <SelectField
              id="composer-dataset-symbol"
              label="Imported dataset"
              value={params.symbol ?? ""}
              options={imported.map((h) => ({ id: h.symbol, label: h.symbol }))}
              placeholder={
                imported.length
                  ? "Select an imported dataset"
                  : "No datasets imported"
              }
              disabled={!imported.length}
              error={imported.length ? issues["dataset.symbol"] : undefined}
              hint={
                latest
                  ? `Version ${latest.version} · sha256 ${latest.sha256.slice(0, 12)}… · ${formatDay(latest.created_at)}`
                  : undefined
              }
              onChange={(symbol) => set({ symbol: symbol || undefined })}
            />
            {number("years", "History to use", {
              suffix: "years",
              hint: "The first years of the file.",
            })}
          </div>
          {imported.length ? (
            <p className="registry-hint">
              Up to <span className="mono">{bars}</span> bars. Imported data is
              hashed with every run, so a changed file shows up in the
              provenance.
            </p>
          ) : (
            <p
              className="registry-note is-warning"
              data-issue="symbol"
              tabIndex={-1}
            >
              <TriangleAlert size={14} aria-hidden="true" />
              <span>
                No historical dataset is imported yet. Import an OHLCV CSV as
                described in <Link to="/methodology">How Quanta works</Link>, or
                test the idea on a synthetic market.
              </span>
            </p>
          )}
        </>
      )}
    </>
  );
}
