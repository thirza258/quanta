import type { Track } from "@/features/learning/model/types";
import { expect, test } from "@playwright/test";
import { readFileSync } from "node:fs";

const catalog = JSON.parse(
  readFileSync(
    new URL("../../content/catalog/curriculum.json", import.meta.url),
    "utf8",
  ),
) as Track[];
const courses = catalog.filter((course) =>
  [
    "econometrics",
    "web3",
    "stock-machine-learning",
    "news-to-markets",
    "c-hpc-trading",
    "algorithm-evaluation",
    "strategy-lab",
    "intelligent-investor",
  ].includes(course.id),
);

test("curriculum places careful investing before Security Analysis and searches its lessons", async ({
  page,
}) => {
  await page.goto("/curriculum");
  await expect(page.locator(".page-subtitle")).toContainText(
    `${catalog.length} connected courses`,
  );
  const cards = page.locator(".track-grid .track-card");
  for (const [index, slug] of [
    "trading-fundamentals",
    "trading-ethics",
    "intelligent-investor",
    "security-analysis",
    "news-to-markets",
  ].entries()) {
    await expect(cards.nth(index)).toHaveAttribute(
      "href",
      `/curriculum/${slug}`,
    );
  }
  await page.getByLabel("Search curriculum").fill("hati-hati");
  await expect(cards).toHaveCount(1);
  await expect(cards.first()).toContainText(
    "The intelligent & careful investor",
  );
  await cards.first().click();
  await page
    .getByRole("link", { name: "Start this course", exact: true })
    .click();
  await expect(page).toHaveURL(/\/learn\/11\.1$/);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Intelligent investing starts with temperament",
  );
});

for (const course of courses) {
  test(`${course.id}: units, downloads, capstone practice, notebook, and worksheet`, async ({
    page,
  }) => {
    await page.goto(`/curriculum/${course.id}`);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText(
      course.title,
    );
    await expect(
      page.getByRole("navigation", { name: "Course units" }).getByRole("link"),
    ).toHaveCount(course.parts!.length);
    await expect(page.locator(".module-row")).toHaveCount(
      course.modules.length,
    );
    await expect(page.locator(".exam-card")).toHaveCount(course.exams.length);
    if (course.id === "stock-machine-learning") {
      await expect(page.locator(".inline-meta")).toContainText(
        "720 minutes of guided study",
      );
      for (const paragraph of course.readingGuide!.split("\n\n")) {
        await expect(page.getByText(paragraph, { exact: true })).toBeVisible();
      }
    }
    for (const resource of course.resources!) {
      const waiting = page.waitForEvent("download");
      await page
        .getByRole("link", { name: resource.title, exact: true })
        .click();
      const file = await waiting;
      expect(file.suggestedFilename()).toBe(resource.url.split("/").at(-1));
      const bytes = readFileSync((await file.path())!);
      expect(bytes.length).toBeGreaterThan(20);
      if (resource.url.endsWith(".zip"))
        expect(bytes.subarray(0, 2).toString()).toBe("PK");
    }
    const lesson = course.modules.at(-1)!;
    await page.goto(`/learn/${lesson.id}`);
    await expect(
      page.getByRole("complementary", { name: "Applied study" }),
    ).toContainText(lesson.reading!);
    await expect(
      page.getByRole("button", { name: "Mark module complete", exact: true }),
    ).toBeDisabled();
    await page.getByText("Review the worked solution", { exact: true }).click();
    await expect(page.locator(".lesson-assignment details")).toContainText(
      lesson.assignment!.solution,
    );
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
    if (lesson.codeLanguage === "c") {
      await page
        .getByRole("button", { name: "Open C lab", exact: true })
        .click();
      const lab = page.getByRole("region", { name: "Local C laboratory" });
      await expect(lab).toContainText("Compile and run");
      await expect(lab.getByLabel("C compile commands")).toContainText(
        "cc -std=c17",
      );
      await expect(
        page.getByRole("button", { name: "Run experiment", exact: true }),
      ).toHaveCount(0);
      const waiting = page.waitForEvent("download");
      await lab
        .getByRole("button", { name: "Download C source", exact: true })
        .click();
      const file = await waiting;
      expect(file.suggestedFilename()).toBe("lesson-9-24.c");
      expect(readFileSync((await file.path())!, "utf8")).toBe(lesson.code);
      return;
    }
    await page.getByRole("button", { name: "Run in sandbox" }).click();
    await page.getByRole("button", { name: "Run experiment" }).click();
    await expect(page.locator(".console-output")).toContainText(
      course.id === "econometrics"
        ? "Rubric total: 100"
        : course.id === "web3"
          ? "Capstone rubric total: 100"
          : course.id === "news-to-markets"
            ? "Base value per share: 11.0625"
            : course.id === "algorithm-evaluation"
              ? "Report rubric total: 100"
              : course.id === "strategy-lab"
                ? "Strategy rubric total: 100"
                : course.id === "intelligent-investor"
                  ? "Investor plan rubric total: 100"
                  : "Planned study hours: 12.0",
    );
  });

  test(`${course.id}: every lesson renders mathematics, assignments, practice, and references`, async ({
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

  for (const exam of [course.exams[0], course.exams.at(-1)!]) {
    test(`${course.id}: ${exam.kind} grades on the server and persists`, async ({
      page,
    }) => {
      await page.goto(`/exams/${exam.id}`);
      await page
        .getByRole("button", { name: "Start exam", exact: true })
        .click();
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
      const waiting = page.waitForResponse(
        (response) =>
          response.url().includes(`/exams/${exam.id}/submit`) &&
          response.request().method() === "POST",
      );
      await page
        .getByRole("button", { name: "Submit exam", exact: true })
        .click();
      expect(await (await waiting).json()).toMatchObject({
        score: 100,
        passed: true,
        grading: "server",
        version: exam.version,
      });
      await page.reload();
      await expect(page.locator(".exam-score")).toContainText("100%");
      if (exam.kind === "checkpoint") {
        const next = course.modules[4];
        await page
          .getByRole("link", { name: `Continue to ${next.title}`, exact: true })
          .click();
        await expect(page).toHaveURL(
          new RegExp(`/learn/${next.id.replace(".", "\\.")}$`),
        );
      }
    });
  }
}

test("expanded course cards and headers remain readable on mobile", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  for (const route of [
    "/curriculum",
    ...courses.map((course) => `/curriculum/${course.id}`),
  ]) {
    await page.goto(route);
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    const artwork = page.locator(".track-art");
    expect(await artwork.count()).toBeGreaterThan(0);
    for (const art of await artwork.all()) {
      expect(await art.locator(":scope > g").count()).toBeGreaterThan(0);
    }
  }
});
