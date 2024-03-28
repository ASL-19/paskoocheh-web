import { expect, test } from "@playwright/test";

import routeUrls from "src/routeUrls";
import { testDefaultRouteArgs } from "src/test/testValues";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

const localeCode = testDefaultRouteArgs.localeCode;
const strings = getServerLocaleStrings(localeCode);
const path = routeUrls.rewardsHowPointsWork(testDefaultRouteArgs);

test("Renders as expected", async ({ page }) => {
  await navigateAndWaitForHydration({
    page,
    path: routeUrls.rewardsHowPointsWork(testDefaultRouteArgs),
  });

  // ---------------------------------
  // --- Main heading and metadata ---
  // ---------------------------------

  await expectPageMainHeadingAndMetadata({
    mainHeading: strings.HowPointsWork.heading,
    metaDescription: strings.HowPointsWorkPage.pageDescription,
    metaTitle: strings.HowPointsWorkPage.pageTitle,
    page,
    path,
    strings,
  });

  // ---------------------
  // --- Accessibility ---
  // ---------------------

  await expectPageToHaveNoAxeViolations({ page });
});

test(`HowPointsWorkPage renders page content`, async ({ page }) => {
  await navigateAndWaitForHydration({
    page,
    path: routeUrls.rewardsHowPointsWork(testDefaultRouteArgs),
  });

  const mainHeadingElement = page.getByRole("heading").first();
  await expect(mainHeadingElement).toContainText(
    strings.HowPointsWorkPage.pageTitle,
  );

  await expect(
    page.getByText(strings.HowPointsWorkPage.lists.earnPoints.heading),
  ).toBeVisible();

  await expect(
    page.getByText(strings.HowPointsWorkPage.lists.redeemPoints.heading),
  ).toBeVisible();

  await expect(
    page.getByRole("heading", {
      name: strings.HowPointsWorkPage.lists.earnPoints.items.rateAndReviewApps
        .heading,
    }),
  ).toBeVisible();

  await expect(
    page.getByText(
      strings.HowPointsWorkPage.lists.earnPoints.items.rateAndReviewApps
        .description,
    ),
  ).toBeVisible();

  await expect(
    page.getByRole("heading", {
      name: strings.HowPointsWorkPage.lists.redeemPoints.items.redeemPaidVpnApps
        .heading,
    }),
  ).toBeVisible();

  await expect(
    page.getByText(
      strings.HowPointsWorkPage.lists.redeemPoints.items.redeemPaidVpnApps
        .description,
    ),
  ).toBeVisible();
});
