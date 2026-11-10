// Pure helpers behind the experiment composer (/research/new): parameter grids,
// strategy-code introspection, the sandbox prefill and pre-submit validation.
// The rules mirror the backend (domain/research/spec.py, analytics.DatasetParams
// and domain/research/validation.py), so a form that passes here is accepted.
import type {
  ExperimentSpec,
  GridParameter,
  ResearchOptions,
} from "@/features/research/model/registry";
import type {
  Config,
  Params as DatasetParams,
} from "@/features/research/model/types";

export const NAME_PATTERN = /^[a-z][a-z0-9_]{0,23}$/;
export const VALUE_BOUND = 1_000_000;
export const STRATEGY_NAME_MAX = 80;
export const BARS_PER_YEAR = 252;
// validation.py: the shortest training and test windows a check accepts.
export const MIN_TRAIN = 126;
export const MIN_TEST = 63;
export const MAX_FOLDS = 40;

type Limits = ResearchOptions["limits"];
type GridLimits = Pick<Limits, "parameters" | "values" | "configurations">;
const defaultLimits: GridLimits = {
  parameters: 3,
  values: 12,
  configurations: 60,
};

export class GridError extends Error {}

/** Drop binary noise (0.1 + 0.2) by rounding to 10 decimals; never returns −0. */
export function tidy(value: number) {
  const rounded = Number(value.toFixed(10));
  return rounded === 0 ? 0 : rounded;
}

function checkBound(value: number) {
  if (Math.abs(value) > VALUE_BOUND)
    throw new GridError("Values must stay within ±1,000,000.");
}

/** Inclusive arithmetic range: rangeValues(10, 30, 10) → [10, 20, 30]. */
export function rangeValues(
  from: number,
  to: number,
  step: number,
  limit = defaultLimits.values,
): number[] {
  if (![from, to, step].every(Number.isFinite))
    throw new GridError("Enter numbers for from, to and step.");
  if (step <= 0) throw new GridError("The step must be greater than zero.");
  if (to < from) throw new GridError("“To” must be at least “from”.");
  checkBound(from);
  checkBound(to);
  const count = Math.floor(tidy((to - from) / step)) + 1;
  if (count > limit)
    throw new GridError(
      `That range has ${count > 9999 ? "thousands of" : count} values; the limit is ${limit}.`,
    );
  return Array.from({ length: count }, (_, i) => tidy(from + i * step));
}

/**
 * Comma- or space-separated numbers, de-duplicated and sorted ascending: the
 * robustness surface treats adjacent grid values as neighbours.
 */
export function parseValues(
  text: string,
  limit = defaultLimits.values,
): number[] {
  const tokens = text.split(/[\s,;]+/).filter(Boolean);
  if (!tokens.length) throw new GridError("Enter at least one value.");
  const values = new Set<number>();
  for (const token of tokens) {
    const value = Number(token);
    if (!Number.isFinite(value))
      throw new GridError(`“${token}” is not a number.`);
    checkBound(value);
    values.add(tidy(value));
  }
  if (values.size > limit)
    throw new GridError(`${values.size} values; the limit is ${limit}.`);
  return [...values].sort((a, b) => a - b);
}

export const configurationCount = <T extends { values: unknown[] }>(
  parameters: T[],
) =>
  parameters.reduce((count, parameter) => count * parameter.values.length, 1);

/**
 * Parameter names of the first `def strategy(...)`, or null when there is no
 * complete definition. Annotations, defaults, comments and line breaks are
 * skipped; bare `*` and `/` markers are not parameters.
 */
export function strategyParams(code: string): string[] | null {
  const match = /^[ \t]*def[ \t]+strategy[ \t]*\(/m.exec(code);
  if (!match) return null;
  const names: string[] = [];
  const push = (segment: string) => {
    const name = /^\s*\**\s*([A-Za-z_]\w*)/.exec(segment)?.[1];
    if (name) names.push(name);
  };
  let depth = 0,
    quote = "",
    segment = "";
  for (let i = match.index + match[0].length; i < code.length; i++) {
    const char = code[i];
    if (quote) {
      if (char === "\\") i++;
      else if (char === quote) quote = "";
      continue;
    }
    if (char === "#") {
      const end = code.indexOf("\n", i);
      i = end < 0 ? code.length : end - 1;
      continue;
    }
    if (char === '"' || char === "'") {
      quote = char;
      continue;
    }
    if ("([{".includes(char)) depth++;
    else if (")]}".includes(char)) {
      if (depth === 0) {
        push(segment);
        return names;
      }
      depth--;
    } else if (char === "," && depth === 0) {
      push(segment);
      segment = "";
      continue;
    }
    segment += char;
  }
  return null;
}

export const strategyArity = (code: string) =>
  strategyParams(code)?.length ?? null;

/** Names the code reads as params["name"], params['name'] or params.get("name"). */
export function referencedParams(code: string): string[] {
  const declared = strategyParams(code);
  const holder = declared && declared.length > 1 ? declared[1] : "params";
  const pattern = new RegExp(
    `\\b${holder}\\s*(?:\\[\\s*(["'])([A-Za-z_]\\w*)\\1\\s*\\]|\\.get\\(\\s*(["'])([A-Za-z_]\\w*)\\3)`,
    "g",
  );
  const found: string[] = [];
  for (const match of code.replace(/#[^\n]*/g, "").matchAll(pattern)) {
    const name = match[2] ?? match[4];
    if (!found.includes(name)) found.push(name);
  }
  return found;
}

// ------------------------------------------------------------ grid drafts

/** One editable grid row: values are typed as a list or generated from a range. */
export type GridDraft = {
  id: string;
  name: string;
  mode: "list" | "range";
  list: string;
  from: string;
  to: string;
  step: string;
  base: number | null;
};

export type GridRow = {
  values: number[];
  base: number | null;
  nameError?: string;
  valuesError?: string;
};

export type GridResolution = {
  rows: GridRow[];
  parameters: GridParameter[];
  base: Record<string, number>;
  count: number;
  complete: boolean;
  error?: string;
};

function uniformStep(sorted: number[]) {
  if (sorted.length < 2) return null;
  const step = tidy(sorted[1] - sorted[0]);
  return sorted.every((v, i) => i === 0 || tidy(v - sorted[i - 1]) === step)
    ? step
    : null;
}

function smallestGap(sorted: number[]) {
  const gaps = sorted.slice(1).map((v, i) => tidy(v - sorted[i]));
  return gaps.length ? Math.min(...gaps) : null;
}

let draftCount = 0;
export function newDraft(parameter?: GridParameter, base?: number): GridDraft {
  const values = parameter ? [...parameter.values].sort((a, b) => a - b) : [];
  const step = uniformStep(values) ?? smallestGap(values);
  return {
    id: `parameter-${++draftCount}`,
    name: parameter?.name ?? "",
    mode: "list",
    list: values.join(", "),
    from: values.length ? String(values[0]) : "",
    to: values.length ? String(values[values.length - 1]) : "",
    step: step === null ? "" : String(step),
    base: base ?? null,
  };
}

const readNumber = (text: string) => (text.trim() ? Number(text) : NaN);

export function draftValues(
  draft: GridDraft,
  limit = defaultLimits.values,
):
  | { values: number[]; error?: undefined }
  | { values?: undefined; error: string } {
  try {
    return {
      values:
        draft.mode === "range"
          ? rangeValues(
              readNumber(draft.from),
              readNumber(draft.to),
              readNumber(draft.step),
              limit,
            )
          : parseValues(draft.list, limit),
    };
  } catch (error) {
    if (error instanceof GridError) return { error: error.message };
    throw error;
  }
}

/** Switch how a row is entered while keeping its values where possible. */
export function switchDraftMode(
  draft: GridDraft,
  mode: GridDraft["mode"],
  limit = defaultLimits.values,
): GridDraft {
  if (draft.mode === mode) return draft;
  const { values } = draftValues(draft, limit);
  if (!values) return { ...draft, mode };
  if (mode === "list") return { ...draft, mode, list: values.join(", ") };
  const step = uniformStep(values) ?? smallestGap(values);
  return {
    ...draft,
    mode,
    from: String(values[0]),
    to: String(values[values.length - 1]),
    step: step === null ? draft.step || "1" : String(step),
  };
}

/** Validate every row; the base defaults to the middle value, as the backend does. */
export function resolveGrid(
  drafts: GridDraft[],
  limits: GridLimits = defaultLimits,
): GridResolution {
  const names = drafts.map((draft) => draft.name.trim());
  const rows = drafts.map((draft, i): GridRow => {
    const name = names[i];
    const result = draftValues(draft, limits.values);
    const values = result.values ?? [];
    return {
      values,
      base: values.length
        ? draft.base !== null && values.includes(draft.base)
          ? draft.base
          : values[Math.floor(values.length / 2)]
        : null,
      nameError: !name
        ? "Name the parameter."
        : !NAME_PATTERN.test(name)
          ? "Start with a lowercase letter; then use a–z, 0–9 or _ (24 at most)."
          : names.indexOf(name) !== i
            ? "Another parameter already uses this name."
            : undefined,
      valuesError: result.error,
    };
  });
  const complete = rows.every((row) => !row.nameError && !row.valuesError);
  const count = configurationCount(rows);
  return {
    rows,
    parameters: rows.map((row, i) => ({ name: names[i], values: row.values })),
    base: Object.fromEntries(
      rows.flatMap((row, i) =>
        row.base === null ? [] : [[names[i], row.base] as const],
      ),
    ),
    count,
    complete,
    error:
      drafts.length > limits.parameters
        ? `Use at most ${limits.parameters} parameters.`
        : complete && count > limits.configurations
          ? `${count} configurations exceed the limit of ${limits.configurations}. Remove values or a parameter.`
          : undefined,
  };
}

// ------------------------------------------------------------ the form

export type ComposerForm = {
  title: string;
  hypothesis: string;
  dataset: ExperimentSpec["dataset"];
  name: string;
  code: string;
  grid: GridDraft[];
  costs: ExperimentSpec["costs"];
  validation: ExperimentSpec["validation"];
};

export function formFromSpec(
  spec: ExperimentSpec,
  title = "",
  hypothesis = "",
): ComposerForm {
  return {
    title,
    hypothesis,
    dataset: { kind: spec.dataset.kind, params: { ...spec.dataset.params } },
    name: spec.strategy.name,
    code: spec.strategy.code,
    grid: spec.strategy.parameters.map((parameter) =>
      newDraft(parameter, spec.strategy.base[parameter.name]),
    ),
    costs: { ...spec.costs },
    validation: { ...spec.validation },
  };
}

export type NumberRule = {
  label: string;
  min: number;
  max: number;
  integer?: boolean;
  /** The minimum itself is not allowed. */
  above?: boolean;
  /** Displayed value = stored value × scale (fractions shown as percentages). */
  scale?: number;
  unit?: string;
};

type DatasetNumber = {
  [K in keyof DatasetParams]-?: DatasetParams[K] extends number ? K : never;
}[keyof DatasetParams];
type ValidationNumber =
  "train_bars" | "test_bars" | "permutations" | "seed_paths";

export const datasetRules: Record<DatasetNumber, NumberRule> = {
  years: { label: "Years", min: 1, max: 30, integer: true },
  seed: { label: "Seed", min: 0, max: 4294967295, integer: true },
  mu: { label: "Drift μ", min: -1, max: 1, scale: 100, unit: "%" },
  sigma: { label: "Volatility σ", min: 0.001, max: 2, scale: 100, unit: "%" },
  jump_frequency: { label: "Jumps per year", min: 0, max: 50 },
  kappa: { label: "Mean reversion κ", min: 0, max: 20, above: true },
  theta: { label: "Long-run variance θ", min: 0, max: 2, above: true },
  xi: { label: "Vol of variance ξ", min: 0, max: 2 },
  rho: { label: "Correlation ρ", min: -1, max: 1 },
  window: { label: "Window", min: 2, max: 252, integer: true },
};

export const costRules: Record<keyof ExperimentSpec["costs"], NumberRule> = {
  capital: { label: "Capital", min: 100, max: 1e9 },
  commission_bps: { label: "Commission", min: 0, max: 500, unit: " bps" },
  slippage_bps: { label: "Slippage", min: 0, max: 500, unit: " bps" },
};

export const validationRules: Record<ValidationNumber, NumberRule> = {
  train_bars: { label: "Training bars", min: 126, max: 5040, integer: true },
  test_bars: { label: "Test bars", min: 63, max: 2520, integer: true },
  permutations: { label: "Permutations", min: 0, max: 500, integer: true },
  seed_paths: { label: "Alternative paths", min: 0, max: 10, integer: true },
};

const keys = <K extends string>(rules: Record<K, NumberRule>) =>
  Object.keys(rules) as K[];

export function numberIssue(value: number, rule: NumberRule) {
  const scale = rule.scale ?? 1;
  const show = (v: number) =>
    `${tidy(v * scale).toLocaleString("en-US")}${rule.unit ?? ""}`;
  if (!Number.isFinite(value)) return "Enter a number.";
  if (rule.integer && !Number.isInteger(value)) return "Use a whole number.";
  if ((rule.above ? value <= rule.min : value < rule.min) || value > rule.max)
    return `Use ${rule.above ? "more than" : "at least"} ${show(rule.min)} and at most ${show(rule.max)}.`;
  return undefined;
}

/** The dataset numbers the form shows for this source and model. */
export function visibleDatasetFields(
  dataset: ExperimentSpec["dataset"],
): DatasetNumber[] {
  if (dataset.kind === "historical") return ["years"];
  const model = dataset.params.model;
  return [
    "years",
    "seed",
    "mu",
    "sigma",
    ...(model === "merton" ? (["jump_frequency"] as const) : []),
    ...(model === "heston" ? (["kappa", "theta", "xi", "rho"] as const) : []),
  ];
}

/**
 * Every reason the form cannot be submitted, keyed by field: "title",
 * "hypothesis", "name", "code", "grid", "arity", "grid:<draft id>:name",
 * "grid:<draft id>:values", "dataset.<field>", "costs.<field>" and
 * "validation.<field>".
 */
export function composerIssues(
  form: ComposerForm,
  grid: GridResolution,
  options: Pick<ResearchOptions, "limits" | "historical">,
): Record<string, string> {
  const { limits } = options;
  const issues: Record<string, string> = {};
  const title = form.title.trim(),
    hypothesis = form.hypothesis.trim(),
    name = form.name.trim();
  if (!title) issues.title = "Give the experiment a title.";
  else if (title.length > limits.title)
    issues.title = `Keep the title within ${limits.title} characters.`;
  if (hypothesis.length < limits.hypothesis_min)
    issues.hypothesis = `Write at least ${limits.hypothesis_min} characters: a claim that could be shown false.`;
  else if (hypothesis.length > limits.hypothesis_max)
    issues.hypothesis = `Keep the hypothesis within ${limits.hypothesis_max} characters.`;
  if (!name) issues.name = "Name the strategy.";
  else if (name.length > STRATEGY_NAME_MAX)
    issues.name = `Keep the name within ${STRATEGY_NAME_MAX} characters.`;
  const arity = strategyArity(form.code);
  if (!form.code.trim()) issues.code = "Write the strategy code.";
  else if (form.code.length > limits.code)
    issues.code = `The code has ${form.code.length.toLocaleString("en-US")} characters; the limit is ${limits.code.toLocaleString("en-US")}.`;
  else if (arity === 0)
    issues.code = "strategy() must accept data: def strategy(data, params):";
  form.grid.forEach((draft, i) => {
    const row = grid.rows[i];
    if (row?.nameError) issues[`grid:${draft.id}:name`] = row.nameError;
    if (row?.valuesError) issues[`grid:${draft.id}:values`] = row.valuesError;
  });
  if (grid.error) issues.grid = grid.error;
  if (form.grid.length && arity === 1)
    issues.arity =
      "strategy(data) takes one argument, so grid values never reach it. Declare def strategy(data, params): or remove the parameters.";
  if (arity !== null && arity >= 2) {
    const declaredNames = form.grid.map((d) => d.name.trim());
    const referenced = referencedParams(form.code);
    const missing = referenced.filter((name) => !declaredNames.includes(name));
    if (missing.length && !issues.grid) {
      issues.grid = `The strategy code reads params["${missing[0]}"], which has no row in the grid. Add ${missing[0]} to the parameter grid or update the code.`;
    }
  }
  if (form.dataset.kind === "historical" && !form.dataset.params.symbol)
    issues["dataset.symbol"] = options.historical.length
      ? "Choose an imported dataset."
      : "No historical dataset is imported yet.";
  for (const key of visibleDatasetFields(form.dataset)) {
    const issue = numberIssue(form.dataset.params[key], datasetRules[key]);
    if (issue) issues[`dataset.${key}`] = issue;
  }
  for (const key of keys(costRules)) {
    const issue = numberIssue(form.costs[key], costRules[key]);
    if (issue) issues[`costs.${key}`] = issue;
  }
  for (const key of keys(validationRules)) {
    if (key === "seed_paths" && form.dataset.kind === "historical") continue;
    const issue = numberIssue(form.validation[key], validationRules[key]);
    if (issue) issues[`validation.${key}`] = issue;
  }
  return issues;
}

/**
 * The spec to send. Values the form hides (another model's settings, synthetic
 * paths on historical data) fall back to the defaults when they are invalid.
 */
export function specFromForm(
  form: ComposerForm,
  grid: GridResolution,
  defaults: ExperimentSpec,
): ExperimentSpec {
  const params = { ...form.dataset.params };
  for (const key of keys(datasetRules))
    if (numberIssue(params[key], datasetRules[key]))
      params[key] = defaults.dataset.params[key];
  params.symbol =
    form.dataset.kind === "historical" && params.symbol
      ? params.symbol
      : undefined;
  const validation = {
    ...form.validation,
    split: Math.round(form.validation.split * 100) / 100,
  };
  for (const key of keys(validationRules))
    if (numberIssue(validation[key], validationRules[key]))
      validation[key] = defaults.validation[key];
  return {
    dataset: { kind: form.dataset.kind, params },
    strategy: {
      name: form.name.trim(),
      code: form.code,
      parameters: grid.parameters,
      base: grid.base,
    },
    costs: { ...form.costs },
    validation,
  };
}

/** Bars in the dataset: exact for synthetic data, an upper estimate for imports. */
export const datasetBars = (dataset: ExperimentSpec["dataset"]) =>
  Number.isFinite(dataset.params.years)
    ? Math.max(0, Math.round(dataset.params.years)) * BARS_PER_YEAR
    : 0;

/** The train/test cut validation.py makes, and whether the check can run. */
export function splitBars(bars: number, split: number) {
  const train = Math.round(bars * split);
  return {
    train,
    test: bars - train,
    ok: train >= MIN_TRAIN && bars - train >= MIN_TEST,
  };
}

/** Walk-forward test windows validation.py builds; it needs at least two. */
export function walkForwardFolds(bars: number, train: number, test: number) {
  if (!(train > 0 && test > 0)) return 0;
  let folds = 0;
  for (
    let start = train;
    start + MIN_TEST <= bars && folds < MAX_FOLDS;
    start = Math.min(start + test, bars)
  )
    folds++;
  return folds;
}

// ------------------------------------------------------------ sandbox prefill

export type LabPrefill = { code: string; config: Config; title?: string };

/** Accept router state only when it has the shape the strategy lab sends. */
export function readLabPrefill(state: unknown): LabPrefill | null {
  if (!state || typeof state !== "object") return null;
  const { code, config, title } = state as Record<string, unknown>;
  if (typeof code !== "string" || !config || typeof config !== "object")
    return null;
  const { dataset_type, dataset_params } = config as Partial<Config>;
  if (
    (dataset_type !== "synthetic" && dataset_type !== "real") ||
    !dataset_params ||
    typeof dataset_params !== "object"
  )
    return null;
  return {
    code,
    config: config as Config,
    title: typeof title === "string" ? title : undefined,
  };
}

const finite = (value: unknown, fallback: number) =>
  typeof value === "number" && Number.isFinite(value) ? value : fallback;

/**
 * Map a strategy-lab snapshot onto an experiment spec. A one-argument
 * strategy(data) gets an empty grid; a two-argument one gets a row for every
 * parameter the code reads, with the default values when the names match.
 */
export function specFromLab(
  code: string,
  config: Config,
  defaults: ExperimentSpec,
  title?: string,
  maxParameters = defaultLimits.parameters,
): ExperimentSpec {
  const kind = config.dataset_type === "real" ? "historical" : "synthetic";
  const params: DatasetParams = { ...defaults.dataset.params };
  for (const [key, value] of Object.entries(config.dataset_params))
    if (
      (typeof value === "number" && Number.isFinite(value)) ||
      (typeof value === "string" && value)
    )
      Object.assign(params, { [key]: value });
  params.symbol =
    kind === "historical" && config.dataset_params.symbol
      ? config.dataset_params.symbol
      : undefined;
  const arity = strategyArity(code);
  const names =
    arity !== null && arity >= 2
      ? referencedParams(code).slice(0, maxParameters)
      : [];
  const parameters = names.map((name) => ({
    name,
    values: [
      ...(defaults.strategy.parameters.find((p) => p.name === name)?.values ??
        []),
    ],
  }));
  return {
    dataset: { kind, params },
    strategy: {
      name: title?.trim().slice(0, STRATEGY_NAME_MAX) || "Strategy lab rule",
      code,
      parameters,
      base: Object.fromEntries(
        Object.entries(defaults.strategy.base).filter(([name]) =>
          names.includes(name),
        ),
      ),
    },
    costs: {
      capital: finite(config.capital, defaults.costs.capital),
      commission_bps: finite(
        config.commission_bps,
        defaults.costs.commission_bps,
      ),
      slippage_bps: finite(config.slippage_bps, defaults.costs.slippage_bps),
    },
    validation: { ...defaults.validation },
  };
}
