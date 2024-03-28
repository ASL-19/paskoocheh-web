import { css } from "@emotion/react";

import zIndexes from "src/values/zIndexes";

export const overflowIndicatorContainer = css(
  {
    maxWidth: "100%",
    overflow: "hidden",
    position: "relative",
  },
  {
    "::before, ::after": {
      backgroundAttachment: "scroll, scroll",
      backgroundRepeat: "no-repeat",
      backgroundSize: "1em 100%",
      content: "' '",
      height: "100%",
      opacity: 0,
      pointerEvents: "none",
      position: "absolute",
      top: 0,
      transition: "opacity 0.3s",
      width: "50px",
      zIndex: zIndexes.OverflowIndicatorWrapper_container_indicator,
    },
  },
  {
    "::before": {
      borderRadius: "0 0.5em 0.5em 0 / 0 50% 50% 0",
      boxShadow: "5px 0 10px rgba(0, 0, 0, 0.25)",
      left: "-50px",
    },
  },
  {
    "::after": {
      borderRadius: "0.5em 0 0 0.5em / 50% 0 0 50%",
      boxShadow: "-5px 0 10px rgba(0, 0, 0, 0.25)",
      right: "-50px",
    },
  },
);

export const overflowIndicatorContainerLeftActive = css({
  "::before": {
    opacity: 1,
  },
});

export const overflowIndicatorContainerRightActive = css({
  "::after": {
    opacity: 1,
  },
});
