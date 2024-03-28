import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageContent from "src/components/PageContent";
import { GqlStaticPage } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo } from "src/stores/appStore";
import {
  PaskoochehNextPage,
  PaskoochehPageRequiredProps,
} from "src/types/pageTypes";

export type TermsOfServicePageProps = PaskoochehPageRequiredProps & {
  staticPage: GqlStaticPage;
};

// ==============================
// === Next.js page component ===
// ==============================
const TermsOfServicePage: PaskoochehNextPage<TermsOfServicePageProps> = ({
  staticPage,
}) => {
  const { localeCode } = useAppLocaleInfo();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  return (
    <PageContainer as="main">
      <PageMeta
        canonicalPath={routeUrls.termsOfService({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        })}
        description={staticPage.searchDescription || null}
        image={null}
        isAvailableInAlternateLocales={true}
        title={staticPage.seoTitle || staticPage.title || null}
      />
      <PageContent staticPage={staticPage} />
      <A11yShortcutPreset preset="skipToNavigation" />
    </PageContainer>
  );
};

export default TermsOfServicePage;
