import { describe, expect, it } from "vitest";
import type {
  CostStress,
  ExperimentSpec,
  GridParameter,
  MetricSet,
  RedTeamCheck,
  RunSummary,
  Surface,
} from "@/features/research/model/registry";
import {
  appendLimitation,
  binClass,
  breakEven,
  describeActionError,
  divergingBin,
  downsample,
  extent,
  fingerprintRows,
  formatDay,
  formatDecay,
  formatDuration,
  formatElapsed,
  formatMetric,
  formatParams,
  formatPValue,
  formatSeeds,
  hasProvenance,
  isSkipped,
  latestRun,
  lifecycleSteps,
  methodSummary,
  niceScale,
  niceTicks,
  notebookDirty,
  position,
  progressFraction,
  qualityBreakdown,
  runElapsed,
  runNotice,
  sharpeExtent,
  shortHash,
  stageLabel,
  suggestedLimitations,
  surfaceGrid,
} from "@/features/research/model/experiment";

const metrics = (sharpe: number | null): MetricSet => ({
  total_return: null,
  cagr: null,
  sharpe,
  sortino: null,
  max_drawdown: null,
  calmar: null,
  volatility: null,
  turnover: null,
  win_rate: null,
  profit_factor: null,
  exposure: null,
  trades: null,
  final_equity: null,
});

/** A surface over the full grid, with points deliberately shuffled. */
function makeSurface(
  parameters: GridParameter[],
  sharpe: (params: Record<string, number>) => number | null,
  base = 0,
  best = 0,
): Surface {
  const combos: Record<string, number>[] = parameters.reduce<
    Record<string, number>[]
  >(
    (acc, p) =>
      acc.flatMap((combo) => p.values.map((v) => ({ ...combo, [p.name]: v }))),
    [{}],
  );
  const points = combos
    .map((params, index) => ({ index, params, ...metrics(sharpe(params)) }))
    .reverse();
  return {
    configurations: combos.length,
    parameters,
    points,
    base,
    best,
    median: 0,
    worst: 0,
    base_rank: 1,
    positive_share: 1,
    sharpe_distribution: { min: null, median: null, max: null, std: null },
    influence: [],
    stability: { score: null, class: "untested", neighbors: 0, reason: "" },
    best_stability: {
      score: null,
      class: "untested",
      neighbors: 0,
      reason: "",
    },
  };
}

const run = (number: number, status: RunSummary["status"]): RunSummary => ({
  id: `run-${number}`,
  experiment_id: "exp",
  number,
  kind: "run",
  rerun_of: null,
  status,
  stage: null,
  progress: { done: 0, total: null },
  summary: {},
  reproduction: null,
  strategy: { id: "s", name: "momentum", version: 1, sha256: "a" },
  error: status === "failed" ? "boom" : null,
  created_at: "2026-11-09T10:00:00Z",
  started_at: null,
  finished_at: null,
  duration_ms: null,
});

describe("surfaceGrid", () => {
  it("returns the single configuration when there is no grid", () => {
    const surface = makeSurface([], () => 0.4);
    const grid = surfaceGrid(surface);
    expect(grid.kind).toBe("single");
    if (grid.kind === "single") expect(grid.point?.sharpe).toBe(0.4);
  });

  it("lays out one parameter in value order", () => {
    const surface = makeSurface(
      [{ name: "window", values: [10, 20, 30] }],
      (p) => p.window / 10,
      1,
      2,
    );
    const grid = surfaceGrid(surface);
    expect(grid.kind).toBe("line");
    if (grid.kind !== "line") return;
    expect(grid.cells.map((c) => c.point?.sharpe)).toEqual([1, 2, 3]);
    expect(grid.cells.map((c) => [c.base, c.best])).toEqual([
      [false, false],
      [true, false],
      [false, true],
    ]);
  });

  it("places two-parameter points by value, not list order", () => {
    const surface = makeSurface(
      [
        { name: "fast", values: [5, 10] },
        { name: "slow", values: [50, 100, 200] },
      ],
      (p) => p.fast * 1000 + p.slow,
      0,
      5,
    );
    const grid = surfaceGrid(surface);
    expect(grid.kind).toBe("grid");
    if (grid.kind !== "grid") return;
    expect(grid.rows.name).toBe("fast");
    expect(grid.columns.name).toBe("slow");
    expect(grid.cells.map((row) => row.map((c) => c.point?.sharpe))).toEqual([
      [5050, 5100, 5200],
      [10050, 10100, 10200],
    ]);
    expect(grid.cells[0][0].base).toBe(true);
    expect(grid.cells[1][2].best).toBe(true);
    expect(grid.slices).toEqual([]);
  });

  it("slices extra parameters at the base value, or the selection", () => {
    const parameters = [
      { name: "a", values: [1, 2] },
      { name: "b", values: [1, 2] },
      { name: "c", values: [0.1, 0.2, 0.3] },
    ];
    // index order: a, b, c nested -> base index 4 is a=1, b=2, c=0.2
    const surface = makeSurface(parameters, (p) => p.a + p.b + p.c, 4, 11);
    const grid = surfaceGrid(surface);
    if (grid.kind !== "grid") throw new Error("expected a grid");
    expect(grid.slices).toEqual([
      { name: "c", values: [0.1, 0.2, 0.3], selected: 0.2 },
    ]);
    expect(grid.cells[0][1].base).toBe(true);
    expect(grid.cells[0][1].point?.params).toEqual({ a: 1, b: 2, c: 0.2 });

    const other = surfaceGrid(surface, { c: 0.3 });
    if (other.kind !== "grid") throw new Error("expected a grid");
    expect(other.slices[0].selected).toBe(0.3);
    expect(other.cells[1][1].best).toBe(true);
    expect(other.cells.flat().some((c) => c.base)).toBe(false);

    // An unknown selection falls back to the first value
    const fallback = surfaceGrid(surface, { c: 9 });
    if (fallback.kind !== "grid") throw new Error("expected a grid");
    expect(fallback.slices[0].selected).toBe(0.1);
  });

  it("matches float grid values despite rounding noise", () => {
    const surface = makeSurface([{ name: "x", values: [0.3] }], () => 1);
    surface.points[0].params.x = 0.1 + 0.2;
    const grid = surfaceGrid(surface);
    if (grid.kind !== "line") throw new Error("expected a line");
    expect(grid.cells[0].point).not.toBeNull();
  });

  it("leaves missing configurations empty", () => {
    const surface = makeSurface(
      [
        { name: "a", values: [1, 2] },
        { name: "b", values: [1, 2] },
      ],
      () => 1,
    );
    surface.points = surface.points.filter(
      (p) => !(p.params.a === 2 && p.params.b === 2),
    );
    const grid = surfaceGrid(surface);
    if (grid.kind !== "grid") throw new Error("expected a grid");
    expect(grid.cells[1][1].point).toBeNull();
  });
});

describe("diverging scale", () => {
  it("floors the extent so a flat grid is not painted as extreme", () => {
    expect(sharpeExtent([0.1, -0.05, null])).toBe(0.5);
    expect(sharpeExtent([1.2, -2.4])).toBe(2.4);
    expect(sharpeExtent([])).toBe(0.5);
  });

  it("bins by share of the extent, symmetric around zero", () => {
    expect(divergingBin(null, 2)).toBeNull();
    expect(divergingBin(Number.NaN, 2)).toBeNull();
    expect(divergingBin(0, 2)).toBe(0);
    expect(divergingBin(0.004, 2)).toBe(0);
    expect(divergingBin(0.01, 2)).toBe(1);
    expect(divergingBin(0.5, 2)).toBe(1);
    expect(divergingBin(0.51, 2)).toBe(2);
    expect(divergingBin(2, 2)).toBe(4);
    expect(divergingBin(5, 2)).toBe(4);
    expect(divergingBin(-1.5, 2)).toBe(-3);
    expect(divergingBin(-3, 2)).toBe(-4);
  });

  it("maps bins to class names", () => {
    expect(binClass(null)).toBe("xd-bin-na");
    expect(binClass(0)).toBe("xd-bin-0");
    expect(binClass(3)).toBe("xd-bin-p3");
    expect(binClass(-2)).toBe("xd-bin-n2");
  });
});

describe("lifecycle and runs", () => {
  it("marks the first unfinished step as current", () => {
    const steps = lifecycleSteps({
      status: "PASSED",
      steps: [
        { id: "configured", label: "Configured", done: true },
        { id: "ran", label: "Ran", done: true },
        { id: "documented", label: "Documented", done: false },
        { id: "reproduced", label: "Reproduced", done: false },
      ],
    });
    expect(steps.map((s) => s.state)).toEqual([
      "done",
      "done",
      "current",
      "pending",
    ]);
  });

  it("finds the latest run regardless of order", () => {
    expect(latestRun([])).toBeNull();
    expect(
      latestRun([run(1, "completed"), run(3, "failed"), run(2, "completed")])
        ?.number,
    ).toBe(3);
  });

  it("explains why there are no fresh results", () => {
    expect(runNotice([])).toEqual({ kind: "never" });
    expect(runNotice([run(2, "failed"), run(1, "completed")])?.kind).toBe(
      "failed",
    );
    expect(runNotice([run(1, "interrupted")])?.kind).toBe("interrupted");
    expect(runNotice([run(2, "completed"), run(1, "failed")])).toBeNull();
  });

  it("reports progress and elapsed time", () => {
    expect(progressFraction({ done: 3, total: 12 })).toBe(0.25);
    expect(progressFraction({ done: 3, total: null })).toBeNull();
    expect(progressFraction({ done: 20, total: 12 })).toBe(1);
    expect(
      runElapsed(
        {
          started_at: "2026-11-09T10:00:00Z",
          created_at: "2026-11-09T09:59:00Z",
        },
        Date.parse("2026-11-09T10:01:05Z"),
      ),
    ).toBe(65000);
    expect(
      runElapsed(
        { started_at: null, created_at: "2026-11-09T10:00:00Z" },
        Date.parse("2026-11-09T09:00:00Z"),
      ),
    ).toBe(0);
    expect(stageLabel("red team", "running")).toBe("Red-teaming the result");
    expect(stageLabel("strategies", "queued")).toBe("Waiting in the queue");
    expect(stageLabel("custom stage", "running")).toBe("Custom stage");
    expect(stageLabel(null, "running")).toBe("Starting the run");
  });

  it("describes action errors by status", () => {
    const generic = "The request could not be completed.";
    expect(describeActionError(409, generic, "run")).toMatch(
      /already in progress/,
    );
    expect(describeActionError(409, "A run is active.", "run")).toBe(
      "A run is active.",
    );
    expect(describeActionError(429, generic, "rerun")).toMatch(/Wait a minute/);
    expect(describeActionError(503, "Worker pool full.", "run")).toBe(
      "The research runner is busy or unavailable. Try again shortly. Worker pool full.",
    );
    expect(describeActionError(500, "Kaput.", "save")).toBe("Kaput.");
  });
});

describe("formatting", () => {
  it("renders undefined numbers as a dash, never zero", () => {
    expect(formatMetric(null, "percent")).toBe("—");
    expect(formatMetric(undefined, "ratio")).toBe("—");
    expect(formatMetric(0.1234, "percent")).toBe("12.3%");
    expect(formatMetric(1.5, "times")).toBe("1.50×");
    expect(formatMetric(1234, "count")).toBe("1,234");
    expect(formatPValue(0.0004)).toBe("< 0.001");
    expect(formatPValue(0.0421)).toBe("0.042");
  });

  it("states the direction of decay", () => {
    expect(formatDecay(null)).toBe("—");
    expect(formatDecay(0.45)).toBe("45% lost");
    expect(formatDecay(-0.2)).toBe("20% better out of sample");
  });

  it("formats durations", () => {
    expect(formatElapsed(42_000)).toBe("42s");
    expect(formatElapsed(185_000)).toBe("3m 05s");
    expect(formatElapsed(3_720_000)).toBe("1h 02m");
    expect(formatDuration(820)).toBe("820 ms");
    expect(formatDuration(4200)).toBe("4.2s");
    expect(formatDuration(null)).toBe("—");
  });

  it("formats bar dates in UTC", () => {
    expect(formatDay("2019-01-02")).toBe("Jan 2, 2019");
    expect(formatDay("not a date")).toBe("not a date");
  });

  it("orders parameters by the grid", () => {
    expect(formatParams({ slow: 50, fast: 0.1 + 0.2 }, ["fast", "slow"])).toBe(
      "fast=0.3 · slow=50",
    );
    expect(formatParams({})).toBe("Single configuration");
  });

  it("truncates hashes and lists seeds", () => {
    expect(shortHash("a".repeat(64))).toBe(`${"a".repeat(12)}…`);
    expect(shortHash(null)).toBe("—");
    expect(shortHash("abc")).toBe("abc");
    expect(
      formatSeeds({
        dataset: 42,
        random_timing: 7,
        alternative_paths: [43, 44],
      }),
    ).toBe("dataset: 42 · random timing: 7 · alternative paths: 43, 44");
    expect(formatSeeds({ dataset: null, alternative_paths: [] })).toBe(
      "dataset: none · alternative paths: none",
    );
  });
});

describe("scales", () => {
  it("pads an extent that includes zero", () => {
    const [low, high] = extent([1, 2]);
    expect(low).toBeLessThan(0);
    expect(high).toBeGreaterThan(2);
    const [flatLow, flatHigh] = extent([null]);
    expect(flatLow).toBeCloseTo(-0.58);
    expect(flatHigh).toBeCloseTo(0.58);
    expect(position(5, [0, 10])).toBe(50);
    expect(position(20, [0, 10])).toBe(100);
  });

  it("produces round ticks", () => {
    expect(niceTicks([0, 100], 5)).toEqual([0, 20, 40, 60, 80, 100]);
    expect(niceTicks([-0.4, 1.3], 4)).toEqual([0, 0.5, 1]);
  });

  it("snaps a value axis outward to round steps", () => {
    expect(niceScale([1.05, -1.75])).toEqual({
      domain: [-2, 2],
      ticks: [-2, -1, 0, 1, 2],
    });
    expect(niceScale([0.62, 1.42, null])).toEqual({
      domain: [0, 1.5],
      ticks: [0, 0.5, 1, 1.5],
    });
    expect(niceScale([])).toEqual({
      domain: [-0.6, 0.6],
      ticks: [-0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6],
    });
  });

  it("downsamples while keeping both ends", () => {
    const items = Array.from({ length: 100 }, (_, i) => i);
    const sample = downsample(items, 10);
    expect(sample).toHaveLength(10);
    expect(sample[0]).toBe(0);
    expect(sample.at(-1)).toBe(99);
    expect(downsample([1, 2], 10)).toEqual([1, 2]);
  });
});

describe("cost stress", () => {
  const base: CostStress = {
    levels: [
      { cost_bps: 0, sharpe: 1, cagr: 0.1, total_return: 0.2, final_equity: 1 },
      { cost_bps: 100, sharpe: -1, cagr: 0, total_return: 0, final_equity: 1 },
    ],
    current_bps: 10,
    break_even_bps: 37.5,
    margin: 3.75,
  };
  it("classifies the break-even cost", () => {
    expect(breakEven(base)).toEqual({
      kind: "value",
      bps: 37.5,
      inRange: true,
      margin: 3.75,
    });
    expect(breakEven({ ...base, break_even_bps: 400 })).toMatchObject({
      inRange: false,
    });
    expect(
      breakEven({
        ...base,
        break_even_bps: null,
        break_even_above: 1000,
        reason: "Stays positive.",
      }),
    ).toEqual({ kind: "above", bps: 1000, reason: "Stays positive." });
    expect(
      breakEven({ ...base, break_even_bps: null, reason: "Never trades." }),
    ).toEqual({ kind: "none", reason: "Never trades." });
  });
});

describe("notebook", () => {
  it("tracks unsaved changes", () => {
    expect(notebookDirty({}, { conclusion: "", decision: "" })).toBe(false);
    expect(notebookDirty({ decision: "trust" }, { decision: "reject" })).toBe(
      true,
    );
    expect(notebookDirty({ limitations: "a" }, { limitations: "a" })).toBe(
      false,
    );
  });

  it("suggests limitations from warnings and failures, worst first", () => {
    const check = (
      id: string,
      status: RedTeamCheck["status"],
      severity: RedTeamCheck["severity"] = null,
    ): RedTeamCheck => ({
      id,
      title: id.toUpperCase(),
      status,
      severity,
      finding: `${id} finding`,
      evidence: {},
      lesson: null,
    });
    const out = suggestedLimitations([
      check("a", "pass"),
      check("b", "warn", "medium"),
      check("c", "fail"),
      check("d", "warn", "high"),
      check("e", "skip"),
    ]);
    expect(out.map((s) => s.id)).toEqual(["c", "d", "b"]);
    expect(out[0].text).toBe("C: c finding");
  });

  it("appends a limitation once", () => {
    expect(appendLimitation("", "X")).toBe("- X");
    expect(appendLimitation("Notes\n\n", "X")).toBe("Notes\n- X");
    expect(appendLimitation("- X", "X")).toBe("- X");
  });

  it("normalizes quality weights", () => {
    const parts = qualityBreakdown([
      { id: "a", label: "A", weight: 15, score: 100, note: "" },
      { id: "b", label: "B", weight: 15, score: 50, note: "" },
    ]);
    expect(parts.map((p) => p.share)).toEqual([0.5, 0.5]);
    expect(parts.map((p) => p.points)).toEqual([50, 25]);
    expect(parts.map((p) => p.maxPoints)).toEqual([50, 50]);
  });

  it("writes a method summary from the specification", () => {
    const spec: ExperimentSpec = {
      dataset: {
        kind: "synthetic",
        params: {
          model: "gbm",
          scenario: "custom",
          mu: 0.07,
          sigma: 0.2,
          years: 5,
          seed: 42,
          window: 50,
          jump_frequency: 0,
          kappa: 2,
          theta: 0.04,
          xi: 0.3,
          rho: -0.7,
        },
      },
      strategy: {
        name: "Momentum",
        code: "",
        parameters: [
          { name: "fast", values: [10, 20] },
          { name: "slow", values: [50, 100, 200] },
        ],
        base: { fast: 20, slow: 100 },
      },
      costs: { capital: 100000, commission_bps: 5, slippage_bps: 5 },
      validation: {
        split: 0.7,
        walk_forward: true,
        train_bars: 504,
        test_bars: 126,
        anchored: false,
        permutations: 500,
        seed_paths: 8,
      },
    };
    const lines = methodSummary(spec);
    expect(lines.map((l) => l.label)).toEqual([
      "Dataset",
      "Strategy",
      "Costs",
      "Validation",
    ]);
    expect(lines[0].text).toContain("geometric Brownian motion");
    expect(lines[1].text).toContain("6 configurations");
    expect(lines[1].text).toContain("base fast=20 · slow=100");
    expect(lines[2].text).toContain("10 bps per fill");
    expect(lines[3].text).toContain("Rolling walk-forward");
    expect(lines[3].text).toContain("8 alternative synthetic paths");
  });
});

describe("guards", () => {
  it("recognises skipped sections and missing provenance", () => {
    expect(isSkipped({ status: "skipped" })).toBe(true);
    expect(isSkipped({ status: "undefined" })).toBe(true);
    expect(isSkipped({ status: "completed" })).toBe(false);
    expect(hasProvenance({})).toBe(false);
    expect(hasProvenance(null)).toBe(false);
  });

  it("lists every fingerprint", () => {
    const rows = fingerprintRows({
      quanta_version: "0.4.0",
      engine: { name: "quanta-engine", version: "1.0", sha256: "e".repeat(64) },
      environment: {
        python: "3.12.1",
        implementation: "CPython",
        numpy: "2.1.0",
        platform: "linux-x86_64",
        sha256: "f".repeat(64),
      },
      runtime: "native",
      git_commit: null,
      dataset: {
        kind: "synthetic",
        key: "synthetic/gbm",
        label: "GBM seed 42",
        source: "generated",
        version: 1,
        version_sha256: "b".repeat(64),
        sha256: "a".repeat(64),
        bars: 1260,
        start: "2020-01-01",
        end: "2024-12-31",
      },
      strategy: {
        id: "s",
        name: "Momentum",
        version: 3,
        sha256: "c".repeat(64),
      },
      config_sha256: "d".repeat(64),
      seeds: { dataset: 42 },
      configurations: 6,
      result_sha256: "9".repeat(64),
    });
    expect(rows.map((r) => r.id)).toEqual([
      "dataset",
      "dataset-version",
      "strategy",
      "config",
      "engine",
      "environment",
      "runtime",
      "quanta",
      "git",
      "seeds",
      "result",
    ]);
    expect(rows.find((r) => r.id === "git")?.detail).toBe("Not recorded");
  });
});
