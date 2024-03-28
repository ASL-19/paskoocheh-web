import { expect, test } from "@playwright/test";

import routeUrls from "src/routeUrls";
import topicTestDataBySlug from "src/test/data/topicTestDataBySlug";
import { testDefaultRouteArgs } from "src/test/testValues";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

const strings = getServerLocaleStrings(testDefaultRouteArgs.localeCode);
const path = routeUrls.blog(testDefaultRouteArgs);

test(`Blog page renders expected text and metadata`, async ({ page }) => {
  await navigateAndWaitForHydration({ page, path });

  // ---------------------------------
  // --- Main heading and metadata ---
  // ---------------------------------

  await expectPageMainHeadingAndMetadata({
    mainHeading: strings.BlogPage.pageTitle,
    metaDescription: strings.BlogPage.pageDescription,
    metaTitle: strings.BlogPage.pageTitle,
    page,
    path,
    strings,
  });

  // ---------------------
  // --- Accessibility ---
  // ---------------------

  await expectPageToHaveNoAxeViolations({ page });
});

test(`Blog page test filter`, async ({ page }) => {
  await page.goto(path);

  await expect(
    page.getByRole("link", {
      name: topicTestDataBySlug["digital-security"].name,
    }),
  ).toHaveAttribute(
    "href",
    `${routeUrls.blog({
      localeCode: testDefaultRouteArgs.localeCode,
      platform: testDefaultRouteArgs.platform,
      topic: topicTestDataBySlug["digital-security"].slug,
    })}`,
  );
});
