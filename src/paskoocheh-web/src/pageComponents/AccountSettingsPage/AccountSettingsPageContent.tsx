import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";

import AccountSettingsForm from "src/components/AccountSettings/AccountSettingsForm";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import { GqlMinimalUser } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { headingH5SmallSemiBold } from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import { formPageContentWidths } from "src/values/layoutValues";

export type AccountSettingsPageContentProps = {
  user: GqlMinimalUser;
};

export type AccountSettingsPageContentStrings = {
  buttonDelete: string;
  buttonLink: string;
  buttonUpdate: string;
  emailLabel: string;
  oldPassword: string;
  pageDescription: string;
  pageTitle: string;
  passwordLabel: string;
  reenterPasswordLabel: string;
  signIn: string;
  updatedConfirmationText: string;
  usernameLabel: string;
};

// ==============
// === Styles ===
// ==============
const pageSegmentCenteredContainerCss = css(
  {
    display: "flex",
    flexDirection: "column",
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
const AccountSettingsPageContent: StylableFC<
  AccountSettingsPageContentProps
> = ({ user }) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  return (
    <PageContainer>
      <PageMeta
        canonicalPath={routeUrls.account({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        })}
        description={strings.AccountSettingsPageContent.pageDescription}
        image={null}
        isAvailableInAlternateLocales={true}
        title={strings.AccountSettingsPageContent.pageTitle}
      />

      <PageSegment
        as="main"
        centeredContainerCss={pageSegmentCenteredContainerCss}
      >
        <h1 css={headingH5SmallSemiBold} id="main-heading">
          {strings.AccountSettingsPageContent.pageTitle}
        </h1>
        <AccountSettingsForm user={user} />
      </PageSegment>
    </PageContainer>
  );
};

export default AccountSettingsPageContent;
