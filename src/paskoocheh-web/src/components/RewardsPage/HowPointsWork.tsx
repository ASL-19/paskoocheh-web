import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import ButtonLink from "src/components/ButtonLink";
import StaticImage from "src/components/StaticImage";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import howPointsWorkPng from "src/static/images/howPointsWork.png";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import {
  dashboardGridItemSmall,
  dashboardItemContainer,
  dashboardItemDescription,
  dashboardItemHeadingAndDescription,
  dashboardItemTitle,
} from "src/styles/dashboardStyles";

export type HowPointsWorkStrings = {
  /**
   * Text for How points work description
   */
  description: string;
  /**
   * Text for How points work heading
   */
  heading: string;
};

const container = css(dashboardGridItemSmall, dashboardItemContainer, {
  flexDirection: "row",
  justifyContent: "space-between",
});
const content = css(dashboardItemContainer, {
  alignItems: "start",
  padding: 0,
});

const image = css({
  borderRadius: "100%",
  height: "12.5rem",
  minWidth: "12.5rem",
});

const HowPointsWork: StylableFC = memo((props) => {
  const { localeCode } = useAppLocaleInfo();
  const { HowPointsWork: strings, shared: sharedStrings } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  return (
    <div css={container} {...props}>
      <div css={content}>
        <div css={dashboardItemHeadingAndDescription}>
          <h2 css={dashboardItemTitle}>{strings.heading}</h2>
          <p css={dashboardItemDescription}>{strings.description}</p>
        </div>
        <ButtonLink
          href={routeUrls.rewardsHowPointsWork({
            localeCode,
            platform: queryOrDefaultPlatformSlug,
          })}
          text={sharedStrings.button.learnMore}
          variant="secondary"
        />
      </div>
      <StaticImage
        css={image}
        src={howPointsWorkPng.src}
        alt=""
        staticImageData={howPointsWorkPng}
      />
    </div>
  );
});

HowPointsWork.displayName = "HowPointsWork";

export default HowPointsWork;
