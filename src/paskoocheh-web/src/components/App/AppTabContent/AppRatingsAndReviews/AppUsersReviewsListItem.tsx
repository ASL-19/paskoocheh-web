/* eslint-disable react-memo/require-usememo */
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { useRouter } from "next/router";
import { memo, useCallback, useMemo, useState } from "react";

import AppUsersReviewsListItemVoteButton from "src/components/App/AppTabContent/AppRatingsAndReviews/AppUsersReviewsListItemVoteButton";
import StarRatingDisplay from "src/components/StarRatingDisplay";
import {
  GqlDoVoteReview,
  GqlReviewVoteOptions,
  GqlVersionReview,
} from "src/generated/graphQl";
import useDateInfo from "src/hooks/useDateInfo";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import {
  useAppLocaleInfo,
  useAppStrings,
  useAppUsername,
} from "src/stores/appStore";
import {
  captionRegular,
  paragraphP1Regular,
  paragraphP2SemiBold,
} from "src/styles/typeStyles";
import { ValidVersion } from "src/types/appTypes";
import getErrorMessagesFromExpectedError from "src/utils/api/getErrorMessagesFromResponseErrorsByFieldKey";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getValidToolPrimaryToolType from "src/utils/getValidToolPrimaryToolType";
import colors from "src/values/colors";

const item = css({
  borderBottom: `solid 1px ${colors.secondary50}`,
  display: "flex",
  flexDirection: "column",
  padding: "1.25rem 0 1rem",
  rowGap: "1rem",
});

const dateAndRatingContainer = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "0.5rem",
});

const rowContainer = css({
  alignItems: "center",
  columnGap: "1rem",
  display: "flex",
  lineHeight: "1.188rem",
});

const date = css(captionRegular, {
  color: colors.secondary400,
});

const starRatingDisplay = css({
  fontSize: "1.25rem",
});

type VoteState = {
  userVoteType: GqlReviewVoteOptions | null;
  voteCounts: {
    [key in GqlReviewVoteOptions]: number;
  };
};

export const getAppUsersReviewsListItemElementId = (review: GqlVersionReview) =>
  `AppUsersReviewsListItem-${review.id}`;

const AppUsersReviewsListItem: StylableFC<{
  userReview: GqlVersionReview;
  version: ValidVersion;
}> = memo(({ userReview, version, ...remainingProps }) => {
  const strings = useAppStrings();
  const username = useAppUsername();
  const router = useRouter();
  const { localeCode } = useAppLocaleInfo();
  const platform = useQueryOrDefaultPlatformSlug();

  const [errorMessage, setErrorMessage] = useState<string>();

  const initialVoteState: VoteState = useMemo(
    () => ({
      userVoteType: userReview.hasUserVoted.voteType,
      voteCounts: {
        DOWNVOTE: userReview.downvotes,
        NOVOTE: userReview.hasUserVoted.hasVoted ? 0 : 1,
        UPVOTE: userReview.upvotes,
      },
    }),
    [userReview],
  );

  const [voteState, setVoteState] = useState<VoteState>(initialVoteState);

  const encodedPath = encodeURIComponent(
    routeUrls.app({
      localeCode,
      platform,
      slug: version.tool.slug,
      toolType: getValidToolPrimaryToolType(version.tool).slug,
    }),
  );

  const handleVoteClick = useCallback(
    async (reviewVoteOption: GqlReviewVoteOptions) => {
      if (!username) {
        router.push(
          routeUrls.signIn({ localeCode, platform, returnPath: encodedPath }),
        );
        return;
      }

      const isRemovingVote = voteState.userVoteType === reviewVoteOption;

      setVoteState((prevVoteState) => {
        const oppositeReviewVoteOption: GqlReviewVoteOptions =
          reviewVoteOption === "DOWNVOTE" ? "UPVOTE" : "DOWNVOTE";

        if (isRemovingVote) {
          return {
            userVoteType: "NOVOTE",
            voteCounts: {
              ...prevVoteState.voteCounts,
              [reviewVoteOption]:
                prevVoteState.voteCounts[reviewVoteOption] - 1,
            },
          };
        }

        return {
          userVoteType: reviewVoteOption,
          // This uses `as "DOWNVOTE"` and `as "UPVOTE"` for type safety (since
          // voteCounts must include both DOWNVOTE and UPVOTE properties, but
          // there’s no way to express that they will always be different)
          voteCounts: {
            ...prevVoteState.voteCounts,
            [oppositeReviewVoteOption as "DOWNVOTE"]:
              prevVoteState.userVoteType === oppositeReviewVoteOption
                ? prevVoteState.voteCounts[oppositeReviewVoteOption] - 1
                : prevVoteState.voteCounts[oppositeReviewVoteOption],
            [reviewVoteOption as "UPVOTE"]:
              prevVoteState.voteCounts[reviewVoteOption] + 1,
          },
        };
      });

      let voteResponse: GqlDoVoteReview;

      try {
        const graphQlSdk = await getGraphQlSdk({ method: "POST" });

        voteResponse = await graphQlSdk.doVoteReview({
          reviewPk: userReview.pk,
          vote: isRemovingVote ? "NOVOTE" : reviewVoteOption,
        });
      } catch (error) {
        setErrorMessage(strings.shared.form.errorMessages.network);
        return;
      }

      if (
        !voteResponse?.voteReview?.success &&
        voteResponse?.voteReview?.errors
      ) {
        const errorMessages = getErrorMessagesFromExpectedError({
          expectedError: voteResponse?.voteReview?.errors,
        });

        setErrorMessage(errorMessages[0] ?? "");
        return;
      }
    },
    [
      encodedPath,
      localeCode,
      platform,
      router,
      strings.shared.form.errorMessages.network,
      userReview.pk,
      username,
      voteState.userVoteType,
    ],
  );

  const formattedDate = useDateInfo({
    dateString: userReview.timestamp,
  })?.localeFormatted;

  return (
    <li
      css={item}
      id={getAppUsersReviewsListItemElementId(userReview)}
      {...remainingProps}
    >
      <div css={dateAndRatingContainer}>
        <div css={rowContainer}>
          <StarRatingDisplay
            css={starRatingDisplay}
            rating={userReview.rating}
          />
          <p css={paragraphP2SemiBold}>{userReview.subject}</p>
        </div>
        <p css={date}>{formattedDate ?? ""}</p>
      </div>

      <p>{userReview.text}</p>
      <div css={rowContainer}>
        <AppUsersReviewsListItemVoteButton
          count={voteState.voteCounts.UPVOTE}
          onClick={() => handleVoteClick("UPVOTE")}
          isActive={voteState.userVoteType === "UPVOTE"}
          direction="up"
        />
        <AppUsersReviewsListItemVoteButton
          count={voteState.voteCounts.DOWNVOTE}
          onClick={() => handleVoteClick("DOWNVOTE")}
          isActive={voteState.userVoteType === "DOWNVOTE"}
          direction="down"
        />
        <p css={paragraphP1Regular}>{errorMessage}</p>
      </div>
    </li>
  );
});

AppUsersReviewsListItem.displayName = "AppUsersReviewsListItem";

export default AppUsersReviewsListItem;
