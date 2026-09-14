"""Original C17/HPC bot course, with independently compilable C worksheets."""

from applied_courses import checkpoints_for, study
from book_courses import finish

CLANG = (
    "LLVM contributors · Clang compiler user manual",
    "https://clang.llvm.org/docs/UsersManual.html",
)
ASAN = ("LLVM contributors · AddressSanitizer", "https://clang.llvm.org/docs/AddressSanitizer.html")
UBSAN = (
    "LLVM contributors · UndefinedBehaviorSanitizer",
    "https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html",
)
THREADS = (
    "Linux man-pages project · pthread_create",
    "https://man7.org/linux/man-pages/man3/pthread_create.3.html",
)
JOIN = (
    "Linux man-pages project · pthread_join",
    "https://man7.org/linux/man-pages/man3/pthread_join.3.html",
)
CLOCK = (
    "Linux man-pages project · clock_gettime",
    "https://man7.org/linux/man-pages/man3/clock_gettime.3.html",
)
GCC = (
    "GNU compiler contributors · Optimization options",
    "https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html",
)
VECTOR = ("LLVM contributors · Loop and SLP vectorizers", "https://llvm.org/docs/Vectorizers.html")
OMP = (
    "OpenMP Architecture Review Board · Specifications",
    "https://www.openmp.org/specifications/",
)
CUDA = (
    "NVIDIA · CUDA best practices guide",
    "https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html",
)
MPI = ("MPI Forum · Message Passing Interface standards", "https://www.mpi-forum.org/docs/")
ATOMICS = (
    "GNU compiler contributors · Atomic memory-order builtins",
    "https://gcc.gnu.org/onlinedocs/gcc/_005f_005fatomic-Builtins.html",
)
LEAKAGE = (
    "scikit-learn contributors · Data leakage and common pitfalls",
    "https://scikit-learn.org/stable/common_pitfalls.html",
)


def build_c_hpc_trading():
    modules = []

    def add(
        title,
        objective,
        principle,
        case,
        workflow,
        formula,
        code,
        expected,
        task,
        solution,
        questions,
        refs,
    ):
        index = len(modules) + 1
        # Rotate the correct option; practice, final and checkpoint are distinct cases.
        rows = []
        for offset, (prompt, correct, wrong1, wrong2, explanation) in enumerate(questions):
            options = [correct, wrong1, wrong2]
            shift = (index + offset) % 3
            options = options[shift:] + options[:shift]
            rows.append((prompt, options, options.index(correct), explanation))
        item = study(
            f"9.{index}",
            (index - 1) // 4 + 1,
            title,
            objective,
            principle,
            case,
            workflow
            + "\n\n### Local C laboratory\n\nOpen the C lab, download the worksheet, and compile it with the displayed C17 command. Predict the output before running it. Change one input, explain the new result, and save both observations in your notebook. Compare the mechanism with the named source file in the full project. Compiler errors are part of the exercise: read the first diagnostic, fix its cause, and rebuild before interpreting any timing. The downloadable reference project uses synthetic data; its returns do not establish investment merit.",
            formula,
            "",
            task,
            solution,
            rows,
            refs,
        )
        item["codeLanguage"] = "c"
        item["code"] = (
            "/* Original Quanta C17 worksheet. Compile and run locally. */\n"
            "#include <stdio.h>\n#include <stdint.h>\n#include <inttypes.h>\n#include <stddef.h>\n#include <stdlib.h>\n#include <limits.h>\n\n"
            + code.strip()
            + "\n"
        )
        item["expectedOutput"] = expected
        item["minutes"] = 30
        item["reading"] = (
            "30-minute session: 10 minutes reading and primary references, 10 minutes compiling and modifying the C worksheet, and 10 minutes completing the assignment. Use a local C17 compiler; the full project additionally needs POSIX threads and make (macOS, Linux, or WSL)."
        )
        modules.append(item)

    add(
        "From a Python prototype to a C research engine",
        "Separate research throughput, trading latency, numerical correctness, and investment validity.",
        "The first bot course established the research and execution process. This second course rebuilds its systems foundation in C. A faster implementation earns its place by preserving a written contract: input timestamps, signal timing, position rules, costs, rejected orders, and final valuation. Language choice alone establishes none of these.\n\nResearch throughput measures complete trials per second. Execution latency measures how long a specific event takes to reach a response, including queues and downstream dependencies. A million fast synthetic backtests cannot establish exchange latency or strategy quality. Keep the sequential event engine as an oracle, then parallelize independent experiments. The reference has four boundaries: public types, deterministic engine, worker orchestration, and command-line measurement.",
        "A research batch takes 120 seconds: 90 in simulation and 30 in preparation. Making simulation three times faster gives 30 + 30 = 60 seconds overall, a 2× speedup. Reporting 3× for the whole pipeline would hide unchanged work.",
        "Download the full lab and read quanta.h before engine.c. Write the expected behavior of a close-based signal and inspect the next-open fill rule. Build with make, run make test, and retain a baseline output before modifying a single loop.",
        r"S = \frac{T_{\mathrm{before}}}{T_{\mathrm{after}}}",
        r"""
int main(void) {
    double total = 30.0 + 90.0 / 3.0;
    printf("total=%.0f speedup=%.1f\n", total, 120.0 / total);
    return 0;
}""",
        "total=60 speedup=2.0",
        "Draw the four project boundaries and calculate whole-program speedup when only 80 of 100 seconds is accelerated fourfold. Explain what this says about exchange latency.",
        "The new total is 20 + 80/4 = 40 seconds, giving 2.5×. Types define contracts, engine owns chronological state, orchestration schedules trials, and main measures. This workload does not measure an exchange round trip.",
        [
            (
                "Which metric answers how many parameter trials finish each second?",
                "Research throughput",
                "Portfolio return",
                "Order round-trip latency",
                "Throughput counts completed work per time under a specified workload.",
            ),
            (
                "A C rewrite produces different fills from the baseline. What comes first?",
                "Explain and resolve the contract mismatch",
                "Publish its faster timing",
                "Increase worker count",
                "A performance comparison is invalid until both programs implement the same behavior.",
            ),
            (
                "A 100-second run has 40 unchanged seconds and 60 seconds sped up threefold. Overall speedup is:",
                "About 1.67×",
                "3×",
                "5×",
                "The new time is 40 + 20 = 60 seconds, so speedup is 100/60.",
            ),
            (
                "Does a fast synthetic sweep demonstrate production order latency?",
                "No; the gateway and exchange path were not measured",
                "Yes, if implemented in C",
                "Yes, if it uses all cores",
                "The measurement boundary excludes network, gateway and exchange dependencies.",
            ),
        ],
        [CLANG, THREADS],
    )
    add(
        "Build, link, diagnose, and reproduce a C17 program",
        "Use compiler diagnostics, separate translation units, and reproducible build flags.",
        "A C source file becomes a translation unit after preprocessing. Compilation checks declarations and produces machine code; linking resolves definitions across object files and libraries. A header describes a shared interface. Putting inconsistent declarations into several files can undermine that interface even when a small example seems to work.\n\nUse explicit C17 mode and warnings while learning. Fix the first meaningful diagnostic before the cascade that follows. Debug information helps inspection; optimization changes code generation. Rebuilding with different flags requires a clean build in this simple Makefile because command-line flags are not tracked as file dependencies. Record compiler version, operating system and exact flags with every performance result.",
        "The project links main.c, engine.c and parallel.c with -pthread. Compiling only main.c leaves q_sweep unresolved. A standalone lesson worksheet needs no project objects because it defines its own main and all helper functions.",
        "Compile the worksheet with -std=c17 -Wall -Wextra -Werror. In the project, run make clean before switching from -O2 to -O0. Deliberately misspell a function in a temporary copy, identify whether the failure arises during compilation or linking, then restore it.",
        r"\text{program} = \text{translation units} + \text{linked dependencies}",
        r"""
static int fee(int fills) {
    return fills * 5;
}
int main(void) {
    printf("fee=%d cents\n", fee(4));
    return 0;
}""",
        "fee=20 cents",
        "Record a successful build command and explain why a declared but undefined q_sweep fails when linking only main.c. Compare two optimization builds after cleaning.",
        "The header provides a declaration but parallel.c provides the definition. Link all required source/object files and thread support. Clean between flag changes, record both commands, and require equal results before comparing performance.",
        [
            (
                "Which stage resolves a referenced function defined in another object file?",
                "Linking",
                "Reading a price CSV",
                "Backtest evaluation",
                "The linker resolves symbols across object files and libraries.",
            ),
            (
                "Why use make clean when changing CFLAGS in this simple project?",
                "Its rules do not track changed command-line flags",
                "C17 requires deleting source files",
                "It changes the strategy seed",
                "File timestamps alone will not necessarily rebuild a target after a flag change.",
            ),
            (
                "A prototype exists but its implementation is absent from the link command. The likely failure is:",
                "An unresolved symbol during linking",
                "A valid zero-valued result",
                "An automatic Python fallback",
                "A declaration does not supply the machine-code definition required by the linker.",
            ),
            (
                "Which evidence belongs with a benchmark build?",
                "Compiler version and exact compile/link flags",
                "Only the executable name",
                "Only the winning window",
                "Compiler and flags influence generated code and are necessary for reproduction.",
            ),
        ],
        [CLANG, GCC],
    )
    add(
        "Integer cents, floating point, and checked arithmetic",
        "Choose numeric representations and prove intermediate bounds before arithmetic.",
        "Decimal currency is not generally represented exactly by binary floating point. The lab uses integer cents for its ledger and doubles only for elapsed time. Integer arithmetic does not remove risk: signed overflow is undefined behavior in C. Validate inputs before multiplication, addition, or negation, including intermediate expressions that might overflow even when a final answer would fit.\n\nThe project's maximum share count and price bound a notional product by 10^15, safely below signed 64-bit capacity. The limits are a proof obligation, not decorative constants. Reject a negative quantity before converting it to size_t. Fees and tick rounding need an explicit economic rule; do not silently truncate a price during a port from another language.",
        "Three shares at 12,345 cents cost 37,035 cents. With a five-cent fill fee and 50,000 cents cash, remaining cash is 12,960 cents. Check affordable notional first, then check the fee against the remaining balance; neither subtraction should underflow.",
        "Read q_target's validation and derive each product bound. Compile with the undefined-behavior sanitizer through make sanitize. Add a boundary fixture before raising any limit. Keep research statistics separate from exact ledger fields.",
        r"N = q p, \qquad q \le \left\lfloor\frac{\mathrm{INT64\_MAX}}{p}\right\rfloor",
        r"""
int main(void) {
    int64_t q = 3, p = 12345, cash = 50000, fee = 5;
    if (p <= 0 || q < 0 || q > INT64_MAX / p)
        return 1;
    int64_t n = q * p;
    if (n > cash || fee > cash - n)
        return 1;
    printf("cash=%" PRId64 "\n", cash - n - fee);
    return 0;
}""",
        "cash=12960",
        "Prove the project notional and moving-sum bounds. Add an INT64_MAX input to a local rejected-order test and verify the account remains unchanged.",
        "Notional is at most 10^6 × 10^9 = 10^15. A million bounded closes also sum to at most 10^15 (a transient extra close remains safe). Validate before evaluating larger products; the invalid target must return failure without changing cash or shares.",
        [
            (
                "When must a multiplication overflow check happen?",
                "Before evaluating the multiplication",
                "After storing the wrapped result",
                "Only when cash becomes negative",
                "Signed overflow itself is undefined behavior, so a later check is too late.",
            ),
            (
                "Which representation does this project use for exact cash?",
                "Signed 64-bit integer cents with bounds",
                "Unbounded signed C integers",
                "A floating-point string",
                "The ledger uses integer cents and explicit limits on all inputs and intermediates.",
            ),
            (
                "Four shares at 2,500 cents plus a 5-cent fee from 20,000 cents leaves:",
                "9,995 cents",
                "10,005 cents",
                "9,980 cents",
                "Subtract 4 × 2,500 and one five-cent fill fee from initial cash.",
            ),
            (
                "What changes when the allowed share limit increases?",
                "The proof that all intermediate arithmetic fits",
                "Only the user-facing label",
                "The definition of C signed overflow",
                "Larger inputs can invalidate the bounds that previously made arithmetic safe.",
            ),
        ],
        [UBSAN, CLANG],
    )
    add(
        "Pointers, ownership, and allocation lifetimes",
        "Make array extent, ownership, and cleanup explicit at C interfaces.",
        "A pointer identifies an address; it does not carry the length or ownership policy of an array. Pass an extent with the pointer. The creator of a heap allocation owns the obligation to free it exactly once, after all readers finish. Borrowed const pointers communicate read-only access through that interface, but other aliases can still mutate the object unless the design forbids them.\n\nThe lab allocates bars once, borrows them in every trial, and frees them after all workers join. Scratch results belong to the sweep call. A worker must never keep a pointer to a caller's expired stack frame. Failure handling needs the same lifetime discipline as the successful path. Check count against a safe limit before count multiplied by element size reaches malloc.",
        "An array of four int64_t prices needs 4 × sizeof(int64_t) bytes. A second pointer to it is an alias, not a copy. Freeing the first pointer invalidates access through both. The worksheet has one allocation, one checked use, and one release.",
        "Annotate each pointer in main.c and parallel.c as owner or borrower and state its lifetime. Use AddressSanitizer on tests. It can detect many invalid accesses on exercised paths; passing it does not prove all possible paths safe.",
        r"\text{allocation bytes} = n\,\mathrm{sizeof}(T)",
        r"""
int main(void) {
    size_t n = 4;
    if (n > SIZE_MAX / sizeof(int64_t))
        return 1;
    int64_t *p = malloc(n * sizeof(*p));
    if (!p)
        return 1;
    for (size_t i = 0; i < n; ++i)
        p[i] = (int64_t)(i + 1) * 100;
    printf("last=%" PRId64 "\n", p[n - 1]);
    free(p);
    return 0;
}""",
        "last=400",
        "Draw the lifetimes of bars, worker arguments, scratch results and caller output. Explain why returning before joining workers can corrupt memory.",
        "Bars outlive every trial; stack worker arguments and scratch outlive each join. Caller output is written only after successful completion. An early return can expire stack storage while a worker still references it, creating use-after-return.",
        [
            (
                "Does a raw C pointer carry its array length?",
                "No; the interface must supply or otherwise establish it",
                "Yes, malloc attaches a portable length",
                "Only if it points to double",
                "Array extent is part of the API contract, not generally encoded in a pointer.",
            ),
            (
                "Who releases the shared bar allocation in this project?",
                "The owner after all readers have joined",
                "Each worker independently",
                "The fastest worker",
                "Shared borrowed input has one owner, avoiding double-free and premature release.",
            ),
            (
                "A worker keeps a pointer to a returned function's local array. This is:",
                "A lifetime violation even if one run appears correct",
                "Safe because the pointer is const",
                "A valid way to save heap memory",
                "Stack lifetime ends on return; const does not extend the object's lifetime.",
            ),
            (
                "What can a clean sanitizer run establish?",
                "No detected violation on the paths exercised",
                "Proof that every possible execution is safe",
                "A guarantee against all races",
                "Dynamic instrumentation checks executed paths and does not replace ownership reasoning.",
            ),
        ],
        [ASAN, JOIN],
    )
    add(
        "Market data contracts and validation at the boundary",
        "Define field units, availability, missing values, and rejection before computation.",
        "A fast loop over malformed data produces fast mistakes. Specify instrument, currency, price scale, timestamp meaning, timezone, sequence, and whether fields are adjusted. A zero price is not a valid substitute for a missing observation. OHLC consistency and corporate-action policy belong in a real feed adapter; the reference accepts synthetic open and close fields with a narrower contract.\n\nValidate before publishing data to workers. Keep the raw record for diagnosis and attach provenance to a cleaned version. Do not repair a record using future prices in a historical simulation. An eventual CSV importer must bound line lengths, check complete numeric conversion, reject overflow and unexpected trailing fields, and report the row that failed. This project generates deterministic bars; it does not ship that importer.",
        "The closes 100, 102, 0, 101 contain a missing or invalid value under a strictly positive-price contract. Rejecting row 3 is observable. Treating zero as a real crash creates a false signal; filling it with tomorrow's 101 introduces future information.",
        "Find q_backtest's preflight checks and q_generate's seeded path. Extend a local test with zero, negative and above-limit values. Specify a separate ingestion error report rather than allowing a failed trial to masquerade as a successful zero return.",
        r"\mathrm{valid}(p) = (0 < p \le p_{\max})",
        r"""
int main(void) {
    int64_t close[] = {100, 102, 0, 101};
    for (size_t i = 0; i < 4; ++i)
        if (close[i] <= 0) {
            printf("invalid_row=%zu\n", i + 1);
            return 0;
        }
    return 1;
}""",
        "invalid_row=3",
        "Write a schema for a future CSV feed with units, timestamps, sequence, missing-data behavior and error reporting. Explain why silently replacing a zero with the next observation is invalid.",
        "Require positive bounded integer cents, a named instrument, event and receipt time, strictly specified sequence handling and an explicit adjustment convention. Reject or quarantine missing records with their row/source. A future observation was unavailable at the earlier decision time.",
        [
            (
                "How should zero price be handled under this lab's input contract?",
                "Reject it as invalid",
                "Treat it as a free purchase",
                "Replace it with the future close",
                "The contract requires strictly positive bounded prices and makes failure explicit.",
            ),
            (
                "What does a cleaned dataset need for reproducibility?",
                "Source identity and an explicit transformation policy",
                "Only its final average",
                "The fastest parser name",
                "Provenance and transformation rules explain which observations the engine consumed.",
            ),
            (
                "A parser accepts 123xyz as 123 without checking remaining characters. It is:",
                "Accepting malformed numeric input",
                "Performing safe missing-value imputation",
                "Required by integer-cent arithmetic",
                "Successful prefix conversion is not proof that the entire field was a valid number.",
            ),
            (
                "Which ingestion implementation is included in the lab?",
                "A bounded seeded synthetic bar generator",
                "A live exchange WebSocket adapter",
                "A universal CSV repair engine",
                "The shipped generator makes controlled fixtures; real ingestion is an explicit extension.",
            ),
        ],
        [CLANG, LEAKAGE],
    )
    add(
        "Cache locality: arrays of structures and structures of arrays",
        "Relate access patterns to memory traffic before changing data layout.",
        "An array of structures stores each record's fields together; a structure of arrays groups each field contiguously. Neither wins universally. The lab's QBar has open and close because each event uses both. A research kernel that scans only closes may fetch unused fields in a wide record layout. Estimate useful bytes relative to transferred bytes, then measure the actual workload.\n\nCache lines, alignment, prefetching and vector loads influence behavior. sizeof includes implementation padding; field widths do not necessarily add to the structure's total. Avoid claiming a portable cache-line size or forcing packed structs into hot arithmetic. A split layout also has costs: more allocations, more ownership bookkeeping, and potentially more streams for a kernel that needs every field.",
        "Assume a 64-byte cache line and eight-byte closes. A close-only contiguous array can hold eight closes per line. A 32-byte record with one close field uses only one quarter of transferred record bytes for this particular scan. This is a traffic estimate, not a measured fourfold speedup.",
        "Create an alternative close array from the same immutable bars outside the measured kernel. Compare identical sums and include conversion time if conversion belongs to the real use case. Read compiler vectorization remarks before attributing a timing change to the cache alone.",
        r"\text{useful-byte fraction} = \frac{\text{bytes consumed}}{\text{bytes transferred}}",
        r"""
int main(void) {
    struct Bar {
        int64_t open, close;
    };
    struct Bar a[] = {{100, 101}, {102, 103}, {104, 105}};
    int64_t closes[] = {101, 103, 105}, x = 0, y = 0;
    for (size_t i = 0; i < 3; ++i) {
        x += a[i].close;
        y += closes[i];
    }
    printf("equal=%d sum=%" PRId64 "\n", x == y, x);
    return x != y;
}""",
        "equal=1 sum=309",
        "Compare a close-only sum in both layouts, preserving input and arithmetic. Record sizeof the record, theoretical useful-byte fraction and measured time; explain why the fraction does not equal guaranteed speedup.",
        "Both sums must agree before timing. Padding and access patterns determine traffic; caches, loop overhead, vectorization and memory bandwidth also affect execution. Include layout conversion when it is required per run, and report assumptions about cache-line size.",
        [
            (
                "Which access pattern often benefits from a close-only array?",
                "Scanning closes without using other wide-record fields",
                "Always processing every field of one record",
                "Changing event order randomly",
                "Grouping the needed field can reduce unused bytes fetched in a field-oriented scan.",
            ),
            (
                "Why inspect sizeof rather than sum field widths?",
                "Structures may contain padding",
                "C fields have no size",
                "All structures are exactly one cache line",
                "The implementation may insert padding for alignment and structure layout.",
            ),
            (
                "Eight useful bytes in each 32-byte record imply what useful-byte fraction?",
                "25% for that field-only access",
                "A guaranteed 4× speedup",
                "75%",
                "Eight divided by 32 is one quarter; performance still requires measurement.",
            ),
            (
                "When should layout conversion time be included?",
                "When that conversion occurs in the measured real workflow",
                "Never, because it makes results slower",
                "Only in the baseline",
                "Comparison boundaries must charge equivalent work that users actually perform.",
            ),
        ],
        [VECTOR, GCC],
    )
    add(
        "Streaming indicators without repeated window scans",
        "Replace an O(nw) moving-average scan with a bounded O(n) rolling sum.",
        "Recomputing every trailing window repeats almost all additions. Maintain a rolling sum by adding the incoming close and subtracting the observation leaving the window. Keep a clear warmup rule and require the same inequality at the signal boundary. Algorithmic work reduction should precede instruction-level tuning.\n\nFor integer prices, compare close multiplied by window against the sum to avoid division rounding. Prove both products and sums fit before adopting this shortcut. The full reference retains the bar array; a live stream would need a bounded ring of previous closes. A circular index is not by itself a concurrent queue. Validate a scalar full-window implementation against the rolling implementation on equality, rising, falling and short input cases.",
        "With window three and closes 100, 102, 104, 106, the first full sum is 306; the next is 306 + 106 − 100 = 312. The means are 102 and 104. The close strictly exceeds each mean, but the first signal still cannot fill before the next open.",
        "Inspect sum and pending in q_backtest. Write a simple nested-loop oracle, then compare every warmup and signal decision. Benchmark several windows: the naive method scales with both n and w, while the rolling update performs constant work per observation.",
        r"S_t=S_{t-1}+p_t-p_{t-w}, \qquad \mathrm{SMA}_t=S_t/w",
        r"""
int main(void) {
    int64_t p[] = {100, 102, 104, 106}, sum = 0;
    size_t w = 3;
    for (size_t i = 0; i < 4; ++i) {
        sum += p[i];
        if (i >= w)
            sum -= p[i - w];
        if (i + 1 >= w)
            printf("sum=%" PRId64 "\n", sum);
    }
    return 0;
}""",
        "sum=306\nsum=312",
        "Implement an independent nested-loop moving sum and compare it with the project rolling sum for windows 1, 2 and the full dataset. Explain the equality and warmup rules.",
        "Both methods must produce the same full-window sums. Before w observations there is no active signal; equality to the moving average means cash. For window one, close equals its own average, so this strict rule never goes long.",
        [
            (
                "What work does the rolling update remove?",
                "Repeatedly summing the overlapping observations",
                "All validation and execution cost",
                "The need for chronological input",
                "It reuses the prior window sum instead of scanning the overlap again.",
            ),
            (
                "For window one, close > its own SMA produces:",
                "No long signals",
                "A long signal on every bar",
                "Undefined behavior necessarily",
                "With a one-element window, close equals the mean and strict greater-than is false.",
            ),
            (
                "A sum of 500 loses 90 and gains 110. The next sum is:",
                "520",
                "700",
                "480",
                "The rolling recurrence adds the incoming value and subtracts the outgoing value.",
            ),
            (
                "What must be proven before replacing division with close × window?",
                "The product and moving sum fit the numeric type",
                "That division is illegal in C",
                "That all returns are positive",
                "Cross-multiplication preserves the comparison only when arithmetic stays valid.",
            ),
        ],
        [GCC, UBSAN],
    )
    add(
        "Causal event loops and next-open execution",
        "Separate the timestamp when information is observed from the time an order can fill.",
        "A close-based strategy cannot observe the completed close and also buy at an earlier point in that same bar. The reference executes yesterday's pending target at today's open, then consumes today's close to form tomorrow's target. The event loop is sequential because cash, position and pending state depend on the previous event.\n\nSpecify what happens at both ends of the dataset. Warmup accumulates enough information before signaling; the final pending signal has no next bar and remains unfilled. A final position is marked at the final close, not silently liquidated for free. Real execution adds spread, liquidity, partial fills and exchange timing; the reference's complete next-open fills deliberately simplify those mechanisms.",
        "Closes are 100, 120, 80, 80 with window two. The second close creates a long target. It buys at the third open, 130, then sells at the fourth open, 90. With five cents per fill and one share, the round trip loses 50 cents, leaving 999,950 from 1,000,000 cents.",
        "Trace the four-bar fixture in test.c by hand. For each bar record incoming target, open fill, updated cash, moving sum and outgoing target. Change only the third open and confirm the buy price changes while the prior signal does not.",
        r"\mathrm{signal}(C_t) \longrightarrow \mathrm{fill}(O_{t+1})",
        r"""
int main(void) {
    int64_t cash = 1000000, buy_open = 130, sell_open = 90, fee = 5;
    cash -= buy_open + fee;
    cash += sell_open - fee;
    printf("equity=%" PRId64 " fills=2\n", cash);
    return 0;
}""",
        "equity=999950 fills=2",
        "Write the full four-bar event trace and a truncated two-bar trace. State why the truncated test has no fills even though its last close produces a signal.",
        "The full trace buys at 130 and sells at 90 with two five-cent fees. At two bars the signal is only formed on the terminal close; no next open exists, so cash stays 1,000,000 and fills stay zero.",
        [
            (
                "Where does this lab fill a signal formed at close t?",
                "Open t+1",
                "Open t before observing the close",
                "The cheapest future price",
                "Next-open execution respects the information available when the signal was formed.",
            ),
            (
                "How is a final unexecuted signal handled?",
                "It remains unfilled without a next bar",
                "It earns a free closing fill",
                "It is moved backward one bar",
                "The data contains no subsequent execution event for the terminal signal.",
            ),
            (
                "One share buys at 200 and sells at 210 with two 3-cent fees. Net change is:",
                "4 cents",
                "10 cents",
                "7 cents",
                "The ten-cent price gain is reduced by six cents in round-trip fill fees.",
            ),
            (
                "Why not parallelize successive bars of one stateful account naively?",
                "Later account state depends on earlier events",
                "C does not support threads",
                "Parallelism always changes price data",
                "The chronological ledger and pending orders form a dependency chain.",
            ),
        ],
        [LEAKAGE, THREADS],
    )
    add(
        "Profile the workload with monotonic clocks",
        "Define the measurement boundary and distinguish wall time from CPU consumption.",
        "Measure complete work using a clock appropriate to elapsed intervals. A monotonic clock is designed for duration measurement without wall-calendar adjustments. Resolution is not the same as measurement accuracy. Short kernels may need repeated runs so call overhead and scheduling noise do not dominate.\n\nWall time answers how long the caller waits. Summed CPU time can exceed wall time when multiple workers execute simultaneously. In the reference, timing includes per-trial validation, scheduling, thread creation and joins; it excludes synthetic data generation and output formatting. Warmup is explicit. Avoid moving cost outside only one candidate's measurement boundary. Keep profiling and sanitizer builds separate from release benchmarks and explain their different purposes.",
        "A serial run waits 80 milliseconds and a parallel run waits 30 milliseconds while consuming 100 milliseconds of total worker CPU time. Wall-time speedup is 80/30 = 2.67×; CPU consumption increased. Both statements can be true.",
        "Read now() and the paired loop in main.c. Run two input sizes, preserve the output, and report which setup work is included. If a clock call fails, report an error; a fabricated zero interval is not a valid benchmark.",
        r"T_{\mathrm{elapsed}} = t_{\mathrm{finish}}-t_{\mathrm{start}}",
        r"""
int main(void) {
    double wall_serial_ms = 80, wall_parallel_ms = 30, cpu_parallel_ms = 100;
    printf("wall_speedup=%.2f cpu_ms=%.0f\n", wall_serial_ms / wall_parallel_ms,
           cpu_parallel_ms);
    return 0;
}""",
        "wall_speedup=2.67 cpu_ms=100",
        "Measure the project at 2,000 and 200,000 bars with the same compiler flags. State the timed boundary and explain why worker CPU seconds need not equal elapsed seconds.",
        "The timed sweep includes validation and worker setup/join; generation and printing remain outside both paths. Concurrent workers can consume CPU simultaneously, so their summed usage differs from elapsed wall time. Preserve all five repetitions at each size.",
        [
            (
                "Which clock property is useful for elapsed intervals?",
                "Monotonic progression",
                "A human-readable local timezone",
                "Daily wall-clock correction",
                "Duration measurement should avoid discontinuities caused by calendar clock adjustment.",
            ),
            (
                "Can parallel CPU usage exceed elapsed wall time?",
                "Yes, several workers can consume CPU concurrently",
                "No, the values are always identical",
                "Only if the ledger is wrong",
                "Summed CPU usage measures work across workers while wall time measures caller waiting.",
            ),
            (
                "A baseline takes 90 ms and a candidate 45 ms under equal boundaries. Speedup is:",
                "2×",
                "45×",
                "0.5×",
                "Speedup is baseline elapsed time divided by candidate elapsed time.",
            ),
            (
                "Removing parsing only from the candidate's timed region makes the comparison:",
                "Unfair unless the workflow boundary really changed",
                "Automatically more accurate",
                "A proof of compiler quality",
                "Both measured paths must account for equivalent required work.",
            ),
        ],
        [CLOCK, CLANG],
    )
    add(
        "Benchmark distributions, tail latency, and Amdahl's law",
        "Report repeatability and apply parallel speedup limits without hiding overhead.",
        "One timing is an observation, not a performance distribution. Run multiple repetitions, alternate comparison order, and document hardware load and power conditions. Report a central statistic and spread. The middle of five sorted values is a useful descriptive median; five runs do not estimate production p99 latency reliably.\n\nAmdahl's law models a fixed workload with serial fraction f and ideally parallelizable remainder. It gives an upper bound under the model, before scheduling, communication, synchronization and imbalance. If a serial fraction is large, adding cores quickly produces diminishing returns. A throughput batch benchmark cannot be relabeled as an order-response tail-latency measurement; define the measured event and sample population for each metric.",
        "With f = 0.2 and four workers, ideal speedup is 1/(0.2 + 0.8/4) = 2.5×. Even infinitely many workers cannot exceed 5× under this fixed-work model. The observed result may be lower or noisy because overhead is excluded from the simple formula.",
        "Use the performance notebook to capture all five paired timings. Calculate medians outside the hot loop. Increase workers from one to two to four with the same bars and windows, then explain any slowdown using measured work and overhead.",
        r"S(p) \le \frac{1}{f+(1-f)/p}",
        r"""
int main(void) {
    double f = 0.2, p = 4;
    printf("ideal=%.2f limit=%.2f\n", 1.0 / (f + (1 - f) / p), 1.0 / f);
    return 0;
}""",
        "ideal=2.50 limit=5.00",
        "Calculate the modeled speedup for serial fraction 0.25 with four workers and its infinite-worker limit. Compare it with measured project timings without claiming the model predicts exact speed.",
        "The ideal four-worker value is 1/(0.25 + 0.75/4) ≈ 2.286× and the asymptotic limit is 4×. Actual performance includes overhead and a workload-dependent fraction; estimates and measured distributions should be reported separately.",
        [
            (
                "Is a p99 from five benchmark repetitions a stable tail estimate?",
                "No; the sample is far too small for that claim",
                "Yes, because it is C code",
                "Yes, if sorted first",
                "A few observations cannot characterize rare tail events reliably.",
            ),
            (
                "What does the simple Amdahl model omit?",
                "Scheduling and communication overhead",
                "The existence of serial work",
                "The requested worker count",
                "The ideal expression accounts for fractions of work but not actual parallel overheads.",
            ),
            (
                "If the serial fraction is 0.1, the ideal infinite-worker limit is:",
                "10×",
                "100×",
                "Unlimited",
                "The parallel term tends to zero, leaving the reciprocal of the serial fraction.",
            ),
            (
                "Why alternate serial and parallel benchmark order?",
                "To reduce systematic order and warmup bias",
                "To make results non-deterministic",
                "To avoid checking equality",
                "Alternation helps expose order effects, though it does not remove all measurement noise.",
            ),
        ],
        [CLOCK, OMP],
    )
    add(
        "Correctness before speed: fixtures and sanitizers",
        "Use independent expected results and dynamic diagnostics as complementary evidence.",
        "A test that merely calls the same implementation twice checks repeatability, not correctness. Start with small independent fixtures that can be worked by hand, then add properties spanning larger inputs. The four-bar ledger detects execution-timing and fee errors; serial/parallel equality detects scheduling-related changes but cannot prove both engines are financially correct.\n\nAddressSanitizer targets memory errors such as out-of-bounds accesses and use-after-free. UndefinedBehaviorSanitizer instruments selected undefined operations. Thread race detection requires separate tooling and a supported environment; a clean address-sanitized threaded run is not evidence of race freedom. Keep failing programs out of published performance comparisons. Make failure return a nonzero status so automation can observe it.",
        "If both implementations incorrectly buy at the observed close of 120 instead of the next open of 130, they may match each other yet disagree with the independent 999,950-cent expected result. The golden ledger and equality test answer different questions.",
        "Run make test and make sanitize. Add a fixture for exact affordability and one for a rejected fee. Classify each test by the defect it can expose. Record sanitizer tool and platform, and avoid saying that untested execution paths are covered.",
        r"\text{evidence} = \text{independent oracle} + \text{invariants} + \text{diagnostics}",
        r"""
int main(void) {
    int64_t expected = 999950, actual = 1000000 - 130 - 5 + 90 - 5;
    if (actual != expected) {
        fputs("FAIL\n", stderr);
        return 1;
    }
    puts("golden ledger PASS");
    return 0;
}""",
        "golden ledger PASS",
        "List one test each for causality, arithmetic limits, ownership, and scheduling. Describe a bug that serial/parallel equality alone would miss.",
        "Use the hand-derived next-open ledger, an extreme rejected target, sanitizer-exercised lifetime paths, and equality across worker counts. A shared same-close fill bug can affect both implementations identically; only an independent causal expectation exposes it.",
        [
            (
                "What does equality between two implementations fail to prove by itself?",
                "That their shared financial model is correct",
                "That their outputs matched on this input",
                "That comparison code ran",
                "Two implementations can share the same mistaken assumptions or bugs.",
            ),
            (
                "Which tool is aimed at many invalid memory accesses?",
                "AddressSanitizer",
                "A profit chart",
                "The parameter sorter",
                "AddressSanitizer instruments memory access and lifetime checks on executed paths.",
            ),
            (
                "A hand-calculated result is 500 but both optimized paths report 505. What should happen?",
                "Investigate before accepting a speedup",
                "Accept because both paths agree",
                "Remove the golden test",
                "Agreement does not override an independent expected result without explaining the discrepancy.",
            ),
            (
                "Does an address-sanitized run prove the absence of data races?",
                "No; race detection is a separate concern",
                "Yes, all sanitizers detect all races",
                "Only when compiled at -O2",
                "Memory-access sanitization does not replace synchronization reasoning or race-specific tooling.",
            ),
        ],
        [ASAN, UBSAN, JOIN],
    )
    add(
        "Optimization experiments and compiler evidence",
        "Change one measured bottleneck while preserving contracts and comparison fairness.",
        "After establishing a baseline, form a narrow hypothesis. For example, repeated validation may dominate small trials; moving it to a trusted immutable-dataset boundary could reduce repeated work. That change also moves a safety obligation. A private validated engine function should not become an unchecked public entry point accidentally.\n\nInspect generated-code or vectorization reports when they help explain behavior. A higher optimization level is a compiler request, not a speed guarantee. Aggressive floating-point options can change permitted transformations, infinities, NaNs and rounding assumptions. Do not enable them merely because they sound faster. Keep exact ledger arithmetic and statistical tolerance contracts explicit, and compare against the scalar oracle after every experiment.",
        "A candidate improves five measurements but changes the equality signal rule from > to >=. Its economic behavior changed, so the timings do not establish an equivalent implementation speedup. Preserve the boundary case and rerun the experiment with matching semantics.",
        "Choose one local branch: hoist validated-data checks, change layout, or alter scheduling. Record the change, expected effect, compiler evidence and correctness results. Revert an unsupported optimization hypothesis rather than stacking more changes on it.",
        r"\Delta T=T_{\mathrm{candidate}}-T_{\mathrm{baseline}}",
        r"""
int main(void) {
    double baseline[] = {10, 11, 9, 12, 10}, candidate[] = {8, 9, 8, 10, 9}, a = 0,
           b = 0;
    for (size_t i = 0; i < 5; ++i) {
        a += baseline[i];
        b += candidate[i];
    }
    printf("mean_delta=%.2f ms\n", (b - a) / 5);
    return 0;
}""",
        "mean_delta=-1.60 ms",
        "Propose one optimization, its new validation boundary, an independent correctness check, and a fair measurement plan. Do not submit a faster result with a changed signal rule.",
        "For hoisted validation, accept only an already-validated immutable dataset internally while retaining checks at the public boundary. Preserve every signal and fill against the oracle, including equality and warmup cases. Measure equivalent required work with identical build settings.",
        [
            (
                "What should justify a local optimization?",
                "A measured bottleneck and testable hypothesis",
                "Its longer compiler flag list",
                "A promise that C is always faster",
                "Measurement directs effort and a narrow hypothesis makes the effect interpretable.",
            ),
            (
                "Changing > to >= while timing a rewrite changes:",
                "The strategy contract at equality",
                "Only a cosmetic symbol",
                "Nothing on any dataset",
                "Equality observations generate different targets under the two comparisons.",
            ),
            (
                "Hoisting validation is sound only if:",
                "The downstream engine receives immutable validated data under an enforced contract",
                "All checks disappear everywhere",
                "Worker count is greater than one",
                "Moving a check must preserve its obligation at a reliable boundary.",
            ),
            (
                "What must accompany aggressive floating-point optimization?",
                "An explicit numerical contract and validation of changed assumptions",
                "A claim of exact decimal arithmetic",
                "Removal of reference results",
                "Compiler transformations may alter rounding and exceptional-value behavior.",
            ),
        ],
        [GCC, VECTOR],
    )
    add(
        "POSIX threads for independent parameter research",
        "Partition independent trials and keep the market event loop chronological.",
        "A parameter sweep offers a useful unit of parallel work: each trial reads the same market history but owns its account, moving sum and result. Assign disjoint result slots to workers. Do not parallelize bars of one stateful ledger without an algorithm that accounts for the dependencies.\n\nThe lab uses a bounded number of POSIX threads with static strided assignment. Worker k processes k, k+p, k+2p and so on. The one-worker path executes directly, avoiding thread creation overhead. If the caller requests more workers than jobs, cap the active workers to the job count. Static assignment is simple and reproducible, but varied job costs can cause imbalance. Dynamic scheduling is an optional measured extension.",
        "Seven trials assigned across three workers produce index sets {0,3,6}, {1,4}, and {2,5}. Each output index has one writer. The final report still follows parameter index, independent of the order workers finish.",
        "Read Worker and work() in parallel.c. Draw the assignment for seven windows and four workers. Run the equality tests for 1–32 requested workers, noting that requests above seven activate at most seven workers in that fixture.",
        r"\mathrm{jobs}(k)=\{k+mp:m\ge0,\ k+mp<J\}",
        r"""
int main(void) {
    size_t jobs = 7, workers = 3;
    for (size_t k = 0; k < workers; ++k) {
        printf("worker%zu:", k);
        for (size_t j = k; j < jobs; j += workers)
            printf(" %zu", j);
        puts("");
    }
    return 0;
}""",
        "worker0: 0 3 6\nworker1: 1 4\nworker2: 2 5",
        "Trace job ownership for seven windows and four workers, then explain which state is shared and which is private. Measure small and large workloads before choosing a worker count.",
        "Workers own {0,4}, {1,5}, {2,6}, {3}. Bars and window definitions are borrowed read-only; each backtest owns its ledger and each output index has one writer. Thread setup may dominate small inputs, so use measured workload sizes.",
        [
            (
                "Which object should be private to each parameter trial?",
                "Its account and rolling state",
                "A shared mutable cash balance",
                "The global output print stream",
                "Independent trials need isolated path-dependent state even when they share input data.",
            ),
            (
                "With three workers, who owns job index 5 under striding?",
                "Worker 2",
                "Worker 0",
                "Every worker",
                "Index 5 is congruent to 2 modulo 3 and belongs to that worker's stride.",
            ),
            (
                "Ten requested workers and three jobs should activate at most:",
                "Three workers in this lab",
                "Ten required busy loops",
                "Zero workers",
                "Capping active workers avoids creating workers with no assigned trials.",
            ),
            (
                "Why can static assignment be imbalanced?",
                "Some trials may take longer than others",
                "Its indices overlap by definition",
                "It forces shared account state",
                "Equal job counts do not imply equal execution cost per worker.",
            ),
        ],
        [THREADS, JOIN],
    )
    add(
        "Data races, publication, and synchronization",
        "Explain happens-before relationships and publish results only after successful joins.",
        "A data race arises when unsynchronized conflicting accesses occur across threads, with at least one writer. Disjoint result elements avoid shared writes, but consumers must still wait until workers finish before reading their output. Volatile does not provide thread synchronization or make compound operations atomic.\n\nThe lab's join boundary establishes completion before publication. Worker arguments live until their joins, and scratch output stays private to the orchestration call. If thread creation fails partway, join all already-created workers before returning failure. A join failure is treated as a fatal lifetime invariant violation: returning normally could expose expired stack storage to a still-running worker. This is a deliberate narrow reference policy, not a universal production recovery strategy.",
        "Two workers each execute counter = counter + 1 on a shared ordinary integer. Both may read zero and write one, losing an update; in C the unsynchronized conflict is a data race, so reasoning only about that interleaving is insufficient. Use private counters and combine after joins, or a correct atomic operation.",
        "Trace all returns in q_sweep. Confirm none returns while successfully created workers can still reference stack arguments. Do not infer race freedom from one correct benchmark; use the ownership design, join contract and suitable race diagnostics on supported systems.",
        r"\mathrm{worker\ completion}\ \prec\ \mathrm{join}\ \prec\ \mathrm{publish}",
        r"""
int main(void) {
    size_t private_counts[] = {4, 3, 3},
           total = 0; /* Combine only after worker completion in a threaded program. */
    for (size_t i = 0; i < 3; ++i)
        total += private_counts[i];
    printf("total=%zu\n", total);
    return 0;
}""",
        "total=10",
        "Explain why volatile is not a fix for a shared increment. Audit the thread-creation failure path and describe when caller output becomes visible.",
        "Volatile does not make a read-modify-write atomic or establish cross-thread synchronization. The lab joins all created workers, validates scratch results, then copies them to caller output. A failed creation publishes nothing and returns only after existing workers join.",
        [
            (
                "Does volatile make counter++ safe across threads?",
                "No; it does not provide the required atomicity or synchronization",
                "Yes, on every C compiler",
                "Only when counter starts at zero",
                "Volatile access semantics do not create a synchronization protocol for shared updates.",
            ),
            (
                "When may the caller consume worker results here?",
                "After successful joins and result validation",
                "As soon as the first worker starts",
                "When a progress message prints",
                "The join and validation boundary ensures finished, accepted data is published.",
            ),
            (
                "The third pthread_create fails after two successes. What must happen before returning?",
                "Join the two created workers",
                "Free their argument storage immediately",
                "Pretend every result succeeded",
                "Created workers may still use the function's storage and must finish before it expires.",
            ),
            (
                "Disjoint output writers remove which conflict?",
                "Concurrent writes to the same result slot",
                "Every possible lifetime bug",
                "All need to join",
                "One writer per slot avoids that race but does not replace lifetime and completion rules.",
            ),
        ],
        [JOIN, ATOMICS],
    )
    add(
        "Deterministic seeds, reductions, and experiment identity",
        "Make parallel completion order irrelevant to the research report.",
        "Reproducibility starts with a stable experiment identity: source version, data identity, parameter values, cost model and seed. The lab generates the complete bar array once from a local unsigned-state generator. Each trial reads the identical path, so worker scheduling does not advance a shared random number generator.\n\nStore results by parameter index and report them in that order. Do not use worker completion order as an implicit ranking. Floating-point reductions can vary when addition order changes; define a fixed order or an approved tolerance where exact arithmetic is inappropriate. The integer ledger permits exact equality here. Avoid comparing raw structure bytes because padding can differ even when all meaningful fields match.",
        "Three jobs complete in order 2, 0, 1. Their report still lists 0, 1, 2 by stable index. If equal scores need a winner, declare a tie rule such as the smaller parameter index, then apply it consistently after completion.",
        "Inspect q_equal's field-by-field comparison and q_generate's local seed. Save all output rows from one- and four-worker runs. For stochastic extensions, derive separate stable streams from experiment identity, not thread number or wall-clock time.",
        r"\mathrm{result}[j] = f(\mathrm{data},\theta_j,\mathrm{seed}_j)",
        r"""
int main(void) {
    size_t completion[] = {2, 0, 1};
    int scores[3] = {0};
    for (size_t i = 0; i < 3; ++i) {
        size_t j = completion[i];
        scores[j] = (int)(100 + j);
    }
    for (size_t j = 0; j < 3; ++j)
        printf("job%zu=%d\n", j, scores[j]);
    return 0;
}""",
        "job0=100\njob1=101\njob2=102",
        "Create a reproduction manifest and explain why thread-number seeds change results when worker count changes. Define an explicit tie-breaking policy for equal trial scores.",
        "Record data, source, seed, parameters, costs, compiler and flags. Thread assignments change with worker count, so thread-derived random streams can change a trial's data. Key randomness and ties to stable experiment identifiers; keep presentation order independent of completion order.",
        [
            (
                "What should determine a stochastic trial's random stream?",
                "A stable experiment identity",
                "Whichever thread finishes first",
                "The current wall-clock second",
                "Stable experiment-based streams preserve identity across scheduling and worker counts.",
            ),
            (
                "Why does q_equal compare fields rather than raw struct bytes?",
                "Padding bytes are not meaningful result fields",
                "C cannot compare integers",
                "It changes the model's fees",
                "Object padding can differ while every semantically relevant field is equal.",
            ),
            (
                "Jobs finish 3, 1, 2, 0. A deterministic indexed report lists:",
                "0, 1, 2, 3",
                "3, 1, 2, 0 necessarily",
                "Only the fastest job",
                "Stable index ordering decouples the report from runtime scheduling.",
            ),
            (
                "Why may floating-point parallel sums vary?",
                "Changing addition order can change rounding",
                "All parallel arithmetic is invalid",
                "Integers and floats share identical rounding",
                "Finite precision means addition is not generally associative for floating-point values.",
            ),
        ],
        [THREADS, GCC],
    )
    add(
        "OpenMP scheduling and scaling experiments",
        "Translate independent-trial parallelism into an OpenMP design with explicit data sharing.",
        "OpenMP offers directives and runtime support for shared-memory parallelism in C and other supported languages. A parallel-for construct can schedule independent parameter trials, but the directive does not repair shared account state or invalid iteration dependencies. Identify read-only arrays, private temporary state and each iteration's unique output location before adding a directive.\n\nStatic scheduling has low overhead and predictable assignment; dynamic scheduling may balance varied task costs at additional runtime cost. The best choice depends on job granularity and workload variation. Compiler support and runtime installation vary. The downloadable reference uses POSIX threads, so learners can complete the course without an OpenMP installation; porting the sweep is an extension with its own build and measurement evidence.",
        "Jobs costing 10, 1, 1 and 10 milliseconds can be poorly balanced by some static partitions. A dynamic scheduler may improve balance but cannot make 22 milliseconds of work disappear. For tiny jobs, scheduling overhead may overwhelm any benefit.",
        "Read the OpenMP specification sections on data sharing and worksharing loops. Sketch a parallel-for over job indices with the ledger allocated inside each trial. If your toolchain supports it, compile an optional port and compare every output field and timed boundary with the POSIX implementation.",
        r"T_{\mathrm{parallel}}\ge\max_k\sum_{j\in\mathrm{worker}(k)}T_j",
        r"""
int main(void) {
    int costs[] = {10, 1, 1, 10};
    int a = costs[0] + costs[1], b = costs[2] + costs[3];
    printf("balanced_partition_ms=%d\n", a > b ? a : b);
    return 0;
}""",
        "balanced_partition_ms=11",
        "Design an OpenMP sweep showing shared inputs, per-trial private state and indexed outputs. Describe a workload where dynamic scheduling may help and one where its overhead may hurt.",
        "Share only immutable bars and parameters; create each account inside its iteration and write one distinct output slot. Uneven expensive jobs can benefit from dynamic balancing; many tiny equal jobs can favor low-overhead static assignment. The optional port needs runtime support and fresh equality checks.",
        [
            (
                "Does a parallel-for directive fix dependencies between successive account events?",
                "No; dependencies still require a valid algorithm",
                "Yes, the compiler invents missing prices",
                "Only when using four threads",
                "Parallel directives require valid independent work or a correctly expressed dependency model.",
            ),
            (
                "What is a potential advantage of dynamic scheduling?",
                "Balancing trials with uneven runtime",
                "Eliminating every scheduling cost",
                "Changing the seed to favor profits",
                "Dynamic assignment can reduce imbalance, at the cost of additional runtime coordination.",
            ),
            (
                "Two workers each receive 12 ms of work; ignoring overhead, the time lower bound is:",
                "12 ms",
                "24 ms",
                "6 ms",
                "Completion cannot precede the slowest worker's assigned work in this model.",
            ),
            (
                "Is OpenMP required to build the provided reference project?",
                "No; the reference uses POSIX threads",
                "Yes, alongside CUDA",
                "Yes, for every standalone worksheet",
                "OpenMP is a course extension; the shipped CPU implementation uses pthreads.",
            ),
        ],
        [OMP, CLANG],
    )
    add(
        "SIMD and vectorization without changing numerical meaning",
        "Identify independent lanes and inspect compiler decisions instead of assuming vector speed.",
        "SIMD applies one operation to multiple data lanes. Contiguous, independent arithmetic often presents a better vectorization opportunity than a loop with stateful branches and cross-iteration dependencies. The lab's event engine includes ledger transitions, so a more promising first experiment is a pure feature kernel over an array.\n\nAliasing, alignment, loop bounds and reductions affect what transformations the compiler can prove safe. A restrict-qualified pointer makes a promise about access relationships; violating it can invalidate the program. Do not add it to silence a missed-optimization remark without proving the contract. Keep a scalar reference and check short lengths, non-multiple tails, extreme values and numerical tolerances. A vectorization report explains a transformation; timing establishes whether it helped.",
        "Processing ten values with a conceptual four-lane vector requires two full groups and a two-value tail. Ignoring the tail loses data; reading a full third vector without valid storage can go out of bounds. Actual compiler-generated tail handling depends on target and optimization choices.",
        "Use Clang loop-vectorization remarks or GCC optimization reports for a standalone feature loop. Compare fixed build targets and avoid treating -march=native output as portable to every machine. The worksheet illustrates exact lane-independent arithmetic, not a guaranteed vector instruction sequence.",
        r"n = L\left\lfloor n/L\right\rfloor + (n\bmod L)",
        r"""
int main(void) {
    int64_t p[] = {100, 102, 105, 104, 108};
    int64_t delta[4];
    for (size_t i = 0; i < 4; ++i)
        delta[i] = p[i + 1] - p[i];
    printf("deltas=%" PRId64 ",%" PRId64 ",%" PRId64 ",%" PRId64 "\n", delta[0],
           delta[1], delta[2], delta[3]);
    return 0;
}""",
        "deltas=2,3,-1,4",
        "Identify a pure feature kernel, inspect its vectorization report, and test lengths 1, 3, 4 and 5. Explain what would make adding restrict invalid.",
        "Independent deltas or transforms are candidates, provided bounds are correct. Test short and tail lengths against the scalar oracle. restrict is invalid when actual accesses violate its non-aliasing promise; it must describe an established contract, not an optimization wish.",
        [
            (
                "Which loop is a more direct SIMD candidate?",
                "Independent transforms over contiguous values",
                "A ledger whose cash depends on the previous fill",
                "A loop waiting for network acknowledgments",
                "Independent regular arithmetic exposes lane-level work without account-state dependencies.",
            ),
            (
                "Ten values with four conceptual lanes leave a tail of:",
                "Two values",
                "Four values",
                "Zero values",
                "Ten contains two full groups of four and two remaining elements.",
            ),
            (
                "What does restrict communicate?",
                "A pointer-access contract the program must satisfy",
                "A runtime bounds check",
                "A guarantee of faster execution",
                "The qualifier permits assumptions only when actual aliasing behavior obeys its rules.",
            ),
            (
                "Does a vectorization remark prove an end-to-end speedup?",
                "No; measure the actual workload too",
                "Yes, regardless of memory cost",
                "Only if results are hidden",
                "Generated vector operations may not improve a workload limited by other costs.",
            ),
        ],
        [VECTOR, GCC],
    )
    add(
        "GPU batching, transfer cost, and the roofline model",
        "Decide when an accelerator experiment is plausible and account for the full data path.",
        "GPU research works best when enough regular parallel work amortizes transfers, launch overhead and synchronization. Small sequential account decisions can be poor accelerator candidates. An initial experiment might batch independent scenarios or compute dense features, while a causal ledger remains on the CPU. Porting a loop requires a data layout, memory lifetime and synchronization design, not merely a device label.\n\nArithmetic intensity is useful operations per byte moved at a stated memory boundary. A roofline estimate bounds achievable rate by the smaller of peak compute and bandwidth times intensity. It is an explanatory model, not a measured guarantee. Host-device transfers and kernel launch overhead are separate costs in the end-to-end workflow. The reference project has no GPU kernel or GPU requirement.",
        "A CPU task takes 8 ms. A proposed GPU path spends 3 ms transferring in, 1 ms computing and 3 ms transferring out, totaling 7 ms before other overhead. Its kernel is 8× faster than the entire CPU task numerically, but end-to-end speedup is only about 1.14× under these assumptions.",
        "Read the CUDA best-practices discussion of transfer minimization and batching. Create a cost model for one batch and for ten reused batches. Label assumed versus measured numbers and identify data that could remain resident without violating freshness or ownership.",
        r"P\le\min(P_{\mathrm{peak}}, B\cdot I),\qquad T=T_{\mathrm{in}}+T_{\mathrm{kernel}}+T_{\mathrm{out}}",
        r"""
int main(void) {
    double cpu = 8, in = 3, kernel = 1, out = 3;
    printf("gpu_total=%.1f speedup=%.2f\n", in + kernel + out,
           cpu / (in + kernel + out));
    return 0;
}""",
        "gpu_total=7.0 speedup=1.14",
        "Build an accelerator cost table including transfers, launch/synchronization and kernel work. Explain which measured workload would justify implementing a GPU extension.",
        "Count all required costs at the user-visible boundary. Favor large regular batches with reusable device-resident data only when freshness permits. Demonstrate equality or justified tolerance against the CPU oracle. The table is a hypothesis until hardware measurements exist.",
        [
            (
                "What often makes a small GPU task slower end to end?",
                "Transfer and launch overhead relative to useful work",
                "The existence of parallel lanes",
                "Integer prices alone",
                "Fixed overhead can outweigh acceleration of a small amount of computation.",
            ),
            (
                "What two ceilings appear in the simple roofline bound?",
                "Peak compute and bandwidth times arithmetic intensity",
                "Profit and cash balance",
                "Compiler version and account name",
                "The model relates compute capacity to data-movement capacity at a chosen boundary.",
            ),
            (
                "A CPU takes 12 ms; GPU transfer, compute and return take 4, 2 and 4 ms. Modeled speedup is:",
                "1.2×",
                "6× end to end",
                "3×",
                "The full GPU path takes ten milliseconds, so twelve divided by ten is 1.2.",
            ),
            (
                "What GPU implementation ships with the lab?",
                "None; accelerator work is an optional design extension",
                "A tested CUDA exchange gateway",
                "A mandatory multi-GPU cluster",
                "The executable reference is CPU C/POSIX; the lesson teaches how to assess an extension.",
            ),
        ],
        [CUDA, VECTOR],
    )
    add(
        "Distributed research manifests and deterministic collection",
        "Design process and machine boundaries around reproducible independent jobs.",
        "A cluster adds partial failures, message passing, data distribution and inconsistent environments. Start with an immutable job manifest: dataset identity, strategy source, parameters, cost assumptions, seed and expected output schema. A stable job identifier lets retries be collected once without confusing a duplicate result with a new experiment.\n\nMPI provides process communication primitives, but a communication library does not determine your research protocol. Decide how workers receive data, how errors are reported, and how the collector verifies completeness. Do not partition time segments of a stateful account without transporting the correct warmup and account state. Independent trials are the simpler unit. The course reference is single-machine; a distributed implementation is an architectural extension.",
        "A manifest has jobs 0, 1, 2 and 3. Results arrive 2, 0, 2, 3. The duplicate 2 should not inflate completed work: job 1 is still missing. A collector may retry job 1 under the same identity and publish a complete report only after validating every expected result.",
        "Write a four-job manifest and simulate duplicates, missing results and a mismatched data hash. Define idempotent collection and a deterministic final ordering. Include data transfer and worker startup when estimating whether a cluster beats a local batch.",
        r"\mathrm{complete}\iff\mathrm{accepted\ job\ IDs}=\mathrm{manifest\ job\ IDs}",
        r"""
int main(void) {
    size_t arrived[] = {2, 0, 2, 3};
    int seen[4] = {0};
    for (size_t i = 0; i < 4; ++i)
        seen[arrived[i]] = 1;
    for (size_t j = 0; j < 4; ++j)
        if (!seen[j])
            printf("missing_job=%zu\n", j);
    return 0;
}""",
        "missing_job=1",
        "Design a manifest and collector contract for eight independent trials. Specify duplicate, timeout, wrong-source and incomplete-report behavior without claiming a cluster is implemented.",
        "Each job carries stable data/source/parameter/seed identity. The collector accepts one valid result per expected identity, rejects mismatched provenance, retries missing work under the same identity, and publishes only a complete validated set in stable order.",
        [
            (
                "What is a straightforward unit for distributing this research?",
                "An independent full-history parameter trial",
                "An arbitrary bar from one shared cash ledger",
                "A mutable global RNG update",
                "Independent trials isolate state and avoid splitting the sequential account dependency chain.",
            ),
            (
                "Receiving the same valid job twice should usually:",
                "Count as one completed manifest item",
                "Double the reported sample size",
                "Delete every other result",
                "Idempotent collection prevents retries from inflating the completed research set.",
            ),
            (
                "Manifest {0,1,2} receives {0,2,2}. Which job is missing?",
                "1",
                "2",
                "None",
                "Duplicate job 2 does not substitute for the absent job 1.",
            ),
            (
                "What should happen to a result with a different dataset identity?",
                "Reject or quarantine it before aggregation",
                "Average it into the report silently",
                "Rename its strategy and accept it",
                "Provenance mismatches violate the declared experiment and must remain observable.",
            ),
        ],
        [MPI, THREADS],
    )
    add(
        "Bounded queues, backpressure, and memory ordering",
        "Define overload behavior before designing a concurrent market-data queue.",
        "A bounded queue makes resource limits explicit. When arrival rate exceeds service rate, the backlog grows until capacity is exhausted. Specify whether the producer blocks, drops a permitted class of message, sheds a subscription, or stops new risk. Silently overwriting an order or an unreconciled fill is not an acceptable generic policy. Different event types require different handling.\n\nA ring buffer needs a full/empty convention and ownership of each index. A concurrent single-producer/single-consumer design additionally needs correct memory ordering around payload publication and consumption. Acquire/release operations can establish required ordering when applied in a valid protocol; sprinkling atomics on indices is not a proof. The reference sweep does not require a queue, and this worksheet is deliberately single-threaded.",
        "A four-slot ring that reserves one slot to distinguish full from empty can hold three items. The fourth push must be rejected or handled through an explicit overload policy. At 1,200 arrivals and 1,000 departures per second, backlog grows by 200 items per second while these rates persist.",
        "Write the full/empty rule, then test wraparound and saturation sequentially. For a future concurrent queue, document who writes each field and the publication ordering before implementing it. Prefer a simpler synchronized design when you cannot justify the lock-free protocol.",
        r"\Delta Q/\Delta t = \lambda-\mu\quad\text{while backlog grows}",
        r"""
int main(void) {
    size_t capacity = 4, head = 0, tail = 0, accepted = 0;
    for (size_t i = 0; i < 4; ++i) {
        size_t next = (head + 1) % capacity;
        if (next == tail)
            break;
        head = next;
        ++accepted;
    }
    printf("accepted=%zu full=%d\n", accepted, (head + 1) % capacity == tail);
    return 0;
}""",
        "accepted=3 full=1",
        "Design distinct overload policies for replaceable quote updates and execution fills. Test a reserved-slot ring's empty, full and wraparound cases, and state why that does not validate concurrent memory ordering.",
        "Quote coalescing may be acceptable under a declared model, while fills require lossless handling or a stop-and-reconcile failure path. A four-slot reserved-slot ring holds three items. Sequential tests validate indexing only; synchronization and payload publication need separate concurrent reasoning and testing.",
        [
            (
                "How many items fit in a four-slot ring reserving one slot?",
                "Three",
                "Four",
                "Five",
                "One unused slot disambiguates full and empty under this convention.",
            ),
            (
                "Which event should not be silently overwritten as generic queue policy?",
                "An unreconciled execution fill",
                "A documented replaceable quote snapshot",
                "A decorative progress count",
                "Losing fills breaks account reconstruction and requires explicit recovery rather than silent loss.",
            ),
            (
                "Arrivals are 900/s and service is 700/s. Backlog growth while overloaded is:",
                "200 items/s",
                "1,600 items/s",
                "No growth",
                "The difference between arrival and service rates accumulates as backlog.",
            ),
            (
                "Do correct sequential ring indices prove a lock-free queue safe?",
                "No; synchronization and publication also need proof",
                "Yes, modulo arithmetic provides memory ordering",
                "Only when capacity is a power of two",
                "Concurrent correctness additionally depends on ownership, ordering and object lifetimes.",
            ),
        ],
        [ATOMICS, OMP],
    )
    add(
        "Pre-trade risk and atomic account transitions",
        "Validate an entire proposed fill before committing cash and position changes.",
        "Risk checks must happen before the operation they constrain. Validate input range, position limit, notional, funds and fee affordability before mutating the account. Either the complete accepted transition is applied, or the original account remains intact. Incrementally changing cash before a later rejection can leave a corrupted ledger.\n\nThe reference's q_target enforces long-only bounds, available cash and a cash ceiling. A repeated already-achieved target is a no-op and incurs no second fee. This target-level behavior is useful for the teaching engine; it is not durable broker idempotency. A real gateway needs stable intent identifiers, persisted acknowledgments, reconciliation and handling for partial fills and uncertain responses. Do not confuse a function returning failure with a real exchange guaranteeing no order exists.",
        "Cash is 100 cents and the requested one share costs 100 cents plus a five-cent fee. The order must be rejected before mutation. A check that only tests notional affordability accepts an economically impossible fill or drives cash negative.",
        "Read q_target and test exact affordability, fee rejection, repeated target and invalid extreme input. Add proposed maximum notional and kill-switch checks in a local extension, keeping the original account unchanged after any rejected transition.",
        r"\mathrm{accept\ buy}\iff N\le C\ \land\ F\le C-N",
        r"""
int main(void) {
    int64_t cash = 100, notional = 100, fee = 5;
    int accept = notional <= cash && fee <= cash - notional;
    if (accept)
        cash -= notional + fee;
    printf("accepted=%d cash=%" PRId64 "\n", accept, cash);
    return 0;
}""",
        "accepted=0 cash=100",
        "Add a fee-only affordability rejection test and inspect cash and shares afterward. Explain how target-position no-op behavior differs from durable order idempotency after a network timeout.",
        "An unaffordable fee rejects the entire proposal with the original account intact. A target no-op observes current local shares; after a gateway timeout, local state may be stale. Durable intent identity and reconciliation are needed before deciding whether to submit another real order.",
        [
            (
                "An order affordable before fees but unaffordable after fees should:",
                "Be rejected without account mutation",
                "Borrow the fee silently",
                "Debit cash before returning failure",
                "Affordability includes the complete accepted transition, including its fee.",
            ),
            (
                "Repeating the same already-filled target in q_target incurs:",
                "No additional fill fee",
                "A fee on every call",
                "An automatic short sale",
                "The unchanged target is a no-op in this local target-position model.",
            ),
            (
                "With 210 cents cash, two 100-cent shares and a 5-cent fill fee leave:",
                "5 cents",
                "10 cents",
                "0 cents",
                "The one fill costs 200 cents notional plus one five-cent fee.",
            ),
            (
                "Does a local target no-op guarantee broker idempotency after restart?",
                "No; durable intent state and reconciliation are separate",
                "Yes, all remote orders become atomic",
                "Yes, if prices use cents",
                "The lab's local ledger is not a persisted network-order acknowledgment system.",
            ),
        ],
        [UBSAN, CLANG],
    )
    add(
        "Replay, order state machines, and recovery design",
        "Separate an intended order from acknowledgments, fills, cancellations, and recovered state.",
        "A live execution adapter must represent uncertainty. An intent can be submitted, acknowledged, partially filled, filled, canceled or rejected; a timeout alone may leave its outcome unknown. Reconcile with authoritative order and fill records before retrying an uncertain action. A cancellation request is not proof that no further fill occurred.\n\nRecord events with stable identifiers, sequence and enough context to reconstruct state. Deterministic replay should apply each accepted event exactly once under a declared ordering rule. Duplicated messages, sequence gaps and out-of-order arrivals need explicit policies. A target-based backtest omits this complexity, so its transition function should remain separate from any future gateway state machine. The downloadable project has no network gateway or persisted order log.",
        "An order for ten shares reports fills of three and then four shares. Filled quantity is seven and remaining quantity is three. Replaying the same four-share fill twice without duplicate detection incorrectly reports eleven, exceeding the original order.",
        "Design a paper-only order state machine and a replay table containing a duplicate fill, a timeout and a cancel/fill race. Define which source resolves unknown state and when new exposure must pause. Keep the event log separate from derived account snapshots.",
        r"q_{\mathrm{remaining}}=q_{\mathrm{ordered}}-\sum_{\mathrm{unique\ fills}}q_i",
        r"""
int main(void) {
    size_t ids[] = {11, 12, 12};
    int qty[] = {3, 4, 4}, filled = 0;
    for (size_t i = 0; i < 3; ++i) {
        int duplicate = 0;
        for (size_t j = 0; j < i; ++j)
            if (ids[j] == ids[i])
                duplicate = 1;
        if (!duplicate)
            filled += qty[i];
    }
    printf("filled=%d remaining=%d\n", filled, 10 - filled);
    return 0;
}""",
        "filled=7 remaining=3",
        "Write a paper order replay with partial fills, a duplicate and a cancel request followed by a fill. Explain the evidence needed before retrying a timed-out submission.",
        "Apply unique fill identifiers once, maintain ordered and remaining quantities, and treat cancel as pending until confirmed. A late fill can still change exposure. Query/reconcile authoritative broker state under the original intent identifier before deciding whether a retry is appropriate.",
        [
            (
                "A submission timeout necessarily means:",
                "Its outcome may be unknown",
                "The exchange rejected it",
                "It is safe to duplicate the order",
                "Loss of a response does not establish whether the remote system accepted the request.",
            ),
            (
                "A cancel request guarantees what immediately?",
                "Only that cancellation was requested",
                "That no later fill can arrive",
                "That all shares are sold",
                "Cancellation must be acknowledged and reconciled with any concurrent execution.",
            ),
            (
                "An order for 12 has unique fills of 2 and 5; the second message is duplicated. Remaining is:",
                "5 shares",
                "0 shares",
                "10 shares",
                "Count unique fills once: twelve minus seven leaves five shares.",
            ),
            (
                "Which source should resolve uncertain remote order state?",
                "Authoritative order and fill records under stable identifiers",
                "The local progress animation",
                "A fresh random client order ID",
                "Recovery needs evidence of the original intent's outcome, not a new untracked request.",
            ),
        ],
        [MPI, JOIN],
    )
    add(
        "Operational budgets, stale data, and research discipline",
        "Connect systems measurements to a paper deployment plan and independent strategy evaluation.",
        "A useful operational budget includes data age, queue waiting, computation, risk checks and outbound delay. Fast calculation cannot compensate for stale inputs. Define maximum accepted age using timestamps whose clock domains and units are understood. When clocks are not synchronized, a naive subtraction can misstate freshness; use appropriate receipt-time or synchronization policy.\n\nSet observable limits and failure actions: pause new exposure, retain diagnostics and reconcile existing state. Track rejected orders, stale events, queue saturation and latency distributions. Separate these health metrics from strategy evaluation. Parallel sweeps make it easier to try many variants, increasing selection pressure. Fix chronological train/validation/test rules and transaction-cost assumptions before choosing a winner; synthetic speed benchmarks provide no evidence of expected returns.",
        "A received quote is 250 ms old against a 100 ms freshness limit. Even a 5-microsecond signal calculation should not open new risk under that policy. In a separate research example, selecting the best of thousands of windows on the test period consumes the test set.",
        "Write a paper deployment readiness table: freshness limit, queue capacity, numeric limits, stop conditions, reconciliation and telemetry. Attach a separate evaluation protocol with holdout dates and selection rules. Label the lab's missing spread, impact and real fill uncertainty.",
        r"T_{\mathrm{response}}=T_{\mathrm{queue}}+T_{\mathrm{compute}}+T_{\mathrm{risk}}+T_{\mathrm{send}}",
        r"""
int main(void) {
    int64_t received_ms = 1000, now_ms = 1250, limit_ms = 100;
    int stale = now_ms - received_ms > limit_ms;
    printf("age_ms=%" PRId64 " allow_new_risk=%d\n", now_ms - received_ms, !stale);
    return 0;
}""",
        "age_ms=250 allow_new_risk=0",
        "Create an operational readiness table and an independent research evaluation plan. Explain why optimizing p50 computation and selecting the best synthetic return do not establish deployment readiness.",
        "Readiness includes age and clock policy, queue overload, tail measurements, risk rejection, recovery and monitoring. Evaluation needs untouched chronological holdout data and realistic costs. Median kernel latency omits other response costs, and synthetic winners are not evidence of alpha.",
        [
            (
                "Can very fast computation make a stale quote current?",
                "No; freshness is a separate input constraint",
                "Yes, if compiled with -O3",
                "Yes, with more workers",
                "Calculation speed does not change when the source information became available.",
            ),
            (
                "What happens when many strategies are chosen using the test period?",
                "The test period becomes part of model selection",
                "It remains untouched by definition",
                "Parallel execution removes selection bias",
                "Repeated selection consumes holdout information and biases the final performance estimate.",
            ),
            (
                "A 180 ms-old quote exceeds a 100 ms new-risk limit. The configured action is:",
                "Block new exposure under that policy",
                "Ignore age because the ledger is integer",
                "Submit twice to catch up",
                "Freshness limits must be enforced independently of computation speed.",
            ),
            (
                "Which report separates system health from investment evidence?",
                "Latency/rejections plus an independent chronological evaluation protocol",
                "Only the fastest profitable synthetic trial",
                "Only the compiler logo",
                "Operational performance and strategy validity require different datasets, metrics and evidence.",
            ),
        ],
        [CLOCK, LEAKAGE],
    )
    add(
        "Capstone: defend a reproducible C trading research engine",
        "Deliver a measured optimization with causal results, boundary evidence, and a clear scope.",
        "The capstone integrates the entire lifecycle: define the contract, establish independent fixtures, build and instrument, identify a bottleneck, change one mechanism, measure fairly, and defend the result. Start with the provided serial and POSIX paths. Choose a manageable extension such as hoisted validated-data checks, a feature layout experiment, or different independent-trial scheduling.\n\nA complete submission includes source, commands, environment, data/seed identity, parameter manifest, expected results, test evidence, timing distribution and limitations. Separate implemented behavior from proposals for OpenMP, SIMD, GPU or distributed systems. A conceptual exam score cannot certify a compiler build, trading validity or production safety. The notebook rubric evaluates those artifacts separately and makes unresolved causality or corruption defects a reason to withhold acceptance.",
        "The mandatory golden fixture ends at 999,950 cents with two fills. The full seeded sweep must match fields exactly between serial and parallel execution for all 64 windows. A candidate that is slower can still be a valuable capstone if the experiment is reproducible, explains the bottleneck and rejects its original hypothesis honestly.",
        "Run make test, make sanitize and the benchmark at two workload sizes and several worker counts. Preserve complete outputs and compare every result row. Complete performance-notebook.md, score the separate capstone rubric, and take the final exam only after reviewing all six unit checkpoints.",
        r"\mathrm{acceptance}=\mathrm{correctness}\land\mathrm{reproducibility}\land\mathrm{honest\ measurement}",
        r"""
int main(void) {
    int64_t cash = 1000000;
    cash -= 130 + 5;
    cash += 90 - 5;
    if (cash != 999950)
        return 1;
    puts("capstone oracle: equity=999950 fills=2");
    puts("Next: make test && make sanitize; compare all serial/parallel rows.");
    return 0;
}""",
        "capstone oracle: equity=999950 fills=2",
        "Submit source and a filled performance notebook: contract, independent fixtures, sanitizer output, exact serial/parallel equality, two workload sizes, measured timings, one explained optimization, and a paper deployment/evaluation plan.",
        "Require the 999,950-cent two-fill golden result and all-window equality, then report fair build settings and all repetitions. Score at least 80/100 on the separate rubric with no unresolved causality, corruption or duplicate-execution issue. Disclose unimplemented gateway/GPU/cluster features and synthetic execution limits.",
        [
            (
                "A slower candidate disproves the speed hypothesis. A strong capstone should:",
                "Report it and explain the measured cause",
                "Delete slow runs until it looks faster",
                "Change costs to improve equity",
                "Honest reproducible negative findings are valid engineering evidence.",
            ),
            (
                "What exact golden ledger must the provided four-bar fixture produce?",
                "999,950 cents and two fills",
                "1,000,000 cents and no fees",
                "999,960 cents with free execution",
                "The fixture buys at 130, sells at 90 and pays two five-cent fees.",
            ),
            (
                "A candidate passes its exam but fails a causality fixture. It is:",
                "Not accepted until the defect is resolved",
                "Ready because the score replaces code evidence",
                "Automatically faster",
                "Conceptual assessment cannot override a demonstrated execution-model defect.",
            ),
            (
                "Which artifact completes a defensible optimization claim?",
                "Reproducible source, equivalent outputs and fair timing distributions",
                "Only a screenshot of the fastest run",
                "Only the selected profitable parameter",
                "A claim needs inspectable behavior and measurements under documented comparable conditions.",
            ),
        ],
        [CLANG, ASAN, UBSAN, THREADS, LEAKAGE],
    )

    parts = [
        (
            "C foundations and program contracts",
            "Compiler workflow, numeric bounds, pointers and ownership.",
        ),
        (
            "Market data and the chronological engine",
            "Validation, memory layout, streaming indicators and causal fills.",
        ),
        (
            "Measure and verify before optimizing",
            "Clocks, distributions, speedup limits, diagnostics and experiments.",
        ),
        (
            "Parallel CPU research",
            "POSIX workers, synchronization, deterministic results and OpenMP design.",
        ),
        (
            "HPC beyond one scalar loop",
            "SIMD, GPU cost models, distributed manifests and bounded queues.",
        ),
        (
            "Risk, recovery and the systems capstone",
            "Atomic transitions, replay, operational limits and a measured final project.",
        ),
    ]
    track = finish(
        {
            "id": "c-hpc-trading",
            "number": 9,
            "title": "Algorithmic trading II: C & high-performance computing",
            "description": "Build a compiled C trading research engine. Learn memory ownership, causal execution, profiling, POSIX parallel sweeps, SIMD and accelerator design, risk checks, and reproducible performance evaluation.",
            "source": "Original Quanta course · LLVM, GNU, POSIX/Linux man-pages, OpenMP, NVIDIA & MPI references",
            "level": "Advanced",
            "icon": "systems",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Complete Algorithmic trading & AI bots first, or bring equivalent backtesting and market knowledge. Know variables, loops, functions and a terminal. The first unit introduces C-specific build, numeric and ownership concepts. Labs use a local C17 compiler; the full project needs make and POSIX threads on macOS, Linux or WSL.",
            "outcomes": [
                "Compile, diagnose and structure a C17 program with explicit numeric and ownership contracts.",
                "Implement and test rolling indicators, next-open fills and an exact integer-cent ledger.",
                "Measure fair elapsed-time distributions and explain overhead and speedup limits.",
                "Run independent POSIX-thread parameter trials with deterministic, exactly matching results.",
                "Evaluate SIMD, OpenMP, GPU and distributed designs using dependencies and full data-movement costs.",
                "Defend risk, replay and overload policies with a reproducible systems capstone.",
            ],
            "readingGuide": "24 lessons × 30 minutes = 12 hours of guided study across six units: 10 minutes reading, 10 minutes local C experimentation and 10 minutes assignment work per lesson; exam time is additional. Includes 48 practice questions, six four-question checkpoints, a 24-question final and a separately self-assessed capstone. All 24 worksheets are C17. The browser provides a C editor and source downloads; compile and execute on your own machine. The full lab implements serial and POSIX-thread CPU sweeps. OpenMP, SIMD, GPU, cluster and gateway work are explicit extensions/design exercises. No real-money orders or performance guarantees.",
            "parts": [
                {"id": str(i), "title": t, "description": d} for i, (t, d) in enumerate(parts, 1)
            ],
            "references": [
                {"title": t, "url": u}
                for t, u in [CLANG, ASAN, UBSAN, THREADS, VECTOR, OMP, CUDA, MPI]
            ],
            "resources": [
                {
                    "title": "Download the complete C/HPC bot lab",
                    "url": "/course-assets/c-hpc-trading/c-hpc-bot-lab.zip",
                },
                {
                    "title": "Download the C build and project guide",
                    "url": "/course-assets/c-hpc-trading/README.md",
                },
                {
                    "title": "Download the performance notebook and capstone rubric",
                    "url": "/course-assets/c-hpc-trading/performance-notebook.md",
                },
            ],
        },
        checkpoints_for(modules, parts, 6),
    )
    track["exams"][-1]["version"] = 1
    return track
