import { css } from "@emotion/react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import WriteAReview from "src/components/form/WriteAReview";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import { GqlVersionPreview } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { formHeadingSmall } from "src/styles/formStyles";
import {
  PaskoochehNextPage,
  PaskoochehPageRequiredProps,
} from "src/types/pageTypes";
import { breakpointStyles } from "src/utils/media/media";
import { formPageContentWidths } from "src/values/layoutValues";

// =============
// === Types ===
// =============
export type WriteAReviewPageProps = PaskoochehPageRequiredProps & {
  versionPreview: GqlVersionPreview;
};

export type WriteAReviewPageStrings = {
  description: string;
  title: string;
};

// ==============
// === Styles ===
// ==============
const pageSegmentCenteredContainerCss = css(
  {
    display: "flex",
    flexDirection: "column",
    gap: "3.25rem",
    maxWidth: formPageContentWidths.regular,
    padding: "3.25rem 1rem",
    rowGap: "1.5rem",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        maxWidth: "100%",
        padding: "1.5rem",
      },
    },
  }),
);

// ==============================
// === Next.js page component ===
// ==============================

const WriteAReviewPage: PaskoochehNextPage<WriteAReviewPageProps> = ({
  versionPreview,
}) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  return (
    <PageContainer>
      <PageMeta
        canonicalPath={routeUrls.writeAReview({
          appId: versionPreview.tool?.pk.toString() || "0",
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        })}
        description={strings.WriteAReviewPage.description}
        image={null}
        isAvailableInAlternateLocales={true}
        title={strings.WriteAReviewPage.title}
      />

      <PageSegment
        as="main"
        centeredContainerCss={pageSegmentCenteredContainerCss}
      >
        <h1 css={formHeadingSmall} id="main-heading">
          {strings.WriteAReviewPage.title}
        </h1>

        <WriteAReview versionPreview={versionPreview} />

        <A11yShortcutPreset preset="skipToNavigation" />
      </PageSegment>
    </PageContainer>
  );
};

export default WriteAReviewPage;
