import { test } from "@playwright/test";

import routeUrls from "src/routeUrls";
import postTestDataBySlug from "src/test/data/postTestDataBySlug";
import { testDefaultRouteArgs } from "src/test/testValues";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";

const strings = getServerLocaleStrings(testDefaultRouteArgs.localeCode);

const post = postTestDataBySlug["test-post"];

const path = routeUrls.blogPost({
  localeCode: testDefaultRouteArgs.localeCode,
  platform: testDefaultRouteArgs.platform,
  slug: post.slug,
});

test(`Blog post page renders expected text and metadata`, async ({ page }) => {
  await page.goto(path);

  // ---------------------------------
  // --- Main heading and metadata ---
  // ---------------------------------

  await expectPageMainHeadingAndMetadata({
    mainHeading: post.title,
    metaDescription: post.searchDescription,
    metaTitle: post.title,
    page,
    path,
    strings,
  });

  // ---------------------
  // --- Accessibility ---
  // ---------------------

  await expectPageToHaveNoAxeViolations({ page });
});
