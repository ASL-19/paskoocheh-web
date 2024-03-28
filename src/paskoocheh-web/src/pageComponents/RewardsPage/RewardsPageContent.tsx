import { invisible } from "@asl-19/emotion-utils";
import { css } from "@emotion/react";
import { FC, useMemo, useRef, useState } from "react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import { AppNavLinkInfo } from "src/components/App/AppTabContent/AppNavLinkListItem";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import RewardsDetailsSection from "src/components/RewardsPage/RewardDetailsSection";
import RewardsPointsSection from "src/components/RewardsPage/RewardsPointsSection";
import {
  RewardsDetailsSectionId,
  rewardsDetailsSectionIds,
} from "src/components/RewardsPage/rewardsValues";
import {
  GqlEarningMethod,
  GqlQuizPage,
  GqlRedemptionMethod,
  GqlRewardRecord,
} from "src/generated/graphQl";
import useOnSectionLinkClick from "src/hooks/useOnSectionLinkClick";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { RewardsProvider, RewardsState } from "src/stores/rewardsStore";
import { dashboardContainer } from "src/styles/dashboardStyles";
import { ValidVersionPreview } from "src/types/appTypes";
import { breakpointStyles } from "src/utils/media/media";

// =============
// === Types ===
// =============

export type RewardsPageContentProps = {
  earningMethods: Array<GqlEarningMethod> | null;
  hasFinishedQuiz: boolean | null;
  initialRewardRecordsHasNextPage: boolean;
  pointsBalance: number;
  purchasedVersionPreviews: Array<ValidVersionPreview>;
  quizPage: GqlQuizPage | null;
  redemptionMethods: Array<GqlRedemptionMethod>;
  referralSlug: string;
  reviewedVersionPreviews: Array<ValidVersionPreview>;
  rewardRecords: Array<GqlRewardRecord>;
  userPinCode: number;
};

export type RewardsPageContentStrings = {
  /**
   * Dashboard heading
   */
  dashboard: string;
  /**
   * MyReview heading
   */
  myReview: string;
  /**
   * Page SEO description
   */
  pageDescription: string;
  /**
   * Page SEO title.
   */
  pageTitle: string;
  /**
   * text for points
   */
  points: string;
  /**
   * Records heading
   */
  records: string;
  /**
   * Redemption heading
   */
  redemption: string;
  /**
   * Share you referral link heading
   */
  shareYourReferral: string;
  /**
   * weekly challenge heading
   */
  weeklyChallenge: string;
  /**
   * Your Points Balance heading
   */
  yourPointsBalance: string;
};

// ==============
// === Styles ===
// ==============

const pageContainer = css(
  {
    padding: "3.25rem 0",
  },
  breakpointStyles({ singleColumn: { lt: { padding: "1rem 0" } } }),
);

const centeredContainerCss = css({
  display: "flex",
  flexDirection: "column",
  gap: "3.25rem",
});

// ==============================
// ===== Next.js component ======
// ==============================

const RewardsPageContent: FC<RewardsPageContentProps> = ({
  earningMethods,
  hasFinishedQuiz,
  initialRewardRecordsHasNextPage,
  pointsBalance,
  purchasedVersionPreviews,
  quizPage,
  redemptionMethods,
  referralSlug,
  reviewedVersionPreviews,
  rewardRecords,
  userPinCode,
}) => {
  const { localeCode } = useAppLocaleInfo();
  const { RewardsPageContent: strings } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const dashboardSectionRef = useRef<HTMLDivElement>(null);
  const myReviewSectionRef = useRef<HTMLDivElement>(null);
  const redemptionSectionRef = useRef<HTMLDivElement>(null);

  const dashboardNavItemRef = useRef<HTMLLIElement>(null);
  const myReviewsNavItemRef = useRef<HTMLLIElement>(null);
  const redemptionNavItemRef = useRef<HTMLLIElement>(null);

  const navLinkInfos = useMemo<
    [
      AppNavLinkInfo<RewardsDetailsSectionId>,
      AppNavLinkInfo<RewardsDetailsSectionId>,
      AppNavLinkInfo<RewardsDetailsSectionId>,
    ]
  >(() => {
    const appUrl = routeUrls.rewards({
      localeCode,
      platform: queryOrDefaultPlatformSlug,
    });

    return [
      {
        id: rewardsDetailsSectionIds.dashboard,
        navItemRef: dashboardNavItemRef,
        sectionRef: dashboardSectionRef,
        text: strings.dashboard,
        url: `${appUrl}#${rewardsDetailsSectionIds.dashboard}`,
      },
      {
        id: rewardsDetailsSectionIds.myReview,
        navItemRef: myReviewsNavItemRef,
        sectionRef: myReviewSectionRef,
        text: strings.myReview,
        url: `${appUrl}#${rewardsDetailsSectionIds.myReview}`,
      },
      {
        id: rewardsDetailsSectionIds.redemption,
        navItemRef: redemptionNavItemRef,
        sectionRef: redemptionSectionRef,
        text: strings.redemption,
        url: `${appUrl}#${rewardsDetailsSectionIds.redemption}`,
      },
    ];
  }, [localeCode, queryOrDefaultPlatformSlug, strings]);

  const [activeSectionId, setActiveSectionId] = useState(navLinkInfos[0].id);

  const quizCompletedEarningPoints =
    earningMethods?.find((item) => item.earningMethod === "quiz_completed")
      ?.earningPoints ?? 1;

  const quizWonEarningPoints =
    earningMethods?.find((item) => item.earningMethod === "quiz_won")
      ?.earningPoints ?? 1;

  const initialRewardsState: RewardsState = useMemo(
    () => ({
      initialRewardRecordsHasNextPage,
      pointsBalance,
      purchasedVersionPreviews,
      quizCompletedEarningPoints,
      quizPage,
      quizWonEarningPoints,
      redemptionMethods,
      reviewedVersionPreviews,
      rewardRecords,
      userPinCode,
    }),
    [
      initialRewardRecordsHasNextPage,
      pointsBalance,
      purchasedVersionPreviews,
      quizCompletedEarningPoints,
      quizPage,
      quizWonEarningPoints,
      redemptionMethods,
      reviewedVersionPreviews,
      rewardRecords,
      userPinCode,
    ],
  );

  const onRedemptionLinkClick = useOnSectionLinkClick({
    linkInfo: navLinkInfos[2],
    setActiveSectionId,
  });

  return (
    <PageContainer css={pageContainer}>
      <PageMeta
        canonicalPath={routeUrls.rewards({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        })}
        description={strings.pageDescription}
        image={null}
        isAvailableInAlternateLocales={false}
        title={strings.pageTitle}
      />

      <RewardsProvider initialState={initialRewardsState}>
        <PageSegment as="main" centeredContainerCss={centeredContainerCss}>
          <h1 css={invisible} id="main-heading">
            {strings.pageTitle}
          </h1>

          <RewardsPointsSection onRedemptionLinkClick={onRedemptionLinkClick} />

          <div css={dashboardContainer}>
            <RewardsDetailsSection
              activeSectionId={activeSectionId}
              navLinkInfos={navLinkInfos}
              setActiveSectionId={setActiveSectionId}
              referralSlug={referralSlug}
              hasFinishedQuiz={hasFinishedQuiz}
            />
          </div>

          <A11yShortcutPreset preset="skipToNavigation" />
        </PageSegment>
      </RewardsProvider>
    </PageContainer>
  );
};

export default RewardsPageContent;
