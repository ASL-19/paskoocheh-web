import { css } from "@emotion/react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import ResetPasswordForm from "src/components/form/ResetPasswordForm";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { formHeading } from "src/styles/formStyles";
import {
  PaskoochehNextPage,
  PaskoochehPageRequiredProps,
} from "src/types/pageTypes";
import { breakpointStyles } from "src/utils/media/media";
import { formPageContentWidths } from "src/values/layoutValues";
// =============
// === Types ===
// =============

export type ResetPasswordPageProps = PaskoochehPageRequiredProps & {};

export type ResetPasswordPageStrings = {
  /**
   * Confirmation message after successful submission.
   */
  confirmation: string;
  /**
   * Page SEO description.
   */
  pageDescription: string;
  /**
   * Label for Password field.
   */
  passwordLabel: string;
  /**
   * Label for Confirm Password field.
   */
  reenterPasswordLabel: string;
  /**
   * Text for ResetPassword Heading
   */
  resetPasswordHeading: string;
  /**
   * Title (used for heading and page title).
   */
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
    maxWidth: formPageContentWidths.narrow,
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

const resetPasswordForm = css({
  width: "100%",
});

// ==============================
// === Next.js page component ===
// ==============================

const ResetPasswordPage: PaskoochehNextPage<ResetPasswordPageProps> = () => {
  const { localeCode } = useAppLocaleInfo();
  const { ResetPasswordPage: strings } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  return (
    <PageContainer>
      <PageMeta
        canonicalPath={routeUrls.resetPassword({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
          token: "token",
        })}
        description={strings.pageDescription}
        image={null}
        isAvailableInAlternateLocales={true}
        title={strings.title}
      />
      <PageSegment
        as="main"
        centeredContainerCss={pageSegmentCenteredContainerCss}
      >
        <h1 css={formHeading} id="main-heading">
          {strings.resetPasswordHeading}
        </h1>

        <ResetPasswordForm css={resetPasswordForm} />

        <A11yShortcutPreset preset="skipToNavigation" />
      </PageSegment>
    </PageContainer>
  );
};

export default ResetPasswordPage;
