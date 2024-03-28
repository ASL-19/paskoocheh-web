import { css } from "@emotion/react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import AppList from "src/components/App/AppList";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { headingH3SemiBold, paragraphP1Regular } from "src/styles/typeStyles";
import { ValidVersionPreview } from "src/types/appTypes";
import {
  PaskoochehNextPage,
  PaskoochehPageRequiredProps,
} from "src/types/pageTypes";

// =============
// === Types ===
// =============
export type SearchResultsPageProps = PaskoochehPageRequiredProps & {
  query: string;
  searchResults: Array<ValidVersionPreview>;
};

export type SearchResultsPageStrings = {
  pageDescription: string;
  results: string;
  title: string;
};

// ==============
// === Styles ===
// ==============
const centeredContainer = css({
  display: "flex",
  flexDirection: "column",
  padding: "2rem 1rem 4rem",
  rowGap: "2rem",
});

const resultTitle = css(headingH3SemiBold, {
  marginBottom: "0.5rem",
});

// ==============================
// === Next.js page component ===
// ==============================
const SearchResultsPage: PaskoochehNextPage<SearchResultsPageProps> = ({
  query,
  searchResults,
}) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const title = strings.SearchResultsPage.title.replace(
    "{searchQuery}",
    `${query}`,
  );

  const result = strings.SearchResultsPage.results.replace(
    "{count}",
    `${searchResults.length}`,
  );

  return (
    <PageContainer>
      <PageMeta
        canonicalPath={routeUrls.searchResults({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        })}
        description={strings.SearchResultsPage.pageDescription || null}
        image={null}
        isAvailableInAlternateLocales={true}
        title={title}
      />
      <PageSegment centeredContainerCss={centeredContainer}>
        <div>
          <h1 css={resultTitle} id="main-heading">
            {title}
          </h1>
          <p css={paragraphP1Regular}>{result}</p>
        </div>
        <AppList versionPreviews={searchResults} itemHeadingLevel={6} />
      </PageSegment>
      <A11yShortcutPreset preset="skipToNavigation" />
    </PageContainer>
  );
};

export default SearchResultsPage;
