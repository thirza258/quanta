# Real-world applications throughout the curriculum

Every one of the 425 lessons has an original application connected to a practical case. The 23 courses use 43 shared case anchors: 19 documented events, 21 implementations based on primary documentation, and 3 explicitly fictional everyday scenarios. All 117 named units link to the cases their lessons use; the introductory course has lesson applications without a separate unit structure.

Learners can select **Explore the real-world case** at the top of a lesson, read the source context, attempt **Your task**, and expand **Compare your reasoning**. **Work through this case** opens a notebook prompt containing the task, source links, source scope, and assumptions. Saved work follows the existing notebook persistence flow. Case practice is optional additional work and does not change the listed lesson durations or assessment requirements.

The course overview lists its cases, and each unit links directly to a relevant lesson's `#real-world-case` section. References also appear in the existing lesson footer and reference library. The course AI assistant receives the selected lesson's application and resolved case, including its dates, source scope, and illustrative-data boundary. Course-level assistance receives that course's case anchors. The OpenAI SDK/OpenRouter configuration is unchanged.

## Coverage

| Course | Lessons with applications | Named units | Shared cases used |
| --- | ---: | ---: | ---: |
| Trading & market fundamentals | 8 | — | 6 |
| The intelligent & careful investor | 16 | 4 | 7 |
| Security Analysis | 31 | 9 | 12 |
| Financial news to company & stock analysis | 24 | 6 | 12 |
| Quantitative Investment Analysis | 28 | 14 | 15 |
| Financial econometrics | 32 | 8 | 13 |
| The strategy lab | 32 | 8 | 17 |
| Algorithmic & AI stock bots | 48 | 12 | 18 |
| Algorithmic trading II: C & HPC | 24 | 6 | 10 |
| Web3, cryptography & coin creation | 24 | 6 | 7 |
| Machine learning for stocks | 24 | 6 | 9 |
| Algorithm evaluation & results reporting | 16 | 4 | 8 |
| Forensic accounting & earnings quality | 6 | 2 | 5 |
| Credit analysis & distressed securities | 6 | 2 | 4 |
| Business quality, moats & capital allocation | 6 | 2 | 5 |
| Analyzing banks & financial institutions | 6 | 2 | 3 |
| Valuation under uncertainty | 6 | 2 | 6 |
| Cyclicals, commodities & industrials | 6 | 2 | 6 |
| Technology, platforms & intangibles | 6 | 2 | 5 |
| Real-world security analysis casebook | 8 | 2 | 8 |

Cases recur across lessons with different, individually authored tasks. For example, BCA's split connects share ownership, per-share earnings, historical return adjustment, bot account transitions, and ML data repair. Reusing the source event does not substitute one generic task for those distinct applications.

## Indonesian and global context

Indonesian anchors include a fictional household and neighborhood shop, [BCA's 2021 split](https://www.bca.co.id/id/tentang-bca/media-riset/pressroom/siaran-pers/2021/10/07/09/52/saham-bbca-segera-diperdagangkan-dengan-harga-baru), [Bank Indonesia's April 2024 rate release](https://www.bi.go.id/en/publikasi/ruang-media/news-release/Pages/sp_268024.aspx), [BPS's release on 2024 GDP](https://www.bps.go.id/id/pressrelease/2025/02/05/2408/economic-growth.html), and [OJK's account of the IPB investment-fraud case](https://ojk.go.id/id/berita-dan-kegiatan/siaran-pers/Pages/OJK-Tingkatkan-Edukasi-dan-Perlindungan-Konsumen-dalam-Kasus-Penipuan-Berkedok-Investasi-di-IPB.aspx).

Global event anchors include [SVB](https://www.federalreserve.gov/publications/2023-April-SVB-Key-Takeaways.htm), [Knight Capital](https://www.sec.gov/newsroom/press-releases/2013-222), [GameStop](https://www.sec.gov/newsroom/press-releases/2021-212), [the 2010 Flash Crash](https://www.cftc.gov/sites/default/files/idc/groups/public/%40otherif/documents/ifdocs/staff-findings050610.pdf), [the UK gilt/LDI disruption](https://www.bankofengland.co.uk/quarterly-bulletin/2023/2023/financial-stability-buy-sell-tools-a-gilt-market-case-study), [GE's disclosure settlement](https://www.sec.gov/Archives/edgar/data/40545/000004054520000062/ge-20201209.htm), and [CME's negative-price test advisory](https://www.cmegroup.com/notices/clearing/2020/04/Chadv20-160.html).

Implementation anchors use SEC EDGAR, ALFRED, Kenneth French's factor definitions, statsmodels, scikit-learn, AWS Builders' Library, Google SRE, SQLite, LLVM/Clang, OpenMP, NVIDIA CUDA, the Bitcoin paper, ERC-20, EIP-155, Uniswap v2, Chainlink, OWASP, and GIPS reporting principles. Each anchor's exact URL and supported subject are maintained in the [case registry](../content/authoring/real_world_cases.py) and displayed beside the lesson's context. No third-party article or book chapter is reproduced.

## Source and authorship rules

- `documented`: the event's date and historical context come from the named primary source. Exercise numbers are illustrative unless the task explicitly asks the learner to read figures from the cited release.
- `implementation`: the source explains the technical method. The original local workflow and sample results are not claimed to be a named organization's production system.
- `illustrative`: people, organizations, amounts, and outcomes are fictional. References explain the underlying method.

Keep historical policy rates separate from current rates. Do not infer causality from an event chart, treat a stock split as wealth creation, call a legal lender the perpetrator of a separate investment fraud, or claim that completing a report establishes GIPS compliance. CME's cited April 2020 advisory supports testing for negative prices; it is not used as a settlement-price dataset. U.S. factor definitions illustrate research methods and require explicit adaptation to another market.

## Authoring and rebuilding

Shared anchors live in `content/authoring/real_world_cases.py`. Lesson applications are explicit tuples `(lesson_id, case_id, connection, task, walkthrough)` in:

- `case_applications_investing.py`: fundamentals, careful investing, security analysis, and news.
- `case_applications_quant.py`: quantitative methods, econometrics, and strategy research.
- `case_applications_systems.py`: bots, C/HPC, and Web3.
- `case_applications_evaluation.py`: stock ML and results reporting.

Run `npm run content:build` after editing. The builder rejects missing, duplicate, unknown, or empty applications. Each course stores its used anchors in `caseStudies`; each lesson stores `realWorld` with its case ID and application. Case references merge into course and lesson references by URL. Existing lesson content, worksheets, IDs, ordering, first-practice answer keys, exam versions, downloads, and durations remain intact.

## Verification

`backend/tests/test_real_world_cases.py` checks complete coverage, reference propagation, unique applications, rebuild stability, and authoring failures. Independent arithmetic checks cover split-adjusted ownership returns, constant-product swap output, and separating contributions from investment returns. The assistant transport tests check that OpenRouter receives the selected case's context through the OpenAI SDK.

`frontend/src/features/learning/model/cases.test.ts` checks unit/lesson destinations and notebook evidence. `frontend/e2e/real-world-cases.spec.ts` visits every lesson, checks its source and worked explanation, follows a unit deep link, saves a case response through the notebook, and checks mobile layouts in both themes. The external source pages are references, not runtime dependencies or automated-test fixtures.

Verified on 14 September 2026: production build, 597 backend tests, 47 frontend tests, and 19 browser tests spanning the case and assistant flows passed. Browser coverage includes all 300 lessons and 82 units. Targeted follow-up checks passed for the corrected Investor.gov link, reopening saved case notes, all 35 references in the library, and mobile layouts. Desktop and mobile pages were also visually inspected with agent-browser, with no page errors reported.
