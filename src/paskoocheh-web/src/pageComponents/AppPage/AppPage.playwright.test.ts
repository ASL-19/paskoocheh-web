import { expect, test } from "@playwright/test";

import { appDetailsSectionIds } from "src/components/App/appValues";
import routeUrls from "src/routeUrls";
import toolTestDataBySlug from "src/test/data/toolTestDataBySlug";
import { testDefaultRouteArgs } from "src/test/testValues";
import formatNumber from "src/utils/formatNumber";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

const localeCode = testDefaultRouteArgs.localeCode;
const strings = getServerLocaleStrings(localeCode);
const slug = toolTestDataBySlug["beepass-vpn"].slug;
const platform = testDefaultRouteArgs.platform;
const toolType = toolTestDataBySlug["beepass-vpn"]?.toolTypes
  ? toolTestDataBySlug["beepass-vpn"]?.toolTypes[0]?.slug
  : "";
const path = routeUrls.app({
  localeCode,
  platform,
  slug,
  toolType: toolType ?? "tool-type",
});

test(`AppPage renders expected metadata`, async ({ page }) => {
  await navigateAndWaitForHydration({ page, path });

  // ---------------------------------
  // --- Main heading and metadata ---
  // ---------------------------------

  // TODO: update with App description when available
  await expectPageMainHeadingAndMetadata({
    mainHeading: toolTestDataBySlug["beepass-vpn"].name,
    metaDescription:
      toolTestDataBySlug["beepass-vpn"].info?.edges[0]?.node.seoDescription ??
      null,
    metaTitle: toolTestDataBySlug["beepass-vpn"].name,
    page,
    path,
    strings,
  });

  // ---------------------
  // --- Accessibility ---
  // ---------------------

  await expectPageToHaveNoAxeViolations({ page });
});

test(`AppPage renders AppTopHeaderSection`, async ({ page }) => {
  await navigateAndWaitForHydration({ page, path });

  const main = page.getByRole("main");

  await expect(
    main.getByRole("heading", { name: toolTestDataBySlug["beepass-vpn"].name }),
  ).toBeVisible();

  const appStatsList = main.getByRole("list", {
    name: strings.AppStatsDetails.a11yLabel,
  });

  await expect(appStatsList).toContainText(
    `${toolTestDataBySlug["beepass-vpn"].versions?.edges[0]?.node.averageRating?.starRating}`,
  );

  await expect(appStatsList).toContainText(
    formatNumber({
      localeCode,
      number:
        toolTestDataBySlug["beepass-vpn"].versions?.edges[0]?.node
          .downloadCount ?? 0,
    }),
  );

  const availableOperatingSystemsList = main.getByRole("list", {
    name: strings.AppOverviewSection.operatingSystem,
  });

  const androidPlatformLink = availableOperatingSystemsList.getByLabel(
    strings.shared.operatingSystemsNames[platform],
  );

  await expect(androidPlatformLink).toHaveAttribute("aria-current", "page");
});

test(`AppPage renders AppDetailsSection`, async ({ page }) => {
  await navigateAndWaitForHydration({ page, path });

  const appDetailsTabs = page.getByLabel(strings.AppNavLinkList.a11yLabel);

  // Ratings and Reviews
  const ratingsAndReviewsTab = appDetailsTabs.getByRole("link", {
    name: strings.AppDetailsSection.headings.ratingsAndReviews,
  });
  await expect(ratingsAndReviewsTab).toHaveAttribute(
    "href",
    `${routeUrls.app({
      localeCode,
      platform,
      slug,
      toolType: toolType ?? "tool-type",
    })}#${appDetailsSectionIds.ratingsAndReviews}`,
  );
  await ratingsAndReviewsTab.click();

  const ratingsAndReviewsContent = page.locator(
    `#${appDetailsSectionIds.ratingsAndReviews}`,
  );
  await expect(
    ratingsAndReviewsContent.getByRole("heading", {
      name: strings.OverallRatings.overallRating,
    }),
  ).toBeVisible();
  await expect(
    ratingsAndReviewsContent.getByRole("link", {
      name: strings.OverallRatings.buttonText,
    }),
  ).toHaveAttribute(
    "href",
    routeUrls.writeAReview({
      appId: toolTestDataBySlug["beepass-vpn"].slug,
      localeCode,
      platform,
    }),
  );

  // Additional Information
  const additionalInformationTab = appDetailsTabs.getByRole("link", {
    name: strings.AppDetailsSection.headings.additionalInfo,
  });
  await expect(additionalInformationTab).toHaveAttribute(
    "href",
    `${routeUrls.app({
      localeCode,
      platform,
      slug,
      toolType: toolType ?? "",
    })}#${appDetailsSectionIds.additionalInfo}`,
  );
  await additionalInformationTab.click();

  await expect(
    page.getByRole("heading", {
      name: strings.AppAdditionalInfoListItem.developerInformation,
    }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", {
      name: strings.AppAdditionalInfoListItem.productDescription,
    }),
  ).toBeVisible();

  // FAQ
  const faqTab = appDetailsTabs.getByRole("link", {
    name: strings.AppDetailsSection.headings.faq,
  });
  await expect(faqTab).toHaveAttribute(
    "href",
    `${routeUrls.app({
      localeCode,
      platform,
      slug,
      toolType: toolType ?? "",
    })}#${appDetailsSectionIds.faq}`,
  );

  // How to Use
  const howToUseTab = appDetailsTabs.getByRole("link", {
    name: strings.AppDetailsSection.headings.howToUse,
  });
  await expect(howToUseTab).toHaveAttribute(
    "href",
    `${routeUrls.app({
      localeCode,
      platform,
      slug,
      toolType: toolType ?? "",
    })}#${appDetailsSectionIds.howToUse}`,
  );
});
