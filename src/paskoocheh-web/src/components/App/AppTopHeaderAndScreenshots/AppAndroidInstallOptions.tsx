import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { lazy, memo } from "react";
import { match, P } from "ts-pattern";

import AppAndroidInstallButton from "src/components/App/AppTopHeaderAndScreenshots/AppAndroidInstallButton";
import AppDownloadBadge from "src/components/AppDownloadBadge";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { appInstallBadge } from "src/styles/appStyles";
import { ValidVersion } from "src/types/appTypes";
import { breakpointStyles } from "src/utils/media/media";
import { paskoochehAppSlug } from "src/values/apiValues";
import colors from "src/values/colors";

/* eslint-disable react-memo/require-memo */
const GooglePlayBadgeEnSvg = lazy(
  () => import("src/components/icons/GooglePlayBadgeEnSvg"),
);

const GooglePlayBadgeFaSvg = lazy(
  () => import("src/components/icons/GooglePlayBadgeFaSvg"),
);
/* eslint-enable react-memo/require-memo */

const container = css(
  {
    display: "flex",
    gap: "2rem",
  },
  breakpointStyles({
    tablet: {
      lt: {
        flexDirection: "column",
      },
    },
  }),
);

const line = css(
  {
    backgroundColor: colors.secondary50,
    height: "2.5rem",
    width: "2px",
  },
  breakpointStyles({
    tablet: {
      lt: {
        display: "none",
      },
    },
  }),
);

const AppAndroidInstallOptions: StylableFC<{
  platformPaskoochehAppPath: string | null;
  version: ValidVersion;
}> = memo(({ platformPaskoochehAppPath, version, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();

  const isAvailableOnGooglePlay = match(version.downloadUrl)
    .with(P.string.regex(/play\.google\.com/), () => true)
    .otherwise(() => false);

  const GooglePlayDownloadBadge = match(localeCode)
    .with("en", () => GooglePlayBadgeEnSvg)
    // eslint-disable-next-line react-memo/require-memo
    .otherwise(() => GooglePlayBadgeFaSvg);

  return (
    <div css={container} {...remainingProps}>
      {version.tool.slug !== paskoochehAppSlug && platformPaskoochehAppPath && (
        <AppAndroidInstallButton
          css={appInstallBadge}
          platformPaskoochehAppPath={platformPaskoochehAppPath}
        />
      )}

      {isAvailableOnGooglePlay && version.downloadUrl && (
        <>
          <div css={line} />

          <AppDownloadBadge
            BadgeSvg={GooglePlayDownloadBadge}
            href={version.downloadUrl}
            label={strings.shared.googleDownloadButton}
          />
        </>
      )}
    </div>
  );
});

AppAndroidInstallOptions.displayName = "AppAndroidInstallOptions";

export default AppAndroidInstallOptions;
