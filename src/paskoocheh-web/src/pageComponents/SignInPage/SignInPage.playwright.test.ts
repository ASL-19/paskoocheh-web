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
const path = routeUrls.signIn(testDefaultRouteArgs);

test("Renders as expected", async ({ page }) => {
  await navigateAndWaitForHydration({
    page,
    path,
  });

  // ---------------------------------
  // --- Main heading and metadata ---
  // ---------------------------------

  await expectPageMainHeadingAndMetadata({
    mainHeading: strings.SignInPage.title,
    metaDescription: strings.SignInPage.pageDescription,
    metaTitle: strings.SignInPage.title,
    page,
    path,
    strings,
  });

  // ---------------------
  // --- Accessibility ---
  // ---------------------

  await expectPageToHaveNoAxeViolations({ page });
});

test("SignInPage form submission works", async ({ page }) => {
  await navigateAndWaitForHydration({
    page,
    path,
  });

  const confirmationMessage = strings.SignInPage.confirmation;
  const errorMessage = strings.shared.form.errorMessages.network;

  await navigateAndWaitForHydration({
    page,
    path,
  });
  await page
    .getByLabel(strings.SignInPage.usernameLabel)
    .fill(usersByUsername.mockuser.username);
  await page
    .getByLabel(strings.SignInPage.passwordLabel)
    .fill(usersByUsername.mockuser.username);

  await page
    .getByRole("button", { name: strings.SignInPage.submitButton })
    .click();

  await expect(page.getByText(confirmationMessage)).toBeVisible();
  await expect(page.getByText(errorMessage)).not.toBeVisible();
});
