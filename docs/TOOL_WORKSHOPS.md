# Trading simulator & strategy lab workshops

Two applied courses teach the platform's own tools. They come straight after Trading ethics, so learners practise with their written charter in hand, and before the valuation and strategy courses that rely on the tools. Each course has 12 lessons of 30 minutes (6 hours) in three units of four, 24 practice questions, three four-question checkpoints and a 12-question final.

| Course | Lessons | Builder | Units |
| --- | --- | --- | --- |
| Trading simulator workshop (`simulator-workshop`) | 13.1–13.12 | `content/authoring/simulator_workshop.py` | Set up and read the market · Place and manage orders · Research, review and discipline |
| Strategy lab workshop (`lab-workshop`) | 14.1–14.12 | `content/authoring/lab_workshop.py` | The market sandbox · Read evidence and value businesses · Execution, DeFi and your research trail |

## How the lessons are kept accurate

- **Labels:** every click-by-click step uses the exact labels rendered by the simulator and the lab.
- **Defaults and rules:** these were taken from the frontend components and the backend services that implement them, not from screenshots. Examples:
  - $100,000 starting cash, a $1 commission, 2 bps of slippage and spread, and 1% participation;
  - next-bar eligibility;
  - stop and trailing-stop rules;
  - margin buying power and the 30% buy-in;
  - the sandbox's seed-42 defaults, the valuation worksheet, the factor fit, the paper broker's guards and the AMM quote.
- **Engine-checked figures:** every figure that depends on the engine was recomputed by running the backend with default inputs. Examples:
  - the default trend rule's −23.40% total return and 59 fills;
  - the robustness sweep across seeds 42–46 and the five named scenarios;
  - the one-year versus three-year look-ahead test.
- **Worksheets:** every worksheet runs in the guided Python runtime. `backend/tests/test_platform_workshops.py` runs both capstones and checks independent arithmetic.

## Practice missions and lab links

- **Simulator workshop:** it links all six practice missions, including `stop-discipline`, which no lesson had linked before. Each link only preselects the mission, so every lesson walks through **New simulation run** → **Create new paper account**.
- **Lab workshop:** it links each Strategy lab tool with `/lab?tool=…`.
- **Tests:** they check that every mission link names a real mission and every tool link a real tool.

## Known limitation to revisit

Bracket exit legs in the simulator are saved without a note. They therefore count against the mission objective "Record a thesis on every order" until a note is added through **Journal**, and one bracket counts as three orders. The lessons tell learners to journal each leg, and the assessments avoid depending on this behaviour, so they stay correct if it is fixed.
