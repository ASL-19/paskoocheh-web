import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useId } from "react";

import AppList from "src/components/App/AppList";
import AppListItem from "src/components/App/AppListItem";
import OverflowIndicatorWrapper from "src/components/OverflowIndicatorWrapper";
import PageSegment from "src/components/Page/PageSegment";
import { useAppStrings } from "src/stores/appStore";
import { headingH3SemiBold, headingH5SemiBold } from "src/styles/typeStyles";
import { ValidVersionPreview } from "src/types/appTypes";
import { HeadingLevel } from "src/types/miscTypes";
import { breakpointStyles } from "src/utils/media/media";
import { mediaFeatures } from "src/values/layoutValues";

export type HomePageEditorsChoiceSegmentStrings = {
  heading: string;
};

const heading = css(
  headingH3SemiBold,
  breakpointStyles({
    singleColumn: {
      lt: headingH5SemiBold,
    },
  }),
);
const pageSegmentCentredContent = css({
  display: "flex",
  flexDirection: "column",
  gap: "1.5rem",
});

const overflowIndicatorWrapperMobile = css({
  [`@media (pointer: fine), ${mediaFeatures.viewportWidthGteSingleColumn}`]: {
    display: "none",
  },
});

const appListMobile = css({
  display: "flex",
  gap: "1.25rem",
  overflowX: "scroll",
  paddingBottom: "1rem",
  scrollPadding: "0.5rem",
  scrollSnapType: "x mandatory",
});

const appListDesktop = css(
  breakpointStyles({
    singleColumn: {
      lt: {
        gap: "1rem",
        gridTemplateColumns: `repeat(auto-fill, minmax(10rem, 1fr))`,
      },
    },
  }),
  {
    [`@media (pointer: coarse) and ${mediaFeatures.viewportWidthLtSingleColumn}`]:
      {
        display: "none",
      },
  },
);

const appListDesktopItemLogo = breakpointStyles({
  singleColumn: {
    lt: {
      display: "none",
    },
  },
});

const mobileAppListItem = css({
  scrollSnapAlign: "start",
});

const HomePageEditorsChoiceSegment: StylableFC<{
  versionPreviews: Array<ValidVersionPreview>;
}> = memo(({ versionPreviews, ...remainingProps }) => {
  const strings = useAppStrings();

  const headingId = useId();

  const itemHeadingLevel: HeadingLevel = 3;

  return (
    <PageSegment
      centeredContainerCss={pageSegmentCentredContent}
      {...remainingProps}
    >
      <h2 css={heading} id={headingId}>
        {strings.HomePageEditorsChoiceSegment.heading}
      </h2>

      <OverflowIndicatorWrapper css={overflowIndicatorWrapperMobile}>
        <ul aria-labelledby={headingId} css={appListMobile}>
          {versionPreviews.map((app) => (
            <AppListItem
              versionPreview={app}
              css={mobileAppListItem}
              headingLevel={itemHeadingLevel}
              key={app.id}
              hasPromoImage
              hasLogo={false}
            />
          ))}
        </ul>
      </OverflowIndicatorWrapper>

      <AppList
        versionPreviews={versionPreviews}
        aria-labelledby={headingId}
        css={appListDesktop}
        hasItemPromoImages
        itemHeadingLevel={itemHeadingLevel}
        itemLogoCss={appListDesktopItemLogo}
      />
    </PageSegment>
  );
});

HomePageEditorsChoiceSegment.displayName = "HomePageEditorsChoiceSegment";

export default HomePageEditorsChoiceSegment;
