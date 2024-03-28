import { expect, test } from "@playwright/test";

import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

test.use({
  userAgent:
    // Chrome OS user agent
    "Mozilla/5.0 (X11; CrOS x86_64 15236.80.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.125 Safari/537.36",
});

test("Adds query platform argument if missing", async ({ page }) => {
  const response = await navigateAndWaitForHydration({ page, path: "/en" });

  expect(response?.status()).toBe(200);

  await page.waitForURL(
    `${process.env.NEXT_PUBLIC_WEB_URL}/en?platform=android`,
  );
});
