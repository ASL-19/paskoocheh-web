import { css } from "@emotion/react";

import { breakpointStyles } from "src/utils/media/media";

export const fullWidthWrapper = css({
  display: "block",
  flex: "0 0 auto",
  padding: "0",
  position: "relative",
  width: "100%",
});

export const gridContainerGap = "1.25rem";

export const threeColumnGridContainer = css({
  display: "grid",
  gap: "1.25rem",
  gridTemplateColumns: "repeat(auto-fill, minmax(19rem, 1fr))",
  overflow: "hidden",
  position: "relative",
  rowGap: "2.5rem",
});

/**
 * Grid item that’s inset by one column when viewportWidthGteDesktopNarrow.
 */
export const insetGridItem = ({ inset }: { inset: number }) =>
  css(
    {
      gridColumn: `${inset} / -${inset}`,
    },
    breakpointStyles({
      desktopNarrow: {
        lt: { gridColumn: "1 / -1" },
      },
    }),
  );
