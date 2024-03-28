import { expect, test } from "@playwright/test";

import routeUrls from "src/routeUrls";
import { testDefaultRouteArgs } from "src/test/testValues";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

const localeCode = testDefaultRouteArgs.localeCode;
const strings = getServerLocaleStrings(localeCode);

const path = routeUrls.home(testDefaultRouteArgs);

test(`Renders as expected`, async ({ page }) => {
  await navigateAndWaitForHydration({
    page,
    path: routeUrls.home(testDefaultRouteArgs),
  });

  // ---------------------------------
  // --- Main heading and metadata ---
  // ---------------------------------

  await expectPageMainHeadingAndMetadata({
    mainHeading: strings.shared.siteTitle,
    metaDescription: strings.HomePage.pageDescription,
    metaTitle: null,
    page,
    path,
    strings,
  });

  // -------------------------
  // --- Popular apps list ---
  // -------------------------

  const popularAppsList = page.getByRole("list", {
    name: `${strings.HomePagePopularAppsSegment.headingPrefix} ${strings.HomePagePopularAppsSegment.headingSuffix}`,
  });

  // Check that at least one item is available in the list
  await expect(popularAppsList.getByRole("listitem").first()).toBeVisible();

  // ----------------------------
  // --- Editor’s choice list ---
  // ----------------------------

  const editorsChoiceList = page.getByRole("list", {
    name: strings.HomePageEditorsChoiceSegment.heading,
  });

  // Check that at least one item is available in the list
  await expect(editorsChoiceList.getByRole("listitem").first()).toBeVisible();

  // ---------------------
  // --- Accessibility ---
  // ---------------------

  await expectPageToHaveNoAxeViolations({ page });
});
