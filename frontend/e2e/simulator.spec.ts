import { expect, test, type Page } from "@playwright/test";
import { randomUUID } from "node:crypto";

// The simulator lists fictional companies. NVRA (Novara Microsystems, ~$148) is
// the default symbol; VLOC (Velocity Motorworks) and ZEPH (Zephyr Robotics,
// ~$20 and the heaviest traded name) stand in for a second and a cheap company.
type Quote = { symbol: string; name: string; close: number };

async function open(page: Page) {
  await page.goto("/simulator");
  await expect(page.getByTestId("trading-terminal")).toBeVisible();
  await expect(page.locator(".sim-chart-canvas canvas").first()).toBeVisible();
  await expect(page.getByLabel("Next replay bar")).toBeEnabled();
}
async function submit(page: Page, side = "buy") {
  await page
    .getByRole("button", { name: `Preview ${side} order`, exact: true })
    .click();
  await expect(page.getByRole("dialog")).toContainText("Estimated notional");
  await page
    .getByRole("button", { name: `Place ${side} order`, exact: true })
    .click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
}
// The single bar control and the jump controls post the same replay endpoint.
async function advance(page: Page, control = "Next replay bar") {
  const response = page.waitForResponse(
    (r) => r.url().endsWith("/advance") && r.request().method() === "POST",
  );
  await page.getByLabel(control).click();
  expect((await response).status()).toBe(200);
}
async function account(page: Page) {
  return (await (await page.request.get("/api/v1/simulator")).json()).run;
}
function quoteFor(run: { quotes: Quote[] }, symbol: string) {
  const quote = run.quotes.find((q: Quote) => q.symbol === symbol);
  expect(quote, `${symbol} is quoted in this run`).toBeTruthy();
  return quote!;
}

test("chart workspace, indicator, drawing forms and watchlist persist by symbol", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.setViewportSize({ width: 1440, height: 900 });
  await open(page);
  const chart = await page.locator(".sim-chart-region").boundingBox();
  expect(chart!.width).toBeGreaterThan(1440 * 0.6);
  expect(chart!.height).toBeGreaterThan((900 - 48 - 49 - 42 - 30) * 0.5);
  await page.getByRole("button", { name: "NVRA", exact: true }).click();
  await page.getByLabel("Search stocks").fill("velocity");
  // Scoped to the dialog: a headline in the ticker strip names companies too.
  await page
    .getByRole("dialog")
    .getByRole("button", { name: /VLOC Velocity Motorworks/ })
    .click();
  await page.getByRole("button", { name: "5m", exact: true }).click();
  await expect(page.locator(".sim-chart-readout")).toContainText("VLOC");
  await page.getByLabel("Fullscreen chart workspace").click();
  await expect
    .poll(() => page.evaluate(() => !!document.fullscreenElement))
    .toBe(true);
  await page.getByRole("button", { name: "Indicators", exact: true }).click();
  await page
    .getByRole("combobox", { name: "Add indicator", exact: true })
    .selectOption("RSI");
  await page.getByLabel("Close dialog").click();
  await page.getByLabel("Fullscreen chart workspace").click();
  await expect
    .poll(() => page.evaluate(() => !!document.fullscreenElement))
    .toBe(false);
  await page.getByRole("button", { name: "Objects", exact: true }).click();
  await page.getByLabel("Add drawing with form").selectOption("trend");
  await page.getByLabel("Drawing label").fill("Trend thesis");
  await page.getByLabel("Lock drawing").check();
  await expect(page.getByLabel("First price")).toBeDisabled();
  await page.getByLabel("Lock drawing").uncheck();
  await page
    .getByRole("button", { name: "Delete drawing", exact: true })
    .click();
  await page.getByLabel("Undo drawing").click();
  await expect(page.locator(".sim-object-list")).toContainText("Trend thesis");
  await expect(page.locator(".sim-statusbar")).toContainText("Layout saved");
  await page.reload();
  await expect(page.locator(".sim-chart-readout")).toContainText("VLOC");
  await expect(page.locator(".sim-indicator-legend")).toContainText("RSI");
  await expect(
    page.getByRole("button", { name: "5m", exact: true }),
  ).toHaveClass("active");
  await page.getByRole("button", { name: "Objects", exact: true }).click();
  await expect(page.locator(".sim-object-list")).toContainText("Trend thesis");
  await page.getByRole("button", { name: "VLOC", exact: true }).click();
  await page.getByLabel("Search stocks").fill("NVRA");
  await page
    .getByRole("dialog")
    .getByRole("button", { name: /NVRA Novara Microsystems/ })
    .click();
  await page.getByRole("button", { name: "Objects", exact: true }).click();
  await expect(page.locator(".sim-object-list button")).toHaveCount(0);
  expect(errors).toEqual([]);
});

test("keyboard buy, reduce and close reconcile positions, journals and exports", async ({
  page,
}) => {
  await open(page);
  await page.locator(".sim-quick-trade .buy").focus();
  await page.keyboard.press("Enter");
  await page.getByLabel("Shares", { exact: true }).fill("10");
  await page
    .getByRole("button", { name: "Preview buy order", exact: true })
    .focus();
  await page.keyboard.press("Enter");
  await page
    .getByRole("button", { name: "Place buy order", exact: true })
    .focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await expect(
    page.getByRole("tabpanel", { name: "Open orders" }),
  ).toContainText("working");
  await advance(page);
  await page.getByRole("tab", { name: /^Positions/ }).click();
  await expect(
    page.getByRole("tabpanel", { name: "Positions" }).locator("tbody tr"),
  ).toHaveCount(1);
  await page.getByRole("button", { name: "Reduce", exact: true }).click();
  await expect(page.getByLabel("Shares", { exact: true })).toHaveValue("5");
  await submit(page, "sell");
  await advance(page);
  await page.getByRole("tab", { name: /^Positions/ }).click();
  await expect(
    page.getByRole("tabpanel", { name: "Positions" }).locator("td").nth(1),
  ).toHaveText("5");
  await page.getByRole("button", { name: "Close", exact: true }).click();
  await submit(page, "sell");
  await advance(page);
  await page.getByRole("tab", { name: /^Positions/ }).click();
  await expect(
    page.getByRole("tabpanel", { name: "Positions" }).locator("tbody tr"),
  ).toHaveCount(0);
  await page.getByRole("tab", { name: "Trade history", exact: true }).click();
  await expect(
    page.getByRole("tabpanel", { name: "Trade history" }).locator("tbody tr"),
  ).toHaveCount(3);
  await page.getByRole("tab", { name: "Order history", exact: true }).click();
  await page
    .getByRole("button", { name: "Journal", exact: true })
    .first()
    .click();
  await page
    .getByRole("dialog")
    .getByLabel("Trade thesis")
    .fill("Reduced risk before exiting.");
  await page
    .getByRole("dialog")
    .getByLabel("Linked lesson")
    .selectOption("0.7");
  await page.getByRole("button", { name: "Save journal" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  const csv = page.waitForEvent("download");
  await page.getByLabel("Export table as CSV").click();
  expect((await csv).suggestedFilename()).toBe("quanta-order-history.csv");
  const before = (await (await page.request.get("/api/v1/simulator")).json())
    .run;
  await page.getByLabel("New simulation run").click();
  await page.getByRole("button", { name: "Create new paper account" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await expect(page.locator(".sim-account-metrics")).toContainText(
    "$100,000.00",
  );
  await page.getByLabel("Simulation run history").selectOption(before.id);
  await expect(page.locator(".sim-archive-banner")).toContainText(
    "Archived run",
  );
  await page.getByRole("tab", { name: "Trade history", exact: true }).click();
  await expect(
    page.getByRole("tabpanel", { name: "Trade history" }).locator("tbody tr"),
  ).toHaveCount(3);
  await expect(page.getByLabel("Next replay bar")).toBeDisabled();
});

test("nonmarketable limit, rejected amendment, partial fill and cancellation", async ({
  page,
}) => {
  await open(page);
  await page.getByLabel("New simulation run").click();
  // Every new run generates its own market unless a seed is given, and this test
  // reads a partial fill out of one bar's volume. Pin the market so the traded
  // size stays far above the share of volume this account may take.
  await page.getByLabel("Market seed (optional)").fill("777");
  await page.getByLabel("Volume participation (0–1)").fill("0.001");
  await page.getByRole("button", { name: "Create new paper account" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  // ZEPH is the cheapest heavily traded company: 3000 shares cost well under the
  // $100,000 account, and a thousandth of a bar's volume is a few dozen shares.
  await page.getByRole("button", { name: "NVRA", exact: true }).click();
  await page.getByLabel("Search stocks").fill("zephyr");
  await page
    .getByRole("dialog")
    .getByRole("button", { name: /ZEPH Zephyr Robotics/ })
    .click();
  await expect(page.locator(".sim-chart-readout")).toContainText("ZEPH");
  await page.locator(".sim-quick-trade .buy").click();
  await page.getByLabel("Order type").selectOption("limit");
  await page.getByLabel("Shares", { exact: true }).fill("3000");
  await page.getByLabel("Limit price", { exact: true }).fill("1");
  await submit(page);
  await advance(page);
  await expect(
    page.getByRole("tabpanel", { name: "Open orders" }),
  ).toContainText("3000 / 0");
  await page.getByRole("button", { name: "Edit", exact: true }).click();
  await page.getByLabel("New limit price").fill("100000");
  await page.getByRole("button", { name: "Confirm amendment" }).click();
  await expect(page.getByRole("dialog").getByRole("alert")).toContainText(
    "Insufficient available cash",
  );
  await page.getByLabel("Close dialog").click();
  const run = await account(page);
  expect(run.orders[0].limit_price).toBe("1");
  await page.getByRole("button", { name: "Edit", exact: true }).click();
  await page
    .getByLabel("New limit price")
    .fill((quoteFor(run, "ZEPH").close * 1.03).toFixed(2));
  await page.getByRole("button", { name: "Confirm amendment" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await advance(page);
  await expect(
    page.getByRole("tabpanel", { name: "Open orders" }),
  ).toContainText("partially filled");
  await page.getByRole("button", { name: "Cancel", exact: true }).click();
  await expect(
    page.getByRole("tabpanel", { name: "Open orders" }).locator("tbody tr"),
  ).toHaveCount(0);
  const canceled = await account(page);
  expect(canceled.reserved).toBe("0.00");
  expect(canceled.orders[0].filled).toBeGreaterThan(0);
  expect(canceled.orders[0].filled).toBeLessThan(3000);
  await advance(page);
  const after = await account(page);
  expect(after.orders[0].filled).toBe(canceled.orders[0].filled);
});

test("lost accepted response recovers exactly one order after reload", async ({
  page,
}) => {
  await open(page);
  await page.locator(".sim-quick-trade .buy").click();
  await page.route("**/api/v1/simulator/runs/*/orders", async (route) => {
    await route.fetch();
    await route.abort("connectionfailed");
  });
  await page
    .getByRole("button", { name: "Preview buy order", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Place buy order", exact: true })
    .click();
  await expect(page.getByRole("dialog").getByRole("alert")).toContainText(
    "Connection lost",
  );
  await page.getByLabel("Close dialog").click();
  await page.unroute("**/api/v1/simulator/runs/*/orders");
  await page.reload();
  await page
    .getByRole("button", { name: "Reconnect & retry action", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Reconnect & retry action", exact: true }),
  ).not.toBeVisible();
  const run = (await (await page.request.get("/api/v1/simulator")).json()).run;
  expect(run.orders).toHaveLength(1);
  expect(run.orders[0].quantity).toBe(10);
  await advance(page);
  const filled = (await (await page.request.get("/api/v1/simulator")).json())
    .run;
  expect(filled.positions[0].quantity).toBe(10);
});

test("mobile buy and portfolio remain accessible without horizontal overflow", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await open(page);
  await page
    .locator(".sim-mobile-trade-entry")
    .getByRole("button", { name: "Buy", exact: true })
    .click();
  await submit(page);
  await page
    .getByRole("navigation", { name: "Simulator navigation" })
    .getByRole("button", { name: "Chart", exact: true })
    .click();
  await advance(page);
  await page
    .getByRole("navigation", { name: "Simulator navigation" })
    .getByRole("button", { name: "Portfolio", exact: true })
    .click();
  await page.getByRole("tab", { name: /^Positions/ }).click();
  await page.getByRole("button", { name: "Close", exact: true }).click();
  await submit(page, "sell");
  await page
    .getByRole("navigation", { name: "Simulator navigation" })
    .getByRole("button", { name: "Chart", exact: true })
    .click();
  await advance(page);
  await page
    .getByRole("navigation", { name: "Simulator navigation" })
    .getByRole("button", { name: "Portfolio", exact: true })
    .click();
  await page.getByRole("tab", { name: "Trade history", exact: true }).click();
  await expect(
    page.getByRole("tabpanel", { name: "Trade history" }).locator("tbody tr"),
  ).toHaveCount(2);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
});

test("signed-in orders and settings recover on a second device and isolate logout", async ({
  page,
  browser,
  baseURL,
}) => {
  const email = `sim-${randomUUID()}@example.com`,
    password = "simulator-test-password";
  expect(
    (
      await page.request.post("/api/v1/auth/register", {
        data: { name: "Trading learner", email, password },
      })
    ).status(),
  ).toBe(201);
  await open(page);
  await page.locator(".sim-quick-trade .buy").click();
  await submit(page);
  await advance(page);
  await page.getByRole("button", { name: "5m", exact: true }).click();
  await expect(page.locator(".sim-statusbar")).toContainText("Layout saved");
  const run = (await (await page.request.get("/api/v1/simulator")).json()).run;
  const other = await browser.newContext({ baseURL });
  expect(
    (
      await other.request.post("/api/v1/auth/login", {
        data: { email, password },
      })
    ).status(),
  ).toBe(200);
  const second = await other.newPage();
  await open(second);
  await second.getByRole("tab", { name: /^Positions/ }).click();
  await expect(
    second.getByRole("tabpanel", { name: "Positions" }).locator("tbody tr"),
  ).toHaveCount(1);
  await expect(
    second.getByRole("button", { name: "5m", exact: true }),
  ).toHaveClass("active");
  await other.request.post("/api/v1/auth/logout");
  await second.reload();
  await expect(second.locator(".sim-account-metrics")).toContainText(
    "$100,000.00",
  );
  expect(
    (await other.request.get(`/api/v1/simulator/runs/${run.id}`)).status(),
  ).toBe(404);
  await other.close();
});

test("chart drawing gestures and rejected dragged order amendment preserve confirmed state", async ({
  page,
}) => {
  await open(page);
  const rect = (await page.locator(".sim-chart-canvas").boundingBox())!;
  await page.getByRole("button", { name: "Trend line", exact: true }).click();
  await page.mouse.click(rect.x + 300, rect.y + 180);
  await expect(page.locator(".sim-drawing-hint")).toContainText(
    "Click the second point",
  );
  await page.mouse.click(rect.x + 550, rect.y + 220);
  await expect(page.locator(".sim-object-list button")).toHaveCount(1);
  const first = Number(await page.getByLabel("First price").inputValue());
  const line = page.locator("g.sim-drawing line").first();
  const box = (await line.boundingBox())!;
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.down();
  await page.mouse.move(
    box.x + box.width / 2 + 20,
    box.y + box.height / 2 + 30,
    { steps: 8 },
  );
  await page.mouse.up();
  await expect
    .poll(async () => Number(await page.getByLabel("First price").inputValue()))
    .not.toBe(first);
  await page
    .locator(".sim-sidebar-tabs")
    .getByRole("button", { name: "Trade", exact: true })
    .click();
  // Rest the order one cent under the live quote so its line always falls inside
  // the visible price scale, and reserve all but a fraction of a share of the
  // account so that dragging the line upward has to fail the cash check.
  const opening = await account(page);
  const limit = (quoteFor(opening, "NVRA").close - 0.01).toFixed(2);
  const shares = Math.floor(
    (Number(opening.available) - Number(opening.config.commission) - 1) /
      Number(limit),
  );
  await page.getByLabel("Order type").selectOption("limit");
  await page.getByLabel("Shares", { exact: true }).fill(String(shares));
  await page.getByLabel("Limit price", { exact: true }).fill(limit);
  await submit(page);
  const confirmed = await account(page);
  await expect(page.getByLabel("Next replay bar")).toBeEnabled();
  const order = (await page.locator("g.sim-order-line rect").boundingBox())!;
  await page.mouse.move(order.x + 50, order.y + 10);
  await page.mouse.down();
  await page.mouse.move(order.x + 50, rect.y + 8, { steps: 8 });
  await page.mouse.up();
  await expect(page.getByRole("dialog")).toContainText(
    "Confirm order amendment",
  );
  await page
    .getByRole("button", { name: "Confirm amendment", exact: true })
    .click();
  await expect(page.getByRole("dialog").getByRole("alert")).toContainText(
    "Insufficient available cash",
  );
  await page.getByLabel("Close dialog").click();
  const after = await account(page);
  expect(after.orders).toEqual(confirmed.orders);
  expect(after.reserved).toBe(confirmed.reserved);
});

test("disconnection preserves ticket and blocks trading until the account reconnects", async ({
  page,
  context,
}) => {
  await open(page);
  await page.locator(".sim-quick-trade .buy").click();
  await page.getByLabel("Shares", { exact: true }).fill("17");
  await context.setOffline(true);
  await expect(page.locator(".sim-notice")).toContainText("Disconnected");
  await expect(
    page.getByRole("button", { name: "Preview buy order", exact: true }),
  ).toBeDisabled();
  await context.setOffline(false);
  await expect(
    page.getByRole("button", { name: "Preview buy order", exact: true }),
  ).toBeEnabled();
  await expect(page.getByLabel("Shares", { exact: true })).toHaveValue("17");
  await submit(page);
});

test("a trade waits for an in-flight layout save without losing the click", async ({
  page,
}) => {
  await open(page);
  await page.locator(".sim-quick-trade .buy").click();
  let release!: () => void;
  const held = new Promise<void>((resolve) => {
    release = resolve;
  });
  await page.route("**/api/v1/simulator/runs/*/preferences", async (route) => {
    await held;
    await route.continue();
  });
  const saving = page.waitForRequest(
    (r) => r.url().endsWith("/preferences") && r.method() === "PUT",
  );
  await page.getByLabel("Shares", { exact: true }).fill("13");
  await saving;
  await page
    .getByRole("button", { name: "Preview buy order", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Place buy order", exact: true })
    .click();
  await expect(page.getByRole("dialog")).toContainText("Submitting");
  release();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  const run = (await (await page.request.get("/api/v1/simulator")).json()).run;
  expect(run.orders).toHaveLength(1);
  expect(run.orders[0].quantity).toBe(13);
});

test("simulated newsroom, company statements and performance analytics follow the replay clock", async ({
  page,
}) => {
  await open(page);
  await page.getByLabel("New simulation run").click();
  // A pinned market pins its news schedule and reported quarters with it.
  await page.getByLabel("Market seed (optional)").fill("4242");
  await page.getByRole("button", { name: "Create new paper account" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await page
    .locator(".sim-sidebar-tabs")
    .getByRole("button", { name: "News", exact: true })
    .click();
  const feed = page.getByRole("region", { name: "Simulated news feed" });
  await expect(feed.locator(".sim-sim-badge")).toHaveText("SIMULATED");
  await expect(feed).toContainText("fictional companies, fictional headlines");
  const headlines = feed.locator(".sim-news-headline");
  await expect(headlines.first()).toBeVisible();
  const latest = await headlines.first().innerText();
  await advance(page, "Jump forward by one session");
  // A session of replay releases new headlines, so the feed leads with another.
  await expect
    .poll(async () => await headlines.first().innerText())
    .not.toBe(latest);
  await page.getByRole("tab", { name: "Company", exact: true }).click();
  const company = page.getByRole("region", { name: "Company financials" });
  await expect(company).toContainText("Novara Microsystems");
  await expect(company.locator(".sim-sim-badge")).toHaveText("SIMULATED");
  await company
    .getByRole("button", { name: "Income statement", exact: true })
    .click();
  await expect(
    company.locator(".sim-statement thead th", { hasText: /^Q[1-4] \d{4}$/ }),
  ).not.toHaveCount(0);
  await expect(
    company.getByRole("rowheader", { name: "Revenue", exact: true }),
  ).toBeVisible();
  await expect(company).toContainText(
    "Generated accounts for a fictional company",
  );
  await page
    .locator(".sim-sidebar-tabs")
    .getByRole("button", { name: "Trade", exact: true })
    .click();
  await submit(page);
  await advance(page);
  await page.getByRole("tab", { name: "Performance", exact: true }).click();
  const performance = page.getByRole("region", { name: "Account performance" });
  await expect(performance).toContainText("Equity");
  await expect(performance).toContainText("Win rate");
  await expect(
    performance.locator("tbody tr", { hasText: "NVRA" }),
  ).toHaveCount(1);
  const filled = await account(page);
  expect(filled.positions[0].quantity).toBe(10);
});

test("monitor windows add tools beside the chart and survive a reload", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await open(page);

  // One window by default: the chart alone, exactly as before.
  await expect(page.locator(".sim-monitor-pane")).toHaveCount(0);

  const tape = page.waitForResponse(
    (r) => r.url().includes("/monitor?") && r.status() === 200,
  );
  await page
    .getByRole("group", { name: "Monitor windows" })
    .getByText("2")
    .click();
  await tape;
  const second = page.getByRole("region", { name: /^Monitor 2:/ });
  await expect(second).toBeVisible();
  await expect(
    second.locator(".sim-tape-table tbody tr").first(),
  ).toBeVisible();
  // A print's price is a real number the tape shows against the clock.
  await expect(
    second.locator(".sim-tape-table tbody tr").first(),
  ).toContainText("$");

  // A third window is independent of the second.
  await page
    .getByRole("group", { name: "Monitor windows" })
    .getByText("3")
    .click();
  const third = page.getByRole("region", { name: /^Monitor 3:/ });
  await expect(third).toBeVisible();
  await expect(third.locator(".sim-heat-cell").first()).toBeVisible();
  await page.getByLabel("Tool for monitor 3").selectOption("screener");
  await expect(third.getByLabel("Screen")).toBeVisible();
  await third.getByLabel("Screen").selectOption("oversold");
  await expect(third).toContainText("RSI under 30");

  // Clicking a company in a tool moves the whole terminal to it.
  await page.getByLabel("Tool for monitor 2").selectOption("quotes");
  const symbol = await second
    .locator(".sim-monitor-table tbody tr td button")
    .first()
    .textContent();
  await second.locator(".sim-monitor-table tbody tr td button").first().click();
  await expect(page.locator(".sim-symbol-details")).toContainText(
    symbol!.trim(),
  );

  // The layout is stored with the rest of the workspace, not in the browser.
  const saved = page.waitForResponse(
    (r) => r.url().endsWith("/preferences") && r.request().method() === "PUT",
  );
  await saved;
  await page.reload();
  await expect(page.getByRole("region", { name: /^Monitor 2:/ })).toBeVisible();
  await expect(page.getByRole("region", { name: /^Monitor 3:/ })).toBeVisible();
  await expect(page.getByLabel("Tool for monitor 2")).toHaveValue("quotes");
  await expect(page.getByLabel("Tool for monitor 3")).toHaveValue("screener");

  // Advancing the clock regenerates every open tool.
  const refreshed = page.waitForResponse((r) => r.url().includes("/monitor?"));
  await advance(page);
  expect((await refreshed).status()).toBe(200);
  expect(errors).toEqual([]);
});

test("a bracket entry places both exits and arms them when it fills", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await open(page);
  const run = await account(page);
  const last = quoteFor(run, "NVRA").close;

  await page.locator(".sim-quick-trade .buy").click();
  await page.getByLabel("Attach exits to this entry").check();
  await page.getByLabel("Take profit").fill((last * 1.03).toFixed(2));
  await page.getByLabel("Stop loss").fill((last * 0.97).toFixed(2));
  await expect(page.locator(".sim-bracket")).toContainText("Risking");
  await expect(page.locator(".sim-bracket")).toContainText(":1");

  // The preview says what is actually being sent.
  await page
    .getByRole("button", { name: "Preview buy order", exact: true })
    .click();
  await expect(page.getByRole("dialog")).toContainText("Two exits go with it");
  await page
    .getByRole("button", { name: "Place buy order", exact: true })
    .click();
  await expect(page.getByRole("dialog")).not.toBeVisible();

  // Both legs are in the blotter, held rather than working.
  await page.getByRole("tab", { name: /^Open orders/ }).click();
  await expect(page.locator(".sim-order-status.held")).toHaveCount(2);
  await expect(page.locator("tbody")).toContainText("Take profit");
  await expect(page.locator("tbody")).toContainText("Stop loss");

  // The entry fills and both exits arm for what it bought.
  await advance(page);
  await expect(page.locator(".sim-order-status.held")).toHaveCount(0);
  await expect(page.locator(".sim-order-status.working")).toHaveCount(2);

  // A stop above the entry is refused before anything is sent.
  await page
    .getByRole("button", { name: /^Trade/ })
    .first()
    .click();
  await page.getByLabel("Stop loss").fill((last * 1.2).toFixed(2));
  await expect(page.locator(".sim-validation")).toContainText(
    "below the entry it protects",
  );
  await expect(
    page.getByRole("button", { name: "Preview buy order", exact: true }),
  ).toBeDisabled();
  expect(errors).toEqual([]);
});

test("a trailing stop follows the price up and is shown with its trail", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await open(page);
  await page.locator(".sim-quick-trade .buy").click();
  await page.getByLabel("Shares", { exact: true }).fill("20");
  await submit(page);
  await advance(page);

  await page.getByRole("button", { name: "Sell", exact: true }).click();
  await page.getByLabel("Order type").selectOption("trailing_stop");
  await page.getByLabel("Shares", { exact: true }).fill("20");
  await page.getByLabel("Trail (% below the high)").fill("4");
  await page
    .getByRole("button", { name: "Preview sell order", exact: true })
    .click();
  await expect(page.getByRole("dialog")).toContainText("Trailing 4%");
  await page
    .getByRole("button", { name: "Place sell order", exact: true })
    .click();
  await expect(page.getByRole("dialog")).not.toBeVisible();

  await page.getByRole("tab", { name: /^Open orders/ }).click();
  await expect(page.locator("tbody")).toContainText("4% trail");
  await expect(page.locator("tbody")).toContainText("trailing-stop");
  expect(errors).toEqual([]);
});

test("a margin account sells short, carries the borrow, and buys it back", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await open(page);

  // A cash account says so, and refuses a sale it cannot cover.
  await expect(page.locator(".sim-account-metrics")).not.toContainText(
    "MARGIN",
  );

  await page.getByLabel("New simulation run").click();
  await page.getByLabel("Account type").selectOption("margin");
  await page.getByRole("button", { name: "Create new paper account" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await expect(page.locator(".sim-account-metrics")).toContainText("MARGIN");
  await expect(page.locator(".sim-account-metrics")).toContainText(
    "Buying power",
  );

  await page.locator(".sim-quick-trade .sell").click();
  await page.getByLabel("Shares", { exact: true }).fill("40");
  // Selling stock it does not own is borrowing, and the ticket says so.
  await expect(page.locator(".sim-ticket")).toContainText("This sale borrows");
  await expect(page.locator(".sim-ticket")).toContainText("40 shares");
  await expect(page.locator(".sim-ticket")).toContainText("40 shares short");
  await submit(page, "sell");
  await advance(page);

  await page.getByRole("tab", { name: /^Positions/ }).click();
  const position = page
    .getByRole("tabpanel", { name: "Positions" })
    .locator("tbody tr")
    .first();
  await expect(position).toContainText("-40");
  await expect(page.locator(".sim-account-metrics")).not.toContainText(
    "Gross $0.00",
  );

  // Close buys the borrowed stock back rather than selling more of it.
  await position.getByRole("button", { name: "Close", exact: true }).click();
  await expect(page.locator(".sim-ticket")).toContainText("Preview buy order");
  await submit(page, "buy");
  await advance(page);
  await page.getByRole("tab", { name: /^Positions/ }).click();
  await expect(
    page.getByRole("tabpanel", { name: "Positions" }).locator("tbody tr"),
  ).toHaveCount(0);
  expect(errors).toEqual([]);
});

test("the market flow pane shows other desks trading the same bars", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await open(page);

  await page
    .getByRole("group", { name: "Monitor windows" })
    .getByText("2")
    .click();
  const pane = page.getByRole("region", { name: /^Monitor 2:/ });
  await page.getByLabel("Tool for monitor 2").selectOption("crowd");
  await expect(pane).toContainText("they do not move prices");
  const rows = pane.locator(".sim-crowd-table tbody tr");
  await expect(rows.first()).toBeVisible();

  // Every row names a desk, a side and a size.
  const first = rows.first();
  await expect(first).toContainText(/BUY|SELL/);
  await expect(pane).toContainText(/filled ·/);

  // Advancing the clock brings new flow with it.
  const before = await rows.first().textContent();
  const refreshed = page.waitForResponse((r) => r.url().includes("/monitor?"));
  await page.getByLabel("Jump forward by one session").click();
  expect((await refreshed).status()).toBe(200);
  await expect.poll(async () => rows.first().textContent()).not.toBe(before);
  expect(errors).toEqual([]);
});

test("the clock stops at an event and asks for a decision", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await open(page);

  // Off by default: a jump runs its whole length, as it always has.
  await expect(page.getByLabel("Stop the replay on")).toHaveValue("off");
  const opening = (await account(page)).cursor;
  await page.getByLabel("Jump forward by one hour").click();
  await expect
    .poll(async () => (await account(page)).cursor)
    .toBe(opening + 60);
  await expect(page.getByRole("alert", { name: "Replay stopped" })).toHaveCount(
    0,
  );

  // Switched on, the next fill cuts the jump short.
  await page.getByLabel("Stop the replay on").selectOption("on");
  await page.locator(".sim-quick-trade .buy").click();
  await page.getByLabel("Shares", { exact: true }).fill("5");
  await submit(page);
  const resumed = (await account(page)).cursor;
  await page.getByLabel("Jump forward by one session").click();

  const card = page.getByRole("alert", { name: "Replay stopped" });
  await expect(card).toBeVisible();
  await expect(card).toContainText("Your order filled");
  await expect(card).toContainText("still to run");
  // It stopped on the fill, far short of the 390 bars asked for.
  expect((await account(page)).cursor).toBe(resumed + 1);

  // Deciding clears it and records what was known at the time.
  page.once(
    "dialog",
    (d) => void d.accept("Entry as planned; stop stays where it is."),
  );
  await card.getByRole("button", { name: "Hold, and say why" }).click();
  await expect(card).toHaveCount(0);
  const state = await account(page);
  expect(state.interrupted).toBeNull();
  expect(state.decisions.at(-1).note).toContain("Entry as planned");
  expect(state.decisions.at(-1).choice).toBe("hold");
  expect(errors).toEqual([]);
});

test("a campaign opens its stages as the week runs", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/simulator?mission=desk-week");
  await expect(page.getByTestId("trading-terminal")).toBeVisible();
  await page.getByLabel("New simulation run").click();
  await expect(page.getByLabel("Practice mission (optional)")).toHaveValue(
    "desk-week",
  );
  // The mission declares its account, so the picker is not the learner's to set.
  await expect(page.getByLabel("Account type")).toBeDisabled();
  await page.getByRole("button", { name: "Create new paper account" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();

  const mission = page.locator(".sim-mission");
  await mission.locator("summary").click();
  await expect(mission).toContainText("A week on the desk");
  await expect(mission).toContainText("Stage 1: Open the week");
  // A stage the clock has not reached is locked, not failed.
  await expect(mission).toContainText("Stage 2: Answer the tape");
  await expect(mission).toContainText("opens in 390 bars");
  await expect(mission).toContainText("of 9 objectives");

  await page.getByLabel("Jump forward by one session").click();
  await expect(mission).not.toContainText("opens in 390 bars");
  await expect(mission).toContainText("Stage 3: Stand in front of the print");
  expect(errors).toEqual([]);
});
