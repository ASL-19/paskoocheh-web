/* eslint-disable @mizdra/layout-shift/require-size-attributes */
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Image from "next/image";
import { memo, useMemo } from "react";

import AppOverviewSection from "src/components/App/AppTopHeaderAndScreenshots/AppOverviewSection";
import AppShareAndSupportLinks from "src/components/App/AppTopHeaderAndScreenshots/AppShareAndSupportLinks";
import PageSegment from "src/components/Page/PageSegment";
import { isValidToolImage, ValidVersion } from "src/types/appTypes";

const logoHeightAndWidth = "13rem";

const container = css({
  columnGap: "2rem",
  display: "flex",
  flexWrap: "wrap",
  padding: "2rem 1rem",
  rowGap: "2rem",
});

const image = css({
  borderRadius: "0.5rem",
  height: logoHeightAndWidth,
  objectFit: "contain",
  width: logoHeightAndWidth,
});

const AppTopHeaderSection: StylableFC<{
  currentPlatformVersion: ValidVersion;
  platformPaskoochehAppPath: string | null;
}> = memo(({ currentPlatformVersion, platformPaskoochehAppPath }) => {
  const logoValidToolImage = useMemo(() => {
    const logoToolImage = currentPlatformVersion.tool.images?.filter(
      (image) => image?.imageType === "logo",
    )[0];

    return logoToolImage && isValidToolImage(logoToolImage)
      ? logoToolImage
      : null;
  }, [currentPlatformVersion.tool.images]);

  return (
    <PageSegment centeredContainerCss={container}>
      {logoValidToolImage && (
        <Image
          src={`${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${logoValidToolImage.image}`}
          alt=""
          css={image}
          height={logoValidToolImage.height}
          width={logoValidToolImage.width}
          sizes={logoHeightAndWidth}
          priority
        />
      )}
      <AppOverviewSection
        currentPlatformVersion={currentPlatformVersion}
        platformPaskoochehAppPath={platformPaskoochehAppPath}
      />
      <AppShareAndSupportLinks tool={currentPlatformVersion.tool} />
    </PageSegment>
  );
});

AppTopHeaderSection.displayName = "AppTopHeaderSection";

export default AppTopHeaderSection;
