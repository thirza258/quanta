import { test, expect } from "@playwright/test";
import { readFileSync } from "node:fs";
import type { Track } from "../src/lib/types";

const catalog = JSON.parse(
  readFileSync(new URL("../src/data/curriculum.json", import.meta.url), "utf8"),
) as Track[];
const course = catalog.find((track) => track.id === "stock-bots")!;

test("bot course: plan, project download, practice, notebook, and runnable worksheet", async ({
  page,
}) => {
  await page.goto(`/curriculum/${course.id}`);
  await expect(
    page.getByRole("heading", { name: "Your course plan" }),
  ).toBeVisible();
  await expect(
    page.getByRole("navigation", { name: "Course units" }).getByRole("link"),
  ).toHaveCount(12);
  await expect(page.locator(".module-row")).toHaveCount(48);
  await expect(page.locator(".exam-card")).toHaveCount(12);
  const download = page.waitForEvent("download");
  await page
    .getByRole("link", { name: "Download the Python paper-bot lab" })
    .click();
  const file = await download;
  expect(file.suggestedFilename()).toBe("paper_bot_lab.py");
  const source = readFileSync((await file.path())!, "utf8");
  expect(source).toContain("class PaperBot:");
  expect(source).toContain("def ridge_walkforward():");
  await page.goto("/learn/5.29");
  await expect(page.locator(".learning-room")).toHaveClass(/view-reader/);
  await expect(
    page.getByRole("complementary", { name: "Applied study" }),
  ).toBeVisible();
  const lesson = course.modules.find((item) => item.id === "5.29")!;
  for (const [index, question] of lesson.exercises!.entries()) {
    const card = page.locator(".exercise-card").nth(index);
    await card.getByRole("radio").nth(question.answer).check();
    await card.getByRole("button", { name: "Check answer" }).click();
    await expect(card.getByRole("status")).toContainText("That’s right.");
  }
  await page
    .getByRole("button", { name: "Mark module complete", exact: true })
    .click();
  await page.reload();
  await expect(
    page.getByRole("button", { name: "Completed · undo" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Write in notebook" }).click();
  await expect(page.getByLabel("Research note")).toHaveValue(/Assignment:/);
  await page.getByRole("button", { name: "Save to notebook" }).click();
  await page.getByRole("button", { name: "Run in sandbox" }).click();
  await page.getByRole("button", { name: "Run experiment" }).click();
  await expect(page.locator(".console-output")).toContainText(
    "Project equity: 10025.39",
  );
});

for (const exam of [course.exams[0], course.exams.at(-1)!]) {
  test(`bot assessment: ${exam.kind} grades and survives reload`, async ({
    page,
  }) => {
    await page.goto(`/exams/${exam.id}`);
    await page.getByRole("button", { name: "Start exam", exact: true }).click();
    for (const [index, question] of exam.questions.entries()) {
      await page
        .getByRole("button", { name: new RegExp(`^Question ${index + 1},`) })
        .click();
      await page.getByRole("radio").nth(question.answer).check();
    }
    await page
      .locator(".exam-navigation")
      .getByRole("button", { name: "Review answers" })
      .click();
    const submission = page.waitForResponse(
      (response) =>
        response.url().includes(`/exams/${exam.id}/submit`) &&
        response.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "Submit exam", exact: true })
      .click();
    expect(await (await submission).json()).toMatchObject({
      score: 100,
      passed: true,
      grading: "server",
      version: exam.version,
    });
    await page.reload();
    await expect(page.locator(".exam-score")).toContainText("100%");
    if (exam.kind === "checkpoint") {
      await page
        .getByRole("link", {
          name: "Continue to Rule-based strategy bots",
          exact: true,
        })
        .click();
      await expect(page).toHaveURL(/\/learn\/5\.2$/);
    }
  });
}

test("every bot lesson renders equations, assignment, practice, and its named sources", async ({
  page,
}) => {
  test.setTimeout(90000);
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  for (const lesson of course.modules) {
    await page.goto(`/learn/${lesson.id}`);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText(
      lesson.title,
    );
    await expect(page.locator(".katex-display")).toHaveCount(1);
    await expect(page.locator(".katex-error")).toHaveCount(0);
    await expect(page.locator(".exercise-card")).toHaveCount(2);
    await expect(page.locator(".lesson-assignment")).toContainText(
      lesson.assignment!.prompt,
    );
    const footer = page.getByRole("contentinfo", {
      name: "Sources and attribution",
    });
    for (const reference of lesson.references!) {
      await expect(
        footer.getByRole("link", { name: reference.title, exact: true }),
      ).toHaveAttribute("href", reference.url);
    }
  }
  expect(errors).toEqual([]);
});

test("sources appear across all page types, with readable mobile cards and headers", async ({
  page,
  request,
}) => {
  test.setTimeout(90000);
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  for (const route of [
    "/",
    "/curriculum",
    "/curriculum/security-analysis",
    "/learn/0.1",
    "/learn/1.24",
    "/learn/2.28",
    "/exams/stock-bots-final",
    "/lab",
    "/simulator",
    "/experiments",
    "/notebook",
    "/library",
    "/methodology",
    "/missing-page",
  ]) {
    await page.goto(route);
    const footer = page.getByRole("contentinfo", {
      name: "Sources and attribution",
    });
    await expect(footer).toContainText("independent learning project");
    expect(await footer.locator('a[href^="https://"]').count()).toBeGreaterThan(
      0,
    );
  }
  const notices = await request.get("/third-party-notices.txt");
  expect(notices.ok()).toBe(true);
  expect(await notices.text()).toContain("Copyright (с) 2025 TradingView");
  for (const width of [390, 768, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    for (const route of [
      "/curriculum",
      "/curriculum/security-analysis",
      "/curriculum/statistical-foundations",
      "/curriculum/stock-bots",
    ]) {
      await page.goto(route);
      await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth + 1,
        ),
      ).toBe(true);
      if (route === "/curriculum") {
        const boxes = await page.locator(".track-card").evaluateAll((cards) =>
          cards.map((card) => {
            const box = card.getBoundingClientRect();
            const metadata = card
              .querySelector(".track-assessment-meta")!
              .getBoundingClientRect();
            return {
              width: box.width,
              gap: box.bottom - metadata.bottom,
              overflow: card.scrollWidth > card.clientWidth + 1,
            };
          }),
        );
        expect(
          boxes.every(
            (box) => box.width >= 260 && box.gap >= 12 && !box.overflow,
          ),
        ).toBe(true);
      }
    }
  }
  expect(errors).toEqual([]);
});
