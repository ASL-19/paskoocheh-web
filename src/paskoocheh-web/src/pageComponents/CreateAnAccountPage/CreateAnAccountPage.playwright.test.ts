import { expect, test } from "@playwright/test";

import routeUrls from "src/routeUrls";
import { testDefaultRouteArgs } from "src/test/testValues";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

const localeCode = testDefaultRouteArgs.localeCode;
const strings = getServerLocaleStrings(localeCode);
const path = routeUrls.createAnAccount(testDefaultRouteArgs);

test("Renders as expected", async ({ page }) => {
  await page.goto(path);
  await navigateAndWaitForHydration({
    page,
    path: routeUrls.createAnAccount(testDefaultRouteArgs),
  });

  // ---------------------------------
  // --- Main heading and metadata ---
  // ---------------------------------

  await expectPageMainHeadingAndMetadata({
    mainHeading: strings.CreateAnAccountPage.title,
    metaDescription: strings.CreateAnAccountPage.pageDescription,
    metaTitle: strings.CreateAnAccountPage.title,
    page,
    path,
    strings,
  });

  // ---------------------
  // --- Accessibility ---
  // ---------------------

  await expectPageToHaveNoAxeViolations({ page });
});

test("CreateAnAccountPage form submission works", async ({ page }) => {
  await navigateAndWaitForHydration({
    page,
    path: routeUrls.createAnAccount(testDefaultRouteArgs),
  });

  // TODO: Update message text once form is working
  const confirmationMessage = strings.shared.form.errorMessages.network;

  // Test form submission
  await page
    .getByLabel(strings.CreateAnAccountPage.usernameLabel)
    .fill("testUser");
  await page
    .getByLabel(strings.CreateAnAccountPage.emailLabel)
    .fill("testUser@test.com");
  await page
    .getByLabel(strings.CreateAnAccountPage.passwordLabel, { exact: true })
    .fill("myPassword");
  await page
    .getByLabel(strings.CreateAnAccountPage.reenterPasswordLabel, {
      exact: true,
    })
    .fill("myPassword");
  await page
    .getByRole("button", { name: strings.CreateAnAccountPage.submitButton })
    .click();
  await expect(page.getByText(confirmationMessage)).toBeVisible();
});
