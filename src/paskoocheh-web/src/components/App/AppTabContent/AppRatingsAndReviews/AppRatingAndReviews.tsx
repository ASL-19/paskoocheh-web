import { hiddenWhenNoJs } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useCallback, useEffect, useState } from "react";

import AppUsersReviewsContent from "src/components/App/AppTabContent/AppRatingsAndReviews/AppUsersReviewsContent";
import { getAppUsersReviewsListItemElementId } from "src/components/App/AppTabContent/AppRatingsAndReviews/AppUsersReviewsListItem";
import OverallRatings from "src/components/OverallRatings";
import { GqlVersionReview } from "src/generated/graphQl";
import { IndexPageLoadingState } from "src/hooks/useIndexPageLoadingAndQueryLogic";
import { useAppUsername } from "src/stores/appStore";
import { ValidVersion } from "src/types/appTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import focusElement from "src/utils/focus/focusElement";
import { breakpointStyles } from "src/utils/media/media";
import { versionReviewsPerPage } from "src/values/indexPageValues";

const container = css(
  {
    columnGap: "1.25rem",
    display: "flex",
    rowGap: "1.25rem",
  },
  breakpointStyles({
    desktopNarrow: {
      lt: {
        flexDirection: "column",
      },
    },
  }),
);

const AppRatingAndReviews: StylableFC<{
  version: ValidVersion;
}> = memo(({ version, ...remainingProps }) => {
  const username = useAppUsername();

  const [userReviews, setUserReviews] = useState<Array<GqlVersionReview>>([]);
  const [currentOffset, setCurrentOffset] = useState(versionReviewsPerPage);
  const [focusElementId, setFocusElementId] = useState<string | null>(null);

  const [indexPageLoadingState, setIndexPageLoadingState] =
    useState<IndexPageLoadingState>({ type: "loadingNew" });

  useEffect(() => {
    const abortController = new AbortController();

    const getVersionReviews = async () => {
      setIndexPageLoadingState({ type: "loadingNew" });
      if (username !== undefined) {
        try {
          const graphQlSdk = await getGraphQlSdk();

          const currentPlatformVersionReviewResponse =
            await graphQlSdk.getVersionReviews({
              count: versionReviewsPerPage,
              offset: 0,
              platformSlug: version.platform.slugName,
              toolSlug: version.tool.slug,
              username: username ?? "",
            });

          const currentPlatformVersionReview = (
            currentPlatformVersionReviewResponse.version?.reviews?.edges ?? []
          ).reduce(
            (acc, edges) => (edges.node ? [edges.node, ...acc] : acc),
            [],
          );

          setIndexPageLoadingState({
            type: currentPlatformVersionReviewResponse.version?.reviews
              ?.pageInfo.hasNextPage
              ? "hasMore"
              : "hasNoMore",
          });

          setUserReviews(currentPlatformVersionReview);
        } catch (error) {
          setIndexPageLoadingState({ type: "error" });
        }
      }
    };

    getVersionReviews();

    return () => {
      abortController.abort();
    };
  }, [username, version.platform.slugName, version.tool.slug]);

  const onLoadMoreReviewsClick = useCallback(async () => {
    setIndexPageLoadingState({ type: "loadingMore" });
    try {
      const graphQlSdk = await getGraphQlSdk();

      const currentPlatformVersionReviewResponse =
        await graphQlSdk.getVersionReviews({
          count: versionReviewsPerPage,
          offset: currentOffset,
          platformSlug: version.platform.slugName,
          toolSlug: version.tool.slug,
          username: username ?? "",
        });

      const moreCurrentPlatformVersionReview = (
        currentPlatformVersionReviewResponse.version?.reviews?.edges ?? []
      ).reduce((acc, edges) => (edges.node ? [edges.node, ...acc] : acc), []);

      setIndexPageLoadingState({
        type: currentPlatformVersionReviewResponse.version?.reviews?.pageInfo
          .hasNextPage
          ? "hasMore"
          : "hasNoMore",
      });

      setCurrentOffset(() => currentOffset + versionReviewsPerPage);

      if (moreCurrentPlatformVersionReview.length > 0) {
        setUserReviews((previousReviews) => [
          ...previousReviews,
          ...moreCurrentPlatformVersionReview.filter(
            (newReview) =>
              !previousReviews.some(
                (previousReview) => newReview.id === previousReview.id,
              ),
          ),
        ]);
      }
      if (moreCurrentPlatformVersionReview[0]) {
        const focusElementId = getAppUsersReviewsListItemElementId(
          moreCurrentPlatformVersionReview[0],
        );

        setFocusElementId(focusElementId);
      }
    } catch (error) {
      setIndexPageLoadingState({ type: "error" });
    }
  }, [currentOffset, username, version.platform.slugName, version.tool.slug]);

  useEffect(() => {
    if (focusElementId) {
      focusElement(document.getElementById(focusElementId), {
        preventScroll: true,
      });
    }
  }, [focusElementId]);

  return (
    <div css={container} {...remainingProps}>
      <OverallRatings version={version} isStarRating={true} />

      <AppUsersReviewsContent
        css={hiddenWhenNoJs}
        userReviews={userReviews}
        indexPageLoadingState={indexPageLoadingState}
        onLoadMoreReviewsClick={onLoadMoreReviewsClick}
        version={version}
      />
    </div>
  );
});

AppRatingAndReviews.displayName = "AppRatingAndReviews";

export default AppRatingAndReviews;
