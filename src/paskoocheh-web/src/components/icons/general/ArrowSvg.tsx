import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";
import { match } from "ts-pattern";

import { useAppLocaleInfo } from "src/stores/appStore";
import { Direction } from "src/types/layoutTypes";
import { IconDirection } from "src/types/miscTypes";

/**
 * Arrow (↑) icon, facing up by default.
 *
 * Use `transform: rotate(90deg)` to align right;
 * `transform: rotate(180deg)` to align down;
 * `transform: rotate(270deg)` to align left.
 */
const ArrowSvg: StylableFC<{ direction: IconDirection }> = memo(
  ({ direction, ...remainingProps }) => {
    const { direction: localeDirection } = useAppLocaleInfo();

    const rotation = match<[Direction, IconDirection]>([
      localeDirection,
      direction,
    ])
      .with(["ltr", "start"], ["rtl", "end"], () => "0")
      .with(["ltr", "up"], ["rtl", "up"], () => "90")
      .with(["ltr", "end"], ["rtl", "start"], () => "180")
      .with(["ltr", "down"], ["rtl", "down"], () => "270")
      .exhaustive();

    return (
      <svg
        fill="none"
        viewBox="0 0 24 24"
        transform={`rotate(${rotation})`}
        {...remainingProps}
      >
        <path
          stroke="currentcolor"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          d="M19 12H5M12 19l-7-7 7-7"
        />
      </svg>
    );
  },
);

ArrowSvg.displayName = "ArrowSvg";

export default ArrowSvg;
