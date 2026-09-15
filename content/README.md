# Shared learning content

`authoring/` contains original course builders and reusable authoring helpers. `catalog/curriculum.json` is the canonical generated course and exam data, imported by the frontend and read by the backend. `projects/` owns all downloadable educational source files.

`authoring/learning_guidance.py` owns the plain-language introductions, step-by-step worked explanations, and shared vocabulary. The generator applies these to the lesson bodies after assembling the courses. Keep explanations tied to the actual example: define the inputs, show the intermediate calculation, and explain the conclusion. Add context before technical detail, and preserve the lesson's equations, assessment keys, and executable worksheets when editing prose. Use `$$` for Markdown equations; ordinary `$` amounts remain currency in the reader.

From the repository root, run `npm run content:build` after editing course builders or projects. It regenerates the catalog and the copies/archives under `frontend/public/course-assets/`. Both scripts resolve repository paths from their own locations and can also run from another working directory.

Preserve existing course IDs, lesson IDs, first-practice answer keys, and exam-version semantics when expanding courses. The array order controls the recommended learning sequence and displayed track labels. Case explanations and exercises should be original; distinguish documented events, practical implementations, and fictional scenarios, and include references at the lesson level. Project files included in archives are explicitly listed in `scripts/package_projects.py`.

The [real-world case system](../docs/REAL_WORLD_CASES.md) covers all 300 lessons with a mix of Indonesian and global context. Edit shared source anchors in `authoring/real_world_cases.py` and individual applications in the four `case_applications_*.py` files. Every new lesson needs an explicit application; the build rejects missing or duplicate coverage. Cite the source beside the case, explain what it supports, and label any invented exercise numbers.

The [news interpretation course](../docs/NEWS_COURSE.md) follows Security Analysis and uses the new `8.x` lesson namespace.

The [C and high-performance bot course](../docs/C_HPC_COURSE.md) follows Python bots and uses `9.x`. Mark its worksheets `codeLanguage: "c"` and provide `expectedOutput`; do not append the Python strategy helper to C source. Every worksheet is compiled in course tests; the source-only C/POSIX archive is extracted, built and tested independently. Generated C binaries are ignored and excluded from downloads.

The [algorithm evaluation/reporting course](../docs/ALGORITHM_EVALUATION.md) is last, after stock ML, using `10.x`. Its project owns the report generator, example valuations/timings/manifest and report rubric. Generated personal report outputs are ignored; only the explicit original source files enter the downloadable archive.

The [careful-investor companion](../docs/INTELLIGENT_INVESTOR.md) appears before Security Analysis with `11.x` lesson IDs. Its workbook contains original cases and a plan, not the book. The [expanded Strategy Lab](../docs/STRATEGY_LAB_COURSE.md) preserves legacy `4.1`–`4.4` first practice keys and upgrades its final to version 2; its local project exports valuations directly to the final reporting course.
