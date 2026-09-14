# Algorithmic trading II: C & high-performance computing

Original Quanta teaching project. C17 plus POSIX threads; no Python, broker credentials, live orders, downloaded prices, or required GPU. Use macOS with command-line developer tools, Linux with a C compiler and make, or Windows through WSL with those tools installed.

## Build and run

Unzip into a folder, open a terminal in that folder, then run:

```sh
make
make test
make sanitize
./quanta-bot 4 200000
./quanta-bot 1 200000
```

`make sanitize` needs a Clang/GCC installation with AddressSanitizer and UndefinedBehaviorSanitizer runtimes. The ordinary build has no sanitizer dependency. To select a compiler: `make clean` then `make CC=clang` (or `CC=gcc`). The printed compiler version and local CPU matter when interpreting timings. A Windows-native MSVC build is not provided.

Every lesson also provides an independent C worksheet. Download it from the lesson's C lab and compile it in the folder where you saved it:

```sh
cc -std=c17 -Wall -Wextra -Werror -O2 lesson.c -o lesson
./lesson
```

Use the actual downloaded filename in place of `lesson.c`. Worksheets explain small mechanisms; the full project is the threaded integration exercise.

## Architecture and contract

- `quanta.h`: public types, validated limits and function contracts.
- `engine.c`: seeded synthetic bars, checked target-position ledger and chronological backtest.
- `parallel.c`: a bounded set of workers over independent windows. Each worker owns disjoint result indices and reads the same immutable bars. Results publish only after every job succeeds and every thread joins.
- `main.c`: strict command-line parsing and five paired wall-clock benchmark repetitions.
- `test.c`: hand-calculated fixtures, rejected-order atomicity, terminal-signal timing, invalid data and serial/parallel equality for 1–32 requested workers.

The long/cash rule targets one share when close is strictly above its trailing simple moving average. It observes close t and can fill only at open t+1. Equality means cash. Initial capital is 1,000,000 cents ($10,000). Every change in position costs 5 cents. There is no spread or market impact; trades fill completely at the next synthetic open. The final position is marked at the final close; a last-bar signal is not executed. This is a deterministic research model, not a claim about realistic exchange execution or investment performance.

Prices and cash use signed 64-bit cents. Validate input bounds BEFORE multiplication. Limits bound the largest intermediate below `INT64_MAX`; they are part of the numeric proof. The RNG intentionally uses defined unsigned wrap. Changing these limits requires revisiting that proof. One-share research trials may fail if funds are exhausted; failure is explicit, never a partial successful report.

The benchmark includes per-trial validation and thread creation/join, excludes data generation and printing, and alternates serial/parallel order after warmup. It prints five timings, observed speedups and all 64 result rows. It refuses a serial/parallel mismatch. For tiny inputs or busy machines, threads can be slower. Rank quality on separate chronological validation/test periods; these synthetic sweep results provide no evidence of alpha.

## Assignments and capstone

Follow `performance-notebook.md`. First establish the tests, then change exactly one mechanism: data layout, validation placement, or trial scheduling. Preserve the scalar implementation as an oracle. Demonstrate equality on boundary fixtures and multiple seeds; report median timing and run-to-run spread for at least two workload sizes. Save compiler flags, CPU/OS, input count, seed, windows and full output. Never compare an instrumented debug build against an optimized release as an algorithmic speedup.

OpenMP, vectorization, GPU batching and distributed manifests are taught as design/measurement extensions in the course. This downloadable reference implements the C/POSIX CPU path. No CUDA/OpenCL kernel, exchange gateway, real-time guarantee, lock-free queue, or cluster deployment is shipped.

## Primary references

- [Clang user manual](https://clang.llvm.org/docs/UsersManual.html)
- [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) and [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)
- [Linux man-pages: pthread_create](https://man7.org/linux/man-pages/man3/pthread_create.3.html), [pthread_join](https://man7.org/linux/man-pages/man3/pthread_join.3.html), [clock_gettime](https://man7.org/linux/man-pages/man3/clock_gettime.3.html)
- [OpenMP specifications](https://www.openmp.org/specifications/)
- [GCC optimization options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)

Examples and assignments are original; references acknowledge source concepts and do not imply endorsement.
