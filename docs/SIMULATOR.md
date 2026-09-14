# Stock trading simulator

The new `/simulator` terminal implements PRD Section 6.3's first release. Open **Trading simulator** in navigation, or follow the practice link in beginner lessons 0.4, 0.5, 0.7, and 0.8. The research lab's small execution calculator remains a separate teaching tool.

## First trade

1. Choose a stock using the ticker search or watchlist. Inspect the chart, change timeframe, or add indicators.
2. Open **Buy**, enter whole shares and the order type, then preview the estimated value, fees, reservations, and resulting position. **Place buy order** explicitly submits it.
3. Advance replay. Accepted orders wait for a subsequent eligible bar; acceptance itself does not change holdings.
4. Open **Positions** to reduce or close through a prefilled sell ticket. Review fills, fees, P&L, and cash entries in the bottom tabs.
5. Add a trade thesis and lesson to the journal. Export each table as CSV or the run, settings, and journal as JSON.

The chart supports candles, OHLC bars, line, pan/zoom, crosshair, fit/latest, volume, SMA, EMA, Wilder RSI, and MACD. The left toolbar provides trend/horizontal lines, rectangles, text, and price measurements. Objects can also be created and edited using the **Objects** form, including dates, prices, color, label, lock, delete, and undo/redo. Drawings belong to their symbol and run. Dragging an order price opens an amendment confirmation; its form is also available through **Open orders → Edit**.

Desktop panels resize by dragging their separators or using arrow keys while a separator has focus. At tablet widths the right panel becomes a drawer; the toolbar toggles it. At mobile widths, Chart, Watchlist, Trade, and Portfolio tabs accompany persistent Buy/Sell entry buttons. Dense tables scroll inside the trading panel. Light/dark themes follow the learning workspace. An optional walkthrough explains the first trade and execution model.

## Market data and clock

The default run starts with $100,000 of virtual cash and six fictional stocks. Seeded synthetic runs contain 6,000 one-minute bars over weekday sessions, 09:30–16:00 America/New_York, starting January 6, 2025. Exchange holidays are omitted. The first 500 observations are available as warm-up. This is a deterministic teaching market, not a reconstruction or live feed.

Installed historical datasets come from the existing licensed CSV → Parquet importer described in the README. The terminal snapshots an imported dataset into its database, so removing or replacing an import cannot rewrite an existing run. Historical imports contain daily OHLCV; intraday choices are disabled. Daily bar timestamps label completed sessions at 16:00 ET; they do not assert the exact intraday time of a modeled fill. The initial warm-up is at most 31 daily bars, retaining at least one replay step.

Only observations at or before the run's cursor leave the server. Coarser intervals aggregate those observations, including the observed portion of an unfinished aggregate bar. Indicators receive the same observed series, with missing warm-up values omitted. Quotes, positions, and fills share one server clock. Play, speed, and next-bar advance it; pause allows order entry and cancellation without advancing prices. Moving back is accomplished by creating a new run, preserving the previous run for review/export.

Historical corporate-action treatment is explicitly **undeclared** for existing imports. Prices are used as supplied: this engine adds no split adjustments, dividends, or other corporate-action cash flows. Import suitably adjusted data and interpret returns using its provider's conventions. No historical files or live-data credentials ship with the application; unavailable imports remain unavailable.

## Execution profile: cash-whole-shares-v1

- Long-only, whole-share, USD cash account with immediate settlement. Default commission is $1 per order, slippage 2 bps, spread 2 bps, and volume participation 1%. New-run configuration changes these assumptions explicitly.
- Orders entered after a completed bar first become eligible on the next bar. Market orders use its opening price with adverse slippage plus half-spread. Buy reservations round estimates upward to cents; ledger and fill arithmetic use Decimal and cent rounding.
- Buy orders reserve their remaining estimated notional and unpaid commission. Sell orders reserve remaining shares. Execution rechecks cash, reserved orders, proceeds, and fees; gaps cannot create borrowing. A gap may partially fill an affordable quantity and cancel its unaffordable remainder. A sale whose commission cannot be covered is rejected.
- Passive limit orders require trading strictly through the limit. An opening price at or better than the limit is eligible, subject to liquidity. Limit fills never breach the limit. A stop-market triggers on the high/low and gaps at the worse opening/trigger price, before costs. A stop-limit triggers on one bar and cannot fill before a later bar; this conservative rule avoids assuming an unknown intrabar path.
- All orders for a symbol share `floor(bar volume × participation)` shares of capacity, in FIFO arrival order. There is no implied Level 2 book. Partial fills preserve quantity and charge the flat commission only on the first fill. Cancellation releases only the unfilled reservation.
- DAY orders entered within a session expire at its boundary. Orders entered after its final bar are valid for the next modeled session, including daily replay. GTC orders remain until filled/canceled or the run is archived. End-of-replay never force-liquidates positions.
- Average cost includes entry fees. Partial exits allocate weighted-average basis to cents; the final exit consumes any remaining basis. Realized P&L deducts exit fees. Every fill produces an account ledger entry; unrealized P&L marks remaining holdings to the latest available close.

## Persistence and recovery

`TradingRun` stores account ownership, an optimistic version, and transactional order/fill/position/cash/journal state. `TradingDataset` stores immutable imported bars. Both tables are added during normal database initialization, without rewriting learning state. SQLite supports local development; Compose uses PostgreSQL.

Signed-in runs are owned by the existing authenticated account. Guests use a separate signed, HttpOnly, browser-scoped cookie valid for 30 days; their preview is also server-backed. Losing that cookie loses access to the guest preview. Guest and account trading balances never migrate or merge during sign-in/out. Simulator storage and pending drafts use their own namespaces, separate from lesson/exam progress and experiments.

Every write carries a stable UUID and expected version. An identical retry returns confirmed state; a reused identifier with different content or an outdated new action is rejected. The ledger and request record commit together. Reset also competes on the previous run's version, preventing an order from being committed to an account after its reset succeeds.

The browser saves an uncertain action and ticket locally. Network failures, server errors, and version conflicts pause replay. **Reconnect & retry action** first reloads authoritative state, then retries the same UUID. Unconfirmed trades are never inferred locally. New-run requests also retain their configuration and UUID until acknowledged. Old runs remain reviewable but cannot accept new economic actions.

Chart preferences save to the account and a device cache; unsaved local changes survive reload. Confirmed account changes refresh on reconnect and during idle polling. Layout preferences are shared across devices; the most recently saved layout wins. Financial writes always require the current version. Limits: 2,000 orders, 20,000 mutations, and 200 KB of chart preferences per run; export and start another run when reached.

## HTTP interface

All paths below start with `/api/v1/simulator`. Authentication uses the existing session cookie or separate guest cookie. GET and write responses are private/no-store. Interactive schemas are available at `/docs` on the API.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | Base path `/api/v1/simulator` | Current run, owned run summaries, available symbols/imports |
| POST | `/runs` | Create/reset; UUID plus mode, seed or historical symbol, and cost/liquidity configuration |
| GET | `/runs/{run_id}` | Owned account snapshot |
| GET | `/runs/{run_id}/market?symbol=AAPL&interval=1m` | Observed bars only |
| POST | `/runs/{run_id}/orders` | Place market, limit, stop, or stop_limit; side buy/sell, integer quantity, DAY/GTC |
| POST | `/runs/{run_id}/advance` | Advance 1–390 observations |
| POST | `/runs/{run_id}/orders/{order_id}/cancel` | Cancel unfilled remainder |
| POST | `/runs/{run_id}/orders/{order_id}/amend` | Confirm changed limit/stop prices |
| PUT | `/runs/{run_id}/preferences` | Save chart settings |
| PUT | `/runs/{run_id}/orders/{order_id}/journal` | Save thesis/lesson on the order and its fills |

All mutations within a run require `id` (UUID) and `version` (integer). Prices are decimal strings with at most two fractional digits. Client balances, execution prices, and P&L are not accepted. Orders also accept `note` and `lesson`. The same service can support a future Python client without reimplementing financial logic.

See [verification results](VERIFICATION.md) for acceptance coverage and local performance measurements. The broader PRD roadmap still includes later work: licensed live feeds, shorts/margin, bracket/OCO/trailing orders, Level 2, bots, server alerts, and multi-chart layouts.
