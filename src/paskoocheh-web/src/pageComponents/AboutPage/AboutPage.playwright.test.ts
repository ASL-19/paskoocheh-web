import { test } from "@playwright/test";

import routeUrls from "src/routeUrls";
import staticPageTestDataBySlug from "src/test/data/staticPageTestDataBySlug";
import { testDefaultRouteArgs } from "src/test/testValues";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

const path = routeUrls.about(testDefaultRouteArgs);
const staticPage = staticPageTestDataBySlug.about;
const strings = getServerLocaleStrings(testDefaultRouteArgs.localeCode);

test("Renders as expected", async ({ page }) => {
  await navigateAndWaitForHydration({ page, path });

  // ---------------------------------
  // --- Main heading and metadata ---
  // ---------------------------------

  await expectPageMainHeadingAndMetadata({
    mainHeading: staticPage.title,
    metaDescription: staticPage.searchDescription,
    metaTitle: staticPage.seoTitle,
    page,
    path,
    strings,
  });

  // ---------------------
  // --- Accessibility ---
  // ---------------------

  await expectPageToHaveNoAxeViolations({ page });
});
