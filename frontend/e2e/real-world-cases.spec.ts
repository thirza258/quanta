import { expect, test } from "@playwright/test";
import { readFileSync } from "node:fs";
import type { Track } from "@/features/learning/model/types";

const catalog = JSON.parse(
  readFileSync(
    new URL("../../content/catalog/curriculum.json", import.meta.url),
    "utf8",
  ),
) as Track[];

for (const track of catalog) {
  test(`${track.id}: every lesson and unit has accessible case references and a worked application`, async ({
    page,
  }) => {
    test.setTimeout(120000);
    const errors: string[] = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await page.goto(`/curriculum/${track.id}`);
    await expect(
      page.getByRole("heading", {
        name: "Real-world practice in every lesson",
      }),
    ).toBeVisible();
    await expect(page.locator(".unit-cases")).toHaveCount(
      track.parts?.length ?? 0,
    );
    for (const part of track.parts ?? []) {
      const links = page.locator(`[id="unit-${part.id}"] .unit-cases a`);
      const expected = new Set(
        track.modules
          .filter((lesson) => lesson.part === part.id)
          .map((lesson) => lesson.realWorld.caseId),
      );
      await expect(links).toHaveCount(expected.size);
    }
    for (const lesson of track.modules) {
      await page.goto(`/learn/${lesson.id}`);
      const caseStudy = track.caseStudies.find(
        (item) => item.id === lesson.realWorld.caseId,
      )!;
      const panel = page.getByRole("region", {
        name: caseStudy.title,
        exact: true,
      });
      await expect(panel).toContainText(caseStudy.context);
      await expect(panel).toContainText(caseStudy.boundary);
      await expect(panel).toContainText(lesson.realWorld.connection);
      await expect(panel).toContainText(lesson.realWorld.task);
      for (const reference of caseStudy.references) {
        await expect(
          panel.getByRole("link", { name: reference.title, exact: true }),
        ).toHaveAttribute("href", reference.url);
        await expect(panel).toContainText(reference.scope);
      }
      await expect(panel.locator(".case-walkthrough p")).not.toBeVisible();
      await panel.getByText("Compare your reasoning", { exact: true }).click();
      await expect(panel.locator(".case-walkthrough p")).toHaveText(
        lesson.realWorld.walkthrough,
      );
    }
    expect(errors).toEqual([]);
  });
}

test("case links open the correct lesson and notebook work survives reload with its references", async ({
  page,
}) => {
  const track = catalog.find((item) => item.id === "stock-bots")!;
  const lesson = track.modules.find((item) => item.id === "5.6")!;
  const caseStudy = track.caseStudies.find(
    (item) => item.id === lesson.realWorld.caseId,
  )!;
  await page.goto(`/curriculum/${track.id}`);
  await page
    .locator(".unit-cases")
    .first()
    .getByRole("link", { name: caseStudy.title })
    .click();
  await expect(page).toHaveURL(/\/learn\/5\.6#real-world-case$/);
  const panel = page.locator("#real-world-case");
  await expect(panel).toBeFocused();
  expect(
    await panel.evaluate((element) => element.getBoundingClientRect().top),
  ).toBeLessThan(150);
  await panel.getByRole("button", { name: "Work through this case" }).click();
  const input = page.getByLabel("Research note");
  const text = await input.inputValue();
  expect(text).toContain(lesson.realWorld.task);
  expect(text).toContain(caseStudy.references[0].url);
  await input.fill(
    text + "\nMy decision: halt new orders when the quote is stale.",
  );
  await page.getByRole("button", { name: "Save to notebook" }).click();
  await page.goto("/notebook");
  await page.reload();
  await expect(
    page.getByText("My decision: halt new orders when the quote is stale.", {
      exact: false,
    }),
  ).toBeVisible();
  await expect(
    page.getByText(caseStudy.references[0].url, { exact: false }),
  ).toBeVisible();
  await page.locator(".note-edit").click();
  const saved = await page
    .getByRole("textbox", { name: "Your note", exact: true })
    .inputValue();
  expect(saved).toContain(lesson.realWorld.task);
  expect(saved).toContain(caseStudy.references[0].url);
  expect(saved).toContain(
    "My decision: halt new orders when the quote is stale.",
  );
  await page.goto("/library");
  const urls = new Set(
    catalog.flatMap((course) =>
      course.caseStudies.flatMap((item) =>
        item.references.map((ref) => ref.url),
      ),
    ),
  );
  for (const url of urls) {
    await expect(page.locator(`.reference-card a[href="${url}"]`)).toHaveCount(
      1,
    );
  }
});

test("cases and source links remain readable on mobile in both themes", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  for (const theme of ["light", "dark"]) {
    await page.goto("/curriculum/news-to-markets");
    await page.evaluate((value) => {
      localStorage.setItem("quanta-theme", value);
      document.documentElement.dataset.theme = value;
      window.dispatchEvent(new Event("quanta-theme-change"));
    }, theme);
    await page
      .getByText("Explore the cases in this course", { exact: true })
      .click();
    await expect(page.locator(".course-case-grid li")).toHaveCount(12);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth + 1,
      ),
    ).toBe(true);
    await page.goto("/learn/8.3#real-world-case");
    await expect(page.locator("#real-world-title")).toBeInViewport();
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth + 1,
      ),
    ).toBe(true);
    await page.locator(".case-walkthrough summary").click();
    await expect(page.locator(".case-walkthrough p")).toContainText("5.03%");
    await expect(page.locator(".case-sources a")).toHaveAttribute(
      "href",
      /bps\.go\.id/,
    );
  }
});
