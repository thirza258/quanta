import { test, expect, type Page } from "@playwright/test";
import { readFileSync } from "node:fs";
import type { Track } from "../src/lib/types";

const catalog = JSON.parse(
  readFileSync(new URL("../src/data/curriculum.json", import.meta.url), "utf8"),
) as Track[];

const course = catalog[0];
const checkpoint = course.exams[0];
const final = course.exams[1];

async function completePractice(page: Page, index: number) {
  const lesson = course.modules[index];
  await page.goto(`/learn/${lesson.id}`);
  await expect(page.locator(".learning-room")).toHaveClass(/view-reader/);
  const questions = lesson.exercises!;
  for (let i = 0; i < questions.length; i++) {
    const card = page.locator(".exercise-card").nth(i);
    await card.getByRole("radio").nth(questions[i].answer).check();
    await card.getByRole("button", { name: "Check answer" }).click();
    await expect(card.getByRole("status")).toContainText("That’s right.");
  }
  await page
    .getByRole("button", { name: "Mark module complete", exact: true })
    .click();
}

async function answerExam(
  page: Page,
  exam: typeof final,
  correctCount = exam.questions.length,
) {
  for (let i = 0; i < exam.questions.length; i++) {
    const q = exam.questions[i];
    await page
      .getByRole("button", { name: new RegExp(`^Question ${i + 1},`) })
      .click();
    await page
      .getByRole("radio")
      .nth(i < correctCount ? q.answer : (q.answer + 1) % q.options.length)
      .check();
  }
  await page
    .locator(".exam-navigation")
    .getByRole("button", { name: "Review answers" })
    .click();
}

test("beginner practice requires every answer and persists feedback and completion", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/");
  await page.getByRole("link", { name: "Start learning", exact: true }).click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "What investing and trading mean",
  );
  await expect(page.locator(".learning-room")).toHaveClass(/view-reader/);
  await expect(
    page.getByRole("textbox", { name: "Python strategy editor" }),
  ).toHaveCount(0);
  await expect(page.locator(".exercise-card")).toHaveCount(3);
  const complete = page.getByRole("button", {
    name: "Mark module complete",
    exact: true,
  });
  await expect(complete).toBeDisabled();
  // Learners can start with any question; later questions still count as activity.
  const second = page.locator(".exercise-card").nth(1);
  await second
    .getByRole("radio")
    .nth(course.modules[0].exercises![1].answer)
    .check();
  await second.getByRole("button", { name: "Check answer" }).click();
  await expect(second.getByRole("status")).toContainText("That’s right.");
  await page.goto("/curriculum");
  await page.getByRole("button", { name: "In progress", exact: true }).click();
  await expect(page.locator(".track-card")).toHaveCount(1);
  await expect(page.locator(".track-card")).toContainText(course.title);
  await page.getByRole("button", { name: "Not started", exact: true }).click();
  await expect(page.locator(".track-card")).toHaveCount(catalog.length - 1);
  await page.goto(`/learn/${course.modules[0].id}`);
  const first = page.locator(".exercise-card").first();
  await first.getByRole("radio").nth(0).check();
  await first.getByRole("button", { name: "Check answer" }).click();
  await expect(first.getByRole("status")).toContainText("Take another look.");
  await expect(complete).toBeDisabled();
  await first.getByRole("radio").nth(1).check();
  await first.getByRole("button", { name: "Check answer" }).click();
  await expect(first.getByRole("status")).toContainText("That’s right.");
  await expect(complete).toBeDisabled();
  await completePractice(page, 0);
  await page.reload();
  await expect(
    page.getByRole("button", { name: "Completed · undo" }),
  ).toBeVisible();
  await expect(page.locator(".quiz-feedback.correct")).toHaveCount(3);
  await page.getByRole("button", { name: "Run in sandbox" }).click();
  await page.getByRole("button", { name: "Run experiment" }).click();
  await expect(page.locator(".console-output")).toContainText(
    "Simple return (%): 10.0",
  );
  expect(errors).toEqual([]);
});

test("exam draft survives reload, blocks incomplete submission, reviews and retakes", async ({
  page,
}) => {
  await page.goto(`/exams/${checkpoint.id}`);
  await page.getByRole("button", { name: "Start exam", exact: true }).click();
  await page.getByRole("radio").nth(checkpoint.questions[0].answer).check();
  await page.reload();
  await expect(
    page.getByRole("radio").nth(checkpoint.questions[0].answer),
  ).toBeChecked();
  await page
    .locator(".exam-navigation")
    .getByRole("button", { name: "Review answers" })
    .click();
  await expect(
    page.getByRole("button", { name: "Submit exam" }),
  ).toBeDisabled();
  await expect(
    page.getByText("7 questions still need an answer."),
  ).toBeVisible();
  await answerExam(page, checkpoint, 5);
  await page.getByRole("button", { name: "Submit exam" }).click();
  await expect(page.getByRole("region", { name: "Exam result" })).toContainText(
    "62.5%",
  );
  await expect(
    page.getByRole("heading", { name: "Topics to revisit" }),
  ).toBeVisible();
  await expect(page.locator(".exam-review-card")).toHaveCount(8);
  await page.reload();
  await expect(page.getByRole("region", { name: "Exam result" })).toContainText(
    "62.5%",
  );
  await page.getByRole("button", { name: "Retake exam" }).click();
  await expect(page.getByRole("radio").first()).not.toBeChecked();
  await answerExam(page, checkpoint, 6);
  await page.getByRole("button", { name: "Submit exam" }).click();
  await expect(
    page.getByRole("heading", { name: "You passed this exam." }),
  ).toBeVisible();
  await expect(page.getByRole("region", { name: "Exam result" })).toContainText(
    "75%",
  );
  await expect(
    page.getByRole("region", { name: "Attempt history" }).locator("tbody tr"),
  ).toHaveCount(2);
  await page
    .getByRole("link", {
      name: "Continue to Returns, compounding, and trading costs",
    })
    .click();
  await expect(page).toHaveURL(/\/learn\/0\.5$/);
});

test("full fundamentals course finishes only after practice, checkpoint, and final", async ({
  page,
}) => {
  test.setTimeout(90000);
  for (let i = 0; i < course.modules.length; i++)
    await completePractice(page, i);
  await page.goto("/curriculum/trading-fundamentals");
  await expect(page.locator(".track-progress-row")).toContainText("80%");
  await expect(page.locator(".track-progress-row")).toContainText(
    "0 of 2 exams passed",
  );
  for (const exam of course.exams) {
    await page.goto(`/exams/${exam.id}`);
    await page.getByRole("button", { name: "Start exam", exact: true }).click();
    await answerExam(page, exam);
    await page.getByRole("button", { name: "Submit exam" }).click();
    await expect(
      page.getByRole("heading", { name: "You passed this exam." }),
    ).toBeVisible();
  }
  await expect(page.getByRole("region", { name: "Exam result" })).toContainText(
    "All lessons and exams in this course are complete.",
  );
  await page.getByRole("link", { name: "Next course", exact: true }).click();
  await expect(page).toHaveURL(/\/curriculum\/security-analysis$/);
  await page.goto("/curriculum/trading-fundamentals");
  await expect(page.locator(".track-progress-row")).toContainText("100%");
  await expect(page.locator(".track-progress-row")).toContainText(
    "Course complete",
  );
  await page.goto("/curriculum");
  await page.getByRole("button", { name: "Completed", exact: true }).click();
  await expect(page.locator(".track-card")).toHaveCount(1);
  await expect(page.locator(".track-card")).toContainText(
    "Trading & market fundamentals",
  );
});

test("account exam history survives workspace recovery and duplicate submission", async ({
  page,
  browser,
}) => {
  const email = `exam-${Date.now()}@example.com`;
  const password = "exam-account-password";
  await page.goto("/");
  await page
    .getByRole("button", { name: "Create account", exact: true })
    .click();
  await page.getByLabel("Your name").fill("Exam Learner");
  await page.getByLabel("Email address").fill(email);
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Create your workspace" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await page.goto(`/exams/${final.id}`);
  await page.getByRole("button", { name: "Start exam", exact: true }).click();
  await answerExam(page, final, 13);
  const submitted = page.waitForResponse(
    (response) =>
      response.url().endsWith(`/exams/${final.id}/submit`) && response.ok(),
  );
  await page.getByRole("button", { name: "Submit exam" }).click();
  const response = await submitted;
  const attempt = await response.json();
  expect(
    (
      await page.request.post(`/api/v1/exams/${final.id}/submit`, {
        data: JSON.parse(response.request().postData()!),
      })
    ).ok(),
  ).toBe(true);
  expect(
    (
      await (
        await page.request.get(`/api/v1/exams/${final.id}/attempts`)
      ).json()
    ).attempts,
  ).toHaveLength(1);
  await expect(page.locator(".exam-score")).toContainText("81.25%");
  await expect(
    page.getByTitle("Synced to your account", { exact: true }),
  ).toBeVisible();

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
  await other.goto(`/exams/${final.id}`);
  await expect(other.locator(".exam-score")).toContainText("81.25%");
  // The submission log also recovers a result if a workspace copy is missing it.
  const remote = await (await other.request.get("/api/v1/workspace")).json();
  remote.state.examAttempts = {};
  expect(
    (await other.request.put("/api/v1/workspace", { data: remote })).ok(),
  ).toBe(true);
  await other.reload();
  await expect(other.locator(".exam-score")).toContainText("81.25%");
  expect(
    (
      await (
        await other.request.get(`/api/v1/exams/${final.id}/attempts`)
      ).json()
    ).attempts[0].id,
  ).toBe(attempt.id);
  await other.getByRole("button", { name: "Sign out", exact: true }).click();
  await expect(
    other.getByRole("button", { name: "Start exam", exact: true }),
  ).toBeVisible();
  await expect(other.locator(".exam-score")).toHaveCount(0);
  await context.close();
});

test("failed submission preserves the draft for retry", async ({ page }) => {
  await page.goto(`/exams/${checkpoint.id}`);
  await page.getByRole("button", { name: "Start exam", exact: true }).click();
  await answerExam(page, checkpoint);
  await page.route(`**/api/v1/exams/${checkpoint.id}/submit`, (route) =>
    route.fulfill({
      status: 503,
      contentType: "application/json",
      body: JSON.stringify({ detail: "Temporary grading outage" }),
    }),
  );
  await page.getByRole("button", { name: "Submit exam" }).click();
  await expect(page.getByRole("alert")).toContainText(
    "Temporary grading outage",
  );
  await page.reload();
  await expect(
    page.getByText("8 of 8 answered", { exact: true }),
  ).toBeVisible();
  await page.unroute(`**/api/v1/exams/${checkpoint.id}/submit`);
  await page
    .locator(".exam-navigation")
    .getByRole("button", { name: "Review answers" })
    .click();
  await page.getByRole("button", { name: "Submit exam" }).click();
  await expect(
    page.getByRole("heading", { name: "You passed this exam." }),
  ).toBeVisible();
});

for (const edited of [false, true]) {
  test(`a lost grading response recovers the recorded attempt${edited ? " and preserves later edits" : ""}`, async ({
    page,
  }) => {
    await page.goto("/");
    await page
      .getByRole("button", { name: "Create account", exact: true })
      .click();
    await page.getByLabel("Your name").fill("Recovery Learner");
    await page
      .getByLabel("Email address")
      .fill(`recovery-${crypto.randomUUID()}@example.com`);
    await page
      .getByLabel("Password", { exact: true })
      .fill("recovery-exam-password");
    await page.getByRole("button", { name: "Create your workspace" }).click();
    await expect(page.getByRole("dialog")).not.toBeVisible();
    await page.goto(`/exams/${checkpoint.id}`);
    await page.getByRole("button", { name: "Start exam", exact: true }).click();
    await answerExam(page, checkpoint);
    const submitPath = `**/api/v1/exams/${checkpoint.id}/submit`;
    await page.route(submitPath, async (route) => {
      const response = await route.fetch();
      expect(response.ok()).toBe(true);
      await route.abort("connectionreset");
    });
    await page.getByRole("button", { name: "Submit exam" }).click();
    await expect(page.getByRole("alert")).toContainText(
      "Your answers are saved",
    );
    await page.unroute(submitPath);
    const changedAnswer =
      (checkpoint.questions[0].answer + 1) %
      checkpoint.questions[0].options.length;
    if (edited) {
      await page
        .getByRole("button", { name: "Edit question 1", exact: true })
        .click();
      await page.getByRole("radio").nth(changedAnswer).check();
      await page
        .locator(".exam-navigation")
        .getByRole("button", { name: "Review answers" })
        .click();
      await page.getByRole("button", { name: "Submit exam" }).click();
      await expect(
        page.getByRole("button", { name: "Continue as a new attempt" }),
      ).toBeVisible();
      await page.reload();
      await page
        .getByRole("button", { name: "Continue as a new attempt" })
        .click();
      await expect(page.getByRole("radio").nth(changedAnswer)).toBeChecked();
      await page
        .locator(".exam-navigation")
        .getByRole("button", { name: "Review answers" })
        .click();
      await page.getByRole("button", { name: "Submit exam" }).click();
      await expect(page.locator(".exam-score")).toContainText("87.5%");
    } else {
      await page.reload();
      await expect(page.locator(".exam-score")).toContainText("100%");
    }
    await expect(page.locator(".exam-navigation")).toHaveCount(0);
    const attempts = (
      await (
        await page.request.get(`/api/v1/exams/${checkpoint.id}/attempts`)
      ).json()
    ).attempts;
    expect(attempts).toHaveLength(edited ? 2 : 1);
    expect(attempts.at(-1).score).toBe(100);
    await page.reload();
    await expect(page.locator(".exam-score")).toContainText(
      edited ? "87.5%" : "100%",
    );
  });
}

test("device grading and mobile exam navigation work when the API is unavailable", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.route("**/api/v1/**", (route) => route.abort());
  await page.goto(`/exams/${checkpoint.id}`);
  await page.getByRole("button", { name: "Start exam", exact: true }).click();
  await answerExam(page, checkpoint);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await expect(
    page.getByText("This attempt will be graded and saved on this device.", {
      exact: false,
    }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Submit exam" }).click();
  await expect(
    page.getByRole("heading", { name: "You passed this exam." }),
  ).toBeVisible();
  await expect(page.getByRole("region", { name: "Exam result" })).toContainText(
    "Graded on this device",
  );
  await page.getByRole("button", { name: "Switch to dark theme" }).click();
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expect(page.locator(".exam-score")).toContainText("100%");
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
});

test("a late exam response after sign-out does not write into the guest workspace", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByRole("button", { name: "Create account", exact: true })
    .click();
  await page.getByLabel("Your name").fill("Late Response Learner");
  await page
    .getByLabel("Email address")
    .fill(`late-exam-${Date.now()}@example.com`);
  await page.getByLabel("Password", { exact: true }).fill("late-exam-password");
  await page.getByRole("button", { name: "Create your workspace" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await page.goto(`/exams/${checkpoint.id}`);
  await page.getByRole("button", { name: "Start exam", exact: true }).click();
  await answerExam(page, checkpoint);
  let release!: () => void;
  let saved!: () => void;
  const held = new Promise<void>((resolve) => {
    release = resolve;
  });
  const recorded = new Promise<void>((resolve) => {
    saved = resolve;
  });
  await page.route(`**/api/v1/exams/${checkpoint.id}/submit`, async (route) => {
    const response = await route.fetch();
    saved();
    await held;
    await route.fulfill({ response });
  });
  await page.getByRole("button", { name: "Submit exam" }).click();
  await recorded;
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Start exam", exact: true }),
  ).toBeVisible();
  const returned = page.waitForResponse((response) =>
    response.url().endsWith(`/exams/${checkpoint.id}/submit`),
  );
  release();
  await returned;
  await expect(page.locator(".exam-score")).toHaveCount(0);
  await page.reload();
  await expect(
    page.getByRole("button", { name: "Start exam", exact: true }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () =>
        JSON.parse(localStorage.getItem("quanta-workspace:v1:guest")!)
          .examAttempts,
    ),
  ).toEqual({});
});
