import { expect, test } from "@playwright/test";
import { readFileSync } from "node:fs";

test("C lab edits survive navigation and reload, download accurately, and reset", async ({
  page,
}) => {
  const sandboxRequests: string[] = [];
  const errors: string[] = [];
  page.on("request", (request) => {
    if (request.url().includes("sandbox/execute"))
      sandboxRequests.push(request.url());
  });
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/learn/9.13");
  await page.getByRole("button", { name: "Open C lab", exact: true }).click();
  const editor = page.getByRole("textbox", {
    name: "C source editor",
    exact: true,
  });
  await expect(editor).toBeVisible();
  await editor.focus();
  await page.keyboard.press("ControlOrMeta+End");
  await page.keyboard.insertText("\n/* my parallel scheduling experiment */\n");
  await expect
    .poll(async () =>
      page.evaluate(
        () =>
          JSON.parse(localStorage.getItem("quanta-workspace:v1:guest") || "{}")
            .drafts?.["9.13"],
      ),
    )
    .toContain("my parallel scheduling experiment");
  await page.getByRole("button", { name: "Reading view", exact: true }).click();
  await page.getByRole("button", { name: "Open C lab", exact: true }).click();
  await page.reload();
  await page.getByRole("button", { name: "C lab view", exact: true }).click();
  const waiting = page.waitForEvent("download");
  await page
    .getByRole("button", { name: "Download C source", exact: true })
    .click();
  const file = await waiting;
  expect(file.suggestedFilename()).toBe("lesson-9-13.c");
  const source = readFileSync((await file.path())!, "utf8");
  expect(source).toContain("my parallel scheduling experiment");
  expect(source).toContain("int main(void)");
  expect(source).not.toContain("def strategy");
  await page
    .getByRole("button", { name: "Reset template", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Reset template", exact: true }),
  ).toBeDisabled();
  await page.setViewportSize({ width: 390, height: 640 });
  await expect(
    page.getByRole("button", { name: "Download C source", exact: true }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  expect(sandboxRequests).toEqual([]);
  expect(errors).toEqual([]);
});
