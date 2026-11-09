import { expect, test } from "@playwright/test";

test("register a hypothesis, let the red team attack it, document and reproduce it", async ({
  page,
}) => {
  test.setTimeout(150000);
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/research");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await page
    .getByRole("link", { name: "New experiment", exact: true })
    .first()
    .click();
  await expect(page).toHaveURL(/\/research\/new$/);
  await page.getByLabel("Title", { exact: true }).fill("E2E trend crossover");
  await page
    .getByLabel("Hypothesis", { exact: true })
    .fill(
      "A 20/150 moving-average crossover beats buy-and-hold on Sharpe after costs.",
    );
  await page.getByRole("button", { name: "Register & run" }).click();
  await expect(page).toHaveURL(/\/research\/[0-9a-f-]{36}$/);

  // The run is asynchronous: the page polls until the red team has reported.
  const verdict = page.getByText(/Research risk: (LOW|MEDIUM|HIGH)/).first();
  await expect(verdict).toBeVisible({ timeout: 90000 });
  await expect(page.locator("#red-team")).toContainText(
    "No look-ahead detected",
  );
  await expect(page.locator("#provenance")).toContainText("SHA-256");
  await expect(page.locator("#provenance")).toContainText("Canonical results");

  await page.getByLabel("Conclusion").fill("No edge.");
  await page.getByLabel("Limitations").fill("Synthetic data.");
  await page.getByRole("button", { name: "Reject", exact: true }).click();
  await page.getByRole("button", { name: "Save notebook" }).click();
  await expect(page.getByText("Saved", { exact: true }).first()).toBeVisible();

  await page.getByRole("button", { name: "Reproduce", exact: true }).click();
  await expect(
    page.getByText("Identical", { exact: true }).first(),
  ).toBeVisible({ timeout: 90000 });
  await expect(
    page.getByText("Reproducible", { exact: true }).first(),
  ).toBeVisible();

  await page.goto("/research");
  await expect(page.getByText("E2E trend crossover").first()).toBeVisible();
  expect(errors).toEqual([]);
});

test("the strategy lab hands its code to the research composer", async ({
  page,
}) => {
  await page.goto("/lab");
  await page.getByRole("button", { name: "Validate in research" }).click();
  await expect(page).toHaveURL(/\/research\/new$/);
  await expect(page.getByLabel("Title", { exact: true })).toBeVisible();
});
