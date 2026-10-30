# Shared learning content

`authoring/` contains original course builders and reusable authoring helpers. `catalog/curriculum.json` is the canonical generated course and exam data, imported by the frontend and read by the backend. `projects/` owns all downloadable educational source files.

`authoring/learning_guidance.py` owns the plain-language introductions, step-by-step worked explanations, and shared vocabulary. The generator applies these to the lesson bodies after assembling the courses. Keep explanations tied to the actual example: define the inputs, show the intermediate calculation, and explain the conclusion. Add context before technical detail, and preserve the lesson's equations, assessment keys, and executable worksheets when editing prose. Use `$$` for Markdown equations; ordinary `$` amounts remain currency in the reader.

From the repository root, run `npm run content:build` after editing course builders or projects. It regenerates the catalog and the copies/archives under `frontend/public/course-assets/`. Both scripts resolve repository paths from their own locations and can also run from another working directory.

Preserve existing course IDs, lesson IDs, first-practice answer keys, and exam-version semantics when expanding courses. The array order controls the recommended learning sequence and displayed track labels. Case explanations and exercises should be original; distinguish documented events, practical implementations, and fictional scenarios, and include references at the lesson level. Project files included in archives are explicitly listed in `scripts/package_projects.py`.

The [real-world case system](../docs/REAL_WORLD_CASES.md) covers all 425 lessons with a mix of Indonesian and global context. The advanced security-analysis tracks extend the core course with forensic accounting, credit and distress, quality, banks, valuation uncertainty, cyclicals, technology, and a documented casebook; their lesson applications live in `case_applications_security.py`. Edit shared source anchors in `authoring/real_world_cases.py` and individual applications in the four `case_applications_*.py` files. Every new lesson needs an explicit application; the build rejects missing or duplicate coverage. Cite the source beside the case, explain what it supports, and label any invented exercise numbers.

The [news interpretation course](../docs/NEWS_COURSE.md) follows Security Analysis and uses the new `8.x` lesson namespace.

The [C and high-performance bot course](../docs/C_HPC_COURSE.md) follows Python bots and uses `9.x`. Mark its worksheets `codeLanguage: "c"` and provide `expectedOutput`; do not append the Python strategy helper to C source. Every worksheet is compiled in course tests; the source-only C/POSIX archive is extracted, built and tested independently. Generated C binaries are ignored and excluded from downloads.

The [algorithm evaluation/reporting course](../docs/ALGORITHM_EVALUATION.md) is last, after stock ML, using `10.x`. Its project owns the report generator, example valuations/timings/manifest and report rubric. Generated personal report outputs are ignored; only the explicit original source files enter the downloadable archive.

The [careful-investor companion](../docs/INTELLIGENT_INVESTOR.md) appears before Security Analysis with `11.x` lesson IDs. Its workbook contains original cases and a plan, not the book. The [expanded Strategy Lab](../docs/STRATEGY_LAB_COURSE.md) preserves legacy `4.1`–`4.4` first practice keys and upgrades its final to version 2; its local project exports valuations directly to the final reporting course.

## Research extensions

`authoring/research_depth.py` appends a final *Go deeper: what the research says* section to each lesson that has a verified note. It runs in `curriculum.py` after the learning guidance and before `attach_references`, so every cited source reaches the lesson footer and the reference library. A course's notes live in `authoring/research_<course>.py` as `(body, sources)` pairs keyed by lesson ID. Lessons are added individually as each one is verified; a lesson without a note has no section. The build rejects:
- unknown lesson IDs;
- duplicated bodies;
- links, tables or numbered lists inside a body;
- more than one display equation;
- non-https or versioned arXiv URLs;
- a source cited twice in one note.

Write each note in Quanta's own words, at the course's level, tied to the lesson's worked example, with 2–4 sources and at least one arXiv paper where a relevant one exists. Before a note is merged:
- every arXiv ID and DOI must match its registry title and year;
- every figure in the text must be backed by a verbatim snippet of its source, and that snippet must be re-fetched and found.

`backend/tests/test_research_depth.py` checks the rendered sections.

## Tool workshops

The [simulator and lab workshops](../docs/TOOL_WORKSHOPS.md) use the `13.x` and `14.x` namespaces and follow Trading ethics. Their steps quote the exact UI labels and their figures come from running the engine with default inputs. If the simulator's or the lab's labels, defaults or execution rules change, update these lessons in the same change.
