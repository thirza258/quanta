import type { ComponentProps, ReactNode } from "react";
import type OrderTicket from "../components/OrderTicket";
import type { TerminalController } from "../hooks/useTradingTerminal";
import type { orderEstimate } from "./orders";
import type { SimRun } from "./types";
/** Non-null run and presentation values after the page's loading guard. */
export type TerminalView = TerminalController & {
  run: SimRun;
  blocked: boolean;
  complete: boolean;
  estimate: ReturnType<typeof orderEstimate>;
  marketClosed: boolean;
  feedback: ReactNode;
  ticketProps: ComponentProps<typeof OrderTicket>;
};
