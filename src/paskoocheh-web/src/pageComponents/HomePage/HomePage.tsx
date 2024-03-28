import { invisible } from "@asl-19/emotion-utils";
import { focusElement } from "@asl-19/js-dom-utils";
import { getNormalizedQuery } from "@asl-19/js-utils";
import { css } from "@emotion/react";
import { ParsedUrlQuery } from "querystring";
import { ContextType, useCallback, useId, useMemo } from "react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import HomePageCategoryNavList from "src/components/HomePage/HomePageCategoryNavList";
import HomePageEditorsChoiceSegment from "src/components/HomePage/HomePageEditorsChoiceSegment";
import HomePagePopularAppsSegment from "src/components/HomePage/HomePagePopularAppsSegment";
import HomePagePromoBoxSegment from "src/components/HomePage/PromoBox";
import IndexPageLoadingUi from "src/components/IndexPageLoadingUi";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import HomePageContext from "src/contexts/HomePageContext";
import { GqlToolPreview, GqlToolType } from "src/generated/graphQl";
import usePopularAppsFilterLoadingAndQueryLogic, {
  PopularAppsGetPreviews,
} from "src/hooks/usePopularAppsFilterLoadingAndQueryLogic";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import headerHeroPng from "src/static/images/headerHero.png";
import limitedTimeBonusPng from "src/static/images/limitedTimeBonusPng.png";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { headingH2SemiBold } from "src/styles/typeStyles";
import { isValidToolPreview, ValidVersionPreview } from "src/types/appTypes";
import { isValidVersionPreview } from "src/types/appTypes";
import {
  PaskoochehNextPage,
  PaskoochehPageRequiredProps,
} from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getLocaleToolTypeName from "src/utils/getLocaleToolTypeName";
import getValidToolPrimaryToolType from "src/utils/getValidToolPrimaryToolType";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";
import { postsPerPage } from "src/values/indexPageValues";
import { defaultPlatformSlug } from "src/values/miscValues";

export const issuesSectionId = "issues";

// =============
// === Types ===
// =============
export type HomePageProps = PaskoochehPageRequiredProps & {
  featuredToolPreview: GqlToolPreview | null;
  featuredVersionPreviews: Array<ValidVersionPreview>;
  normalizedQuery: HomePageNormalizedQuery;
  popularAppsInitialVersionPreviews: Array<ValidVersionPreview>;
  toolTypes: Array<GqlToolType>;
};

export type HomePageStrings = {
  bonusSectionDescription: string;
  bonusSectionTitle: string;
  heroDescription: string;
  heroTitle: string;
  pageDescription: string;
};

export type HomePageNormalizedQuery = {
  category: string | undefined;
  count: number;
  platform: string;
};

export const getHomePageNormalizedQuery = (query: ParsedUrlQuery) =>
  getNormalizedQuery<HomePageNormalizedQuery>({
    defaults: {
      category: "",
      count: 0,
      platform: defaultPlatformSlug,
    },
    query,
    types: {
      category: "string",
      count: "number",
      platform: "string",
    },
  });

export const getPopularAppsPreview: PopularAppsGetPreviews<
  HomePageNormalizedQuery,
  ValidVersionPreview
> = async ({ normalizedQuery }) => {
  const graphQlSdk = await getGraphQlSdk();

  const response = await graphQlSdk.getVersionPreviews({
    category:
      normalizedQuery.category !== "" ? normalizedQuery.category : undefined,
    first: postsPerPage,
    orderBy: "-download_count",
    platformSlug: normalizedQuery.platform,
  });

  const previews = (response.versions?.edges || []).reduce(
    (acc, edge) =>
      isValidVersionPreview(edge.node) ? [...acc, edge.node] : acc,
    [],
  );

  return previews;
};

// ==============
// === Styles ===
// ==============
const pageContainer = css({
  display: "flex",
  flexDirection: "column",
});

const editorsChoiceSectionContainer = css(
  {
    margin: "2rem 0",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        margin: "1.5rem 0",
      },
    },
  }),
);

const topHeroHeaderAndImageTextSectionButton = css({
  paddingInline: "3rem",
});

const homePageCategoryNavListPageSegment = css({
  paddingBlock: "1rem",
});

const indexPageLoadingUi = css({
  alignSelf: "center",
  margin: "3rem 0 0",
  padding: "0 3rem",
});

// ==============================
// === Next.js page component ===
// ==============================
const HomePage: PaskoochehNextPage<HomePageProps> = ({
  featuredToolPreview,
  featuredVersionPreviews,
  normalizedQuery,
  popularAppsInitialVersionPreviews,
  toolTypes,
}) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();
  const headerImg = `${process.env.NEXT_PUBLIC_WEB_URL}${headerHeroPng.src}`;
  const bonusImg = `${process.env.NEXT_PUBLIC_WEB_URL}${limitedTimeBonusPng.src}`;

  const featuredToolInfo = (featuredToolPreview?.info?.edges || []).reduce(
    (acc, edge) => (edge?.node ? [...acc, edge.node] : acc),
    [],
  );

  const featuredToolBanner = featuredToolPreview?.images?.find(
    (img) => img?.imageType === "header",
  );

  const featuredToolBannerUrl = featuredToolBanner
    ? `${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${featuredToolBanner.image}`
    : headerImg;

  const homePagePopularAppsSegmentHeadingId = useId();

  const onNewPopularAppsLoaded = useCallback(() => {
    focusElement(document.getElementById(homePagePopularAppsSegmentHeadingId));
  }, [homePagePopularAppsSegmentHeadingId]);

  const { popularAppsLoadingState, previews, queryInfo } =
    usePopularAppsFilterLoadingAndQueryLogic<
      HomePageNormalizedQuery,
      ValidVersionPreview
    >({
      getPageNormalizedQuery: getHomePageNormalizedQuery,
      getPreviews: getPopularAppsPreview,
      onNewItemsLoaded: onNewPopularAppsLoaded,
      popularAppsInitialVersionPreviews,
    });

  const homePageContextValue = useMemo<ContextType<typeof HomePageContext>>(
    () => ({ category: normalizedQuery.category || undefined }),
    [normalizedQuery.category],
  );

  const categoryQuery = normalizedQuery.category;

  const toolType = toolTypes.filter(
    (toolType) => toolType.slug === categoryQuery,
  )[0];

  const activeCategoryName = toolType
    ? getLocaleToolTypeName({ localeCode, toolType })
    : null;

  const featuredValidToolPreview =
    featuredToolPreview && isValidToolPreview(featuredToolPreview)
      ? featuredToolPreview
      : null;

  return (
    <HomePageContext.Provider value={homePageContextValue}>
      <PageContainer as="main" css={pageContainer}>
        <PageMeta
          canonicalPath={routeUrls.home({
            localeCode,
            platform: queryOrDefaultPlatformSlug,
          })}
          description={strings.HomePage.pageDescription}
          image={null}
          isAvailableInAlternateLocales={true}
          title={activeCategoryName}
        />
        <h1 css={invisible} id="main-heading">
          {strings.shared.siteTitle}
        </h1>

        {process.env.NEXT_PUBLIC_ENABLE_APP_CATEGORIES_NAV && (
          <PageSegment css={homePageCategoryNavListPageSegment}>
            <HomePageCategoryNavList toolTypes={toolTypes} />
          </PageSegment>
        )}

        {!queryInfo.normalizedQuery.category && featuredValidToolPreview && (
          <HomePagePromoBoxSegment
            buttonCss={topHeroHeaderAndImageTextSectionButton}
            buttonText={strings.shared.downloadNow}
            buttonUrl={routeUrls.app({
              localeCode,
              platform: featuredValidToolPreview.availablePlatforms.includes(
                queryOrDefaultPlatformSlug,
              )
                ? queryOrDefaultPlatformSlug
                : featuredValidToolPreview.availablePlatforms[0],
              slug: featuredValidToolPreview.slug,
              toolType: getValidToolPrimaryToolType(featuredValidToolPreview)
                .slug,
            })}
            buttonVariant="primary"
            imageAlignment="viewport"
            imageUrl={featuredToolBannerUrl}
            description={featuredToolInfo[0]?.promoText ?? ""}
            textColor={colors.shadesWhite}
            title={featuredValidToolPreview.name}
          />
        )}

        {!["error", "hasNone", "loadingNew"].includes(
          popularAppsLoadingState.type,
        ) && (
          <HomePagePopularAppsSegment
            headingId={homePagePopularAppsSegmentHeadingId}
            versionPreviews={previews}
            activeCategoryName={activeCategoryName}
          />
        )}

        <IndexPageLoadingUi
          css={indexPageLoadingUi}
          loadMoreLinkHref=""
          loadMoreLinkText=""
          loadingState={popularAppsLoadingState}
        />

        <HomePagePromoBoxSegment
          buttonText={strings.shared.learnMore}
          buttonUrl={routeUrls.home({
            localeCode,
            platform: queryOrDefaultPlatformSlug,
          })}
          buttonVariant="secondary"
          headingCss={headingH2SemiBold}
          imageAlignment="content"
          imageUrl={bonusImg}
          description={strings.HomePage.bonusSectionDescription}
          textColor={colors.secondary500}
          title={strings.HomePage.bonusSectionTitle}
        />

        <HomePageEditorsChoiceSegment
          versionPreviews={featuredVersionPreviews}
          css={editorsChoiceSectionContainer}
        />

        <A11yShortcutPreset preset="skipToNavigation" />
      </PageContainer>
    </HomePageContext.Provider>
  );
};

export default HomePage;
