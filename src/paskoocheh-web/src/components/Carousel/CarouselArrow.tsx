import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import ChevronSvg from "src/components/icons/general/ChevronSvg";
import colors from "src/values/colors";

type CarouselArrowDirection = "back" | "forward";

const arrow = css({
  fill: colors.black,

  height: "1rem",
});

const button = ({ isEnabled }: { isEnabled: boolean }) =>
  css({
    visibility: isEnabled ? "visible" : "hidden",
  });

const CarouselArrow: StylableFC<{
  ariaLabel: string;
  direction: CarouselArrowDirection;
  isEnabled: boolean;
  onClick: () => void;
}> = memo(({ ariaLabel, className, direction, isEnabled, onClick }) => {
  return (
    <button
      aria-label={ariaLabel}
      aria-hidden
      className={className}
      disabled={!isEnabled}
      onClick={onClick}
      css={button({ isEnabled })}
    >
      <ChevronSvg
        css={arrow}
        direction={direction === "back" ? "start" : "end"}
      />
    </button>
  );
});

CarouselArrow.displayName = "CarouselArrow";

export default CarouselArrow;
