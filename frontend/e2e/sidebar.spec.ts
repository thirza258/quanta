import { expect, test } from "@playwright/test";

for (const width of [900, 1280, 1680]) {
  test(`desktop sidebar collapses and reopens at ${width}px`, async ({
    page,
  }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto("/");
    const sidebar = page.getByRole("complementary", {
      name: "Workspace sidebar",
    });
    const toggle = page.locator(".desktop-menu");
    const main = page.locator(".main-shell");

    await expect(sidebar).toBeInViewport();
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await toggle.click();
    await expect(toggle).toHaveAccessibleName("Expand sidebar");
    await expect(toggle).toHaveAttribute("aria-expanded", "false");
    await expect(sidebar).not.toHaveAttribute("inert", "");
    await expect(sidebar).toBeInViewport();
    await expect(sidebar).toHaveCSS("width", "64px");
    await expect(sidebar.locator(".brand")).toBeHidden();
    for (const link of await sidebar.locator(".nav-item").all()) {
      await expect(link.locator("svg").first()).toBeInViewport();
      await expect(link.locator("span")).toBeHidden();
    }
    await expect
      .poll(() => main.evaluate((el) => el.getBoundingClientRect().left))
      .toBe(64);
    await expect
      .poll(() => main.evaluate((el) => el.getBoundingClientRect().width))
      .toBe(width - 64);

    await sidebar
      .getByRole("link", { name: "Curriculum", exact: true })
      .click();
    await expect(page).toHaveURL(/\/curriculum$/);
    await expect(toggle).toHaveAttribute("aria-expanded", "false");
    await sidebar
      .getByRole("button", { name: "Find a lesson", exact: true })
      .click();
    await expect(
      page.getByRole("dialog", { name: "Find your next idea" }),
    ).toBeVisible();
    await page
      .getByRole("button", { name: "Close dialog", exact: true })
      .click();
    await sidebar
      .getByRole("button", { name: "Open workspace account", exact: true })
      .click();
    await expect(page.getByRole("dialog")).toBeVisible();
    await page
      .getByRole("button", { name: "Close dialog", exact: true })
      .click();
    await toggle.focus();
    await page.keyboard.press("Enter");
    await expect(toggle).toHaveAccessibleName("Collapse sidebar");
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(sidebar).toBeInViewport();
    await expect(sidebar).not.toHaveAttribute("inert", "");
    await expect
      .poll(() => main.evaluate((el) => el.getBoundingClientRect().left))
      .toBeGreaterThan(0);
    await expect(page.locator(".sidebar-backdrop")).toHaveCount(0);
  });
}

test("mobile navigation closes by button, Escape, backdrop, and navigation", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 640 });
  await page.goto("/");
  const sidebar = page.locator(".sidebar");
  const opener = page.getByRole("button", {
    name: "Open navigation",
    exact: true,
  });

  for (const action of [
    "button",
    "escape",
    "backdrop",
    "current link",
    "new link",
  ]) {
    await opener.click();
    await expect(sidebar).toBeInViewport();
    await expect(page.locator(".mobile-menu")).toHaveAttribute(
      "aria-expanded",
      "true",
    );
    await expect(page.locator(".main-shell")).toHaveAttribute("inert", "");
    await expect(
      page.getByRole("button", { name: "Close navigation", exact: true }),
    ).toBeFocused();
    await expect(page.locator("body")).toHaveCSS("overflow", "hidden");

    if (action === "button") {
      await page
        .getByRole("button", { name: "Close navigation", exact: true })
        .click();
    } else if (action === "escape") {
      await page.keyboard.press("Escape");
    } else if (action === "backdrop") {
      await page
        .getByRole("button", { name: "Dismiss navigation", exact: true })
        .click({ position: { x: 380, y: 10 } });
    } else {
      await sidebar
        .getByRole("link", {
          name: action === "current link" ? "Overview" : "Curriculum",
          exact: true,
        })
        .click();
    }

    await expect(sidebar).toHaveAttribute("inert", "");
    await expect(sidebar).not.toBeInViewport();
    await expect(opener).toHaveAttribute("aria-expanded", "false");
    await expect(opener).toBeFocused();
    await expect(page.locator(".main-shell")).not.toHaveAttribute("inert", "");
    await expect(page.locator("body")).not.toHaveCSS("overflow", "hidden");
  }
  await expect(page).toHaveURL(/\/curriculum$/);
});

test("mobile navigation keeps keyboard focus and supports nested dialogs", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 640 });
  await page.goto("/");
  await page
    .getByRole("button", { name: "Open navigation", exact: true })
    .click();
  const sidebar = page.locator(".sidebar");
  const home = sidebar.getByRole("link", { name: "Quanta home", exact: true });
  await home.focus();
  await page.keyboard.press("Shift+Tab");
  await expect(
    sidebar.getByRole("button", { name: "Create account", exact: true }),
  ).toBeFocused();
  await page.keyboard.press("Tab");
  await expect(home).toBeFocused();

  await sidebar.getByRole("button", { name: "Find a lesson" }).click();
  await expect(
    page.getByRole("dialog", { name: "Find your next idea" }),
  ).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(sidebar).not.toHaveAttribute("inert", "");
  await expect(page.locator("body")).toHaveCSS("overflow", "hidden");
  await page.keyboard.press("Escape");
  await expect(sidebar).toHaveAttribute("inert", "");
  await expect(
    page.getByRole("button", { name: "Open navigation", exact: true }),
  ).toBeFocused();
});

test("resizing clears the mobile drawer while preserving the desktop choice", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByRole("button", { name: "Collapse sidebar", exact: true })
    .click();
  await page.setViewportSize({ width: 760, height: 700 });
  await page
    .getByRole("button", { name: "Open navigation", exact: true })
    .click();
  await expect(page.locator(".sidebar")).not.toHaveAttribute("inert", "");
  await page.setViewportSize({ width: 761, height: 700 });
  await expect(page.locator(".sidebar-backdrop")).toHaveCount(0);
  await expect(page.locator(".sidebar")).not.toHaveAttribute("inert", "");
  await expect(page.locator(".sidebar")).toHaveCSS("width", "64px");
  await expect(page.locator("body")).not.toHaveCSS("overflow", "hidden");
  await page
    .getByRole("button", { name: "Expand sidebar", exact: true })
    .click();
  await expect(page.locator(".sidebar")).toBeInViewport();
  await page.setViewportSize({ width: 760, height: 700 });
  await expect(page.locator(".sidebar")).toHaveAttribute("inert", "");
  await expect(
    page.getByRole("button", { name: "Open navigation", exact: true }),
  ).toHaveAttribute("aria-expanded", "false");
});

for (const [width, height] of [
  [1280, 720],
  [1280, 600],
  [900, 400],
  [667, 375],
  [390, 640],
]) {
  test(`sidebar keeps controls reachable at ${width}×${height}`, async ({
    page,
  }) => {
    await page.setViewportSize({ width, height });
    await page.goto("/curriculum/news-to-markets");
    const sidebar = page.locator(".sidebar");
    if (width <= 760) {
      await expect(sidebar).toHaveAttribute("inert", "");
      await page
        .getByRole("button", { name: "Open navigation", exact: true })
        .click();
      await expect(sidebar).not.toHaveAttribute("inert", "");
    }
    const bounds = await sidebar.evaluate((element) => {
      const scroll = element.querySelector(".sidebar-scroll")!;
      const profile = element.querySelector(".profile-row")!;
      const search = element.querySelector(".quick-search")!;
      return {
        bottom: element.getBoundingClientRect().bottom,
        profileBottom: profile.getBoundingClientRect().bottom,
        searchTop: search.getBoundingClientRect().top,
        scrollBottom: scroll.getBoundingClientRect().bottom,
        hasScroll: scroll.scrollHeight > scroll.clientHeight,
        horizontalOverflow: element.scrollWidth > element.clientWidth,
      };
    });
    expect(bounds.bottom).toBeLessThanOrEqual(height + 1);
    expect(bounds.profileBottom).toBeLessThanOrEqual(height + 1);
    expect(bounds.searchTop).toBeGreaterThanOrEqual(bounds.scrollBottom);
    expect(bounds.hasScroll).toBe(true);
    expect(bounds.horizontalOverflow).toBe(false);
    await sidebar
      .getByRole("link", { name: "How Quanta works", exact: true })
      .scrollIntoViewIfNeeded();
    await sidebar.getByRole("button", { name: "Find a lesson" }).click();
    await expect(
      page.getByRole("dialog", { name: "Find your next idea" }),
    ).toBeVisible();
    await page
      .getByRole("button", { name: "Close dialog", exact: true })
      .click();
    await sidebar
      .getByRole("button", { name: "Create account", exact: true })
      .click();
    await expect(page.getByRole("dialog")).toBeVisible();
    await page
      .getByRole("button", { name: "Close dialog", exact: true })
      .click();
    if (width <= 760) {
      await page
        .getByRole("button", { name: "Dismiss navigation", exact: true })
        .click({ position: { x: width - 10, y: 10 } });
      await expect(sidebar).toHaveAttribute("inert", "");
    }
  });
}
