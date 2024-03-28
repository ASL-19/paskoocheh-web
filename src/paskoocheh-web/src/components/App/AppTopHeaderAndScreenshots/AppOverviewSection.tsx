import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useMemo } from "react";

import AppAndroidInstallOptions from "src/components/App/AppTopHeaderAndScreenshots/AppAndroidInstallOptions";
import AppInstallOptions from "src/components/App/AppTopHeaderAndScreenshots/AppInstallOptions";
import AppOperatingSystems from "src/components/App/AppTopHeaderAndScreenshots/AppOperatingSystems";
import AppStatsDetails from "src/components/App/AppTopHeaderAndScreenshots/AppStatsDetails";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import { headingH4SemiBold, paragraphP2Regular } from "src/styles/typeStyles";
import { ValidVersion } from "src/types/appTypes";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

export type AppOverviewSectionStrings = {
  android: string;
  availableOptions: string;
  buttonText: string;
  download: string;
  operatingSystem: string;
  reviews: string;
};

const container = css(
  {
    display: "flex",
    flex: "1",
    flexDirection: "column",
    order: "1",
    rowGap: "2rem",
  },
  breakpointStyles({
    desktopNarrow: {
      lt: {
        flex: "100%",
        order: "3",
      },
    },
  }),
);

const text = css(paragraphP2Regular, {
  color: colors.primary500,
  paddingTop: "0.5rem",
});

const AppOverviewSection: StylableFC<{
  currentPlatformVersion: ValidVersion;
  platformPaskoochehAppPath: string | null;
}> = memo(
  ({
    currentPlatformVersion,
    platformPaskoochehAppPath,
    ...remainingProps
  }) => {
    const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

    const toolPlatforms = useMemo(
      () =>
        (currentPlatformVersion.tool.versions?.edges ?? []).reduce(
          (acc, edge) =>
            edge.node.platform ? [...acc, edge.node.platform] : acc,
          [],
        ),
      [currentPlatformVersion.tool.versions?.edges],
    );

    const companyName =
      currentPlatformVersion.tool.info?.edges[0]?.node.company ?? null;

    return (
      <div css={container} {...remainingProps}>
        <div>
          <h1 css={headingH4SemiBold} id="main-heading">
            {currentPlatformVersion.tool.name}
          </h1>

          <p css={text}>{companyName}</p>
        </div>

        {currentPlatformVersion && (
          <AppStatsDetails version={currentPlatformVersion} />
        )}

        <AppOperatingSystems
          platforms={toolPlatforms}
          tool={currentPlatformVersion.tool}
          currentPlatformVersion={currentPlatformVersion}
        />

        <AppInstallOptions version={currentPlatformVersion} />

        {queryOrDefaultPlatformSlug === "android" && (
          <AppAndroidInstallOptions
            platformPaskoochehAppPath={platformPaskoochehAppPath}
            version={currentPlatformVersion}
          />
        )}
      </div>
    );
  },
);

AppOverviewSection.displayName = "AppOverviewSection";

export default AppOverviewSection;
