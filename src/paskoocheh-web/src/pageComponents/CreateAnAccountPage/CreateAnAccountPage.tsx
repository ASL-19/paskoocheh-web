import { css } from "@emotion/react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import ButtonLink from "src/components/ButtonLink";
import CreateAnAccountReferralMessage from "src/components/CreateAnAccountPage/CreateAnAccountReferralMessage";
import CreateAnAccountForm from "src/components/form/CreateAnAccountForm";
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

export type CreateAnAccountPageProps = PaskoochehPageRequiredProps & {
  referralSlug: string | null;
};

export type CreateAnAccountPageStrings = {
  confirmation: string;
  emailLabel: string;
  pageDescription: string;
  passwordLabel: string;
  reenterPasswordLabel: string;
  signInLink: string;
  signInText: string;
  submitButton: string;
  title: string;
  usernameLabel: string;
  /**
   * Text for You’re already signed in message
   */
  youAlreadySignedIn: string;
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

const signedInContainer = css({
  alignItems: "center",
  display: "flex",
  flexDirection: "column",
  gap: "1rem",
  width: "100%",
});

// ==============================
// === Next.js page component ===
// ==============================

const CreateAnAccountPage: PaskoochehNextPage<CreateAnAccountPageProps> = ({
  referralSlug,
}) => {
  const { localeCode } = useAppLocaleInfo();
  const { CreateAnAccountPage: strings, shared: sharedStrings } =
    useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const username = useAppUsername();

  return (
    <PageContainer>
      <PageMeta
        canonicalPath={routeUrls.createAnAccount({
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
        {username ? (
          <div css={signedInContainer}>
            <div>{strings.youAlreadySignedIn}</div>
            <ButtonLink
              variant="primary"
              text={sharedStrings.button.goToHomePage}
              href={routeUrls.home({
                localeCode,
                platform: queryOrDefaultPlatformSlug,
              })}
            />
          </div>
        ) : (
          <>
            {referralSlug && <CreateAnAccountReferralMessage />}

            <h1 css={formHeading} id="main-heading">
              {strings.title}
            </h1>
            <CreateAnAccountForm referralSlug={referralSlug} />
          </>
        )}

        <A11yShortcutPreset preset="skipToNavigation" />
      </PageSegment>
    </PageContainer>
  );
};

export default CreateAnAccountPage;
