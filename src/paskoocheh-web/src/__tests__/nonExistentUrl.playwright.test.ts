import { expect, test } from "@playwright/test";

import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";
import { localeCodes } from "src/values/localeValues";

localeCodes.forEach((localeCode) => {
  const strings = getServerLocaleStrings(localeCode);

  test(`Non-existent ${localeCode} URL renders localized 404 page with 404 status code`, async ({
    page,
  }) => {
    const response = await navigateAndWaitForHydration({
      page,
      path: `/${localeCode}/NON-EXISTENT-PAGE?platform=android`,
    });

    expect(response?.status()).toBe(404);

    const mainHeadingElement = page.locator("#main-heading");

    await expect(mainHeadingElement).toContainText(
      strings.ErrorPageContent.generic[404].title,
    );
  });
});
