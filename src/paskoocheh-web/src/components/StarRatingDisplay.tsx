import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import StarSvg from "src/components/icons/general/StarSvg";
import colors from "src/values/colors";

const container = css({
  display: "flex",
  fontSize: "1rem",
});

const star = css({
  height: "1em",
  width: "1em",
});

const fullStar = css(star, {
  color: colors.primary500,
});

const emptyStar = css(star, {
  color: colors.neutral200,
});

const StarRatingDisplay: StylableFC<{
  rating: number;
}> = memo(({ rating, ...remainingProps }) => {
  const fullStars = Math.floor(rating);
  const emptyStars = 5 - fullStars;

  return (
    <div css={container} {...remainingProps}>
      {Array.from({ length: fullStars }, (_, index) => (
        <StarSvg css={fullStar} key={index} />
      ))}
      {Array.from({ length: emptyStars }, (_, index) => (
        <StarSvg css={emptyStar} key={index} />
      ))}
    </div>
  );
});

StarRatingDisplay.displayName = "StarRatingDisplay";

export default StarRatingDisplay;
