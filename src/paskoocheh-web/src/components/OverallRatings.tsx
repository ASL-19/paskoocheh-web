import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useMemo } from "react";
import { match } from "ts-pattern";

import ButtonLink from "src/components/ButtonLink";
import OverallRatingsListItem from "src/components/OverallRatingsListItem";
import StarRatingDisplay from "src/components/StarRatingDisplay";
import { GqlTeamAnalysis } from "src/generated/graphQl";
import useFormattedNumber from "src/hooks/useFormattedNumber";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import {
  headingH2SemiBold,
  paragraphP1SemiBold,
  paragraphP2SemiBold,
} from "src/styles/typeStyles";
import { ValidVersion } from "src/types/appTypes";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

export type OverallRatingsStrings = {
  buttonText: string;
  categoryRating: string;
  overallRating: string;
};

const container = css({
  backgroundColor: colors.neutral50,
  borderRadius: "0.5rem",
  display: "flex",
  flex: "1.15",
  flexDirection: "column",
  padding: "1.25rem",
  rowGap: "1.25rem",
});

const overallRating = css({
  alignItems: "center",
  display: "flex",
  flexDirection: "column",
  rowGap: "1.25rem",
});

const list = css({
  gap: "1rem",
  paddingTop: "1.25rem",
});

const title = css(
  paragraphP2SemiBold,
  breakpointStyles({
    tablet: {
      lt: paragraphP1SemiBold,
    },
  }),
);

const ratingContainer = css({
  backgroundColor: colors.neutral500,
  borderRadius: "1rem",
  height: "1.25rem",
  position: "relative",
  width: "100%",
});

const ratingBar = ({ ratingPercentage }: { ratingPercentage: number }) =>
  css({
    backgroundColor: colors.primary500,
    borderRadius: "1rem",
    height: "100%",
    left: " 0",

    position: "absolute",
    top: "0",

    width: `${ratingPercentage}%`,
  });

const starRatingDisplay = css({
  fontSize: "2rem",
});

const button = css({
  width: "100%",
});

const categoryRatingContainer = css({});

const OverallRatings: StylableFC<
  | {
      isStarRating: boolean;
      teamAnalysis: GqlTeamAnalysis;
      version?: never;
    }
  | {
      isStarRating: boolean;
      teamAnalysis?: never;
      version: ValidVersion;
    }
> = memo(({ isStarRating, teamAnalysis, version, ...remainingProps }) => {
  const strings = useAppStrings();
  const { localeCode } = useAppLocaleInfo();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const ratingInfo = useMemo(
    () =>
      match(isStarRating)
        .with(true, () => {
          return {
            rating: version?.averageRating?.starRating ?? 0,
            ratingPercentage: 0,
          };
        })
        .otherwise(() => {
          const teamAnalysisCategoryLength = teamAnalysis?.categoryAnalysis
            ? teamAnalysis?.categoryAnalysis.length
            : 1;

          const averageRating =
            teamAnalysis?.categoryAnalysis?.reduce(
              (acc, category) => acc + (category?.rating ?? 0),
              0,
            ) ?? 0;

          const rating = averageRating / teamAnalysisCategoryLength;

          return {
            rating,
            ratingPercentage: (rating / 10) * 100,
          };
        }),

    [
      isStarRating,
      teamAnalysis?.categoryAnalysis,
      version?.averageRating?.starRating,
    ],
  );

  const formattedRating = useFormattedNumber({
    decimalPoints: 2,
    number: ratingInfo.rating,
  });

  return (
    <div css={container} {...remainingProps}>
      <h3 css={title}>{strings.OverallRatings.overallRating}</h3>
      <div css={overallRating}>
        <p css={headingH2SemiBold}>{formattedRating}</p>
        {isStarRating ? (
          <StarRatingDisplay
            css={starRatingDisplay}
            rating={ratingInfo.rating}
          />
        ) : (
          <div css={ratingContainer}>
            <div
              css={ratingBar({ ratingPercentage: ratingInfo.ratingPercentage })}
            />
          </div>
        )}
      </div>
      {teamAnalysis?.categoryAnalysis && (
        <div css={categoryRatingContainer}>
          <h3 css={title}>{strings.OverallRatings.categoryRating}</h3>
          <ul css={list}>
            {!isStarRating &&
              teamAnalysis?.categoryAnalysis.map(
                (rating) =>
                  rating && (
                    <OverallRatingsListItem
                      key={rating?.id}
                      ratingInfo={rating}
                      isStarRating={isStarRating}
                    />
                  ),
              )}
          </ul>
        </div>
      )}
      {isStarRating && (
        <ButtonLink
          text={strings.OverallRatings.buttonText}
          variant="secondary"
          href={routeUrls.writeAReview({
            appId: version?.tool?.slug ?? "",
            localeCode,
            platform: queryOrDefaultPlatformSlug,
          })}
          css={button}
        />
      )}
    </div>
  );
});

OverallRatings.displayName = "OverallRatings";

export default OverallRatings;
