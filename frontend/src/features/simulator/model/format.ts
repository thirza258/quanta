import type { SimOrder } from "./types";

export const working = (o: SimOrder) =>
  ["working", "partially_filled"].includes(o.status);

export const dollars = (value: string | number) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  }).format(Number(value));

export const price = (value: string | number) =>
  Number(value).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

export const stamp = (time: number | null) =>
  time
    ? new Date(time * 1000).toLocaleString("en-US", {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        timeZone: "America/New_York",
      }) + " ET"
    : "Opening balance";

export function csv(rows: Record<string, unknown>[]) {
  if (!rows.length) return "";
  const keys = [...new Set(rows.flatMap((row) => Object.keys(row)))];
  const cell = (v: unknown) => {
    const raw = String(v ?? "");
    // Preserve ledger amounts as numbers while escaping executable journal text.
    const safe =
      /^[\s]*[=+@\-]/.test(raw) && !/^-?\d+(\.\d+)?$/.test(raw)
        ? "' " + raw
        : raw;
    return '"' + safe.replaceAll('"', '""') + '"';
  };
  return [
    keys.map(cell).join(","),
    ...rows.map((row) => keys.map((k) => cell(row[k])).join(",")),
  ].join("\r\n");
}
