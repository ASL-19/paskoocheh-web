import { expect, Page, test } from "@playwright/test";

import routeUrls from "src/routeUrls";
import minimalUsersByUsername from "src/test/data/minimalUsersByUsername";
import usersByUsername from "src/test/data/usersByUsername";
import { testDefaultRouteArgs } from "src/test/testValues";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import expectPageMainHeadingAndMetadata from "src/utils/playwright/expectPageMainHeadingAndMetadata";
import expectPageToHaveNoAxeViolations from "src/utils/playwright/expectPageToHaveNoAxeViolations";
import navigateAndWaitForHydration from "src/utils/playwright/navigateAndWaitForHydration";

const localeCode = testDefaultRouteArgs.localeCode;
const path = routeUrls.rewards(testDefaultRouteArgs);
const strings = getServerLocaleStrings(localeCode);

const signInAndNavigateToRewardsPage = async ({ page }: { page: Page }) =>
  await navigateAndWaitForHydration({
    page,
    path,
    username: usersByUsername.mockuser.username,
  });

const getVisibleLinkWithName = ({ name, page }: { name: string; page: Page }) =>
  page
    .getByRole("link", {
      name,
    })
    // Useful since e.g. AppNavLinkList renders two lists (using
    // hiddenWhenPointerCoarse and hiddenWhenPointerFine)
    .locator("visible=true");

test("Renders as expected", async ({ page }) => {
  await signInAndNavigateToRewardsPage({ page });

  await expectPageMainHeadingAndMetadata({
    mainHeading: strings.RewardsPageContent.pageTitle,
    metaDescription: strings.RewardsPageContent.pageDescription,
    page,
    path,
    strings,
  });

  // ---------------------
  // --- Accessibility ---
  // ---------------------
  await expectPageToHaveNoAxeViolations({ page });
});

test(`Renders "Your Points Balance" section and opens "Redemption" section when "Redeem" button clicked`, async ({
  page,
}) => {
  await signInAndNavigateToRewardsPage({ page });

  const redeemLink = page.getByRole("link", {
    name: strings.shared.button.redeem,
  });

  await redeemLink.click();

  await expect(
    page.getByRole("region", {
      name: strings.RewardsPageContent.redemption,
    }),
  ).toBeVisible();
});

test(`Renders "Redemption" section`, async ({ page }) => {
  await signInAndNavigateToRewardsPage({ page });

  const redemptionLink = getVisibleLinkWithName({
    name: strings.RewardsPageContent.redemption,
    page,
  });

  await redemptionLink.click();

  await expect(
    page.getByRole("region", { name: strings.RewardsPageContent.redemption }),
  ).toBeVisible();
});

test(`Renders "My Review" section`, async ({ page }) => {
  await signInAndNavigateToRewardsPage({ page });

  const myReviewLink = getVisibleLinkWithName({
    name: strings.RewardsPageContent.myReview,
    page,
  });

  const reviewColumns = page.getByLabel(strings.RewardsPageContent.myReview);
  const purchasedAppCount = reviewColumns.getByText(
    `${strings.RewardsReview.notYetReviewed}(1)`,
  );
  const reviewedAppCount = reviewColumns.getByText(
    `${strings.RewardsReview.previouslyReviewed}(1)`,
  );

  await myReviewLink.click();

  await expect(
    page.getByRole("region", { name: strings.RewardsPageContent.myReview }),
  ).toBeVisible();

  await expect(purchasedAppCount).toBeVisible();
  await expect(reviewedAppCount).toBeVisible();
});

test(`Renders "How Points Work" section and opens "How points work" page when "Learn more" link clicked`, async ({
  page,
}) => {
  await signInAndNavigateToRewardsPage({ page });

  const learnMoreLink = page.getByRole("link", {
    name: strings.shared.learnMore,
  });
  await learnMoreLink.click();
  await page.waitForURL(routeUrls.rewardsHowPointsWork(testDefaultRouteArgs));
});

test(`Renders "Dashboard" tab`, async ({ context, page }) => {
  await signInAndNavigateToRewardsPage({ page });

  await context.grantPermissions(["clipboard-read", "clipboard-write"]);

  // Click "My review" link to switch tabs

  const myReviewLink = getVisibleLinkWithName({
    name: strings.RewardsPageContent.myReview,
    page,
  });

  await myReviewLink.click();

  // Click "Dashboard" link to return to dashboard tab

  const dashboardLink = getVisibleLinkWithName({
    name: strings.RewardsPageContent.dashboard,
    page,
  });

  await dashboardLink.click();

  // Check if dashboard tab is visible

  const dashboardTab = page.getByRole("region", {
    name: strings.RewardsPageContent.dashboard,
  });

  await expect(dashboardTab).toBeVisible();

  // Check if "Get started" button is visible

  const getStartedButton = dashboardTab.getByRole("button", {
    name: strings.shared.button.getStarted,
  });

  await expect(getStartedButton).toBeVisible();

  // TODO: Test starting quiz by clicking getStartedButton?

  await dashboardTab
    .getByRole("button", {
      name: strings.RewardsReferralLink.copyButtonA11yLabel,
    })
    .click();

  const clipboardText = await page.evaluate(
    async () => await navigator.clipboard.readText(),
  );

  expect(clipboardText).toEqual(
    `${process.env.NEXT_PUBLIC_WEB_URL}${routeUrls.createAnAccount({
      localeCode,
      referral: minimalUsersByUsername.mockuser.referralSlug ?? undefined,
    })}`,
  );

  await expect(
    dashboardTab.getByText(strings.RewardsPageContent.records),
  ).toBeVisible();

  // TODO: Test record entries when real data is available
});
