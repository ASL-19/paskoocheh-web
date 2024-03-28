import { css } from "@emotion/react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import ButtonLink from "src/components/ButtonLink";
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
import { formPageContentWidths } from "src/values/layoutValues";

// =============
// === Types ===
// =============

export type ActivateAccountPageProps = PaskoochehPageRequiredProps & {
  didActivate: boolean;
};

export type ActivateAccountPageStrings = {
  /**
   * There are two versions of the messages.
   */
  generic: {
    failed: {
      bodyText: string;
      titleText: string;
    };
    success: {
      bodyText: string;
      titleText: string;
    };
  };
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

const ActivateAccountPage: PaskoochehNextPage<ActivateAccountPageProps> = ({
  didActivate,
}) => {
  const { localeCode } = useAppLocaleInfo();
  const {
    ActivateAccountPage: activateAccountPageStrings,
    shared: sharedStrings,
  } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const bodyDescriptionLocalized = didActivate
    ? activateAccountPageStrings.generic.success.bodyText
    : activateAccountPageStrings.generic.failed.bodyText;

  const titleTextLocalized = didActivate
    ? activateAccountPageStrings.generic.success.titleText
    : activateAccountPageStrings.generic.failed.titleText;

  return (
    <PageContainer>
      <PageMeta
        // We don’t need to provide a canonical path for this page since it
        // shouldn’t ever be shared
        canonicalPath={null}
        description={null}
        image={null}
        isAvailableInAlternateLocales={false}
        title={titleTextLocalized}
      />

      <PageSegment
        as="main"
        centeredContainerCss={pageSegmentCenteredContainerCss}
      >
        <h1 css={formHeading}>{titleTextLocalized}</h1>

        <p>{bodyDescriptionLocalized}</p>

        {didActivate && (
          <>
            <ButtonLink
              href={routeUrls.signIn({
                localeCode,
                platform: queryOrDefaultPlatformSlug,
              })}
              text={sharedStrings.button.signIn}
              variant="primary"
            />
          </>
        )}
      </PageSegment>

      <A11yShortcutPreset preset="skipToNavigation" />
    </PageContainer>
  );
};

export default ActivateAccountPage;
