import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import HtmlContent from "src/components/HtmlContent";
import { captionRegular, paragraphP2Regular } from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

// ==============
// === Styles ===
// ==============

const container = css(
  {
    backgroundColor: colors.primary50,
    borderRadius: "0.5rem",
    display: "flex",
    flexDirection: "column",
    gap: "1.5rem",
    padding: "1.5rem",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        gap: "1rem",
      },
    },
  }),
);

const summaryContent = css(
  paragraphP2Regular,
  {
    display: "flex",
    flexDirection: "column",
    gap: "0.5rem",
    padding: "0 2.5rem",
  },
  breakpointStyles({
    singleColumn: { lt: { ...captionRegular, padding: "0 1rem" } },
  }),
);

const BlogPostSummarySection: StylableFC<{
  summary: string;
}> = memo(({ summary, ...remainingProps }) => (
  <div css={container} {...remainingProps}>
    <HtmlContent dangerousHtml={summary} css={summaryContent} />
  </div>
));

BlogPostSummarySection.displayName = "BlogPostSummarySection";

export default BlogPostSummarySection;
