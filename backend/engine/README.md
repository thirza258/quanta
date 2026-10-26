# Simulator engine

The trading simulator's computation, in C++17: the generated market and the original six-path generator, the execution engine with its exact decimal ledger, and the per-bar desk analytics. The API loads it in-process as a shared library through `backend/quanta/engine` (ctypes, so no Python build dependency). It replaced Python and numpy implementations, and it reproduces them to the cent and the character: runs stored before the port replay against the same bars and settle to the same balances, reasons and identifiers.

## Build and test

```sh
make            # build/libquanta_sim.dylib (macOS) or build/libquanta_sim.so (Linux)
make test       # golden fixtures, refusals, serial/parallel equality
make sanitize   # the same tests under AddressSanitizer + UndefinedBehaviorSanitizer
make bench      # five paired serial/parallel timings; refuses to report if outputs differ
```

Requirements: a C++17 compiler with floating-point `std::to_chars` (Clang 14+ / libc++, or GCC 11+ / libstdc++), make and POSIX threads, on macOS, Linux or WSL. A native Windows build is not provided. Select a compiler with `make clean && make CXX=g++-16`. `make sanitize` needs a compiler that ships the ASan and UBSan runtimes. Root `npm run setup`, `npm run dev`, `npm run test:api` and `npm run check` build the library when it is out of date, and the development API restarts when it is rebuilt.

The differential tests against the original Python live in `backend/tests/test_engine_parity.py`. To run the sanitizers over every engine call the Python suite makes, record a corpus and replay it:

```sh
QUANTA_ENGINE_CORPUS=/tmp/engine.corpus ../.venv/bin/python -m pytest ../tests -q
make replay CORPUS=/tmp/engine.corpus   # byte-identical responses, under ASan + UBSan
```

`QUANTA_SIM_THREADS` caps the worker threads one request may use (default: the hardware's count, at most eight; the Docker image sets 2 to match its CPU limit). `QUANTA_ENGINE_LIB` loads the library from another path.

## Layout

| File | Responsibility |
| --- | --- |
| `include/quanta_sim.h` | The C interface: plain buffers in, plain buffers out, an error code and a per-thread message. No pointer is kept after a call returns and no global state is mutated, so calls on different threads are independent. |
| `src/rng.cpp`, `ziggurat_tables.hpp` | numpy's `SeedSequence`, PCG64 and ziggurat `standard_normal`; CPython's MT19937 `random()`, `gauss()` and `randint()`. |
| `src/market.cpp` | Shock scheduling into the market, sector and company processes; the 21-session block generator; the six-path generator; chart bucketing. |
| `src/calendar.cpp` | The weekday session clock and the New York offset rule. |
| `src/decimal.cpp`, `u256.hpp` | Exact decimal arithmetic with Python `decimal` semantics at 28 digits. |
| `src/engine.cpp`, `json.cpp` | Validation, reservations, fills, brackets, trailing stops, margin, buy-ins and replay stops, behind a JSON request/response protocol. |
| `src/analytics.cpp` | SMA, EMA, Wilder RSI and MACD series; the account and the equal-weighted index marked on every bar. |
| `src/numeric.cpp`, `libm.cpp` | numpy's summation orders, CPython's `round(x, 2)`, and run-time C library calls. |
| `src/parallel.hpp` | Deterministic `parallel_for` over independent tasks. |
| `tests/test_main.cpp` | Hand-calculated fixtures, invalid-input refusals, serial/parallel equality for 1-32 workers. |
| `tests/replay.cpp` | Replays a recorded corpus of engine calls. |
| `bench/bench.cpp` | Paired benchmark. |

On the Python side, `quanta/engine` owns the library handle and the conversion of run state into arrays and JSON; `quanta/domain/simulator.py` keeps the functions the services always called (`validate_order`, `advance_state`, `reservations`, ...) and writes the engine's changes back into the stored run. HTTP routes, persistence, idempotency, the newsroom's headline text and schedule, generated statements, missions, and the monitor tools (tape, book, heat map, participants) remain Python, as do the vectorized numpy statistics of the screener and the shared `summarize()` the research courses also use.

## The contract: identical results

**Random streams.** A block is drawn from `numpy.random.default_rng([seed, first_session, 0x9E3779B9])`; the engine implements numpy's `SeedSequence` pool mixing, the PCG64 128-bit LCG with XSL-RR output, and numpy's ziggurat sampler with numpy's own tables (BSD-3-Clause, read from numpy 2.5.3 and checked draw for draw). The original six paths use `random.Random(seed + 100003 * n)`: MT19937 seeded through `init_by_array`, CPython's 53-bit `random()`, cached Box-Muller `gauss()` and rejection-sampled `randint()`.

**Floating point.** Every expression is evaluated in the order numpy evaluated the Python it replaces, one rounding per operation, and the build disables fused multiply-add (`-ffp-contract=off`) and fast-math. Reductions follow numpy: pairwise summation with eight accumulators along a contiguous array, row-by-row accumulation for an axis-0 mean. `exp`, `log`, `log1p`, `pow`, `sin` and `cos` are called through pointers the optimizer cannot see through, so none is folded at build time or rewritten (`pow(x, 2.0)` is not `x * x` in every library). Prices become cents through `rint` exactly as `np.rint(... * 100)` did. Parity therefore depends on numpy evaluating float64 `exp` and `log` through the C library, as it does on the arm64 Mac every check above ran on (3 million sampled values agreed with the C library exactly). The Linux image compiles the engine against glibc, which numpy also uses there unless the CPU offers AVX-512, where numpy switches to its own vectorized `exp`. That Linux equality is expected, not yet measured. Runs created by the Docker deployment were generated on Linux, so check it before relying on bit-identical replay of those runs:

```sh
docker compose build api
docker run --rm -v "$PWD/backend/tests:/app/backend/tests:ro" quanta-api \
  python -m pytest backend/tests/test_engine_parity.py -q -p no:cacheprovider
```

A failure there means the image's numpy and glibc disagree in the last place, and old Linux-generated runs could differ by a cent on some bars.

**Decimal.** Money in a run is stored as decimal strings, and the account rules multiply cents by configured rates and divide totals by quantities. The engine reproduces Python's `decimal` under its default context exactly: 28 significant digits with round-half-even after every operation, `quantize` with ROUND_HALF_UP, ROUND_CEILING and ROUND_DOWN, the exponents Python chooses, and the sign a zero keeps (`-0.00`). A float price from an imported dataset is read as `Decimal(str(x))` reads it, through its shortest round-trip digits. Decimals travel through the JSON protocol as strings; a JSON float is refused.

**Bounds.** Inputs are validated before any arithmetic: at most a million orders of at most 10^12 shares, positions within 10^15, decimal inputs of at most 38 significant digits, cursors and steps bounded, generator parameters finite and in range. Under those bounds every integer sum fits in int64 and every decimal intermediate fits in 256 bits; conversions that could still exceed int64 (a quantity derived by division) are checked. Out-of-range input is an error, never a wrapped value, and a refused account action changes nothing.

## Parallel work

- **Block generation.** Every draw for a block is made first, on one stream: the ziggurat consumes a variable number of words per normal, so no draw can be located without making the ones before it. Companies are then independent and are built in parallel, each task reading the shared factor paths and writing only its own slice. The sequential draws bound the speedup, as Amdahl's law says they must.
- **Mark to market.** Each bar is independent, so the window is split across workers; each bar still adds its fills in fill order.
- **Six-path generator.** Each symbol has its own stream, so symbols run in parallel.
- **Execution engine.** Sequential by design: a fill on one bar changes the cash and reservations the next order and the next bar see.

`parallel_for` gives each task disjoint outputs, lets the calling thread work, survives a worker the system refuses to start, and rethrows the first failure only after every thread has joined. Results do not depend on the worker count; `make test` checks 1-32 workers and every benchmark pair compares outputs.

## Verification

- `make test`: 170 checks: PRD SIM-AC-03 (buy 10 at $100, sell at $110, $1 fees: $98,999 then $100,098, $98 realized), short round trips, a sale crossing zero, one session's borrow fee ($9.92 on 1,000 shares at $50), a trailing stop ratcheting to $104.50, FIFO volume sharing with one commission, decimal rounding and signed zeros, numpy/CPython stream values, the DST transitions of the session clock, malformed and out-of-range input.
- `backend/tests/test_engine_parity.py`: generated blocks, the session clock, the six paths, bucketing, indicator series and the mark-to-market equal the original implementations kept in `backend/tests/reference/`; 40,000 random decimal operations equal Python's; 28 randomized trading scenarios (generated and hand-built markets, cash and margin, every order type, brackets, amendments, cancellations, DAY expiry, gaps, borrow, buy-ins, event stops) produce byte-identical run state after every action through both engines, plus each rejection branch. Breaking one rounding rule in the engine fails 26 of these tests.
- The library and tests build warning-free with `-Wall -Wextra -Werror -pedantic` under Apple Clang 21 and GCC 16; the parity suite passes against both builds.
- Sanitizers: `make sanitize` passes, and a corpus of 6,980 engine calls recorded from the parity, simulator and mission tests replays under ASan and UBSan with identical responses.
- Stored runs: all 574 runs in a local development database (543 generated, 31 six-path) were replayed read-only through both engines. Every bar of every symbol up to each run's cursor plus a week equals the numpy generator; snapshot figures and reservations match; advancing 1, 390 and 1,950 bars from each stored state leaves byte-identical state.

## Measurements

Apple M2 Pro (10 cores), Darwin 25.6.0, Apple Clang 21, `-O2`, eight workers, one `make bench` run, medians of five pairs with their ranges:

| Workload | Serial | Parallel | Speedup |
| --- | --- | --- | --- |
| One block: 32 companies x 8,190 bars | 34.1 ms (33.5-36.5) | 13.5 ms (13.3-14.2) | 2.5x |
| Mark to market: 200,000 bars x 2,000 fills x 32 symbols | 303.4 ms (298.3-303.8) | 53.6 ms (52.3-56.0) | 5.7x |
| Execution engine: 200 working orders advanced 1,950 bars, JSON included | 12.3 ms (11.8-12.9) | sequential | |

Through the API's Python adapter on the same machine, advancing a modeled week (1,950 bars) on generated seed 47 took, before and after the port (medians of five runs):

| Working orders | Python engine | C++ engine |
| --- | --- | --- |
| 50 | 302.9 ms | 5.0 ms |
| 200 | 1,253.9 ms | 15.4 ms |
| 2,000 | not measured | 148.8 ms |

Generating five blocks, newsroom included, went from 467 ms to 210 ms; the newsroom's Python headline text is now most of it. These are samples from one machine, not a portable guarantee; hardware, compiler, flags and load all move them.

## References

- NumPy random: [SeedSequence](https://numpy.org/doc/stable/reference/random/bit_generators/generated/numpy.random.SeedSequence.html), [PCG64](https://numpy.org/doc/stable/reference/random/bit_generators/pcg64.html); M. E. O'Neill, [PCG](https://www.pcg-random.org/paper.html); G. Marsaglia and W. W. Tsang, "The Ziggurat Method for Generating Random Variables", *Journal of Statistical Software* 5(8), 2000.
- M. Matsumoto and T. Nishimura, "Mersenne Twister", *ACM TOMACS* 8(1), 1998; CPython [`random`](https://docs.python.org/3/library/random.html).
- [General Decimal Arithmetic Specification](https://speleotrove.com/decimal/decarith.html) and CPython [`decimal`](https://docs.python.org/3/library/decimal.html).
- H. Hinnant, [chrono-compatible low-level date algorithms](https://howardhinnant.github.io/date_algorithms.html).
- [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html), [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html), [Clang floating-point options](https://clang.llvm.org/docs/UsersManual.html#controlling-floating-point-behavior).
