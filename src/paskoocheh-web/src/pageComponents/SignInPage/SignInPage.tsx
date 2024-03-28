import { css } from "@emotion/react";
import { useRouter } from "next/router";
import { useEffect } from "react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import SignInForm from "src/components/form/SignInForm";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import {
  useAppLocaleInfo,
  useAppStrings,
  useAppUsername,
} from "src/stores/appStore";
import { formHeading } from "src/styles/formStyles";
import {
  PaskoochehNextPage,
  PaskoochehPageRequiredProps,
} from "src/types/pageTypes";
import { formPageContentWidths } from "src/values/layoutValues";

// =============
// === Types ===
// =============

export type SignInPageProps = PaskoochehPageRequiredProps & {
  decodedReturnPath: string | null;
};

export type SignInPageStrings = {
  confirmation: string;
  forgotPassword: string;
  pageDescription: string;
  passwordLabel: string;
  signUpLink: string;
  signUpText: string;
  submitButton: string;
  title: string;
  usernameLabel: string;
};

// ==============
// === Styles ===
// ==============
const pageSegmentCenteredContainerCss = css({
  display: "flex",
  flexDirection: "column",
  gap: "3.25rem",
  maxWidth: formPageContentWidths.regular,
  padding: "3.25rem 1rem",
  rowGap: "1.5rem",
});

// ==============================
// === Next.js page component ===
// ==============================

const SignInPage: PaskoochehNextPage<SignInPageProps> = ({
  decodedReturnPath,
}) => {
  const router = useRouter();

  const { localeCode } = useAppLocaleInfo();
  const { SignInPage: strings } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const user = useAppUsername();

  useEffect(() => {
    if (user) {
      router.push(
        decodedReturnPath ??
          routeUrls.home({
            localeCode,
            platform: queryOrDefaultPlatformSlug,
          }),
      );
    }
  }, [decodedReturnPath, localeCode, queryOrDefaultPlatformSlug, router, user]);

  return (
    <PageContainer>
      <PageMeta
        canonicalPath={routeUrls.signIn({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
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
          {strings.title}
        </h1>

        <SignInForm />

        <A11yShortcutPreset preset="skipToNavigation" />
      </PageSegment>
    </PageContainer>
  );
};

export default SignInPage;
