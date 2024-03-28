import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import AppUsersReviewsListItem from "src/components/App/AppTabContent/AppRatingsAndReviews/AppUsersReviewsListItem";
import IndexPageLoadingUi from "src/components/IndexPageLoadingUi";
import { GqlVersionReview } from "src/generated/graphQl";
import { IndexPageLoadingState } from "src/hooks/useIndexPageLoadingAndQueryLogic";
import { useAppStrings } from "src/stores/appStore";
import { paragraphP2SemiBold } from "src/styles/typeStyles";
import { ValidVersion } from "src/types/appTypes";
import colors from "src/values/colors";

export type AppUsersReviewsContentStrings = {
  reviews: string;
};

const container = css({
  backgroundColor: colors.neutral50,
  borderRadius: "0.5rem",
  flex: "2",
  padding: "1.25rem",
});

const AppUsersReviewsContent: StylableFC<{
  indexPageLoadingState: IndexPageLoadingState;
  onLoadMoreReviewsClick: () => Promise<void>;
  userReviews: Array<GqlVersionReview>;
  version: ValidVersion;
}> = memo(
  ({
    indexPageLoadingState,
    onLoadMoreReviewsClick,
    userReviews,
    version,
    ...remainingProps
  }) => {
    const strings = useAppStrings();

    return (
      <div css={container} {...remainingProps}>
        <h2 css={paragraphP2SemiBold}>
          {strings.AppUsersReviewsContent.reviews}
        </h2>

        {!["error", "hasNone", "loadingNew"].includes(
          indexPageLoadingState.type,
        ) && (
          <ul>
            {userReviews.map((review) => (
              <AppUsersReviewsListItem
                userReview={review}
                key={review.id}
                version={version}
              />
            ))}
          </ul>
        )}

        <IndexPageLoadingUi
          onClick={onLoadMoreReviewsClick}
          buttonType="button"
          loadMoreLinkText={strings.shared.button.more}
          loadingState={indexPageLoadingState}
        />
      </div>
    );
  },
);

AppUsersReviewsContent.displayName = "AppUsersReviewsContent";

export default AppUsersReviewsContent;
