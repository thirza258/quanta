# Algorithmic trading II: C & high-performance computing

Open `/curriculum/c-hpc-trading`, immediately after the existing Python bot course. Stable lesson IDs are `9.1`–`9.24`; no existing lesson or assessment is renumbered. Source: `content/authoring/c_hpc_course.py`; project: `content/projects/c-hpc-trading/`; generated catalog: `content/catalog/curriculum.json`.

24 sessions × 30 minutes = **12 hours of planned study**, each allocating 10 minutes to reading, 10 to local C experimentation and 10 to the assignment. Exams are additional. Every lesson has original explanatory material, a worked case and equation, a complete C17 worksheet with expected output, two practice items, an assignment/solution and primary references. Six checkpoints cover all units; the 24-question version-1 final requires 80% (20 correct). The separate capstone rubric requires 80/100 and no unresolved causality, corruption or duplicate-execution defect.

| Unit | Lessons | Scope |
| --- | --- | --- |
| C foundations | 9.1–9.4 | Research throughput vs execution latency; compiler/linker workflow; integer bounds and floating point; pointers and ownership |
| Data and event engine | 9.5–9.8 | Data contracts and missingness; AoS/SoA and cache traffic; O(n) rolling indicators; next-open causal fills |
| Measurement and correctness | 9.9–9.12 | Monotonic clocks and timing boundaries; repeated measurements and Amdahl limits; golden fixtures and sanitizers; controlled optimization |
| Parallel CPU research | 9.13–9.16 | POSIX independent trials; races, joins and publication; deterministic seeds/results; OpenMP scheduling design |
| HPC extensions | 9.17–9.20 | SIMD/tails/aliasing; GPU batching, transfer and roofline costs; distributed manifests/retries; bounded queues and backpressure |
| Risk and capstone | 9.21–9.24 | Atomic ledger transitions; order replay/recovery; freshness and operational budgets; reproducible optimization dossier |

## Learner workflow

Read → predict worksheet output → open **C lab** → edit → download `.c` → compile/run locally → record evidence in the notebook → complete practice → take checkpoints/final. Monaco C highlighting is bundled locally. C drafts use existing guest/account workspace persistence and are retained when reopening the lab. Reset is explicit. Expected output is a reference for the original template, not a claim that the browser executed edited code.

The browser does not compile C or submit it to the Python sandbox. Each standalone worksheet uses only C17 standard library headers and compiles with the on-page command. The full project additionally requires POSIX threads and make. Supported development environments are macOS with developer tools, Linux with compiler/make, or WSL; a native Windows/MSVC port is not provided.

## Implemented project

Download `c-hpc-bot-lab.zip` from the course or C lab. It includes header, engine, parallel orchestration, CLI, tests, Makefile, build guide and performance notebook/rubric. It generates deterministic synthetic open/close bars, targets one share above a trailing SMA, fills at the next open and charges five cents per fill. Initial cash is 1,000,000 cents. The final position is marked at the last close; terminal signals have no fill.

Serial and POSIX-thread sweeps evaluate 64 windows and compare each field exactly. Inputs remain immutable; results are indexed independently of completion order. Partial worker creation joins existing workers before failure; caller results publish only after all jobs succeed. The benchmark alternates order across five pairs after warmup and includes validation/thread setup/join in both relevant boundaries. Hardware, flags, workload and timing spread matter; no fixed speedup is promised.

```sh
cd content/projects/c-hpc-trading
make
make test
make sanitize
./quanta-bot 4 200000
```

Tests require a local C17 compiler (`cc`) and make. The normal root `npm run check` compiles all 24 C worksheets and extracts/builds/tests the learner archive, alongside the 276 Python templates. The separate sanitizer target requires a compiler with ASan/UBSan runtimes.

Independent golden fixture: buy at 130, sell at 90, pay two five-cent fees → **999,950 cents, two fills**. Tests also cover no terminal fill, warmup, invalid bounds/data, fee affordability, rejected mutation, duplicate achieved targets, deterministic seeds, worker counts 1–32 and failed-result publication. Source-only packaging excludes binaries, installed dependencies and local state.

## Scope and references

The CPU C/POSIX implementation is runnable. OpenMP porting, SIMD experiments, GPU kernels, multi-machine distribution, a concurrent lock-free queue and a persistent/live gateway are explicit extension or design assignments. All input bars are synthetic; complete next-open fills omit spread, impact, liquidity and remote order uncertainty. System throughput is separate from investment performance and exchange latency.

Primary references accompany every lesson: [Clang](https://clang.llvm.org/docs/UsersManual.html), [ASan](https://clang.llvm.org/docs/AddressSanitizer.html), [UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html), [POSIX thread interfaces in Linux man-pages](https://man7.org/linux/man-pages/man3/pthread_create.3.html), [LLVM vectorizers](https://llvm.org/docs/Vectorizers.html), [OpenMP](https://www.openmp.org/specifications/), [NVIDIA CUDA best practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html), [MPI Forum](https://www.mpi-forum.org/docs/) and [evaluation/leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html). Material and questions are original; references acknowledge concepts without implying endorsement or reproduction rights.
