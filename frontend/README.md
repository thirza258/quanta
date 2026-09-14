# Frontend

React, TypeScript, and Vite application. Source is divided into application composition, feature modules, and shared components/utilities. See [architecture](../docs/ARCHITECTURE.md).

Install with `npm ci` from the repository root, using its shared workspace lockfile. Frontend package commands also work from this directory:

```sh
npm run dev       # Browser application; proxies /api to port 8000 by default
npm run build     # TypeScript check and production output in frontend/dist
npm test          # Colocated model and progression tests
npm run preview
TEST_URL=http://127.0.0.1:8088 npm run test:e2e
```

Set `API_TARGET` to a different API origin when starting Vite or preview. Use root `npm run dev` to start both applications with matched available ports and origins. Vite aliases `@/` to `src/` and `@content/` to the shared content source.

Edit course content and downloadable projects under `../content/`, then run root `npm run content:build`. Public download URLs are stable; do not edit generated download copies directly. To regenerate software notices after installing dependencies, run `python3 scripts/third_party_notices.py`.

Browser scenarios live in `e2e/`; local execution uses installed Chrome, while CI uses Playwright Chromium. Build the web container from the repository root with `docker build -f frontend/Dockerfile .` or use Compose.

Learning worksheets declare an optional `codeLanguage`; existing lessons default to Python. C lessons load `features/learning/components/LocalCodeLab.tsx` for saved source editing and local compile/download instructions. Python lessons retain `features/research/components/Sandbox.tsx`. Keep the global CSS baseline before course overrides in `src/main.tsx` so long cards retain their bottom spacing at all breakpoints.
