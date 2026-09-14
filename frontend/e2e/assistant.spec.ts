import { expect, test } from "@playwright/test";
import type { Page } from "@playwright/test";
import { readFileSync } from "node:fs";

const generatedCode =
  'print("Assistant example")\n\ndef strategy(data):\n    return data["close"] > data["sma_50"]\n';
const answer = {
  message:
    "Compare the close with the moving average. Review this example, then run it.",
  files: [
    {
      path: "lesson.py",
      language: "python",
      content: generatedCode,
      target: "lesson",
    },
  ],
};

async function connected(page: Page) {
  await page.route("**/api/v1/assistant/status", (route) =>
    route.fulfill({ json: { enabled: true } }),
  );
}

test("lesson assistant shares context, previews and applies code with undo, and remembers this lesson", async ({
  page,
}) => {
  await connected(page);
  const requests: Record<string, unknown>[] = [];
  let executions = 0;
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("request", (request) => {
    if (request.url().includes("sandbox/execute")) executions++;
  });
  await page.route("**/api/v1/assistant/chat", (route) => {
    requests.push(route.request().postDataJSON());
    return route.fulfill({ json: answer });
  });
  await page.goto("/learn/0.1");
  await page.getByRole("button", { name: "Ask AI assistant" }).click();
  const dialog = page.getByRole("dialog", { name: "Course assistant" });
  await dialog.getByRole("button", { name: "Help me write code" }).click();
  await expect(dialog.getByText(answer.message)).toBeVisible();
  expect(requests[0]).toMatchObject({
    course_id: "trading-fundamentals",
    lesson_id: "0.1",
    mode: "code",
  });
  expect(requests[0].code).toBeTruthy();
  await dialog.locator("summary").filter({ hasText: "lesson.py" }).click();
  await expect(dialog.locator("pre")).toContainText("Assistant example");
  await dialog.getByRole("button", { name: "Use in lesson editor" }).click();
  await expect(dialog.getByRole("status")).toContainText("Code added");
  expect(executions).toBe(0);
  await dialog.getByRole("button", { name: "Close AI assistant" }).click();
  await expect(
    page.getByRole("textbox", { name: "Python strategy editor" }),
  ).toBeVisible();
  await expect
    .poll(() =>
      page.evaluate(
        () =>
          JSON.parse(localStorage.getItem("quanta-workspace:v1:guest") || "{}")
            .drafts?.["0.1"],
      ),
    )
    .toBe(generatedCode);
  await page.getByRole("button", { name: "Undo code replacement" }).click();
  await expect
    .poll(() =>
      page.evaluate(
        () =>
          JSON.parse(localStorage.getItem("quanta-workspace:v1:guest") || "{}")
            .drafts?.["0.1"],
      ),
    )
    .toBe(requests[0].code);
  await page.reload();
  await page.getByRole("button", { name: "Ask AI assistant" }).click();
  await expect(dialog.getByText(answer.message)).toBeVisible();
  await dialog.getByRole("button", { name: "Close AI assistant" }).click();
  await page.goto("/learn/0.2");
  await page.getByRole("button", { name: "Ask AI assistant" }).click();
  await expect(dialog.getByText("Let’s work through it.")).toBeVisible();
  await expect(dialog.getByText(answer.message)).toHaveCount(0);
  expect(errors).toEqual([]);
});

test("environment setup creates a downloadable project on mobile", async ({
  page,
}) => {
  await connected(page);
  await page.setViewportSize({ width: 390, height: 750 });
  let request: Record<string, unknown> = {};
  await page.route("**/api/v1/assistant/chat", (route) => {
    request = route.request().postDataJSON();
    return route.fulfill({
      json: {
        message:
          "Extract the project and follow README.md to start your environment.",
        files: [
          {
            path: "README.md",
            language: "markdown",
            content: "# Practice project\n\nUse WSL, then run make.\n",
            target: "local",
          },
          {
            path: "src/main.c",
            language: "c",
            content: "int main(void) { return 0; }\n",
            target: "local",
          },
        ],
      },
    });
  });
  await page.goto("/curriculum/c-hpc-trading");
  await page.getByRole("button", { name: "Ask AI assistant" }).click();
  const dialog = page.getByRole("dialog", { name: "Course assistant" });
  await dialog.getByLabel("Assistant help mode").selectOption("environment");
  await dialog
    .getByLabel("Environment operating system")
    .selectOption("windows");
  await dialog.getByRole("button", { name: "Set up my environment" }).click();
  await expect(dialog.getByText("2 files to review")).toBeVisible();
  expect(request).toMatchObject({
    course_id: "c-hpc-trading",
    lesson_id: null,
    platform: "windows",
    mode: "environment",
  });
  const downloadEvent = page.waitForEvent("download");
  await dialog.getByRole("button", { name: "Download project ZIP" }).click();
  const download = await downloadEvent;
  expect(download.suggestedFilename()).toBe("quanta-project.zip");
  expect(
    readFileSync((await download.path())!)
      .subarray(0, 2)
      .toString(),
  ).toBe("PK");
  await dialog.locator("summary").filter({ hasText: "src/main.c" }).click();
  await expect(
    dialog.getByRole("button", { name: "Use in lesson editor" }),
  ).toHaveCount(0);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  const bounds = await dialog.boundingBox();
  expect(bounds!.width).toBeLessThanOrEqual(390);
  await page.keyboard.press("Escape");
  await expect(dialog).not.toBeVisible();
  await expect(
    page.getByRole("button", { name: "Ask AI assistant" }),
  ).toBeFocused();
});

test("last execution error is shared only when the learner includes code", async ({
  page,
}) => {
  await connected(page);
  const requests: Record<string, unknown>[] = [];
  await page.route("**/api/v1/sandbox/execute", (route) =>
    route.fulfill({
      status: 422,
      json: { detail: "Name not defined: missing_variable" },
    }),
  );
  await page.route("**/api/v1/assistant/chat", (route) => {
    requests.push(route.request().postDataJSON());
    return route.fulfill({
      json: { message: "Define the variable before using it.", files: [] },
    });
  });
  await page.goto("/learn/0.1");
  await page.getByRole("button", { name: "Sandbox view", exact: true }).click();
  await page.getByRole("button", { name: "Run experiment" }).click();
  await expect(
    page
      .getByRole("region", { name: "Interactive Python sandbox" })
      .getByRole("alert"),
  ).toContainText("missing_variable");
  await page.getByRole("button", { name: "Ask AI assistant" }).click();
  const dialog = page.getByRole("dialog", { name: "Course assistant" });
  await dialog.getByRole("button", { name: "Help me write code" }).click();
  await expect(
    dialog.getByText("Define the variable before using it."),
  ).toBeVisible();
  expect(requests[0].error).toContain("missing_variable");
  await dialog.getByLabel("Include editor code & last run error").uncheck();
  await dialog
    .getByRole("textbox", { name: "Message the course assistant" })
    .fill("Explain the concept only");
  await dialog.getByRole("button", { name: "Send assistant message" }).click();
  await expect(
    dialog.getByText("Define the variable before using it."),
  ).toHaveCount(2);
  expect(requests[1]).toMatchObject({ code: null, error: null });
  expect((requests[1].history as unknown[]).length).toBe(2);
});

test("failed requests keep the question for retry and stopped replies cannot land in a new chat", async ({
  page,
}) => {
  await connected(page);
  let count = 0;
  let release: (() => void) | undefined;
  await page.route("**/api/v1/assistant/chat", async (route) => {
    count++;
    if (count === 1)
      return route.fulfill({
        status: 503,
        json: { detail: "The AI connection needs attention." },
      });
    if (count === 2) {
      await new Promise<void>((resolve) => {
        release = resolve;
      });
      return route
        .fulfill({ json: { message: "Late response", files: [] } })
        .catch(() => {});
    }
    return route.fulfill({
      json: { message: "Here is your new hint.", files: [] },
    });
  });
  await page.goto("/learn/0.1");
  await page.getByRole("button", { name: "Ask AI assistant" }).click();
  const dialog = page.getByRole("dialog", { name: "Course assistant" });
  const input = dialog.getByRole("textbox", {
    name: "Message the course assistant",
  });
  await input.fill("What is a stock?");
  await dialog.getByRole("button", { name: "Send assistant message" }).click();
  await expect(dialog.getByRole("alert")).toContainText(
    "connection needs attention",
  );
  await expect(input).toHaveValue("What is a stock?");
  await dialog.getByRole("button", { name: "Send assistant message" }).click();
  await expect.poll(() => count).toBe(2);
  await dialog.getByRole("button", { name: "Stop assistant response" }).click();
  await expect(input).toHaveValue("What is a stock?");
  release?.();
  await input.fill("Give me a new hint");
  await dialog.getByRole("button", { name: "Send assistant message" }).click();
  await expect(dialog.getByText("Here is your new hint.")).toBeVisible();
  await expect(dialog.getByText("Late response")).toHaveCount(0);
  await dialog
    .getByRole("button", { name: "Start a new assistant chat" })
    .click();
  await expect(dialog.getByText("Let’s work through it.")).toBeVisible();
  await page.reload();
  await page.getByRole("button", { name: "Ask AI assistant" }).click();
  await expect(dialog.getByText("Here is your new hint.")).toHaveCount(0);
});

test("missing connection keeps course downloads available and chat disabled", async ({
  page,
}) => {
  await page.route("**/api/v1/assistant/status", (route) =>
    route.fulfill({ json: { enabled: false } }),
  );
  await page.goto("/curriculum/stock-machine-learning");
  await page.getByRole("button", { name: "Ask AI assistant" }).click();
  const dialog = page.getByRole("dialog", { name: "Course assistant" });
  await expect(dialog.getByRole("status")).toContainText("isn’t connected yet");
  await expect(
    dialog.getByRole("button", { name: "Help me write code" }),
  ).toBeDisabled();
  await dialog
    .getByRole("textbox", { name: "Message the course assistant" })
    .fill("Help me");
  await expect(
    dialog.getByRole("button", { name: "Send assistant message" }),
  ).toBeDisabled();
  await dialog.getByText("Course project downloads", { exact: true }).click();
  await expect(
    dialog.getByRole("link", {
      name: "Download the full stock-ML lifecycle project",
    }),
  ).toBeVisible();
});
