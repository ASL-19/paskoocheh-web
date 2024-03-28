import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { useRouter } from "next/router";
import { useEffect } from "react";

import ButtonLink from "src/components/ButtonLink";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import {
  useAppDispatch,
  useAppLocaleInfo,
  useAppStrings,
} from "src/stores/appStore";
import { formConfirmationMessage } from "src/styles/formStyles";
import { RouterEventHandler } from "src/types/nextTypes";
import { breakpointStyles } from "src/utils/media/media";
import { formPageContentWidths } from "src/values/layoutValues";

export type AccountSettingsConfirmationPageStrings = {
  pageDescription: string;
  pageTitle: string;
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
const button = css({
  marginTop: "1rem",
});

const successMessageContainer = css({
  alignItems: "center",
  display: "flex",
  flexDirection: "column",
  gap: "1rem",
});

// ==============================
// === Next.js page component ===
// ==============================
const AccountSettingsConfirmationPage: StylableFC = () => {
  const { localeCode } = useAppLocaleInfo();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();
  const strings = useAppStrings();
  const appDispatch = useAppDispatch();

  const router = useRouter();

  useEffect(() => {
    const onRouteChangeComplete: RouterEventHandler = (url, { shallow }) => {
      if (!shallow) {
        appDispatch({ type: "usernameChanged", username: null });
      }
    };

    router.events.on("routeChangeComplete", onRouteChangeComplete);

    return () => {
      router.events.off("routeChangeComplete", onRouteChangeComplete);
    };
  }, [appDispatch, router.events]);
  return (
    <PageContainer>
      <PageMeta
        canonicalPath={routeUrls.account({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        })}
        description={strings.AccountSettingsConfirmationPage.pageDescription}
        image={null}
        isAvailableInAlternateLocales={true}
        title={strings.AccountSettingsConfirmationPage.pageTitle}
      />

      <PageSegment
        as="main"
        centeredContainerCss={pageSegmentCenteredContainerCss}
      >
        <div css={successMessageContainer}>
          <h1 css={formConfirmationMessage} id="main-heading">
            {strings.AccountSettingsPageContent.updatedConfirmationText}
          </h1>
          <ButtonLink
            text={strings.AccountSettingsPageContent.signIn}
            href={routeUrls.signIn({
              localeCode,
              platform: queryOrDefaultPlatformSlug,
            })}
            css={button}
            variant="secondary"
          />
        </div>
      </PageSegment>
    </PageContainer>
  );
};

export default AccountSettingsConfirmationPage;
