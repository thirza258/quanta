import type {
  ExperimentSpec,
  ResearchOptions,
} from "@/features/research/model/registry";
import { defaultConfig } from "@/features/research/model/types";
import { describe, expect, it } from "vitest";
import {
  composerIssues,
  configurationCount,
  draftValues,
  formFromSpec,
  GridError,
  newDraft,
  numberIssue,
  parseValues,
  rangeValues,
  readLabPrefill,
  referencedParams,
  resolveGrid,
  specFromForm,
  specFromLab,
  splitBars,
  strategyArity,
  strategyParams,
  switchDraftMode,
  walkForwardFolds,
} from "./grid";

const trendCode = `def strategy(data, params):
    fast = sma(data["close"], params["fast"])
    slow = sma(data["close"], params["slow"])
    return fast > slow
`;

const defaults: ExperimentSpec = {
  dataset: {
    kind: "synthetic",
    params: { ...defaultConfig.dataset_params, symbol: undefined },
  },
  strategy: {
    name: "Trend rule",
    code: trendCode,
    parameters: [
      { name: "fast", values: [10, 20, 30, 50] },
      { name: "slow", values: [100, 150, 200] },
    ],
    base: { fast: 20, slow: 150 },
  },
  costs: { capital: 100000, commission_bps: 5, slippage_bps: 3 },
  validation: {
    split: 0.7,
    walk_forward: true,
    train_bars: 252,
    test_bars: 126,
    anchored: false,
    permutations: 200,
    seed_paths: 5,
  },
};

const options: Pick<ResearchOptions, "limits" | "historical"> = {
  limits: {
    parameters: 3,
    values: 12,
    configurations: 60,
    code: 20000,
    title: 120,
    hypothesis_min: 12,
    hypothesis_max: 2000,
    notebook: 8000,
  },
  historical: [],
};

describe("rangeValues", () => {
  it("is inclusive", () => {
    expect(rangeValues(10, 30, 10)).toEqual([10, 20, 30]);
    expect(rangeValues(5, 5, 1)).toEqual([5]);
  });

  it("rounds away floating-point noise", () => {
    expect(rangeValues(0.1, 0.3, 0.1)).toEqual([0.1, 0.2, 0.3]);
    expect(rangeValues(0, 1, 0.25)).toEqual([0, 0.25, 0.5, 0.75, 1]);
    expect(rangeValues(-0.2, 0.2, 0.1)).toEqual([-0.2, -0.1, 0, 0.1, 0.2]);
  });

  it("stops before passing the end", () => {
    expect(rangeValues(0, 1, 0.3)).toEqual([0, 0.3, 0.6, 0.9]);
  });

  it("refuses a step that is not positive", () => {
    expect(() => rangeValues(1, 5, 0)).toThrow(GridError);
    expect(() => rangeValues(1, 5, -1)).toThrow("greater than zero");
  });

  it("refuses more values than the limit", () => {
    expect(rangeValues(1, 12, 1)).toHaveLength(12);
    expect(() => rangeValues(1, 13, 1)).toThrow("13 values; the limit is 12");
    expect(() => rangeValues(0, 1e6, 1e-6)).toThrow("thousands of");
    expect(() => rangeValues(1, 4, 1, 3)).toThrow("the limit is 3");
  });

  it("refuses reversed, missing and out-of-bound inputs", () => {
    expect(() => rangeValues(30, 10, 10)).toThrow("at least");
    expect(() => rangeValues(NaN, 10, 1)).toThrow("Enter numbers");
    expect(() => rangeValues(0, 2e6, 1e6)).toThrow("±1,000,000");
  });
});

describe("parseValues", () => {
  it("reads comma and space separated numbers", () => {
    expect(parseValues("10, 20, 30")).toEqual([10, 20, 30]);
    expect(parseValues(" 0.5 1  1.5 ")).toEqual([0.5, 1, 1.5]);
    expect(parseValues("-2;2")).toEqual([-2, 2]);
  });

  it("returns distinct values in ascending order", () => {
    expect(parseValues("30, 10, 20, 10")).toEqual([10, 20, 30]);
    expect(parseValues("0.3, 0.30000000000000004")).toEqual([0.3]);
  });

  it("refuses text, non-finite and empty input", () => {
    expect(() => parseValues("10, x")).toThrow("“x” is not a number");
    expect(() => parseValues("Infinity")).toThrow(GridError);
    expect(() => parseValues("NaN")).toThrow(GridError);
    expect(() => parseValues(" , ")).toThrow("at least one value");
    expect(() => parseValues("2000000")).toThrow("±1,000,000");
  });

  it("refuses more values than the limit", () => {
    expect(() =>
      parseValues(Array.from({ length: 13 }, (_, i) => i).join(",")),
    ).toThrow("13 values; the limit is 12");
  });
});

describe("configurationCount", () => {
  it("multiplies the value counts", () => {
    expect(configurationCount(defaults.strategy.parameters)).toBe(12);
    expect(configurationCount([])).toBe(1);
    expect(
      configurationCount([
        { name: "a", values: [1, 2, 3, 4, 5] },
        { name: "b", values: [1, 2, 3, 4] },
        { name: "c", values: [1, 2, 3] },
      ]),
    ).toBe(60);
  });
});

describe("strategyArity", () => {
  it("counts the declared parameters", () => {
    expect(strategyArity(trendCode)).toBe(2);
    expect(strategyArity('def strategy(data):\n    return data["close"]')).toBe(
      1,
    );
    expect(strategyArity("def strategy():\n    return True")).toBe(0);
  });

  it("handles annotations, defaults, comments and line breaks", () => {
    expect(
      strategyArity(
        "def strategy(\n    data,  # the bars\n    params: dict[str, float] = None,\n):",
      ),
    ).toBe(2);
    expect(strategyArity("def  strategy ( data , *, params ):")).toBe(2);
    expect(strategyParams("def strategy(bars, p=(1, 2)):")).toEqual([
      "bars",
      "p",
    ]);
  });

  it("returns null without a complete definition", () => {
    expect(strategyArity("print('no strategy here')")).toBeNull();
    expect(strategyArity("# def strategy(data, params):")).toBeNull();
    expect(strategyArity("def strategy(data, params")).toBeNull();
    expect(strategyArity("def strategy_two(data):")).toBeNull();
  });
});

describe("referencedParams", () => {
  it("finds every params key the code reads", () => {
    expect(referencedParams(trendCode)).toEqual(["fast", "slow"]);
    expect(
      referencedParams(
        "def strategy(data, p):\n    # p['ignored']\n    return change(data['close'], p.get('lookback', 21)) > p['threshold']",
      ),
    ).toEqual(["lookback", "threshold"]);
  });
});

describe("grid drafts", () => {
  it("round-trips between list and range entry", () => {
    const draft = newDraft({ name: "slow", values: [200, 100, 150] }, 150);
    expect(draft).toMatchObject({
      name: "slow",
      mode: "list",
      list: "100, 150, 200",
      from: "100",
      to: "200",
      step: "50",
      base: 150,
    });
    const range = switchDraftMode(draft, "range");
    expect(draftValues(range).values).toEqual([100, 150, 200]);
    const list = switchDraftMode({ ...range, to: "300" }, "list");
    expect(list.list).toBe("100, 150, 200, 250, 300");
  });

  it("resolves bases to a grid value, defaulting to the middle", () => {
    const grid = resolveGrid([
      newDraft({ name: "fast", values: [10, 20, 30, 50] }, 99),
      newDraft({ name: "slow", values: [100, 150, 200] }, 200),
    ]);
    expect(grid.base).toEqual({ fast: 30, slow: 200 });
    expect(grid.count).toBe(12);
    expect(grid.complete).toBe(true);
    expect(grid.error).toBeUndefined();
  });

  it("flags names, values and the configuration limit", () => {
    const grid = resolveGrid([
      { ...newDraft(), name: "Fast", list: "1, 2" },
      { ...newDraft(), name: "slow", list: "" },
      { ...newDraft(), name: "slow", list: "1" },
    ]);
    expect(grid.rows[0].nameError).toMatch(/lowercase/);
    expect(grid.rows[1].valuesError).toBe("Enter at least one value.");
    expect(grid.rows[2].nameError).toMatch(/already uses/);
    expect(grid.complete).toBe(false);
    const big = resolveGrid([
      newDraft({ name: "a", values: rangeValues(1, 10, 1) }),
      newDraft({ name: "b", values: rangeValues(1, 7, 1) }),
    ]);
    expect(big.count).toBe(70);
    expect(big.error).toMatch("70 configurations exceed the limit of 60");
  });
});

describe("composer validation", () => {
  const form = () => ({
    ...formFromSpec(
      defaults,
      "Trend survives costs",
      "The crossover beats buy-and-hold out of sample.",
    ),
  });

  it("accepts the defaults and builds the same spec", () => {
    const value = form();
    const grid = resolveGrid(value.grid);
    expect(composerIssues(value, grid, options)).toEqual({});
    const spec = specFromForm(value, grid, defaults);
    expect(spec.strategy.parameters).toEqual(defaults.strategy.parameters);
    expect(spec.strategy.base).toEqual(defaults.strategy.base);
    expect(spec.validation).toEqual(defaults.validation);
  });

  it("requires a hypothesis long enough to be falsifiable", () => {
    const value = { ...form(), hypothesis: "   too short " };
    expect(composerIssues(value, resolveGrid(value.grid), options)).toEqual({
      hypothesis:
        "Write at least 12 characters: a claim that could be shown false.",
    });
  });

  it("refuses a grid for a one-argument strategy", () => {
    const value = {
      ...form(),
      code: 'def strategy(data):\n    return data["close"] > data["sma_50"]',
    };
    const issues = composerIssues(value, resolveGrid(value.grid), options);
    expect(issues.arity).toMatch(/strategy\(data\) takes one argument/);
    expect(
      composerIssues({ ...value, grid: [] }, resolveGrid([]), options),
    ).toEqual({});
  });

  it("refuses when the strategy code reads parameters missing from the grid", () => {
    const value = form();
    // form() has default trend code reading params["fast"] and params["slow"].
    // Filter out "fast" from the grid to simulate renaming or removing it:
    value.grid = value.grid.filter((draft) => draft.name !== "fast");
    const issues = composerIssues(value, resolveGrid(value.grid), options);
    expect(issues.grid).toContain('reads params["fast"]');
    expect(issues.grid).toContain("has no row in the grid");
  });

  it("checks the numbers it shows and resets the ones it hides", () => {
    const value = form();
    value.dataset = {
      kind: "historical",
      params: { ...value.dataset.params, kappa: -1 },
    };
    value.validation = {
      ...value.validation,
      split: 0.7000000001,
      test_bars: 10,
    };
    const grid = resolveGrid(value.grid);
    expect(composerIssues(value, grid, options)).toEqual({
      "dataset.symbol": "No historical dataset is imported yet.",
      "validation.test_bars": "Use at least 63 and at most 2,520.",
    });
    const spec = specFromForm(
      {
        ...value,
        dataset: {
          ...value.dataset,
          params: { ...value.dataset.params, symbol: "SPY" },
        },
      },
      grid,
      defaults,
    );
    expect(spec.dataset.params.kappa).toBe(defaults.dataset.params.kappa);
    expect(spec.dataset.params.symbol).toBe("SPY");
    expect(spec.validation.split).toBe(0.7);
  });

  it("explains number rules in display units", () => {
    expect(
      numberIssue(3, {
        label: "Drift",
        min: -1,
        max: 1,
        scale: 100,
        unit: "%",
      }),
    ).toBe("Use at least -100% and at most 100%.");
    expect(
      numberIssue(1.5, { label: "Years", min: 1, max: 30, integer: true }),
    ).toBe("Use a whole number.");
    expect(numberIssue(NaN, { label: "Seed", min: 0, max: 1 })).toBe(
      "Enter a number.",
    );
    expect(numberIssue(0, { label: "κ", min: 0, max: 20, above: true })).toBe(
      "Use more than 0 and at most 20.",
    );
  });
});

describe("validation preview", () => {
  it("mirrors the backend's split and walk-forward windows", () => {
    expect(splitBars(756, 0.7)).toEqual({ train: 529, test: 227, ok: true });
    expect(splitBars(252, 0.8).ok).toBe(false);
    expect(walkForwardFolds(756, 252, 126)).toBe(4);
    expect(walkForwardFolds(252, 252, 126)).toBe(0);
    expect(walkForwardFolds(440, 252, 126)).toBe(1);
    expect(walkForwardFolds(441, 252, 126)).toBe(2);
    expect(walkForwardFolds(100000, 126, 63)).toBe(40);
  });
});

describe("specFromLab", () => {
  it("maps a one-argument sandbox strategy onto an empty grid", () => {
    const config = {
      ...defaultConfig,
      dataset_params: { ...defaultConfig.dataset_params, seed: 7, years: 5 },
      commission_bps: 12,
    };
    const spec = specFromLab(
      'def strategy(data):\n    return data["close"] > data["sma_50"]\n',
      config,
      defaults,
      "Margin of safety research",
    );
    expect(spec.dataset.kind).toBe("synthetic");
    expect(spec.dataset.params).toMatchObject({ seed: 7, years: 5 });
    expect(spec.dataset.params.symbol).toBeUndefined();
    expect(spec.strategy).toMatchObject({
      name: "Margin of safety research",
      parameters: [],
      base: {},
    });
    expect(spec.costs).toEqual({
      capital: 100000,
      commission_bps: 12,
      slippage_bps: 3,
    });
    expect(spec.validation).toEqual(defaults.validation);
  });

  it("maps real data to a historical dataset and keeps read parameters", () => {
    const spec = specFromLab(
      'def strategy(data, params):\n    return change(data["close"], params["lookback"]) > params["fast"]',
      {
        ...defaultConfig,
        dataset_type: "real",
        dataset_params: { ...defaultConfig.dataset_params, symbol: "SPY" },
      },
      defaults,
    );
    expect(spec.dataset).toMatchObject({
      kind: "historical",
      params: { symbol: "SPY" },
    });
    expect(spec.strategy.name).toBe("Strategy lab rule");
    expect(spec.strategy.parameters).toEqual([
      { name: "lookback", values: [] },
      { name: "fast", values: [10, 20, 30, 50] },
    ]);
    expect(spec.strategy.base).toEqual({ fast: 20 });
  });

  it("drops an empty historical symbol", () => {
    const spec = specFromLab(
      "def strategy(data):\n    return True",
      {
        ...defaultConfig,
        dataset_params: { ...defaultConfig.dataset_params, symbol: "" },
      },
      defaults,
    );
    expect(spec.dataset.params.symbol).toBeUndefined();
  });
});

describe("readLabPrefill", () => {
  it("accepts only the strategy lab's router state", () => {
    expect(readLabPrefill(null)).toBeNull();
    expect(readLabPrefill({ code: "x" })).toBeNull();
    expect(
      readLabPrefill({ code: "x", config: { dataset_type: "csv" } }),
    ).toBeNull();
    expect(
      readLabPrefill({ code: "x", config: defaultConfig, title: "Saved" }),
    ).toEqual({ code: "x", config: defaultConfig, title: "Saved" });
  });
});
