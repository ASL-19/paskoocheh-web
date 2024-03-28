import { css } from "@emotion/react";
import { useMemo } from "react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import AppDetailsSection from "src/components/App/AppTabContent/AppDetailsSection";
import AppScreenshots from "src/components/App/AppTopHeaderAndScreenshots/AppScreenshots";
import AppTopHeaderSection from "src/components/App/AppTopHeaderAndScreenshots/AppTopHeaderSection";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo } from "src/stores/appStore";
import { isValidToolImage, ValidVersion } from "src/types/appTypes";
import {
  PaskoochehNextPage,
  PaskoochehPageRequiredProps,
} from "src/types/pageTypes";
import getValidToolPrimaryToolType from "src/utils/getValidToolPrimaryToolType";

// =============
// === Types ===
// =============
export type AppPageProps = PaskoochehPageRequiredProps & {
  currentPlatformVersion: ValidVersion;
  /**
   * Path to current platform’s Paskoocheh app (app with slug "paskoocheh") if
   * it exists.
   *
   * Currently this will only ever be a string for Android, but this leaves the
   * door open to Paskoocheh apps for other platforms in the future.
   */
  platformPaskoochehAppPath: string | null;
};

// ==============
// === Styles ===
// ==============
const pageContainer = css({
  display: "flex",
  flexDirection: "column",
});

// ==============================
// === Next.js page component ===
// ==============================
const AppPage: PaskoochehNextPage<AppPageProps> = ({
  currentPlatformVersion,
  platformPaskoochehAppPath,
}) => {
  const { localeCode } = useAppLocaleInfo();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const infos = (currentPlatformVersion.tool.info?.edges || []).reduce(
    (acc, edge) => (edge?.node ? [...acc, edge.node] : acc),
    [],
  );

  const currentPlatformVersionScreenshotValidToolImages = useMemo(
    () =>
      (currentPlatformVersion.tool.images ?? []).reduce(
        (acc, image) =>
          image && isValidToolImage(image) && image.imageType === "screenshot"
            ? [...acc, image]
            : acc,
        [],
      ),
    [currentPlatformVersion.tool.images],
  );

  return (
    <PageContainer css={pageContainer} as="main">
      <PageMeta
        canonicalPath={routeUrls.app({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
          slug: currentPlatformVersion.tool.slug,
          toolType: getValidToolPrimaryToolType(currentPlatformVersion.tool)
            .slug,
        })}
        description={infos[0]?.seoDescription ?? ""}
        image={null}
        isAvailableInAlternateLocales={true}
        title={currentPlatformVersion.tool.name}
      />

      <AppTopHeaderSection
        currentPlatformVersion={currentPlatformVersion}
        platformPaskoochehAppPath={platformPaskoochehAppPath}
      />

      {currentPlatformVersionScreenshotValidToolImages.length > 0 && (
        <AppScreenshots
          validToolImages={currentPlatformVersionScreenshotValidToolImages}
        />
      )}

      <AppDetailsSection
        currentPlatformVersion={currentPlatformVersion}
        infos={infos}
      />

      <A11yShortcutPreset preset="skipToNavigation" />
    </PageContainer>
  );
};

export default AppPage;
