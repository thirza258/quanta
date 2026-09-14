import { test, expect } from "@playwright/test";

test("complete a lesson, run and restore an experiment, and retain a research note", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toContainText(
    "A little theory",
  );
  await page.getByRole("link", { name: "Start learning", exact: true }).click();
  await expect(page).toHaveURL(/\/learn\/0\.1$/);
  // Existing lessons and saved research still use their original URLs.
  await page.goto("/learn/1.1");
  await expect(
    page.getByRole("textbox", { name: "Python strategy editor" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Run experiment" }).click();
  await expect(page.locator(".console-output")).toContainText(
    "Margin of safety: 40.0 %",
  );
  await page.getByRole("button", { name: "Equity curve", exact: true }).click();
  await expect(page.locator(".financial-chart canvas").first()).toBeVisible();
  await page.getByRole("button", { name: "Returns", exact: true }).click();
  await expect(page.locator(".heatmap-row")).toHaveCount(3);
  await page.getByRole("button", { name: "Save", exact: true }).click();
  await page.getByLabel("Experiment name").fill("Margin of safety research");
  await page
    .getByRole("button", { name: "Save experiment", exact: true })
    .click();
  await page.getByRole("radio", { name: "B 40%" }).check();
  await page.getByRole("button", { name: "Check answer", exact: true }).click();
  await expect(page.locator(".quiz-feedback")).toContainText("That’s right.");
  await page
    .getByRole("button", { name: "Mark module complete", exact: true })
    .click();
  await page.getByRole("button", { name: "Add a note", exact: true }).click();
  await page
    .getByLabel("Research note")
    .fill(
      "A margin of safety depends on the conservatism of the value estimate.",
    );
  await page.getByRole("button", { name: "Save to notebook" }).click();
  await page.reload();
  await expect(
    page.getByRole("button", { name: "Completed · undo" }),
  ).toBeVisible();
  await page
    .getByRole("link", { name: "Saved experiments", exact: false })
    .first()
    .click();
  await page.getByRole("link", { name: "Margin of safety research" }).click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Margin of safety research",
  );
  await page.getByRole("button", { name: "Run experiment" }).click();
  await expect(page.locator(".console-output")).toContainText(
    "Margin of safety: 40.0 %",
  );
  await page.getByRole("link", { name: "My notebook", exact: true }).click();
  await expect(page.locator(".note-card")).toContainText(
    "conservatism of the value estimate",
  );
  await expect(page.locator(".note-card")).toHaveCount(1);
  expect(errors).toEqual([]);
});

test("account workspace survives logout, login, and a fresh browser context", async ({
  page,
  browser,
}) => {
  const email = `quanta-e2e-${Date.now()}@example.com`,
    password = "quanta-test-password-123";
  await page.goto("/");
  await page
    .getByRole("button", { name: "Create account", exact: true })
    .click();
  await page.getByLabel("Your name").fill("Test Researcher");
  await page.getByLabel("Email address").fill(email);
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Create your workspace" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await page.getByRole("link", { name: "My notebook", exact: true }).click();
  await page.getByRole("button", { name: "New note", exact: true }).click();
  await page.getByLabel("Title", { exact: true }).fill("Durable account note");
  await page
    .getByLabel("Your note", { exact: true })
    .fill("This must survive a new browser session.");
  const saved = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/v1/workspace") &&
      r.request().method() === "PUT" &&
      r.status() === 200,
  );
  await page.getByRole("button", { name: "Save note", exact: true }).click();
  await saved;
  const context = await browser.newContext({
    baseURL: process.env.TEST_URL || "http://127.0.0.1:5174",
  });
  const other = await context.newPage();
  await other.goto("/");
  await other
    .getByRole("button", { name: "Create account", exact: true })
    .click();
  await other.getByRole("button", { name: "Sign in", exact: true }).click();
  await other.getByLabel("Email address").fill(email);
  await other.getByLabel("Password", { exact: true }).fill(password);
  await other
    .getByRole("button", { name: "Sign in", exact: true })
    .last()
    .click();
  await expect(other.getByRole("dialog")).not.toBeVisible();
  await other.getByRole("link", { name: "My notebook", exact: true }).click();
  await expect(other.locator(".note-card")).toContainText(
    "Durable account note",
  );
  await other.getByRole("button", { name: "Sign out", exact: true }).click();
  await expect(other.locator(".note-card")).toHaveCount(0);
  await context.close();
});

test("valuation, factors, mock broker and AMM produce observable results", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/lab?tool=valuation");
  await expect(page.locator(".valuation-hero-number strong")).toHaveText(
    "$6.90",
  );
  await page.getByLabel("Market price / share").fill("10");
  await expect(page.locator(".screen-status")).toContainText("Does not pass");
  await page
    .getByRole("button", { name: "Factor studio", exact: true })
    .click();
  await page.getByRole("button", { name: "Fit factor model" }).click();
  await expect(page.locator(".factor-metrics strong").first()).not.toHaveText(
    "—",
  );
  await expect(page.locator("tbody tr")).toHaveCount(4);
  await page
    .getByRole("button", { name: "Paper trading", exact: true })
    .click();
  await page.getByLabel("Order quantity").fill("150");
  await page.getByRole("button", { name: "Submit buy order" }).click();
  await expect(page.locator(".order-log")).toContainText("partially filled");
  await expect(page.locator(".order-log")).toContainText("100 filled");
  await page.getByLabel("Price age (seconds)").fill("65");
  await page.getByRole("button", { name: "Submit buy order" }).click();
  await expect(page.locator(".order-log")).toContainText("Price data is stale");
  await page
    .getByRole("button", { name: "AMM simulator", exact: true })
    .click();
  await expect(page.locator(".swap-output strong")).toContainText("1813.22");
  await expect(page.locator(".valuation-metrics")).toContainText("-5.72%");
  expect(errors).toEqual([]);
});

test("mobile navigation, search and dark theme stay usable without overflow", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await expect(page.locator("h1")).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await page.getByRole("button", { name: "Open navigation" }).click();
  await page.getByRole("button", { name: "Find a lesson" }).click();
  await page
    .getByPlaceholder("Try margin of safety, regression, or AMMs…")
    .fill("impermanent");
  await page.getByRole("button", { name: /AMMs & impermanent loss/ }).click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "AMMs & impermanent loss",
  );
  await page.getByRole("button", { name: "Switch to dark theme" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await page.getByRole("button", { name: "Reading view" }).click();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
});

test("unsynced account edits survive a reload and retry", async ({ page }) => {
  await page.goto("/");
  await page
    .getByRole("button", { name: "Create account", exact: true })
    .click();
  await page.getByLabel("Your name").fill("Recovery Researcher");
  await page
    .getByLabel("Email address")
    .fill(`recovery-${Date.now()}@example.com`);
  await page
    .getByLabel("Password", { exact: true })
    .fill("recovery-test-password");
  await page.getByRole("button", { name: "Create your workspace" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await page.route("**/api/v1/workspace", async (route) => {
    if (route.request().method() === "PUT")
      await route.fulfill({
        status: 503,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Simulated unavailable storage" }),
      });
    else await route.continue();
  });
  await page.getByRole("link", { name: "My notebook", exact: true }).click();
  await page.getByRole("button", { name: "New note", exact: true }).click();
  await page.getByLabel("Title", { exact: true }).fill("Recover this draft");
  await page
    .getByLabel("Your note", { exact: true })
    .fill("My local work must never be discarded when sync fails.");
  await page.getByRole("button", { name: "Save note", exact: true }).click();
  await expect(page.getByRole("alert")).toContainText(
    "Simulated unavailable storage",
  );
  await page.unroute("**/api/v1/workspace");
  const saved = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/v1/workspace") &&
      r.request().method() === "PUT" &&
      r.ok(),
  );
  await page.reload();
  await expect(page.locator(".note-card")).toContainText("Recover this draft");
  await saved;
  const response = await page.request.get("/api/v1/workspace");
  expect((await response.json()).state.notes[0].title).toBe(
    "Recover this draft",
  );
});

test("conflicting account copies preserve local work until explicitly resolved", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByRole("button", { name: "Create account", exact: true })
    .click();
  await page.getByLabel("Your name").fill("Conflict Researcher");
  await page
    .getByLabel("Email address")
    .fill(`conflict-${Date.now()}@example.com`);
  await page
    .getByLabel("Password", { exact: true })
    .fill("conflict-test-password");
  const initialSave = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/v1/workspace") &&
      r.request().method() === "PUT" &&
      r.ok(),
  );
  await page.getByRole("button", { name: "Create your workspace" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await initialSave;
  const remote = await (await page.request.get("/api/v1/workspace")).json();
  remote.state.notes = [
    {
      id: "remote-note",
      title: "Server copy",
      body: "Saved in another session.",
      updatedAt: new Date().toISOString(),
    },
  ];
  expect(
    (await page.request.put("/api/v1/workspace", { data: remote })).ok(),
  ).toBeTruthy();
  await page.getByRole("link", { name: "My notebook", exact: true }).click();
  await page.getByRole("button", { name: "New note", exact: true }).click();
  await page.getByLabel("Title", { exact: true }).fill("Local copy");
  await page
    .getByLabel("Your note", { exact: true })
    .fill("Preserve this until I choose a copy.");
  await page.getByRole("button", { name: "Save note", exact: true }).click();
  await expect(page.getByRole("alert")).toContainText("another session");
  await page.reload();
  await expect(page.locator(".note-card")).toContainText("Local copy");
  const serverState = await (
    await page.request.get("/api/v1/workspace")
  ).json();
  expect(serverState.state.notes[0].title).toBe("Server copy");
  await page.getByRole("button", { name: "Open account", exact: true }).click();
  await page
    .getByRole("button", { name: "Resolve sync conflict", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Use account copy", exact: true })
    .click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await expect(page.locator(".note-card")).toContainText("Server copy");
  await expect(page.locator(".note-card")).not.toContainText("Local copy");
});
