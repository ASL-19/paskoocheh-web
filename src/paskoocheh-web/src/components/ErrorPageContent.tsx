import { replaceArabicNumeralsWithPersianNumerals } from "@asl-19/js-utils";
import { css } from "@emotion/react";
import { FC, memo, useMemo } from "react";
import { match } from "ts-pattern";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import ButtonLink from "src/components/ButtonLink";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { headingH1SemiBold, paragraphP3Regular } from "src/styles/typeStyles";
import { PaskoochehPageRequiredProps } from "src/types/pageTypes";
import type { StringKey } from "src/types/stringTypes";
import getStringByDotSeparatedKey from "src/utils/getStringByDotSeparatedKey";
import { breakpointStyles } from "src/utils/media/media";

// =============
// === Types ===
// =============

export type ErrorPageContentProps = PaskoochehPageRequiredProps & {
  descriptionStringKey?: StringKey | null;
  statusCode: number;
};

export type ErrorPageContentStrings = {
  backToHomeButton: string;
  /**
   * These are the default versions of the error messages. In some cases
   * they’re overridden with more specific messages.
   */
  generic: {
    /**
     * Page not found error.
     *
     * Displayed if a non-existent URL is loaded.
     */
    404: {
      description: string;
      title: string;
    };
    /**
     * Server error.
     *
     * Used if an existent URL is loaded, but something goes wrong while loading
     * it (e.g. the backend is down)
     */
    500: {
      description: string;
      title: string;
    };
  };
};

const pageSegment = css({
  margin: "4rem 0",
});

const pageSegmentCenteredContainerCss = css({
  alignItems: "center",
  display: "flex",
  flexDirection: "column",
  rowGap: "2rem",
  textAlign: "center",
});

const titleAndDescriptionContainer = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "1rem",
});

const title = css(
  headingH1SemiBold,
  breakpointStyles({
    tablet: {
      gte: { fontSize: "2rem" },
    },
  }),
);

const ErrorPageContent: FC<ErrorPageContentProps> = memo(
  ({ descriptionStringKey, statusCode }) => {
    const { localeCode } = useAppLocaleInfo();
    const strings = useAppStrings();
    const platform = useQueryOrDefaultPlatformSlug();

    const localizedSegments = useMemo(() => {
      const genericMessages = match(statusCode)
        .with(404, () => strings.ErrorPageContent.generic[404])
        .otherwise(() => strings.ErrorPageContent.generic[500]);

      const description =
        typeof descriptionStringKey === "string"
          ? getStringByDotSeparatedKey({
              dotSeparatedKey: descriptionStringKey,
              strings,
            })
          : genericMessages.description;

      const title = genericMessages.title;

      const status = match(localeCode)
        .with("fa", () =>
          replaceArabicNumeralsWithPersianNumerals(statusCode.toString()),
        )
        // If other locales have different numerals they should be added here
        .with("en", () => statusCode.toString())
        .exhaustive();

      return { description, status, title };
    }, [descriptionStringKey, localeCode, statusCode, strings]);

    return (
      <PageContainer>
        <PageMeta
          description={localizedSegments.description}
          image={null}
          title={localizedSegments.title}
          isAvailableInAlternateLocales={false}
          canonicalPath={null}
        />

        <PageSegment
          css={pageSegment}
          centeredContainerCss={pageSegmentCenteredContainerCss}
        >
          <div css={titleAndDescriptionContainer}>
            <h1 css={title} id="main-heading">
              {localizedSegments.status}: {localizedSegments.title}
            </h1>

            {/* May be empty depending on what‘s in the strings files */}
            {localizedSegments.description && (
              <p css={paragraphP3Regular}>{localizedSegments.description}</p>
            )}
          </div>

          <ButtonLink
            href={routeUrls.home({ localeCode, platform })}
            text={strings.ErrorPageContent.backToHomeButton}
            variant="primary"
          />

          <A11yShortcutPreset preset="skipToNavigation" />
        </PageSegment>
      </PageContainer>
    );
  },
);

ErrorPageContent.displayName = "ErrorPageContent";

export default ErrorPageContent;
