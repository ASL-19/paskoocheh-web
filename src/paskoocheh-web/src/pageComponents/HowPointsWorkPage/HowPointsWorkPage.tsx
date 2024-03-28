import { css } from "@emotion/react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import HowPointsWorkList from "src/components/RewardsPage/HowPointsWork/HowPointsWorkList";
import { HowPointsWorkListItemInfoText } from "src/components/RewardsPage/HowPointsWork/HowPointsWorkListItem";
import useHowPointsWorkListItemInfos from "src/hooks/useHowPointsWorkListItemInfos";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import {
  dashboardContainer,
  dashboardGridContainer,
} from "src/styles/dashboardStyles";
import { headingH6SemiBold } from "src/styles/typeStyles";
import { PaskoochehNextPage } from "src/types/pageTypes";

export type HowPointsWorkPageStrings = {
  lists: {
    /**
     * "Earn points" list.
     */
    earnPoints: {
      heading: string;
      items: {
        rateAndReviewApps: HowPointsWorkListItemInfoText;
        referFriends: HowPointsWorkListItemInfoText;
        updateApps: HowPointsWorkListItemInfoText;
        weeklyChallenge: HowPointsWorkListItemInfoText;
      };
    };

    /**
     * "Redeem points" list.
     */
    redeemPoints: {
      heading: string;
      items: {
        redeemPaidVpnApps: HowPointsWorkListItemInfoText;
      };
    };
  };

  /**
   * Page SEO description.
   */
  pageDescription: string;

  /**
   * Page title.
   */
  pageTitle: string;
};

const pageTitle = css(headingH6SemiBold, {});

const container = css(dashboardContainer, {
  paddingBottom: "3.25rem",
  paddingTop: "3.25rem",
});

// ==============================
// === Next.js page component ===
// ==============================
const HowPointsWorkPage: PaskoochehNextPage = () => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const { earnPointsListItemInfos, redeemPointsListItemInfos } =
    useHowPointsWorkListItemInfos();

  return (
    <PageContainer>
      <PageMeta
        canonicalPath={routeUrls.rewardsHowPointsWork({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        })}
        description={strings.HowPointsWorkPage.pageDescription || null}
        image={null}
        isAvailableInAlternateLocales={true}
        title={strings.HowPointsWorkPage.pageTitle}
      />

      <PageSegment as="main" centeredContainerCss={container}>
        <h1 css={pageTitle} id="main-heading">
          {strings.HowPointsWorkPage.pageTitle}
        </h1>
        <div css={dashboardGridContainer}>
          <HowPointsWorkList
            list={earnPointsListItemInfos}
            label={strings.HowPointsWorkPage.lists.earnPoints.heading}
          />
          <HowPointsWorkList
            list={redeemPointsListItemInfos}
            label={strings.HowPointsWorkPage.lists.redeemPoints.heading}
          />
        </div>

        <A11yShortcutPreset preset="skipToNavigation" />
      </PageSegment>
    </PageContainer>
  );
};

export default HowPointsWorkPage;
