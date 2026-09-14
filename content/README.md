# Shared learning content

`authoring/` contains original course builders and reusable authoring helpers. `catalog/curriculum.json` is the canonical generated course and exam data, imported by the frontend and read by the backend. `projects/` owns all downloadable educational source files.

From the repository root, run `npm run content:build` after editing course builders or projects. It regenerates the catalog and the copies/archives under `frontend/public/course-assets/`. Both scripts resolve repository paths from their own locations and can also run from another working directory.

Preserve existing course IDs, lesson IDs, first-practice answer keys, and exam-version semantics when expanding courses. The array order controls the recommended learning sequence and displayed track labels. All cases should be original, clearly labeled if fictional, and include references at the lesson level. Project files included in archives are explicitly listed in `scripts/package_projects.py`.

The [news interpretation course](../docs/NEWS_COURSE.md) follows Security Analysis and uses the new `8.x` lesson namespace.

The [C and high-performance bot course](../docs/C_HPC_COURSE.md) follows Python bots and uses `9.x`. Mark its worksheets `codeLanguage: "c"` and provide `expectedOutput`; do not append the Python strategy helper to C source. Every worksheet is compiled in course tests; the source-only C/POSIX archive is extracted, built and tested independently. Generated C binaries are ignored and excluded from downloads.

The [algorithm evaluation/reporting course](../docs/ALGORITHM_EVALUATION.md) is last, after stock ML, using `10.x`. Its project owns the report generator, example valuations/timings/manifest and report rubric. Generated personal report outputs are ignored; only the explicit original source files enter the downloadable archive.
