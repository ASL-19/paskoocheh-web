import { expect, test } from "@playwright/test";

import routeUrls from "src/routeUrls";
import { testDefaultRouteArgs } from "src/test/testValues";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

const strings = getServerLocaleStrings(testDefaultRouteArgs.localeCode);
const path = routeUrls.account(testDefaultRouteArgs);

const dummyUserInfo = {
  email: "abc123@gmail.com",
  id: "9",
  username: "abc123",
};

test(`AccountSettingsPage renders expected text and metadata`, async ({
  page,
}) => {
  await navigateAndWaitForHydration({ page, path });

  // TODO: Update App name and ID when placeholder text is removed
  await expectPageMainHeadingAndMetadata({
    mainHeading: strings.AccountSettingsPageContent.pageTitle,
    metaDescription: strings.AccountSettingsPageContent.pageDescription,
    metaTitle: strings.AccountSettingsPageContent.pageTitle,
    page,
    path,
    strings,
  });

  await expectPageToHaveNoAxeViolations({ page });
});

test(`AccountSettingsPageContent renders form fields default values`, async ({
  page,
}) => {
  await navigateAndWaitForHydration({ page, path });

  await expect(
    page.getByLabel(strings.AccountSettingsPageContent.usernameLabel),
  ).toHaveValue(dummyUserInfo.username);

  await expect(
    page.getByLabel(strings.AccountSettingsPageContent.emailLabel),
  ).toHaveValue(dummyUserInfo.email);

  await expect(
    page.getByLabel(strings.AccountSettingsPageContent.passwordLabel, {
      exact: true,
    }),
  ).toHaveValue("");

  await expect(
    page.getByLabel(strings.AccountSettingsPageContent.reenterPasswordLabel, {
      exact: true,
    }),
  ).toHaveValue("");
});

test(`AccountSettingsPage test "Delete Account" functionality`, async ({
  page,
}) => {
  await navigateAndWaitForHydration({ page, path });

  await page
    .getByRole("button", {
      name: strings.AccountSettingsPageContent.buttonDelete,
    })
    .click();

  const deleteAccountModalHeading = page.getByRole("heading", {
    name: strings.DeleteAccountOverlay.title,
  });

  await expect(deleteAccountModalHeading).toBeVisible();

  // TODO: Add additional functionality when form is active
  await page
    .getByRole("button", { name: strings.DeleteAccountOverlay.cancelButton })
    .click();

  await expect(deleteAccountModalHeading).not.toBeVisible();
});
