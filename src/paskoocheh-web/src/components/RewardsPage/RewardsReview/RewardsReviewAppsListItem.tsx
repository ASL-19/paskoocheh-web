import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import LinkOverlay from "src/components/LinkOverlay";
import StarRatingDisplay from "src/components/StarRatingDisplay";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo } from "src/stores/appStore";
import {
  dashboardItemContainer,
  dashboardItemHeadingAndDescription,
  dashboardItemTitle,
} from "src/styles/dashboardStyles";
import { captionSemiBold } from "src/styles/typeStyles";
import { ValidVersionPreview } from "src/types/appTypes";
import getValidToolPrimaryToolType from "src/utils/getValidToolPrimaryToolType";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

const container = css(dashboardItemContainer, {
  alignItems: "start",
  borderBottom: `1px solid ${colors.secondary50}`,
  flexDirection: "row",
  justifyContent: "start",
  position: "relative",
});
const image = css(
  {
    background: "salmon",
    borderRadius: "100%",
    height: "4rem",
    width: "4rem",
  },
  breakpointStyles({ singleColumn: { lt: { height: "3rem", width: "3rem" } } }),
);
const heading = css(
  dashboardItemTitle,
  { textIndent: "0.5rem" },
  breakpointStyles({ singleColumn: { lt: captionSemiBold } }),
);
const overlay = css({});

const starRatingDisplay = css(
  {
    fontSize: "2rem",
  },
  breakpointStyles({ singleColumn: { lt: { fontSize: "1.5rem" } } }),
);

const RewardsReviewAppListItem: StylableFC<{
  type: "notYetReviewed" | "reviewed";
  versionPreview: ValidVersionPreview;
}> = memo(({ className, type, versionPreview }) => {
  const { localeCode } = useAppLocaleInfo();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const toolType = getValidToolPrimaryToolType(versionPreview.tool);

  const url =
    type === "notYetReviewed"
      ? routeUrls.writeAReview({
          appId: versionPreview?.tool?.id ?? "",
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        })
      : routeUrls.app({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
          slug: versionPreview.tool.slug,
          toolType: toolType.slug,
        });

  const overallRating = versionPreview.averageRating?.starRating ?? 0;

  return (
    <div className={className} css={container}>
      <div css={image}></div>
      <div css={dashboardItemHeadingAndDescription}>
        <h3 css={heading}>{versionPreview.tool?.name}</h3>
        <StarRatingDisplay css={starRatingDisplay} rating={overallRating} />
      </div>
      <LinkOverlay url={url} css={overlay} />
    </div>
  );
});

RewardsReviewAppListItem.displayName = "RewardsReviewAppListItem";

export default RewardsReviewAppListItem;
