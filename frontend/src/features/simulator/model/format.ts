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

/** Statement figures arrive in millions of USD. */
export const millions = (value: number | null | undefined) => {
  if (value === null || value === undefined || !Number.isFinite(value))
    return "—";
  const sign = value < 0 ? "-" : "";
  const size = Math.abs(value);
  if (size >= 1000) return `${sign}$${(size / 1000).toFixed(2)}bn`;
  if (size >= 1) return `${sign}$${size.toFixed(0)}m`;
  return `${sign}$${(size * 1000).toFixed(0)}k`;
};

export const multiple = (value: number | null | undefined, digits = 1) =>
  value === null || value === undefined || !Number.isFinite(value)
    ? "—"
    : `${value.toFixed(digits)}×`;

export const percent = (value: number | null | undefined, digits = 1) =>
  value === null || value === undefined || !Number.isFinite(value)
    ? "—"
    : `${(value * 100).toFixed(digits)}%`;

export const signed = (value: number | null | undefined, digits = 1) =>
  value === null || value === undefined || !Number.isFinite(value)
    ? "—"
    : `${value > 0 ? "+" : ""}${(value * 100).toFixed(digits)}%`;

export const clock = (time: number) =>
  new Date(time * 1000).toLocaleString("en-GB", {
    timeZone: "America/New_York",
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
