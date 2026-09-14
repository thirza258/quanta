import { describe, expect, it } from "vitest";
import { sma, ema, rsi, macd, csv, normalizePreferences } from "./simulator";

describe("observed-bar indicators", () => {
  it("warms up moving averages before returning values", () => {
    expect(sma([1, 2, 3, 4, 5], 3)).toEqual([null, null, 2, 3, 4]);
    expect(ema([1, 2, 3, 4, 8], 3)).toEqual([null, null, 2, 3, 5.5]);
    expect(ema([1, 2], 3)).toEqual([null, null]);
  });
  it("uses Wilder smoothing and handles flat markets", () => {
    expect(rsi([1, 2, 3, 4], 3)).toEqual([null, null, null, 100]);
    expect(rsi([4, 3, 2, 1], 3)).toEqual([null, null, null, 0]);
    expect(rsi([2, 2, 2, 2], 3)).toEqual([null, null, null, 50]);
    expect(rsi([1, 3, 2, 4, 3], 3)[4]).toBeCloseTo(61.5384615385);
  });
  it("seeds MACD signal only after the slow line is available", () => {
    const m = macd([1, 2, 3, 4, 5, 6], 2, 3, 2);
    expect(m.line).toEqual([null, null, 0.5, 0.5, 0.5, 0.5]);
    expect(m.signal).toEqual([null, null, null, 0.5, 0.5, 0.5]);
    expect(m.histogram).toEqual([null, null, null, 0, 0, 0]);
  });
  it("never changes past values when future observations arrive", () => {
    const values = [101, 103, 99, 98, 105, 104, 109, 102];
    for (const calculate of [sma, ema, rsi])
      expect(calculate(values, 3).slice(0, 6)).toEqual(
        calculate(values.slice(0, 6), 3),
      );
    expect(macd(values, 2, 3, 2).histogram.slice(0, 6)).toEqual(
      macd(values.slice(0, 6), 2, 3, 2).histogram,
    );
  });
});
it("keeps a historical workspace in the available symbol and daily interval", () => {
  const p = normalizePreferences(
    { symbol: "AAPL", interval: "1m", watchlist: ["AAPL", "TEST", "TEST"] },
    ["TEST"],
    "1D",
  );
  expect(p.symbol).toBe("TEST");
  expect(p.interval).toBe("1D");
  expect(p.watchlist).toEqual(["TEST"]);
});
it("exports quoted journal text without executable spreadsheet formulas", () => {
  const output = csv([
    { note: '=HYPERLINK("test")', quantity: 2 },
    { note: "A, B\nC", quantity: 3 },
  ]);
  expect(output).toContain('"\' =HYPERLINK(""test"")"');
  expect(output).toContain('"A, B\nC"');
});

it("preserves negative cash flows as numbers and escapes whitespace-prefixed formulas", () => {
  expect(csv([{ amount: "-1001.00", realized: "98.00", note: "\t=1+1" }])).toBe(
    '"amount","realized","note"\r\n"-1001.00","98.00","\' \t=1+1"',
  );
});
