import { expect, test } from "@playwright/test";

import routeUrls from "src/routeUrls";
import versionTestDataBySlug from "src/test/data/versionTestDataBySlug";
import { testDefaultRouteArgs } from "src/test/testValues";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

const localeCode = testDefaultRouteArgs.localeCode;
const strings = getServerLocaleStrings(localeCode);

const appPreview = versionTestDataBySlug["beepass-vpn"];

const path = routeUrls.writeAReview({
  appId: appPreview.tool?.pk.toString() || "0",
  localeCode,
  platform: testDefaultRouteArgs.platform,
});

test("Renders as expected", async ({ page }) => {
  await navigateAndWaitForHydration({ page, path });

  await expectPageMainHeadingAndMetadata({
    mainHeading: strings.WriteAReviewPage.title,
    metaDescription: strings.WriteAReviewPage.description,
    metaTitle: strings.WriteAReviewPage.title,
    page,
    path,
    strings,
  });

  await expect(
    page.getByRole("heading", { name: appPreview.tool?.name }),
  ).toBeVisible();

  // ---------------------
  // --- Accessibility ---
  // ---------------------

  await expectPageToHaveNoAxeViolations({ page });
});

test(`WriteAReviewPage test form submission`, async ({ page }) => {
  await navigateAndWaitForHydration({ page, path });

  // TODO: Update App name and ID when placeholder text is removed
  await expect(
    page.getByRole("heading", { name: appPreview.tool?.name }),
  ).toBeVisible();

  const starOverallRatingHeading = page.getByRole("heading", {
    name: strings.WriteAReview.overallRatingHeading,
  });
  const starOverallRatingThirdStar = page
    .getByRole("button", {
      name: strings.StarRatings.setRatingAriaLabel.replace("{rating}", `3`),
    })
    .first();

  const submitButton = page
    .getByRole("button", { name: strings.shared.form.submitButton })
    .first();

  // Test star ratings
  await expect(starOverallRatingHeading).toBeVisible();
  await starOverallRatingThirdStar.click();
  const starRating = page.getByRole("button", {
    name: strings.StarRatings.unsetRatingAriaLabel,
  });
  expect(starRating).toBeVisible;

  // Test form submission
  await page
    .getByLabel(strings.shared.form.titleLabel)
    .fill("Review title text");
  await page
    .getByLabel(strings.shared.form.messageLabel)
    .fill("Contrary to popular belief, Lorem Ipsum is not simply random text.");
  await submitButton.click();
  // TODO: Check for confirmation once form is functional
  //   await expect(page.getByText(confirmationMessage)).toBeVisible();
});
