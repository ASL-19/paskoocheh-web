/* eslint-disable @emotion/syntax-preference */

import { StylableFC } from "@asl-19/react-dom-utils";
import { css, keyframes } from "@emotion/react";
import { memo } from "react";

import { useAppLocaleInfo } from "src/stores/appStore";
import { Direction } from "src/types/layoutTypes";
import colors from "src/values/colors";

const circlePath = ({ direction }: { direction: Direction }) =>
  css({
    animationDuration: "1000ms",
    animationIterationCount: "infinite",
    animationName: keyframes({
      from: {
        transform: direction === "rtl" ? "rotate(360deg)" : "rotate(0deg)",
      },
      to: {
        transform: direction === "rtl" ? "rotate(0deg)" : "rotate(360deg)",
      },
    }),
    animationTimingFunction: "linear",
    fill: "none",
    stroke: colors.primary500,
    strokeLinecap: "round",
    strokeWidth: 2.8,
    transformOrigin: "center center",
  });

/**
 * This animation is used to show that data is loading.
 */
const LoadingIndicatorSvg: StylableFC = memo((props) => {
  const { direction } = useAppLocaleInfo();

  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" {...props}>
      <circle
        css={circlePath({ direction })}
        cx="50"
        cy="50"
        r="20"
        strokeDasharray="31.41592653589793 31.41592653589793"
      />
    </svg>
  );
});

LoadingIndicatorSvg.displayName = "LoadingIndicatorSvg";

export default LoadingIndicatorSvg;
