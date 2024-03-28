import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import AppList from "src/components/App/AppList";
import PageSegment from "src/components/Page/PageSegment";
import { useAppStrings } from "src/stores/appStore";
import { headingH3SemiBold } from "src/styles/typeStyles";
import { ValidVersionPreview } from "src/types/appTypes";
import { breakpointStyles } from "src/utils/media/media";

export type HomePagePopularAppsSegmentStrings = {
  /**
   * Text that appears before name of active category in popular apps heading.
   *
   * In English, this is the "Popular" segment of:
   *
   * "[Popular] Entertainment Apps"
   */
  headingPrefix: string;
  /**
   * Text that appears after the name of active category in popular apps heading.
   *
   * In English, this is the "Apps" segment of:
   *
   * "Popular Entertainment [Apps]"
   */
  headingSuffix: string;
};

// ==============
// === Styles ===
// ==============
const pageSegment = css(
  {
    display: "flex",
    paddingBlock: "3.5rem",
  },
  breakpointStyles({
    desktopNarrow: {
      lt: {
        flexDirection: "column",
        rowGap: "2rem",
      },
    },
  }),
);

const container = css({
  display: "flex",
  flexDirection: "column",
  padding: "0 0 1.25rem",
  rowGap: "2rem",
  width: "100%",
});

const heading = css(headingH3SemiBold);

// ==============================
// === Next.js page component ===
// ==============================
const HomePagePopularAppsSegment: StylableFC<{
  activeCategoryName: string | null;
  headingId: string;
  versionPreviews: Array<ValidVersionPreview>;
}> = memo(
  ({ activeCategoryName, headingId, versionPreviews, ...remainingProps }) => {
    const {
      HomePagePopularAppsSegment: strings,
      NoResultsIllustrationAndMessage: noResultsStrings,
    } = useAppStrings();

    const headingText = (
      (strings.headingPrefix ? `${strings.headingPrefix} ` : "") +
      (activeCategoryName ? `${activeCategoryName} ` : "") +
      strings.headingSuffix
    ).trim();

    return (
      <PageSegment centeredContainerCss={pageSegment} {...remainingProps}>
        <div css={container} data-testid="popularApps">
          <h2 css={heading} id={headingId}>
            {headingText}
          </h2>

          {versionPreviews.length > 0 && (
            <AppList
              versionPreviews={versionPreviews}
              aria-labelledby={headingId}
              itemHeadingLevel={3}
              hasItemLogos={true}
            />
          )}

          {versionPreviews.length === 0 && (
            <div>{noResultsStrings.message}</div>
          )}
        </div>
      </PageSegment>
    );
  },
);

HomePagePopularAppsSegment.displayName = "HomePagePopularAppsSegment";

export default HomePagePopularAppsSegment;
