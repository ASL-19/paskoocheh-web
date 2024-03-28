import { css } from "@emotion/react";

import { breakpointStyles } from "src/utils/media/media";

export const appInstallBadgeHeight = "3rem";

export const appInstallBadge = css(
  {
    height: appInstallBadgeHeight,
    /* Display badges with matched heights in desktop row layout */
    width: "auto",
  },
  breakpointStyles({
    tablet: {
      lt: {
        height: "auto",
        width: "10rem",
      },
    },
  }),
);
