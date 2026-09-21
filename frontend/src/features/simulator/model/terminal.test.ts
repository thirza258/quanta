import { csv } from "@/features/simulator/model/format";
import { indicatorSpec } from "@/features/simulator/model/preferences";
import { normalizePreferences } from "@/features/simulator/model/preferences";
import { describe, expect, it } from "vitest";

describe("overlay requests", () => {
  it("asks the API for the series the chart draws", () => {
    const base = {
      id: "a",
      visible: true,
      period: 20,
      slow: 26,
      signal: 9,
    } as const;
    expect(indicatorSpec({ ...base, kind: "SMA" })).toBe("SMA:20");
    expect(indicatorSpec({ ...base, kind: "RSI", period: 14 })).toBe("RSI:14");
    expect(indicatorSpec({ ...base, kind: "MACD", period: 12 })).toBe(
      "MACD:12:26:9",
    );
    expect(indicatorSpec({ ...base, kind: "Volume" })).toBe("");
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

it("keeps an intentionally emptied watchlist but refills one from another universe", () => {
  const symbols = ["NVRA", "CLDS", "VLOC"];
  // Cleared on purpose: the choice survives a reload.
  expect(
    normalizePreferences({ watchlist: [] }, symbols, "1m", ["NVRA"]).watchlist,
  ).toEqual([]);
  // Saved against the previous universe: fall back to the run's suggestions.
  expect(
    normalizePreferences({ watchlist: ["AAPL", "MSFT"] }, symbols, "1m", [
      "CLDS",
      "NVRA",
    ]).watchlist,
  ).toEqual(["CLDS", "NVRA"]);
  // Never saved before: the defaults apply.
  expect(normalizePreferences(undefined, symbols, "1m", []).watchlist).toEqual([
    "NVRA",
    "CLDS",
    "VLOC",
  ]);
});
