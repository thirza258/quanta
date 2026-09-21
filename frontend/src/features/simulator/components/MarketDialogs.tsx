import { price } from "@/features/simulator/model/format";
import type { Indicator } from "@/features/simulator/model/types";
import "@/features/simulator/simulator.css";
import { Modal } from "@/shared/components/ui";

import { Check, ChevronRight, Eye, EyeOff, Search, X } from "lucide-react";
import type { TerminalView } from "../model/view";

export default function MarketDialogs({
  terminal,
}: {
  terminal: Pick<
    TerminalView,
    | "root"
    | "searchOpen"
    | "setSearchOpen"
    | "addSymbol"
    | "query"
    | "setQuery"
    | "run"
    | "setPrefs"
    | "prefs"
    | "chooseSymbol"
    | "indicatorOpen"
    | "setIndicatorOpen"
    | "runCommand"
    | "commandFunctions"
  >;
}) {
  const {
    root,
    searchOpen,
    setSearchOpen,
    addSymbol,
    query,
    setQuery,
    run,
    setPrefs,
    prefs,
    chooseSymbol,
    indicatorOpen,
    setIndicatorOpen,
    runCommand,
    commandFunctions,
  } = terminal;
  return (
    <>
      <Modal
        container={root.current}
        open={searchOpen}
        onOpenChange={setSearchOpen}
        title={addSymbol ? "Add to watchlist" : "Command"}
        description={
          addSymbol
            ? "Fictional companies listed in this simulation."
            : "Type a ticker, a function code, or both — NVRA FA opens that company's accounts. Prices follow the replay clock."
        }
      >
        <label className="sim-search">
          <Search size={18} />
          <input
            autoFocus
            aria-label="Search stocks"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key !== "Enter" || addSymbol) return;
              e.preventDefault();
              if (runCommand(query)) {
                setQuery("");
                setSearchOpen(false);
              }
            }}
            placeholder="Ticker or company name · try NVRA N"
          />
        </label>
        {!run.quotes.some((q) =>
          `${q.symbol} ${q.name}`.toLowerCase().includes(query.toLowerCase()),
        ) ? (
          <p className="sim-small">
            No matching stock is available in this run.
          </p>
        ) : null}
        {!addSymbol ? (
          <div className="sim-command-help">
            {Object.entries(commandFunctions)
              .filter(([code]) => !["NEWS", "DESK", "DES"].includes(code))
              .map(([code, label]) => (
                <button
                  key={code}
                  onClick={() => {
                    if (runCommand(`${prefs.symbol} ${code}`))
                      setSearchOpen(false);
                  }}
                >
                  <strong>{code}</strong> {label}
                </button>
              ))}
          </div>
        ) : null}
        <div className="sim-search-results">
          {run.quotes
            .filter((q) =>
              `${q.symbol} ${q.name}`
                .toLowerCase()
                .includes(query.toLowerCase()),
            )
            .map((q) => (
              <button
                key={q.symbol}
                onClick={() => {
                  if (addSymbol) {
                    setPrefs({
                      watchlist: [...new Set([...prefs.watchlist, q.symbol])],
                    });
                    setSearchOpen(false);
                  } else chooseSymbol(q.symbol);
                }}
              >
                <strong>{q.symbol}</strong>
                <span>
                  {q.name}
                  {q.sector ? <small> · {q.sector}</small> : null}
                </span>
                <span>{price(q.close)}</span>
                {addSymbol && prefs.watchlist.includes(q.symbol) ? (
                  <Check size={15} />
                ) : (
                  <ChevronRight size={15} />
                )}
              </button>
            ))}
        </div>
      </Modal>
      <Modal
        container={root.current}
        open={indicatorOpen}
        onOpenChange={setIndicatorOpen}
        title="Indicators"
        description="Calculated only from bars already available in replay. At most eight indicators."
      >
        {prefs.indicators.map((i) => (
          <div className="sim-indicator-editor" key={i.id}>
            <strong>{i.kind}</strong>
            <button
              className="sim-icon"
              aria-label={`${i.visible ? "Hide" : "Show"} ${i.kind}`}
              onClick={() =>
                setPrefs({
                  indicators: prefs.indicators.map((item) =>
                    item.id === i.id ? { ...item, visible: !i.visible } : item,
                  ),
                })
              }
            >
              {i.visible ? <Eye size={16} /> : <EyeOff size={16} />}
            </button>
            <button
              className="sim-icon"
              aria-label={`Remove ${i.kind}`}
              onClick={() =>
                setPrefs({
                  indicators: prefs.indicators.filter(
                    (item) => item.id !== i.id,
                  ),
                })
              }
            >
              <X size={16} />
            </button>
            {i.kind !== "Volume" ? (
              <label className="sim-field">
                {i.kind === "MACD" ? "Fast period" : "Period"}
                <input
                  type="number"
                  min={2}
                  max={200}
                  value={i.period}
                  onChange={(e) => {
                    const period = Number(e.target.value);
                    if (
                      Number.isInteger(period) &&
                      period >= 2 &&
                      period <= 200
                    )
                      setPrefs({
                        indicators: prefs.indicators.map((item) =>
                          item.id === i.id ? { ...item, period } : item,
                        ),
                      });
                  }}
                />
              </label>
            ) : null}
            {i.kind === "MACD"
              ? (["slow", "signal"] as const).map((field) => (
                  <label className="sim-field" key={field}>
                    {field} period
                    <input
                      type="number"
                      min={2}
                      max={200}
                      value={i[field]}
                      onChange={(e) => {
                        const n = Number(e.target.value);
                        if (Number.isInteger(n) && n >= 2 && n <= 200)
                          setPrefs({
                            indicators: prefs.indicators.map((item) =>
                              item.id === i.id ? { ...item, [field]: n } : item,
                            ),
                          });
                      }}
                    />
                  </label>
                ))
              : null}
          </div>
        ))}
        <label className="sim-field">
          Add indicator
          <select
            value=""
            disabled={prefs.indicators.length >= 8}
            onChange={(e) => {
              const kind = e.target.value as Indicator["kind"];
              setPrefs({
                indicators: [
                  ...prefs.indicators,
                  {
                    id: crypto.randomUUID(),
                    kind,
                    period: kind === "RSI" ? 14 : kind === "MACD" ? 12 : 20,
                    slow: 26,
                    signal: 9,
                    visible: true,
                  },
                ],
              });
            }}
          >
            <option value="" disabled>
              Select an indicator
            </option>
            {["SMA", "EMA", "Volume", "RSI", "MACD"].map((k) => (
              <option key={k}>{k}</option>
            ))}
          </select>
        </label>
      </Modal>
    </>
  );
}
