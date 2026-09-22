import { dollars } from "@/features/simulator/model/format";
import "@/features/simulator/simulator.css";
import { Modal } from "@/shared/components/ui";

import { ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";
import type { TerminalView } from "../model/view";

export default function HelpDialog({
  terminal,
}: {
  terminal: Pick<
    TerminalView,
    | "root"
    | "helpOpen"
    | "setHelpOpen"
    | "walkthrough"
    | "setWalkthrough"
    | "run"
  >;
}) {
  const { root, helpOpen, setHelpOpen, walkthrough, setWalkthrough, run } =
    terminal;
  return (
    <>
      <Modal
        container={root.current}
        open={helpOpen}
        onOpenChange={setHelpOpen}
        title="A workspace for learning to trade"
        description="Paper money. Real decisions to practice."
      >
        <div className="sim-walkthrough">
          <span className="eyebrow">STEP {walkthrough + 1} OF 5</span>
          <h3>
            {
              [
                "Find your market",
                "Read the chart",
                "Follow the newsroom",
                "Place a paper order",
                "Review your process",
              ][walkthrough]
            }
          </h3>
          <p>
            {
              [
                "Choose a company from the watchlist or symbol search. A simulated run lists fictional companies whose prices are generated; historical replay uses an installed dataset. The clock always shows what information is available.",
                "Pan, zoom, change the timeframe, and add indicators. Indicator series are calculated by the server from the bars you can already see. Use the left drawing tools or the Objects form; two clicks create a trend line, and Escape cancels a tool.",
                "Open News to read the simulated wire. Headlines drive the generated prices, so a move on the chart has a story on the same bar. Company shows the invented accounts and ratios, Desk shows movers and risk statistics, and the jump buttons step the clock forward from fifteen minutes to a week.",
                "Open Buy or Sell, choose an order type, and preview it. Your account starts with $100,000. Advance replay to process orders on the next eligible bar.",
                "Open Positions and Trade history. Link a thesis to your trade, compare the outcome to the plan, and export the run. A profitable result alone does not establish a sound decision.",
              ][walkthrough]
            }
          </p>
          <button
            className="sim-outline"
            onClick={() =>
              walkthrough < 4
                ? setWalkthrough((v) => v + 1)
                : setHelpOpen(false)
            }
          >
            {walkthrough < 4 ? "Next step" : "Start exploring"}
            <ChevronRight size={16} />
          </button>
        </div>
        <details className="sim-model-details">
          <summary>Execution and accounting model</summary>
          <p>
            FIFO order arrival within each symbol; all orders share a{" "}
            {Number(run.config.participation) * 100}% bar-volume cap. Market
            orders fill at the next bar open, plus {run.config.slippage_bps} bps
            slippage and half of the {run.config.spread_bps} bps spread. Limit
            fills never violate the limit; a touch alone does not fill.
          </p>
          <p>
            Stop-market orders can gap beyond the trigger. Stop-limit orders
            activate on a trigger bar and cannot fill until a later bar, because
            OHLC data does not reveal the intrabar path. DAY orders entered
            during a session expire at its final bar; orders entered after the
            close apply to the next session. Daily replay timestamps label the
            completed session, not the exact intraday fill time. Cash settles
            immediately in this teaching model.
          </p>
          <p>
            Weighted-average cost includes the entry fee; realized P&L deducts
            the exit fee. The flat {dollars(run.config.commission)} commission
            is charged once, on the first fill of each order. No Level 2 order
            book is inferred from bars. Synthetic sessions omit exchange
            holidays.
          </p>
          {run.universe ? (
            <p>
              Every company, headline, wire service, broker, institution and
              financial statement in this run is invented for teaching. The news
              schedule is generated first and its macro, sector and company
              shocks enter the price process, so a move on the chart has a story
              on the same bar. No headline, reported quarter or analyst estimate
              is released ahead of the replay clock, and imported historical
              prices never receive generated news. Indicators, screening, risk
              statistics, valuation ratios and account performance are all
              calculated by the server from the bars you have already observed.
            </p>
          ) : null}
          <p>
            {run.config.source}. Historical splits and dividends are not applied
            by this engine; import adjusted OHLC prices, or explicitly account
            for this limitation when reviewing returns.
          </p>
          <Link className="sim-text-button" to="/learn/0.4">
            Review order types
          </Link>{" "}
          ·{" "}
          <Link className="sim-text-button" to="/learn/0.7">
            Review risk and sizing
          </Link>
        </details>
      </Modal>
    </>
  );
}
