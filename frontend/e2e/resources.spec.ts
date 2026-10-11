import { expect, test } from "@playwright/test";
import {
  learningResources,
  topicLabels,
} from "../src/features/references/model/resources";

test("learning resources: browse from free to paid, filter, search and follow links", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByRole("complementary", { name: "Workspace sidebar" })
    .getByRole("link", { name: "Learning resources", exact: true })
    .click();
  await expect(page).toHaveURL(/\/resources$/);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Learning resources",
  );
  const cards = page.locator(".resource-card");
  await expect(cards).toHaveCount(learningResources.length);
  await expect(page.getByRole("heading", { level: 2 })).toHaveText([
    /^Free\s*\d+$/,
    /^Free with paid options\s*\d+$/,
    /^Paid\s*\d+$/,
  ]);
  for (const resource of learningResources) {
    const card = cards.filter({
      has: page.getByRole("heading", { name: resource.title, exact: true }),
    });
    await expect(
      card.getByRole("link", { name: "Visit official page" }),
    ).toHaveAttribute("href", resource.url);
    await expect(
      card.getByRole("link", { name: "Visit official page" }),
    ).toHaveAttribute("target", "_blank");
  }

  await page.getByRole("button", { name: "Free", exact: true }).click();
  const free = learningResources.filter((r) => r.tier === "free");
  await expect(cards).toHaveCount(free.length);
  await expect(page.getByRole("status")).toContainText(
    `${free.length} resources · free`,
  );

  await page.getByRole("button", { name: "All", exact: true }).click();
  await page
    .getByRole("combobox", { name: "Filter by topic" })
    .selectOption("crypto");
  await expect(cards).toHaveCount(
    learningResources.filter((r) => r.topics.includes("crypto")).length,
  );
  await expect(page.getByRole("status")).toContainText(topicLabels.crypto);

  await page
    .getByRole("combobox", { name: "Filter by topic" })
    .selectOption("all");
  await page.getByRole("textbox", { name: "Search resources" }).fill("bitcoin");
  await expect(
    page.getByRole("heading", {
      name: "Mastering Bitcoin (3rd edition)",
      exact: true,
    }),
  ).toBeVisible();
  await page
    .getByRole("textbox", { name: "Search resources" })
    .fill("no-such-resource");
  await expect(
    page.getByRole("heading", { name: "No matching resources" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Show all resources" }).click();
  await expect(cards).toHaveCount(learningResources.length);

  const statsCard = cards.filter({
    has: page.getByRole("heading", {
      name: "statsmodels documentation",
      exact: true,
    }),
  });
  await statsCard
    .getByRole("link", {
      name: "Financial econometrics & factor models",
      exact: true,
    })
    .click();
  await expect(page).toHaveURL(/\/curriculum\/econometrics$/);
});

test("learning resources stay readable on a phone", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/resources");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth + 1,
    ),
  ).toBe(true);
  await page.goto("/library");
  await page.getByRole("link", { name: "Browse learning resources" }).click();
  await expect(page).toHaveURL(/\/resources$/);
});
