import { chromium } from "@playwright/test";
import { randomUUID } from "node:crypto";
import { cpus, totalmem, platform, release } from "node:os";
import { mkdir, writeFile } from "node:fs/promises";

const baseURL = process.env.TEST_URL || "http://127.0.0.1:8088";
const browser = await chromium.launch({
  channel: process.env.CI ? undefined : "chrome",
});
const context = await browser.newContext({
  baseURL,
  viewport: { width: 1440, height: 900 },
});
const api = context.request;
const p95 = (values) =>
  [...values].sort((a, b) => a - b)[Math.ceil(values.length * 0.95) - 1];
async function json(response) {
  if (!response.ok())
    throw new Error(`${response.status()}: ${await response.text()}`);
  return response.json();
}
try {
  await json(await api.get("/api/v1/simulator"));
  let run = await json(
    await api.post("/api/v1/simulator/runs", {
      data: { id: randomUUID(), seed: 47 },
    }),
  );
  while (run.cursor < 4999)
    run = await json(
      await api.post(`/api/v1/simulator/runs/${run.id}/advance`, {
        data: {
          id: randomUUID(),
          version: run.version,
          steps: Math.min(390, 4999 - run.cursor),
        },
      }),
    );
  run = await json(
    await api.put(`/api/v1/simulator/runs/${run.id}/preferences`, {
      data: {
        id: randomUUID(),
        version: run.version,
        preferences: {
          symbol: "AAPL",
          interval: "1m",
          indicators: [
            {
              id: "volume",
              kind: "Volume",
              period: 20,
              slow: 26,
              signal: 9,
              visible: true,
            },
            {
              id: "sma",
              kind: "SMA",
              period: 20,
              slow: 26,
              signal: 9,
              visible: true,
            },
            {
              id: "rsi",
              kind: "RSI",
              period: 14,
              slow: 26,
              signal: 9,
              visible: true,
            },
          ],
        },
      },
    }),
  );
  const acknowledgements = [];
  for (let i = 0; i < 50; i++) {
    const start = performance.now();
    run = await json(
      await api.post(`/api/v1/simulator/runs/${run.id}/orders`, {
        data: {
          id: randomUUID(),
          version: run.version,
          symbol: "AAPL",
          side: "buy",
          kind: "limit",
          limit_price: "1",
          quantity: 1,
        },
      }),
    );
    acknowledgements.push(performance.now() - start);
  }
  const page = await context.newPage(),
    errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  const marketResponse = page.waitForResponse((r) =>
    r.url().includes("/market?symbol=AAPL&interval=1m"),
  );
  await page.goto("/simulator");
  const bars = (await (await marketResponse).json()).bars.length;
  await page.locator(".sim-chart-canvas canvas").first().waitFor();
  if (
    bars !== 5000 ||
    (await page.locator(".sim-indicator-legend span").count()) !== 3
  )
    throw new Error(
      "Benchmark setup differs from 5,000 bars and three indicators",
    );
  const rect = await page.locator(".sim-chart-canvas").boundingBox();
  await page.mouse.move(rect.x + rect.width * 0.5, rect.y + rect.height * 0.3);
  // One second warm-up before sampling real pan/wheel input over 360 frames.
  await page.evaluate(
    () =>
      new Promise((resolve) => {
        let n = 0;
        const frame = () =>
          ++n === 60 ? resolve() : requestAnimationFrame(frame);
        requestAnimationFrame(frame);
      }),
  );
  await page.evaluate(() => {
    window.simBenchmarkFrames = [];
    window.simBenchmarkActive = true;
    let last = performance.now();
    const frame = (now) => {
      window.simBenchmarkFrames.push(now - last);
      last = now;
      if (window.simBenchmarkActive) requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  });
  for (let i = 0; i < 360; i++) {
    if (i % 60 === 0) await page.mouse.down();
    await page.mouse.move(
      rect.x + rect.width * 0.5 + Math.sin(i / 15) * 110,
      rect.y + rect.height * 0.3,
    );
    if (i % 60 === 45) await page.mouse.up();
    if (i % 60 >= 46) await page.mouse.wheel(0, i % 120 < 60 ? -10 : 10);
    await page.evaluate(() => new Promise(requestAnimationFrame));
  }
  await page.mouse.up();
  const frames = await page.evaluate(() => {
    window.simBenchmarkActive = false;
    return window.simBenchmarkFrames.slice(1);
  });
  if (errors.length) throw new Error(errors.join("\n"));
  const results = {
    date: new Date().toISOString(),
    baseURL,
    hardware: {
      cpu: cpus()[0].model,
      cores: cpus().length,
      memoryGiB: totalmem() / 2 ** 30,
      os: `${platform()} ${release()}`,
    },
    browser: browser.version(),
    viewport: "1440x900",
    dataset: "seed 47 synthetic AAPL, 5,000 observed minute bars",
    indicators: "Volume, SMA20, RSI14",
    concurrency: 1,
    acknowledgement: {
      samples: acknowledgements.length,
      p95ms: p95(acknowledgements),
      maxMs: Math.max(...acknowledgements),
      method:
        "Sequential HTTP order acknowledgements through local web proxy; response body consumed; excludes fills",
    },
    panZoom: {
      samples: frames.length,
      p95ms: p95(frames),
      maxMs: Math.max(...frames),
      method:
        "Headless Chrome requestAnimationFrame intervals during 360 frames of Playwright mouse drags and wheel events after warm-up",
    },
    errors,
  };
  await mkdir("artifacts", { recursive: true });
  await writeFile(
    "artifacts/simulator-performance.json",
    JSON.stringify(results, null, 2) + "\n",
  );
  await page.screenshot({ path: "artifacts/simulator-5000-bars.png" });
  console.log(JSON.stringify(results, null, 2));
} finally {
  await context.close();
  await browser.close();
}
