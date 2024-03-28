import { expect, test } from "@playwright/test";

import routeUrls from "src/routeUrls";
import usersByUsername from "src/test/data/usersByUsername";
import { testDefaultRouteArgs } from "src/test/testValues";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

const localeCode = testDefaultRouteArgs.localeCode;
const strings = getServerLocaleStrings(localeCode);
const path = routeUrls.resetPasswordRequest(testDefaultRouteArgs);

test("Renders as expected", async ({ page }) => {
  await navigateAndWaitForHydration({
    page,
    path,
  });

  // ---------------------------------
  // --- Main heading and metadata ---
  // ---------------------------------

  await expectPageMainHeadingAndMetadata({
    mainHeading: strings.ResetPasswordRequestPage.resetPasswordHeading,
    metaDescription: strings.ResetPasswordRequestPage.pageDescription,
    metaTitle: strings.ResetPasswordRequestPage.title,
    page,
    path,
    strings,
  });

  // ---------------------
  // --- Accessibility ---
  // ---------------------

  await expectPageToHaveNoAxeViolations({ page });
});

test("ResetPasswordPage form submission works", async ({ page }) => {
  await navigateAndWaitForHydration({
    page,
    path,
  });

  // TODO: Update message text once form is working
  const confirmationMessage = strings.shared.form.errorMessages.network;

  // Test form submission
  await page
    .getByLabel(strings.shared.form.emailLabel)
    .fill(usersByUsername.mockuser.email);
  await page.getByRole("button", { name: strings.shared.button.send }).click();
  await expect(page.getByText(confirmationMessage)).toBeVisible();
});
