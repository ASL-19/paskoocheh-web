import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useId } from "react";

import AppOperatingSystemsList from "src/components/App/AppTopHeaderAndScreenshots/AppOperatingSystemsList";
import { GqlPlatform, GqlTool } from "src/generated/graphQl";
import { useAppStrings } from "src/stores/appStore";
import { paragraphP2SemiBold } from "src/styles/typeStyles";
import { ValidVersion } from "src/types/appTypes";

const container = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "1rem",
});

const AppOperatingSystems: StylableFC<{
  currentPlatformVersion: ValidVersion;
  platforms: Array<GqlPlatform> | null;
  tool: GqlTool;
}> = memo(({ currentPlatformVersion, platforms, tool, ...remainingProps }) => {
  const strings = useAppStrings();

  const headingId = useId();

  return (
    <div css={container} {...remainingProps}>
      <h2 css={paragraphP2SemiBold} id={headingId}>
        {strings.AppOverviewSection.operatingSystem}
      </h2>

      <AppOperatingSystemsList
        aria-labelledby={headingId}
        tool={tool}
        platforms={platforms}
        currentPlatformVersion={currentPlatformVersion}
      />
    </div>
  );
});

AppOperatingSystems.displayName = "AppOperatingSystems";

export default AppOperatingSystems;
