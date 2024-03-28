import { css } from "@emotion/react";
import Image from "next/image";
import { match, P } from "ts-pattern";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import Blocks from "src/components/Block/Blocks";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import { GqlStaticPage } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo } from "src/stores/appStore";
import { headingH3SemiBold } from "src/styles/typeStyles";
import {
  PaskoochehNextPage,
  PaskoochehPageRequiredProps,
} from "src/types/pageTypes";
import { breakpointStyles, Media } from "src/utils/media/media";
import { mediaFeatures } from "src/values/layoutValues";

export type AboutPageProps = PaskoochehPageRequiredProps & {
  staticPage: GqlStaticPage;
};

// ==============
// === Styles ===
// ==============
const container = css({
  alignItems: "top",
  columnGap: "1.5rem",
  display: "flex",
  flexDirection: "row",
  paddingBlock: "3rem",
});

const textColumn = css({
  display: "flex",
  flex: "1",
  flexDirection: "column",
  rowGap: "1.5rem",
});

const img = css(
  {
    height: "fit-content",
    objectFit: "cover",
    objectPosition: "center",
  },
  breakpointStyles({
    desktopNarrow: {
      gte: {
        aspectRatio: "1/1",
        borderRadius: "50%",
        flex: "1",
        overflow: "hidden",
      },
      lt: {
        aspectRatio: "2.2/1",
        borderRadius: "0.25rem",
        width: "100%",
      },
    },
  }),
);

const AboutPage: PaskoochehNextPage<AboutPageProps> = ({ staticPage }) => {
  const { localeCode } = useAppLocaleInfo();
  const queryPlatform = useQueryOrDefaultPlatformSlug();

  const imageElement = match(staticPage.image)
    .with(P.not(null), (image) => (
      <Image
        alt={image.caption}
        css={img}
        height={image.height}
        priority
        sizes={`${mediaFeatures.viewportWidthGteDesktopNarrow} 50vw, 100vw`}
        src={`${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${image.file}`}
        width={image.width}
      />
    ))
    .otherwise(() => null);

  return (
    <PageContainer>
      <PageMeta
        canonicalPath={routeUrls.about({ localeCode, platform: queryPlatform })}
        description={staticPage.searchDescription}
        image={null}
        isAvailableInAlternateLocales={true}
        title={staticPage.seoTitle || staticPage.title}
      />

      <PageSegment as="main" centeredContainerCss={container}>
        <div css={textColumn}>
          <h1 css={headingH3SemiBold} id="main-heading">
            {staticPage.title}
          </h1>

          <Media lessThan="desktopNarrow">{imageElement}</Media>

          {staticPage.body && <Blocks blocks={staticPage.body} />}
        </div>

        <Media greaterThanOrEqual="desktopNarrow">{imageElement}</Media>

        <A11yShortcutPreset preset="skipToNavigation" />
      </PageSegment>
    </PageContainer>
  );
};

export default AboutPage;
