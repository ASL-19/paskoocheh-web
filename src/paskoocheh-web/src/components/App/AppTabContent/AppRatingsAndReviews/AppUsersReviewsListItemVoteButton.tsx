import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import ThumbsUpSvg from "src/components/icons/general/ThumbsUpSvg";
import useFormattedNumber from "src/hooks/useFormattedNumber";
import colors from "src/values/colors";

const thumbIconInactive = css({
  width: "1.125rem",
});
const thumbIconActive = css(thumbIconInactive, {
  color: colors.blueLogo,
});

const button = css({
  alignItems: "center",
  columnGap: "0.75rem",
  display: "flex",
});

const AppUsersReviewsListItemVoteButton: StylableFC<{
  count: number;
  direction: "up" | "down";
  isActive: boolean;
  onClick: () => void;
}> = memo(({ count, direction, isActive, onClick, ...remainingProps }) => {
  const formattedCount = useFormattedNumber({ number: count });

  return (
    <button css={button} onClick={onClick} {...remainingProps}>
      <span>{formattedCount}</span>
      <ThumbsUpSvg
        css={isActive ? thumbIconActive : thumbIconInactive}
        direction={direction}
      />
    </button>
  );
});

AppUsersReviewsListItemVoteButton.displayName =
  "AppUsersReviewsListItemVoteButton";

export default AppUsersReviewsListItemVoteButton;
