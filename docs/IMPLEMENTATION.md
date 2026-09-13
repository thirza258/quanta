# PRD implementation scope

The user selected a usable local platform across all tracks. The 18-week production roadmap is not claimed complete. This release is an integrated local learning and research platform, with a Compose deployment suitable for local/private hosting.

| PRD area | Implemented locally | Remaining production work |
| --- | --- | --- |
| LMS foundation | React/TypeScript/Vite, Tailwind, Radix dialogs, local fonts, Monaco, KaTeX, responsive dual-pane reader, search, themes | Formal accessibility audit and broader device/performance targets |
| Accounts & learning state | Email/password, Argon2, signed/revocable HttpOnly sessions, SQLite/PostgreSQL, notes, exercises, progress, experiments, local recovery | GitHub/Google OAuth, account recovery/email delivery, account deletion/export policy, migration tooling |
| Track 1 | Five original modules with runnable arithmetic templates, NCAV/haircuts/Graham worksheet | Complete textbook-length instruction, automated SEC normalization and provenance |
| Track 2 | Five modules with probability/estimation/testing/regression worked examples; synthetic paths | Interactive distribution and bootstrap tools, richer code completion |
| Track 3 | Five modules; factor studio, HAC inference, risk metrics, portfolio optimization API | Historical factor ingestion, GARCH/ARIMA/cointegration-specific interfaces, efficient-frontier UI |
| Track 4 | Four strategy research modules; parameterized long/cash backtester and experiment persistence; ridge validation | Cross-sectional historical universe, full multi-asset and short/borrow execution, purged model search pipeline |
| Track 5 | Five bot engineering modules; deterministic paper broker, partial fills, fees and risk guards | Durable order queues, live broker adapters, XGBoost/LightGBM, LLM provider and evaluation, external alerts, telemetry |
| Track 6 | Five modules; AMM swaps, full-range and concentrated IL, flash-crash paths | CEX/RPC adapters, signing/nonces, real funding histories, deployed bots, a pathwise collateral liquidation engine |
| Synthetic generators | Four seeded stochastic processes and all named stress scenarios | Thousand-path Monte Carlo UI and dedicated large-job queue |
| Empirical data | Validated OHLCV CSV → Parquet → DuckDB → backtest | Licensed 1990–present equity/crypto/funding/macro data, point-in-time SEC fundamentals, corporate actions, delisted/dead-token universes |
| Sandbox | Guided AST VM in isolated subprocess, resource bounds, Redis/local rate limiting; optional non-root Docker scientific worker | Production hardened worker infrastructure (gVisor/microVM), formal security assessment; Pyodide offline runtime |
| Deployment | Four-service Compose, health checks, data volumes, non-root app services, read-only roots, internal database/cache network | Managed TLS/DNS, managed secrets, backups/restore drills, migrations, fleet monitoring, production load/security audit |

## Modeling conventions

- All default prices and factor observations are explicitly synthetic. Names such as “1929-inspired” describe stress mechanisms, not fitted historical reconstructions.
- OHLCV uses a weekday-only synthetic calendar and 252 observations per modeled year. Holidays and intraday execution are not modeled.
- Signals from a close act at the **next open**. Entries commit available cash after fees; exits deduct fees and slippage. The final position is marked to the last close and is not forcibly liquidated.
- The benchmark is buy-and-hold of the same supplied path, including entry fees/slippage. It is not labeled the S&P 500.
- Maximum drawdown includes initial capital. Win rate and profit factor use closed round trips. Profit factor is undefined when there are no gross losses; undefined values are `null`, never infinity in JSON.
- Sharpe and Sortino use a 3% annual risk-free rate. Alpha and beta are a descriptive single-factor comparison against the same-path benchmark. Annualized arithmetic alpha and geometric CAGR are different quantities.
- VaR/CVaR are nonnegative daily loss magnitudes at 95%; they are estimates, not maximum-loss guarantees.
- AMM IL compares a fee-free LP position with holding its initial inventory. Concentrated liquidity uses piecewise inventories clamped to range boundaries. Swap output separately includes the swap fee.
- Regression examples plant known exposures in synthetic data. The ridge comparison trains on the first 75% only, including its scaler. Portfolio optimization uses a fixed 10% diagonal covariance shrinkage; this is not represented as estimated Ledoit–Wolf shrinkage.
- The paper broker is a stateless calculation API with a session-scoped browser account, not a real ledger. Its drawdown breaker compares current marked equity with initial account equity. Unfilled quantity is reported explicitly; automatic durable retries are not implemented.
- Lesson valuation arithmetic and its accompanying price strategy are distinct exercises. Synthetic trend returns do not validate NCAV/Graham selection performance.

## Persistence and recovery

Guest data remains in a versioned browser-storage namespace. Registering copies guest progress into a new account. Signing in loads that account’s remote state. Local pending edits include their base server revision. A same-revision reconnect retries them; a divergent revision preserves the local copy and stops sync instead of silently overwriting either version. Export the local workspace from the profile menu before resolving conflicting versions. Resolve sync conflict → Use account copy explicitly replaces local edits with the latest server copy after confirmation. Passwords and JWTs are never stored in browser storage.

Workspace snapshots store code, parameters, summary metrics, notes, and progress. Full time series are recreated by rerunning the saved seed/configuration. API snapshots are limited to 1.2 MB; local exports provide an escape hatch when retaining many experiments.
