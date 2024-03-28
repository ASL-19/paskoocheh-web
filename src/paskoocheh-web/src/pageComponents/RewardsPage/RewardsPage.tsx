import { useCallback } from "react";

import useDashboardPageAccessAndLoadingLogic, {
  FetchPropsOrErrorMessage,
} from "src/hooks/useDashboardPageAccessAndLoading";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import RewardsPageContent, {
  RewardsPageContentProps,
} from "src/pageComponents/RewardsPage/RewardsPageContent";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { isValidVersionPreview } from "src/types/appTypes";
import { PaskoochehNextPage } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import { rewardRecordsPerPage } from "src/values/indexPageValues";

// =============
// === Types ===
// =============

const RewardsPage: PaskoochehNextPage = () => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryPlatform = useQueryOrDefaultPlatformSlug();

  const fetchPropsOrErrorMessage: FetchPropsOrErrorMessage<RewardsPageContentProps> =
    useCallback(async () => {
      const graphQlSdk = await getGraphQlSdk();

      try {
        const [
          quizzesResponse,
          meResponse,
          rewardRecordsResponse,
          redemptionMethodsResponse,
          earningMethodsResponse,
          userPurchasedAppsResponse,
          userReviewedAppsResponse,
        ] = await Promise.all([
          graphQlSdk.getQuizzes({
            first: 1,
            locale: localeCode,
          }),
          graphQlSdk.getMe(),
          graphQlSdk.getRewardRecords({
            count: rewardRecordsPerPage,
            offset: 0,
          }),
          graphQlSdk.getRedemptionMethods(),
          graphQlSdk.getEarningMethods(),
          graphQlSdk.getUserPurchasedApps({ reviewed: false }),
          graphQlSdk.getUserPurchasedApps({ reviewed: true }),
        ]);

        const quizPage =
          (quizzesResponse.quizzes?.edges || []).reduce(
            (acc, edge) => (edge?.node ? [...acc, edge.node] : acc),
            [],
          )[0] ?? null;

        const hasFinishedQuiz = quizPage
          ? (
              await graphQlSdk.getHasFinishedQuiz({
                quizPk: quizPage.pk,
              })
            ).me?.hasFinishedQuiz ?? null
          : null;

        const pointsBalance = meResponse.me?.pointsBalance ?? 0;

        const rewardRecords = (
          rewardRecordsResponse.me?.rewardsRecords?.edges ?? []
        ).reduce(
          (acc, userRewardRecords) =>
            userRewardRecords.node ? [...acc, userRewardRecords.node] : acc,
          [],
        );

        const initialRewardRecordsHasNextPage =
          !!rewardRecordsResponse.me?.rewardsRecords?.pageInfo.hasNextPage;

        const referralSlug = meResponse.me?.referralSlug ?? "";

        const redemptionMethods = (
          redemptionMethodsResponse.redemptionMethods?.edges ?? []
        ).reduce((acc, edge) => (edge.node ? [...acc, edge.node] : acc), []);

        const userPinCode = meResponse.me?.pin ?? 0;
        const earningMethods = earningMethodsResponse.earningMethods;
        const purchasedVersionPreviews = (
          userPurchasedAppsResponse.me?.purchasedApps || []
        ).reduce(
          (acc, versionPreview) =>
            versionPreview && isValidVersionPreview(versionPreview)
              ? [...acc, versionPreview]
              : acc,
          [],
        );

        const reviewedVersionPreviews = (
          userReviewedAppsResponse.me?.purchasedApps ?? []
        ).reduce(
          (acc, versionPreview) =>
            versionPreview && isValidVersionPreview(versionPreview)
              ? [...acc, versionPreview]
              : acc,
          [],
        );

        return {
          props: {
            earningMethods,
            hasFinishedQuiz,
            initialRewardRecordsHasNextPage,
            platform: queryPlatform,
            pointsBalance,
            purchasedVersionPreviews,
            quizPage,
            redemptionMethods,
            referralSlug,
            reviewedVersionPreviews,
            rewardRecords,
            userPinCode,
          },
        };
      } catch {
        return {
          errorMessage: strings.shared.dashboard.errorMessages.default,
        };
      }
    }, [localeCode, queryPlatform, strings]);

  return useDashboardPageAccessAndLoadingLogic<RewardsPageContentProps>({
    fetchPropsOrErrorMessage,
    PageContentComponent: RewardsPageContent,
  });
};

export default RewardsPage;
