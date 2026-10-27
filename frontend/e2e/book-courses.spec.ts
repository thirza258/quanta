import type { Track } from "@/features/learning/model/types";
import { expect, test } from "@playwright/test";
import { readFileSync } from "node:fs";

const catalog = JSON.parse(
  readFileSync(
    new URL("../../content/catalog/curriculum.json", import.meta.url),
    "utf8",
  ),
) as Track[];
const courses = catalog.filter(
  (track) => track.parts && track.studyType !== "applied",
);

for (const course of courses) {
  test(`${course.title}: reading map, assignment, practice, and runnable capstone`, async ({
    page,
  }) => {
    const errors: string[] = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await page.goto(`/curriculum/${course.id}`);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText(
      course.title,
    );
    await expect(page.locator(".module-row")).toHaveCount(
      course.modules.length,
    );
    await expect(
      page.getByRole("navigation", { name: "Book units" }).getByRole("link"),
    ).toHaveCount(course.parts!.length);
    await expect(page.locator(".exam-card")).toHaveCount(5);
    await page
      .getByRole("navigation", { name: "Book units" })
      .getByRole("link")
      .last()
      .click();
    await expect(page).toHaveURL(
      new RegExp(`#unit-${course.parts!.at(-1)!.id}$`),
    );
    const capstone = course.modules.at(-1)!;
    await page.locator(`.module-row[href="/learn/${capstone.id}"]`).click();
    await expect(page.locator(".learning-room")).toHaveClass(/view-reader/);
    await expect(
      page.getByRole("complementary", { name: "Book reading" }),
    ).toContainText(capstone.reading!);
    await expect(page.locator(".katex-error")).toHaveCount(0);
    await expect(
      page.getByRole("button", { name: "Mark module complete", exact: true }),
    ).toBeDisabled();
    await page.getByText("Review the worked solution", { exact: true }).click();
    await expect(page.locator(".lesson-assignment details")).toContainText(
      capstone.assignment!.solution,
    );
    await page.getByRole("button", { name: "Write in notebook" }).click();
    await expect(page.getByLabel("Research note")).toHaveValue(
      new RegExp("Assignment:"),
    );
    await page
      .getByLabel("Research note")
      .fill(
        `My ${course.title} capstone: verify assumptions before accepting the estimate.`,
      );
    await page.getByRole("button", { name: "Save to notebook" }).click();
    for (let i = 0; i < capstone.exercises!.length; i++) {
      const card = page.locator(".exercise-card").nth(i);
      await card.getByRole("radio").nth(capstone.exercises![i].answer).check();
      const grading = page.waitForResponse(
        (response) =>
          response.url().includes(`/exercises/${capstone.id}/submit`) &&
          response.request().method() === "POST",
      );
      await card.getByRole("button", { name: "Check answer" }).click();
      expect((await grading).status()).toBe(200);
      await expect(card.getByRole("status")).toContainText("That’s right.");
    }
    await page
      .getByRole("button", { name: "Mark module complete", exact: true })
      .click();
    await page.reload();
    await expect(
      page.getByRole("button", { name: "Completed · undo" }),
    ).toBeVisible();
    await page.getByRole("button", { name: "Run in sandbox" }).click();
    await expect(
      page.getByRole("textbox", { name: "Python strategy editor" }),
    ).toBeVisible();
    await page.getByRole("button", { name: "Run experiment" }).click();
    await expect(page.locator(".console-output")).toContainText(
      course.number === 1 ? "NCAV per share: 5.0" : "t statistic: 0.923",
    );
    await page.goto("/notebook");
    await expect(page.locator(".note-card")).toContainText(
      `My ${course.title} capstone`,
    );
    expect(errors).toEqual([]);
  });

  test(`${course.title}: checkpoint continues to the next unit`, async ({
    page,
  }) => {
    const checkpoint = course.exams[0];
    await page.goto(`/exams/${checkpoint.id}`);
    await page.getByRole("button", { name: "Start exam", exact: true }).click();
    for (let i = 0; i < checkpoint.questions.length; i++) {
      await page
        .getByRole("button", { name: new RegExp(`^Question ${i + 1},`) })
        .click();
      await page.getByRole("radio").nth(checkpoint.questions[i].answer).check();
    }
    await page
      .locator(".exam-navigation")
      .getByRole("button", { name: "Review answers" })
      .click();
    await page
      .getByRole("button", { name: "Submit exam", exact: true })
      .click();
    await expect(page.locator(".exam-score")).toContainText("100%");
    const next =
      course.modules[
        course.modules.findIndex(
          (module) => module.id === checkpoint.moduleIds.at(-1),
        ) + 1
      ];
    await page
      .getByRole("link", { name: `Continue to ${next.title}`, exact: true })
      .click();
    await expect(page).toHaveURL(
      new RegExp(`/learn/${next.id.replace(".", "\\.")}$`),
    );
  });

  test(`${course.title}: final exam submits and persists a server-graded result`, async ({
    page,
  }) => {
    const exam = course.exams.at(-1)!;
    await page.goto(`/exams/${exam.id}`);
    await page.getByRole("button", { name: "Start exam", exact: true }).click();
    for (let i = 0; i < exam.questions.length; i++) {
      await page
        .getByRole("button", { name: new RegExp(`^Question ${i + 1},`) })
        .click();
      await page.getByRole("radio").nth(exam.questions[i].answer).check();
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
    const result = await (await submission).json();
    expect(result).toMatchObject({
      score: 100,
      passed: true,
      // Each final's version is bumped when its course grows, so read it per exam.
      version: exam.version,
      grading: "server",
    });
    await expect(page.locator(".exam-score")).toContainText("100%");
    await page.reload();
    await expect(page.locator(".exam-score")).toContainText("100%");
    await expect(page.locator(".exam-review-card .text-link")).toHaveCount(
      exam.questions.length,
    );
  });
}

test("both book courses remain readable on mobile", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  for (const course of courses) {
    await page.goto(`/curriculum/${course.id}`);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText(
      course.title,
    );
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth + 1,
      ),
    ).toBe(true);
    await page
      .getByRole("link", { name: "Start this course", exact: true })
      .click();
    await expect(page.locator(".lesson-reading")).toBeVisible();
    await page.locator(".lesson-assignment").scrollIntoViewIfNeeded();
    await expect(
      page.getByRole("button", { name: "Write in notebook" }),
    ).toBeVisible();
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth + 1,
      ),
    ).toBe(true);
  }
});

test("every expanded lesson renders its mathematics, assignment, and practice", async ({
  page,
}) => {
  test.setTimeout(120000);
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  for (const lesson of courses.flatMap((course) => course.modules)) {
    await page.goto(`/learn/${lesson.id}`);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText(
      lesson.title,
    );
    await expect(page.locator(".katex-error")).toHaveCount(0);
    await expect(page.locator(".katex-display")).toHaveCount(
      // One lesson equation, plus any in the research extension.
      (lesson.content.split("$$").length - 1) / 2,
    );
    await expect(page.locator(".exercise-card")).toHaveCount(2);
    await expect(page.locator(".lesson-assignment")).toContainText(
      lesson.assignment!.prompt,
    );
  }
  expect(errors).toEqual([]);
});
