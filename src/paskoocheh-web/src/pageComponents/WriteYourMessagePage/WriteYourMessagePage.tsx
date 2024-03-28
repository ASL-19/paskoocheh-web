import { css } from "@emotion/react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import WriteYourMessageForm from "src/components/form/WriteYourMessageForm";
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
export type WriteYourMessagePageProps = PaskoochehPageRequiredProps & {
  versionPreview: GqlVersionPreview | null;
};

export type WriteYourMessagePageStrings = {
  pageDescription: string;
  pageTitle: string;
  /**
   * Text for Write your message heading
   */
  writeYourMessageHeading: string;
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

const writeYourMessageForm = css({
  width: "100%",
});

// ==============================
// === Next.js page component ===
// ==============================
const WriteYourMessagePage: PaskoochehNextPage<WriteYourMessagePageProps> = ({
  versionPreview,
}) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const headingId = "main-heading";

  return (
    <PageContainer>
      <PageMeta
        canonicalPath={routeUrls.writeYourMessage({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
          tool: versionPreview?.tool?.pk,
        })}
        description={strings.WriteYourMessagePage.pageDescription}
        image={null}
        isAvailableInAlternateLocales={true}
        title={strings.WriteYourMessagePage.pageTitle}
      />

      <PageSegment
        as="main"
        centeredContainerCss={pageSegmentCenteredContainerCss}
      >
        <h1 css={formHeadingSmall} id={headingId}>
          {strings.WriteYourMessagePage.writeYourMessageHeading}
        </h1>

        <WriteYourMessageForm
          versionPreview={versionPreview}
          aria-labelledby={headingId}
          css={writeYourMessageForm}
        />

        <A11yShortcutPreset preset="skipToNavigation" />
      </PageSegment>
    </PageContainer>
  );
};

export default WriteYourMessagePage;
