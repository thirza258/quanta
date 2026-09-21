import {
  millions,
  multiple,
  percent,
  price,
  signed,
  stamp,
} from "@/features/simulator/model/format";
import type {
  Fundamentals,
  Quarter,
  Valuation,
} from "@/features/simulator/model/types";
import "@/features/simulator/simulator.css";

type Statement = "ratios" | "income" | "balance" | "cash" | "peers";

// Ratios and peers are their own views; these are the line-item statements.
const LINES: Record<
  Exclude<Statement, "ratios" | "peers">,
  [string, keyof Quarter][]
> = {
  income: [
    ["Revenue", "revenue"],
    ["Cost of revenue", "cost_of_revenue"],
    ["Gross profit", "gross_profit"],
    ["Research & development", "research_development"],
    ["Selling, general & admin", "selling_general_admin"],
    ["Operating income", "operating_income"],
    ["EBITDA", "ebitda"],
    ["Interest expense", "interest_expense"],
    ["Pre-tax income", "pretax_income"],
    ["Tax expense", "tax_expense"],
    ["Net income", "net_income"],
  ],
  balance: [
    ["Cash", "cash"],
    ["Receivables", "receivables"],
    ["Inventory", "inventory"],
    ["Current assets", "current_assets"],
    ["Property, plant & equipment", "property_plant_equipment"],
    ["Goodwill", "goodwill"],
    ["Total assets", "total_assets"],
    ["Payables", "payables"],
    ["Short-term debt", "short_term_debt"],
    ["Current liabilities", "current_liabilities"],
    ["Long-term debt", "long_term_debt"],
    ["Total liabilities", "total_liabilities"],
    ["Shareholders' equity", "equity"],
  ],
  cash: [
    ["Net income", "net_income"],
    ["Depreciation & amortization", "depreciation"],
    ["Operating cash flow", "operating_cash_flow"],
    ["Capital expenditure", "capital_expenditure"],
    ["Free cash flow", "free_cash_flow"],
    ["Dividends paid", "dividends_paid"],
    ["Share repurchases", "buybacks"],
    ["External financing raised", "external_financing"],
    ["Net financing cash flow", "financing_cash_flow"],
    ["Opening cash", "opening_cash"],
    ["Closing cash", "cash"],
  ],
};

function ratios(v: Valuation): [string, [string, string][]][] {
  return [
    [
      "Valuation",
      [
        ["Market capitalization", millions(v.market_capitalization)],
        ["Enterprise value", millions(v.enterprise_value)],
        ["Price / earnings", multiple(v.price_earnings)],
        ["Price / sales", multiple(v.price_sales)],
        ["Price / book", multiple(v.price_book)],
        ["EV / EBITDA", multiple(v.enterprise_ebitda)],
        ["EV / sales", multiple(v.enterprise_sales)],
        ["Free cash flow yield", percent(v.free_cash_flow_yield, 2)],
      ],
    ],
    [
      "Profitability",
      [
        ["Gross margin", percent(v.gross_margin)],
        ["Operating margin", percent(v.operating_margin)],
        ["Net margin", percent(v.net_margin)],
        ["Return on equity", percent(v.return_on_equity)],
        ["Return on assets", percent(v.return_on_assets)],
        ["Trailing EPS", `$${price(v.trailing_eps)}`],
      ],
    ],
    [
      "Growth & distribution",
      [
        ["Revenue growth (YoY)", signed(v.revenue_growth)],
        ["Earnings growth (YoY)", signed(v.earnings_growth)],
        ["Dividend yield", percent(v.dividend_yield, 2)],
        ["Payout ratio", percent(v.payout_ratio)],
      ],
    ],
    [
      "Balance sheet",
      [
        ["Current ratio", multiple(v.current_ratio, 2)],
        ["Quick ratio", multiple(v.quick_ratio, 2)],
        ["Working capital", millions(v.working_capital)],
        ["Debt / equity", multiple(v.debt_equity, 2)],
        ["Net debt", millions(v.net_debt)],
        ["Net debt / EBITDA", multiple(v.net_debt_ebitda, 2)],
        ["Interest coverage", multiple(v.interest_coverage)],
      ],
    ],
    [
      "Value screens",
      [
        ["Book value per share", `$${price(v.book_value_per_share)}`],
        ["Net current asset value", `$${price(v.net_current_asset_value)}`],
        [
          "Graham number",
          v.graham_number === null ? "—" : `$${price(v.graham_number)}`,
        ],
        ["Shares outstanding", `${price(v.shares)}m`],
      ],
    ],
  ];
}

export default function CompanyPanel({
  data,
  error,
  statement,
  setStatement,
}: {
  data: Fundamentals | null;
  error: string;
  statement: Statement;
  setStatement: (next: Statement) => void;
}) {
  if (!data)
    return (
      <p className="sim-small" role="status">
        {error || "Loading generated company accounts…"}
      </p>
    );
  const quarters = data.quarters.slice(-6);
  const latest = data.quarters[data.quarters.length - 1];
  return (
    <section className="sim-company" aria-label="Company financials">
      <header className="sim-company-head">
        <div>
          <strong>{data.symbol}</strong> {data.name}
          <span className="sim-sim-badge">SIMULATED</span>
          <p className="sim-small">
            {data.sector} · {data.business} ·{" "}
            {data.structure.employees.toLocaleString("en-US")} employees ·
            fiscal year ends {data.structure.fiscal_year_end}
          </p>
        </div>
        <div className="sim-company-next">
          {data.upcoming ? (
            <>
              <strong>Next report {data.upcoming.label}</strong>
              <span>
                {stamp(data.upcoming.time)} · consensus EPS $
                {price(data.upcoming.consensus_eps)} on revenue{" "}
                {millions(data.upcoming.consensus_revenue)}
              </span>
            </>
          ) : latest?.consensus_eps ? (
            <>
              <strong>{latest.label} reported</strong>
              <span>
                EPS ${price(latest.eps)} against ${price(latest.consensus_eps)}{" "}
                expected ·{" "}
                <span
                  className={
                    (latest.eps_surprise ?? 0) >= 0 ? "sim-up" : "sim-down"
                  }
                >
                  {signed(latest.eps_surprise)} surprise
                </span>
              </span>
            </>
          ) : (
            <span>No report is scheduled in the remaining replay.</span>
          )}
        </div>
      </header>
      <div className="sim-statement-tabs" role="group" aria-label="Statements">
        {(
          [
            ["ratios", "Ratios"],
            ["income", "Income statement"],
            ["balance", "Balance sheet"],
            ["cash", "Cash flow"],
            ["peers", "Peers"],
          ] as const
        ).map(([value, label]) => (
          <button
            key={value}
            className={statement === value ? "active" : ""}
            aria-pressed={statement === value}
            onClick={() => setStatement(value)}
          >
            {label}
          </button>
        ))}
      </div>
      {statement === "peers" ? (
        <>
          <table className="sim-desk-table">
            <caption className="sim-small">
              {data.peers.sector} · each company on the quarters it has
              reported.
            </caption>
            <thead>
              <tr>
                {[
                  "Symbol",
                  "Market cap",
                  "P/E",
                  "P/S",
                  "P/B",
                  "EV/EBITDA",
                  "Op. margin",
                  "ROE",
                  "Revenue growth",
                ].map((head) => (
                  <th key={head} scope="col">
                    {head}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.peers.rows.map((row) => (
                <tr
                  key={row.symbol}
                  className={row.self ? "sim-peer-self" : ""}
                >
                  <td>
                    <strong>{row.symbol}</strong>
                  </td>
                  <td>{millions(row.market_capitalization)}</td>
                  <td>{multiple(row.price_earnings)}</td>
                  <td>{multiple(row.price_sales)}</td>
                  <td>{multiple(row.price_book)}</td>
                  <td>{multiple(row.enterprise_ebitda)}</td>
                  <td>{percent(row.operating_margin)}</td>
                  <td>{percent(row.return_on_equity)}</td>
                  <td>{signed(row.revenue_growth)}</td>
                </tr>
              ))}
              <tr className="sim-peer-median">
                <th scope="row">Sector median</th>
                <td>—</td>
                <td>{multiple(data.peers.median.price_earnings)}</td>
                <td>{multiple(data.peers.median.price_sales)}</td>
                <td>{multiple(data.peers.median.price_book)}</td>
                <td>{multiple(data.peers.median.enterprise_ebitda)}</td>
                <td>{percent(data.peers.median.operating_margin)}</td>
                <td>{percent(data.peers.median.return_on_equity)}</td>
                <td>{signed(data.peers.median.revenue_growth)}</td>
              </tr>
            </tbody>
          </table>
          <p className="sim-small">
            A company whose results are still unreported is compared on the
            quarters already on file, so the columns are not always measured
            over the same periods.
          </p>
        </>
      ) : statement === "ratios" ? (
        <div className="sim-ratio-grid">
          {ratios(data.valuation).map(([group, rows]) => (
            <div key={group}>
              <h4>{group}</h4>
              <dl>
                {rows.map(([label, value]) => (
                  <div key={label}>
                    <dt>{label}</dt>
                    <dd>{value}</dd>
                  </div>
                ))}
              </dl>
            </div>
          ))}
        </div>
      ) : (
        <table className="sim-statement">
          <caption className="sim-small">
            {data.units}. Generated accounts for a fictional company.
          </caption>
          <thead>
            <tr>
              <th scope="col">Line item</th>
              {quarters.map((q) => (
                <th key={q.label} scope="col">
                  {q.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {LINES[statement].map(([label, key]) => (
              <tr key={label}>
                <th scope="row">{label}</th>
                {quarters.map((q) => (
                  <td key={q.label}>{millions(q[key] as number)}</td>
                ))}
              </tr>
            ))}
            {statement === "income" ? (
              <tr>
                <th scope="row">Earnings per share</th>
                {quarters.map((q) => (
                  <td key={q.label}>${price(q.eps)}</td>
                ))}
              </tr>
            ) : null}
          </tbody>
        </table>
      )}
      <p className="sim-small">{data.disclosure}</p>
    </section>
  );
}
