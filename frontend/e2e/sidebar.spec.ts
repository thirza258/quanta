import { expect, test } from "@playwright/test";

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
        .getByRole("button", { name: "Close navigation", exact: true })
        .click({ position: { x: width - 10, y: 10 } });
      await expect(sidebar).toHaveAttribute("inert", "");
    }
  });
}
