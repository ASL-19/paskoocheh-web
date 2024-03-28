import { expect, test } from "@playwright/test";

import routeUrls from "src/routeUrls";
import versionTestDataBySlug from "src/test/data/versionTestDataBySlug";
import { testDefaultRouteArgs } from "src/test/testValues";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

const localeCode = testDefaultRouteArgs.localeCode;
const tool = versionTestDataBySlug["beepass-vpn"].tool?.pk;
const platform = testDefaultRouteArgs.platform;
const strings = getServerLocaleStrings(testDefaultRouteArgs.localeCode);
const path = routeUrls.writeYourMessage({ localeCode, platform, tool });

test("WriteYourMessagePage renders as expected", async ({ page }) => {
  await navigateAndWaitForHydration({ page, path });

  await expectPageMainHeadingAndMetadata({
    mainHeading: strings.WriteYourMessagePage.writeYourMessageHeading,
    metaDescription: strings.WriteYourMessagePage.pageDescription,
    page,
    path,
    strings,
  });

  // ---------------------
  // --- Accessibility ---
  // ---------------------

  await expectPageToHaveNoAxeViolations({ page });
});

test(`Form submits and displays confirmation message`, async ({ page }) => {
  await navigateAndWaitForHydration({ page, path });

  const form = page.getByRole("form", {
    name: strings.WriteYourMessagePage.pageTitle,
  });

  const submitButton = form.getByRole("button", {
    name: strings.shared.form.submitButton,
  });

  // TODO: Update message text once form is working
  const confirmationMessage = "Message Submitted";

  await form
    .getByLabel(strings.shared.form.emailLabel)
    .fill("testUser@test.com");

  await form
    .getByLabel(strings.shared.form.messageLabel)
    .fill("Contrary to popular belief, Lorem Ipsum is not simply random text.");

  await submitButton.click();
  await expect(form.getByText(confirmationMessage)).toBeVisible();
});
