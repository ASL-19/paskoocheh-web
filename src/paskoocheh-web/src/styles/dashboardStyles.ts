import { gridContainer } from "@asl-19/emotion-utils";
import { css } from "@emotion/react";

import {
  captionRegular,
  paragraphP1Regular,
  paragraphP2SemiBold,
} from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

export const dashboardContainer = css({
  display: "flex",
  flexDirection: "column",
  gap: "2rem",
});

export const dashboardItemContainer = css({
  alignItems: "center",
  backgroundColor: colors.neutral50,
  borderRadius: "0.5rem",
  display: "flex",
  flexDirection: "column",
  gap: "1.5rem",
  justifyContent: "center",
  padding: "2rem 1.5rem",
});

export const dashboardGridContainer = css(
  gridContainer({ columnGap: "1.5rem", columns: 12 }),
  breakpointStyles({
    singleColumn: {
      lt: {
        columnGap: "0",
      },
    },
  }),
  {
    width: "100%",
  },
);

export const dashboardGridItemLarge = css(
  {
    gridColumn: "1 / span 7",
  },
  breakpointStyles({
    desktopNarrow: {
      lt: {
        gridColumn: "span 12",
      },
    },
  }),
);
export const dashboardGridItemSmall = css(
  {
    gridColumn: "8 / span 5",
  },
  breakpointStyles({
    desktopNarrow: {
      lt: {
        gridColumn: "span 12",
      },
    },
  }),
);
export const dashboardItemTitle = css(paragraphP2SemiBold, {
  textAlign: "start",
  width: "100%",
});
export const dashboardItemDescription = css(
  paragraphP1Regular,
  breakpointStyles({ singleColumn: { lt: captionRegular } }),
);

export const dashboardItemHeadingAndDescription = css(paragraphP2SemiBold, {
  display: "flex",
  flexDirection: "column",
  gap: "0.5rem",
});
