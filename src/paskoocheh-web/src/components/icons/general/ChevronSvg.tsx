import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";
import { match } from "ts-pattern";

import { useAppLocaleInfo } from "src/stores/appStore";
import { Direction } from "src/types/layoutTypes";
import { IconDirection } from "src/types/miscTypes";

/**
 * Chevron (﹥) icon.
 *
 * Required `direction` prop determines the bidi-safe facing direction.
 */
const ChevronSvg: StylableFC<{ direction: IconDirection }> = memo(
  ({ direction, ...props }) => {
    const { direction: localeDirection } = useAppLocaleInfo();

    const rotation = match<[Direction, IconDirection]>([
      localeDirection,
      direction,
    ])
      .with(["ltr", "end"], ["rtl", "start"], () => "0")
      .with(["ltr", "down"], ["rtl", "down"], () => "90")
      .with(["ltr", "start"], ["rtl", "end"], () => "180")
      .with(["ltr", "up"], ["rtl", "up"], () => "270")
      .exhaustive();

    return (
      <svg
        stroke="none"
        viewBox="0 0 36 36"
        transform={`rotate(${rotation})`}
        {...props}
      >
        <g transform="translate(9 2)">
          <path d="M2.68 31L0 28.42 13.43 15.5 0 2.58 2.68 0l14.77 14.21a1.8 1.8 0 010 2.58L2.68 31z" />
        </g>
      </svg>
    );
  },
);

ChevronSvg.displayName = "ChevronSvg";

export default ChevronSvg;
