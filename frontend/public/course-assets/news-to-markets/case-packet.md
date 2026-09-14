# Banyu Industrials: fictional news packet

Every entity, document, date, quotation-free summary, forecast, and price in this packet is invented for teaching. Units are millions of a single fictional reporting currency, except per-share amounts. No supplied summary reproduces a publisher's article.

## Source ledger

| ID | Availability time, UTC | Document | Evidence and limits |
| --- | --- | --- | --- |
| F1 | 2026-08-01 08:00 | Prior annual filing | Sales 1,000; variable costs 600; fixed operating costs 200. Net debt 300 and diluted shares 100. These are historical figures, not a future forecast. |
| F2 | 2026-09-01 08:00 | Supplier cost notice | A confirmed annualized input-cost increase of 30 at unchanged volumes. The notice does not state Banyu's future pricing response. |
| F3 | 2026-09-01 08:30 | Issuer contract announcement | A conditional order opportunity adds up to 20 annual sales. Teaching assumption: 40% incremental contribution. Customer acceptance and delivery conditions remain unresolved. |
| F4 | 2026-09-01 09:00 | Issuer efficiency update | Management expects annual operating savings of 12. For this worksheet only, use 12 in both scenarios; a real memo should stress execution and implementation costs. |
| F5 | 2026-09-01 10:00 | Analyst scenario sheet | Assumed cash tax 25%, depreciation 30, capex 40, working-capital investment 20 in base and 35 in downside. WACC 10% in base and 11% in downside; long-run growth 2%. These are analyst assumptions, not reported facts. |
| F6 | 2026-09-01 10:15 | Fictional market observation | Last observed share price 12; an earlier price was 10. No bid, ask, depth, market return, or dated consensus is supplied. This is not an executable-fill assumption. |

## Decisions at two times

At **08:15**, F1 and F2 are available. F3–F6 are not eligible evidence. Using those later releases in the earlier decision creates hindsight leakage. A preliminary cost-only EBIT estimate is 170, conditional on unchanged volume and other costs; the packet does not yet provide a complete cash-flow forecast or current price.

At **10:30**, all six documents are available. Construct the following separate cases:

- **Base:** accept the conditional contract, include the cost increase and expected savings; EBIT = 200 − 30 + 8 + 12 = 190.
- **Downside:** remove the uncertain contract, retain the cost increase and savings; EBIT = 182. Use greater working-capital investment and a higher required return.
- **Additional challenge:** remove the management savings too, or add implementation capex. This sensitivity is intentionally left for your memo.

Use FCFF = EBIT × (1 − tax) + depreciation − capex − working-capital investment. Treat it as next-year cash flow in a simplified stable-growth model. Subtract net debt from operating value before dividing by diluted shares. Do not deduct interest again from FCFF or count the same cash twice.

## Independent numerical checks

| Calculation | Base | Downside |
| --- | ---: | ---: |
| EBIT | 190 | 182 |
| FCFF | 112.5 | 91.5 |
| Operating value | 1,406.25 | 1,016.6667 |
| Equity value per share | 11.0625 | 7.1667 |

A hypothetical 25% margin below the downside value produces 5.375. At price 12, the model supplies no conservative discount. It does not prove the stock will fall: its assumptions and omissions need scrutiny.

## Missing evidence to discuss

The packet does not supply dated consensus, a full debt maturity schedule, hedge exposures, detailed contract probabilities, seasonal history, maintenance versus growth capex, a cost-of-capital estimate, or reinvestment sufficient to support perpetual growth. It also cannot identify why the observed price moved from 10 to 12. State those limitations instead of inventing inputs.

Reference methods in the course: SEC financial-statement and disclosure guides, Damodaran's NYU valuation teaching materials, and primary central-bank/statistical-agency explanations. These sources describe methods; they are not sources for the fictional Banyu figures.
