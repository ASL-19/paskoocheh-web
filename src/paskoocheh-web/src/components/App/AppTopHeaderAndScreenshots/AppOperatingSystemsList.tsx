import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import AppOperatingSystemsListItem from "src/components/App/AppTopHeaderAndScreenshots/AppOperatingSystemsListItem";
import { GqlPlatform, GqlTool } from "src/generated/graphQl";
import { ValidVersion } from "src/types/appTypes";

const list = css({
  columnGap: "2rem",
  display: "flex",
});

const AppOperatingSystemsList: StylableFC<{
  currentPlatformVersion: ValidVersion;
  platforms: Array<GqlPlatform> | null;
  tool: GqlTool;
}> = memo(({ currentPlatformVersion, platforms, tool, ...remainingProps }) => (
  <ul css={list} {...remainingProps}>
    {platforms?.map(
      (platform) =>
        platform && (
          <AppOperatingSystemsListItem
            tool={tool}
            platform={platform}
            key={platform.id}
            currentPlatformVersion={currentPlatformVersion}
          />
        ),
    )}
  </ul>
));

AppOperatingSystemsList.displayName = "AppOperatingSystemsList";

export default AppOperatingSystemsList;
