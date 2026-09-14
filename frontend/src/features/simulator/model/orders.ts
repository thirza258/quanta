import type { SimRun, Ticket } from "./types";

export function orderEstimate(run: SimRun, symbol: string, ticket: Ticket) {
  const mark = run.quotes.find((q) => q.symbol === symbol)?.close ?? 0;
  const position = run.positions.find((p) => p.symbol === symbol);
  const buy = ticket.side === "buy",
    quantity = Number(ticket.quantity) || 0;
  const friction =
    (Number(run.config.slippage_bps) + Number(run.config.spread_bps) / 2) /
    10000;
  const hasLimit = ticket.kind === "limit" || ticket.kind === "stop_limit";
  const base =
    ticket.kind === "stop"
      ? buy
        ? Math.max(mark, Number(ticket.stop))
        : Math.min(mark, Number(ticket.stop))
      : mark;
  const price = hasLimit
    ? Number(ticket.limit)
    : buy
      ? Math.ceil(base * (1 + friction) * 100) / 100
      : Math.round(base * (1 - friction) * 100) / 100;
  const notional = quantity * price,
    fee = Number(run.config.commission);
  return {
    price,
    notional,
    total: notional + (buy ? fee : -fee),
    availableShares: position?.available ?? 0,
    after: (position?.quantity ?? 0) + (buy ? quantity : -quantity),
  };
}
