import { expect, test } from "@playwright/test";

// Dollar prices previously became inline mathematics and swallowed sentence spaces.
test("currency remains ordinary prose while lesson equations still render", async ({
  page,
}) => {
  await page.goto("/learn/0.3");
  const example = page
    .locator(".prose p")
    .filter({ hasText: "Harbor Foods issues 100,000" });
  await expect(example).toContainText("at $20, raising $2 million");
  await expect(example).toContainText("for $21 each");
  await expect(example.locator(".katex")).toHaveCount(0);

  await page.goto("/learn/0.5");
  const returnExample = page
    .locator(".prose p")
    .filter({ hasText: "Buy 10 shares at $100" });
  await expect(returnExample).toContainText("$106 / $1,002");
  await expect(returnExample.locator(".katex")).toHaveCount(0);
  await expect(page.locator(".prose .katex").first()).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Build the return from cash movements" }),
  ).toBeVisible();
  await expect(page.locator(".prose")).toContainText(
    "the initial outlay used in the denominator",
  );

  await page.goto("/learn/13.1");
  const frictionParagraph = page
    .locator(".prose p")
    .filter({ hasText: "flat commission per order" });
  await expect(frictionParagraph).toContainText("($1 by default)");
  await expect(frictionParagraph).toContainText(
    "creates a fresh $100,000 account",
  );
  // $c$, $s$, $\sigma$, $\pi$ should be rendered as KaTeX elements inside the paragraph
  await expect(frictionParagraph.locator(".katex")).toHaveCount(4);
});

test("mobile lesson tables scroll by keyboard and numbered instructions retain their markers", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/learn/0.8");
  const list = page.locator(".prose ol");
  await expect(list).toHaveCSS("list-style-type", "decimal");
  await expect(list.locator("li")).toHaveCount(5);
  const tableRegion = page.getByRole("region", { name: "Lesson table" });
  await expect(tableRegion.getByRole("table")).toBeVisible();
  await expect(tableRegion.getByRole("columnheader")).toHaveCount(2);
  await tableRegion.focus();
  await expect(tableRegion).toBeFocused();
  await page.keyboard.press("ArrowRight");
  await expect
    .poll(() => tableRegion.evaluate((element) => element.scrollLeft))
    .toBeGreaterThan(0);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  expect(
    await list.evaluate((element) => getComputedStyle(element).fontSize),
  ).toBe(
    await page
      .locator(".prose p")
      .first()
      .evaluate((element) => getComputedStyle(element).fontSize),
  );
});

test("curriculum search recovers from no results and mobile lesson navigation stays available", async ({
  page,
}) => {
  await page.setViewportSize({ width: 320, height: 740 });
  await page.goto("/curriculum");
  await page
    .getByRole("textbox", { name: "Search curriculum" })
    .fill("no-such-learning-topic");
  await expect(
    page.getByRole("heading", { name: "No matching tracks" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Show all courses" }).click();
  await expect(page.locator(".track-card")).toHaveCount(15);
  await page.getByRole("button", { name: "Not started", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Not started", exact: true }),
  ).toHaveAttribute("aria-pressed", "true");
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);

  await page.goto("/learn/1.1");
  const modules = page.getByRole("combobox", { name: "Navigate to module" });
  await expect(modules).toBeVisible();
  await modules.selectOption("1.6");
  await expect(page).toHaveURL(/\/learn\/1\.6$/);
  await expect(
    page.getByRole("button", { name: "Reading view", exact: true }),
  ).toHaveAttribute("aria-pressed", "true");
  await page.getByRole("button", { name: "Switch to dark theme" }).click();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
});
