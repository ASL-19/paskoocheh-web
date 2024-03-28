import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useCallback, useEffect, useState } from "react";

import IndexPageLoadingUi from "src/components/IndexPageLoadingUi";
import RewardsReviewAppsList from "src/components/RewardsPage/RewardsReview/RewardsReviewAppsList";
import { IndexPageLoadingState } from "src/hooks/useIndexPageLoadingAndQueryLogic";
import { useAppStrings } from "src/stores/appStore";
import {
  useRewardsPurchasedVersionPreviews,
  useRewardsReviewedVersionPreviews,
} from "src/stores/rewardsStore";
import {
  dashboardGridContainer,
  dashboardItemContainer,
  dashboardItemTitle,
} from "src/styles/dashboardStyles";
import { breakpointStyles } from "src/utils/media/media";
import { rewardReviewsPerPage } from "src/values/indexPageValues";

export type RewardsReviewStrings = {
  /**
   * Text for Not yet Reviewed
   */
  notYetReviewed: string;
  /**
   * Text for previously Reviewed
   */
  previouslyReviewed: string;
};

const box = css(
  dashboardItemContainer,
  {
    gridColumn: "span 6",
    justifyContent: "flex-start",
  },
  breakpointStyles({
    desktopNarrow: {
      lt: { gridColumn: "span 12" },
    },
  }),
);
const RewardsReview: StylableFC<{}> = memo(
  ({ className, ...remainingProps }) => {
    const { RewardsReview: strings, shared: sharedStrings } = useAppStrings();

    const purchasedVersionPreviews = useRewardsPurchasedVersionPreviews();
    const reviewedVersionPreviews = useRewardsReviewedVersionPreviews();

    //ReviewTab
    const [
      reviewedVersionPreviewsLoadingState,
      setReviewedVersionPreviewsLoadingState,
    ] = useState<IndexPageLoadingState>({ type: "hasMore" });
    const [
      notYetReviewedVersionPreviewsLoadingState,
      setNotYetReviewedVersionPreviewsLoadingState,
    ] = useState<IndexPageLoadingState>({ type: "hasMore" });

    const loadMoreReviewedVersionPreviews = useCallback(() => {
      setReviewedVersionPreviewsLoadingState({ type: "loadingMore" });
    }, [setReviewedVersionPreviewsLoadingState]);

    const loadMoreNotYetReviewedVersionPreviews = useCallback(() => {
      setNotYetReviewedVersionPreviewsLoadingState({ type: "loadingMore" });
    }, [setNotYetReviewedVersionPreviewsLoadingState]);

    const purchasedAppsLength = purchasedVersionPreviews?.length ?? 0;
    const userReviewsLength = reviewedVersionPreviews?.length ?? 0;

    useEffect(() => {
      setReviewedVersionPreviewsLoadingState({ type: "loadingNew" });
      setNotYetReviewedVersionPreviewsLoadingState({ type: "loadingNew" });

      const reviewedLoadingState =
        userReviewsLength === 0
          ? "hasNone"
          : userReviewsLength > rewardReviewsPerPage
            ? "hasMore"
            : "hasNoMore";
      const notYetReviewedLoadingState =
        purchasedAppsLength === 0
          ? "hasNone"
          : purchasedAppsLength > rewardReviewsPerPage
            ? "hasMore"
            : "hasNoMore";
      setReviewedVersionPreviewsLoadingState({ type: reviewedLoadingState });
      setNotYetReviewedVersionPreviewsLoadingState({
        type: notYetReviewedLoadingState,
      });
    }, [purchasedAppsLength, userReviewsLength]);

    return (
      <div
        className={className}
        css={dashboardGridContainer}
        id="review"
        {...remainingProps}
      >
        <div css={box}>
          <p css={dashboardItemTitle}>
            {strings.notYetReviewed}({purchasedAppsLength})
          </p>
          {!["error", "hasNone", "loadingNew"].includes(
            notYetReviewedVersionPreviewsLoadingState.type,
          ) &&
            purchasedVersionPreviews &&
            purchasedVersionPreviews.length > 0 && (
              <RewardsReviewAppsList
                versionPreviews={purchasedVersionPreviews}
                type="notYetReviewed"
              />
            )}
          <IndexPageLoadingUi
            loadMoreLinkText={sharedStrings.button.more}
            loadingState={notYetReviewedVersionPreviewsLoadingState}
            onClick={loadMoreNotYetReviewedVersionPreviews}
            buttonType="button"
          />
        </div>
        <div css={box}>
          <p css={dashboardItemTitle}>
            {strings.previouslyReviewed}({userReviewsLength})
          </p>
          {!["error", "hasNone", "loadingNew"].includes(
            reviewedVersionPreviewsLoadingState.type,
          ) &&
            reviewedVersionPreviews &&
            reviewedVersionPreviews.length > 0 && (
              <RewardsReviewAppsList
                versionPreviews={reviewedVersionPreviews}
                type="reviewed"
              />
            )}
          <IndexPageLoadingUi
            loadMoreLinkText={sharedStrings.button.more}
            loadingState={reviewedVersionPreviewsLoadingState}
            onClick={loadMoreReviewedVersionPreviews}
            buttonType="button"
          />
        </div>
      </div>
    );
  },
);

RewardsReview.displayName = "RewardsReview";

export default RewardsReview;
