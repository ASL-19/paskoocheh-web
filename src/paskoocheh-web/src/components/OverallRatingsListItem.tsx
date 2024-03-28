import { gridContainer } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import StarRatingDisplay from "src/components/StarRatingDisplay";
import { GqlCategoryAnalysis } from "src/generated/graphQl";
import useFormattedNumber from "src/hooks/useFormattedNumber";
import { paragraphP2Regular } from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";
import { mediaFeatures } from "src/values/layoutValues";

const container = css(
  paragraphP2Regular,
  gridContainer({ columns: 12, gap: "0.5rem" }),
  {
    alignItems: "center",
    paddingBottom: "0.5rem",
  },
);

const text = ({ isStarRating }: { isStarRating: boolean }) =>
  css({
    gridColumn: isStarRating ? "1 / span 6" : "1 / span 3",
  });

const ratingContainer = css(
  {
    backgroundColor: colors.neutral200,
    borderRadius: "0.5rem",
    gridColumn: "4 / span 7",
    height: "0.625rem",
    justifySelf: "center",
    maxWidth: "12.8rem",
    position: "relative",
    width: "90%",
  },
  {
    [`@media (min-width: 30rem) and ${mediaFeatures.viewportWidthLteDesktopNarrow}`]:
      {
        justifySelf: "end",
      },
  },
);

const ratingBar = ({ ratingPercentage }: { ratingPercentage: number }) =>
  css({
    backgroundColor: colors.primary500,
    borderRadius: "0.5rem",
    height: "100%",
    left: "0",

    position: "absolute",
    top: "0",

    width: `${ratingPercentage}%`,
  });

const ratingRatio = css({
  display: "flex",
  gridColumn: "span 1",
  justifySelf: "center",

  paddingInlineStart: "0.5rem",
});

const starRatingDisplay = css(
  {
    fontSize: "1.25rem",
    gridColumn: "7 / span 4",
    justifySelf: "end",
    paddingInlineEnd: "0.5rem",
  },
  breakpointStyles({
    singleColumn: {
      gte: {
        gridColumn: "7 / span 5",
      },
    },
  }),
);

const OverallRatingsListItem: StylableFC<{
  isStarRating: boolean;
  ratingInfo: GqlCategoryAnalysis;
}> = memo(({ className, isStarRating, ratingInfo }) => {
  const maxRating = isStarRating ? 5 : 10;
  const ratingPercentage = (ratingInfo.rating / maxRating) * 100;

  const formattedMaxRating = useFormattedNumber({
    decimalPoints: 1,
    number: maxRating,
  });

  const formattedRating = useFormattedNumber({
    decimalPoints: 1,
    number: ratingInfo.rating,
  });

  return (
    <li className={className} css={container}>
      <h4 css={text({ isStarRating })}>{ratingInfo.ratingCategory?.name}:</h4>

      {isStarRating ? (
        <StarRatingDisplay css={starRatingDisplay} rating={ratingInfo.rating} />
      ) : (
        <div css={ratingContainer}>
          <div css={ratingBar({ ratingPercentage })} />
        </div>
      )}

      <div css={ratingRatio}>
        <div> {formattedRating}</div> /<div>{formattedMaxRating}</div>
      </div>
    </li>
  );
});

OverallRatingsListItem.displayName = "OverallRatingsListItem";

export default OverallRatingsListItem;
