import { expect, test, type Page } from "@playwright/test";
import { readFileSync } from "node:fs";
import type { Track } from "../src/features/learning/model/types";

const tracks = JSON.parse(
  readFileSync(
    new URL("../../content/catalog/curriculum.json", import.meta.url),
    "utf8",
  ),
) as Track[];
const track = tracks[0];

async function seedCompletion(page: Page, course = track) {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await page.evaluate((course) => {
    const key = "quanta-workspace:v1:guest";
    const state = JSON.parse(localStorage.getItem(key) || "{}");
    state.completed = course.modules.map((lesson) => lesson.id);
    state.examAttempts = Object.fromEntries(
      course.exams.map((exam) => [
        exam.id,
        [
          {
            id: crypto.randomUUID(),
            examId: exam.id,
            version: exam.version,
            startedAt: "2026-09-20T00:00:00.000Z",
            submittedAt: "2026-09-20T01:00:00.000Z",
            answers: Object.fromEntries(
              exam.questions.map((question) => [question.id, question.answer]),
            ),
            correctCount: exam.questions.length,
            total: exam.questions.length,
            score: 100,
            passed: true,
            grading: "device",
          },
        ],
      ]),
    );
    localStorage.setItem(key, JSON.stringify(state));
  }, course);
}

async function register(page: Page, name = "Ayu Pratama") {
  const email = `certificate-${Date.now()}-${Math.random().toString(36).slice(2)}@example.com`;
  const password = "certificate-test-password";
  await page
    .getByRole("button", { name: "Create account", exact: true })
    .click();
  await page.getByLabel("Your name", { exact: true }).fill(name);
  await page.getByLabel("Email address").fill(email);
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Create your workspace" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  return { email, password };
}

test("certification requirements block incomplete courses and handle missing records", async ({
  page,
}) => {
  await page.goto("/certifications");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Certifications",
  );
  await expect(
    page.getByText("Your first certificate starts with a course"),
  ).toBeVisible();
  await expect(page.locator(".certification-card")).toHaveCount(tracks.length);
  await page
    .locator(".certification-card")
    .first()
    .getByRole("link", { name: "View requirements" })
    .click();
  await expect(
    page.getByRole("heading", { name: "Course requirements" }),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Claim certificate" }),
  ).toHaveCount(0);
  await page
    .getByRole("link", { name: "Continue learning", exact: true })
    .click();
  await expect(page).toHaveURL(new RegExp(`/learn/${track.modules[0].id}$`));
  await page.goto("/certifications/missing");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Certificate not found",
  );
  await page.goto("/certifications/course/missing");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Course not found",
  );
});

test("claims once, survives reload, and prints a single certificate page on mobile and desktop", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  // Use the longest course title to exercise wrapping in the printable document.
  const course = [...tracks].sort((a, b) => b.title.length - a.title.length)[0];
  await seedCompletion(page, course);
  await page.goto(`/curriculum/${course.id}`);
  await page
    .getByRole("link", { name: "View certificate", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Sign in to claim your certificate" }),
  ).toBeVisible();
  await register(page);
  await page.getByLabel("Name on certificate").fill("");
  await expect(
    page.getByRole("button", { name: "Claim certificate" }),
  ).toBeDisabled();
  const name = "Ayu Pratama ".repeat(6).trim();
  await page.getByLabel("Name on certificate").fill(name);
  await page.getByRole("button", { name: "Claim certificate" }).click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Certificate of completion",
  );
  const certificateUrl = page.url();
  const issued = await page
    .locator(".certificate-details time")
    .getAttribute("datetime");
  await page.reload();
  await expect(page.locator(".certificate-recipient")).toHaveText(name);
  await expect(page.locator(".certificate-course-title")).toHaveText(
    course.title,
  );
  await expect(page.locator(".certificate-details time")).toHaveAttribute(
    "datetime",
    issued!,
  );
  await page.goto(`/certifications/course/${course.id}`);
  await expect(page).toHaveURL(certificateUrl);
  await page.evaluate(() => {
    window.print = () => {
      document.body.dataset.printRequested = "true";
    };
  });
  await page.getByRole("button", { name: "Print / save PDF" }).click();
  await expect(page.locator("body")).toHaveAttribute(
    "data-print-requested",
    "true",
  );
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole("button", { name: "Switch to dark theme" }).click();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  await page.emulateMedia({ media: "print" });
  await expect(page.locator(".certificate-document")).toBeVisible();
  await expect(page.locator(".sidebar")).toBeHidden();
  await expect(page.locator(".topbar")).toBeHidden();
  await expect(page.locator(".page-references")).toBeHidden();
  await page.setViewportSize({ width: 1440, height: 1000 });
  await expect(page.locator(".main-shell")).toHaveCSS("margin-left", "0px");
  await expect(page.locator("html")).toHaveCSS(
    "background-color",
    "rgb(255, 255, 255)",
  );
  const pdf = await page.pdf({
    path: test.info().outputPath("certificate.pdf"),
    preferCSSPageSize: true,
    printBackground: true,
  });
  expect(pdf.toString("latin1").match(/\/Type\s*\/Page\b/g)).toHaveLength(1);
  await page.emulateMedia({ media: "screen" });
  await page.setViewportSize({ width: 390, height: 844 });
  await page
    .getByRole("link", { name: "All certifications", exact: true })
    .click();
  await expect(page.locator(".certification-card.earned")).toHaveCount(1);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  expect(errors).toEqual([]);
});

test("public verification checks the issuer record and account certificates restore after sign-in", async ({
  page,
  browser,
}) => {
  await seedCompletion(page);
  await page.goto(`/certifications/course/${track.id}`);
  const { email, password } = await register(page);
  await page.getByLabel("Name on certificate").fill("Ayu Pratama");
  await page.getByRole("button", { name: "Claim certificate" }).click();
  await expect(page.locator(".certificate-document")).toBeVisible();
  const certificatePath = new URL(page.url()).pathname;
  const stored = await (await page.request.get("/api/v1/certificates")).json();
  expect(stored.certificates).toHaveLength(1);
  expect(stored.certificates[0].recipientName).toBe("Ayu Pratama");
  const otherContext = await browser.newContext({
    baseURL: test.info().project.use.baseURL,
  });
  try {
    const other = await otherContext.newPage();
    await other.goto(`/verify/${stored.certificates[0].id}`);
    await expect(
      other.getByText("Issuer record verified", { exact: true }),
    ).toBeVisible();
    await expect(other.locator(".certificate-recipient")).toHaveText(
      "Ayu Pratama",
    );
    await other
      .getByRole("link", { name: "Verify another certificate", exact: true })
      .click();
    await other
      .getByLabel("Certificate ID", { exact: true })
      .fill(stored.certificates[0].id.toLowerCase());
    await other
      .getByRole("button", { name: "Verify certificate", exact: true })
      .click();
    await expect(
      other.getByText("Issuer record verified", { exact: true }),
    ).toBeVisible();
    await other.goto("/verify/QTA-00000000-0000-0000-0000-000000000000");
    await expect(other.getByRole("heading", { level: 1 })).toHaveText(
      "Certificate not found",
    );
    await expect(
      other.getByText("Issuer record verified", { exact: true }),
    ).toHaveCount(0);
    await other.route("**/api/v1/certificates/*/verify", (route) =>
      route.fulfill({
        status: 503,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Unavailable" }),
      }),
    );
    await other.goto(`/verify/${stored.certificates[0].id}`);
    await expect(other.getByRole("heading", { level: 1 })).toHaveText(
      "Verification unavailable",
    );
    await expect(
      other.getByText("Issuer record verified", { exact: true }),
    ).toHaveCount(0);
    await other.unroute("**/api/v1/certificates/*/verify");
    await other.getByRole("button", { name: "Try again", exact: true }).click();
    await expect(
      other.getByText("Issuer record verified", { exact: true }),
    ).toBeVisible();
    await other.goto("/certifications");
    await expect(other.locator(".certification-card.earned")).toHaveCount(0);
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
    await expect(other.locator(".certification-card.earned")).toHaveCount(1);
    await other
      .getByRole("link", { name: "View certificate", exact: true })
      .click();
    await expect(other).toHaveURL(new RegExp(certificatePath + "$"));
    await expect(other.locator(".certificate-recipient")).toHaveText(
      "Ayu Pratama",
    );
    await expect(other.locator(".certificate-identifier")).toContainText(
      stored.certificates[0].id,
    );
    await other.getByRole("button", { name: "Sign out", exact: true }).click();
    await other.goto("/certifications");
    await expect(other.locator(".certification-card.earned")).toHaveCount(0);
  } finally {
    await otherContext.close();
  }
});

test("a lost issuance response restores the original certificate without a duplicate", async ({
  page,
}) => {
  await seedCompletion(page);
  await page.goto(`/certifications/course/${track.id}`);
  await register(page);
  let issuedId = "";
  await page.route("**/api/v1/certificates", async (route) => {
    if (route.request().method() !== "POST") return route.continue();
    const response = await route.fetch();
    expect(response.ok()).toBe(true);
    issuedId = (await response.json()).id;
    await route.fulfill({
      status: 503,
      contentType: "application/json",
      body: JSON.stringify({
        detail: "The response was interrupted. Please try again.",
      }),
    });
  });
  await page
    .getByRole("button", { name: "Claim certificate", exact: true })
    .click();
  await expect(page.getByRole("alert")).toContainText(
    "response was interrupted",
  );
  await page.unroute("**/api/v1/certificates");
  await page.reload();
  await expect(page.locator(".certificate-identifier")).toContainText(issuedId);
  const records = await (await page.request.get("/api/v1/certificates")).json();
  expect(records.certificates).toHaveLength(1);
});
