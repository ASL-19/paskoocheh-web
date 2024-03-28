import { invisible } from "@asl-19/emotion-utils";
import { getNormalizedQuery } from "@asl-19/js-utils";
import { css } from "@emotion/react";
import { ParsedUrlQuery } from "querystring";
import { ContextType, useMemo } from "react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import BlogPageCategoryNavList from "src/components/BlogPage/BlogPageCategoryNavList";
import BlogPageFilterDialogDisclosure from "src/components/BlogPage/BlogPageFilterDialogDisclosure";
import BlogPostList from "src/components/BlogPage/BlogPostList";
import { getBlogPostListItemElementId } from "src/components/BlogPage/BlogPostListItem";
import DrawerDialogAndDisclosure from "src/components/DrawerDialog/DrawerDialogAndDisclosure";
import DrawerDialogLinksContent from "src/components/DrawerDialog/DrawerDialogLinksContent";
import IndexPageLoadingUi from "src/components/IndexPageLoadingUi";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import RouteDropdownMenu from "src/components/RouteDropdownMenu/RouteDropdownMenu";
import BlogPageContext from "src/contexts/BlogPageContext";
import { GqlPostPreview, GqlTopic } from "src/generated/graphQl";
import useAnimatedDialogState from "src/hooks/useAnimatedDialogState";
import useIndexPageLoadingAndQueryLogic, {
  IndexPageGetPreviewsAndHasNextPage,
} from "src/hooks/useIndexPageLoadingAndQueryLogic";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { RouteInfo } from "src/types/miscTypes";
import {
  PaskoochehNextPage,
  PaskoochehPageRequiredProps,
} from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import { Media } from "src/utils/media/media";
import { postsPerPage } from "src/values/indexPageValues";

// =============
// === Types ===
// =============
export type BlogPageProps = PaskoochehPageRequiredProps & {
  initialFilteredHashtag: string | null;
  initialHasNextPage: boolean;
  initialPreviews: Array<GqlPostPreview>;
  topics: Array<GqlTopic>;
};

export type BlogPageStrings = {
  /**
   * Texts for filter dropdown
   */
  filter: {
    date: string;
    label: string;
    popularity: string;
  };
  pageDescription: string;
  pageTitle: string;
};

export type BlogPageNormalizedQuery = {
  count: number;
  order: string;
  topic: string;
};

export const getBlogPageNormalizedQuery = (query: ParsedUrlQuery) =>
  getNormalizedQuery<BlogPageNormalizedQuery>({
    defaults: {
      count: postsPerPage,
      order: "-published",
      topic: "",
    },
    query,
    types: {
      count: "number",
      order: "string",
      topic: "string",
    },
  });

export const getBlogPagePreviewAndHasNextPage: IndexPageGetPreviewsAndHasNextPage<
  BlogPageNormalizedQuery,
  GqlPostPreview
> = async ({ isLoadMoreQuery, localeCode, normalizedQuery }) => {
  const graphQlSdk = await getGraphQlSdk();

  const response = await graphQlSdk.getPostPreviews({
    count: isLoadMoreQuery ? postsPerPage : normalizedQuery.count,
    localeCode,
    offset: isLoadMoreQuery ? normalizedQuery.count - postsPerPage : 0,
    orderBy: normalizedQuery.order,
    topics: normalizedQuery.topic ? [normalizedQuery.topic] : [],
  });

  const previews = (response.posts?.edges || []).reduce(
    (acc, edge) => (edge?.node ? [...acc, edge.node] : acc),
    [],
  );

  return {
    filteredHashtag: normalizedQuery.topic ?? null,
    hasNextPage: !!response.posts?.pageInfo.hasNextPage,
    previews,
  };
};

// ==============
// === Styles ===
// ==============
const pageContainer = css({
  display: "flex",
  flexDirection: "column",
  padding: "2rem 0",
});

const container = css({
  display: "flex",
  flexDirection: "column",
  gap: "2rem",
  paddingBottom: "3rem",
});

const indexPageLoadingUi = css({
  alignSelf: "center",
  margin: "3rem 0 0",
  padding: "0 3rem",
});

// ==============================
// === Next.js page component ===
// ==============================
const BlogPage: PaskoochehNextPage<BlogPageProps> = ({
  initialFilteredHashtag,
  initialHasNextPage,
  initialPreviews,
  topics,
}) => {
  const { localeCode } = useAppLocaleInfo();
  const { BlogPage: strings, shared: sharedStrings } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const filterAnimatedDialogState = useAnimatedDialogState();

  const { indexPageLoadingState, previews, queryInfo } =
    useIndexPageLoadingAndQueryLogic<BlogPageNormalizedQuery, GqlPostPreview>({
      getPageNormalizedQuery: getBlogPageNormalizedQuery,
      getPreviewElementId: getBlogPostListItemElementId,
      getPreviewsAndHasNextPage: getBlogPagePreviewAndHasNextPage,
      initialFilteredHashtag,
      initialHasNextPage,
      initialPreviews,
    });

  const blogRouteSharedArgs = useMemo(
    () => ({
      localeCode,
      platform: queryOrDefaultPlatformSlug,
      topic: queryInfo.normalizedQuery.topic || undefined,
    }),
    [localeCode, queryInfo.normalizedQuery.topic, queryOrDefaultPlatformSlug],
  ) satisfies Partial<Parameters<typeof routeUrls.blog>[0]>;

  const loadMoreLinkHref = routeUrls.blog({
    ...blogRouteSharedArgs,
    count: queryInfo.normalizedQuery.count + postsPerPage,
  });

  const sortingOptions = useMemo<Array<RouteInfo>>(
    () => [
      {
        key: "-published",
        name: strings.filter.date,
        route: routeUrls.blog({
          ...blogRouteSharedArgs,
          count: queryInfo.normalizedQuery.count,
          order: "-published",
          topic: queryInfo.normalizedQuery.topic || undefined,
        }),
      },
      {
        key: "-views",
        name: strings.filter.popularity + " [BROKEN]",
        route: routeUrls.blog({
          ...blogRouteSharedArgs,
          count: queryInfo.normalizedQuery.count,
          order: "-views",
          topic: queryInfo.normalizedQuery.topic || undefined,
        }),
      },
    ],
    [
      strings,
      blogRouteSharedArgs,
      queryInfo.normalizedQuery.count,
      queryInfo.normalizedQuery.topic,
    ],
  );

  const sortingSelectLabel = useMemo(
    () =>
      sortingOptions.find(
        (sortingOption) =>
          sortingOption.key === queryInfo.normalizedQuery.order,
      )?.name ?? strings.filter.date,
    [queryInfo.normalizedQuery.order, sortingOptions, strings.filter.date],
  );

  const blogPageContextValue = useMemo<ContextType<typeof BlogPageContext>>(
    () => ({ topic: queryInfo.normalizedQuery.topic }),
    [queryInfo.normalizedQuery.topic],
  );

  return (
    <BlogPageContext.Provider value={blogPageContextValue}>
      <PageContainer css={pageContainer} as="main">
        <PageMeta
          canonicalPath={routeUrls.blog({
            localeCode,
            platform: queryOrDefaultPlatformSlug,
          })}
          description={strings.pageDescription}
          image={null}
          isAvailableInAlternateLocales={true}
          title={strings.pageTitle}
        />

        <h1 css={invisible} id="main-heading">
          {strings.pageTitle}
        </h1>

        <PageSegment centeredContainerCss={container}>
          <BlogPageCategoryNavList topics={topics} />

          <Media lessThan="singleColumn">
            <DrawerDialogAndDisclosure
              animatedDialogStore={filterAnimatedDialogState}
              heading={strings.filter.label}
              headingLevel={2}
              disclosureContentElement={useMemo(
                () => (
                  <BlogPageFilterDialogDisclosure label={sortingSelectLabel} />
                ),
                [sortingSelectLabel],
              )}
            >
              <DrawerDialogLinksContent
                routeInfos={sortingOptions}
                animatedDialogState={filterAnimatedDialogState}
              />
            </DrawerDialogAndDisclosure>
          </Media>

          <Media greaterThanOrEqual="singleColumn">
            <RouteDropdownMenu
              routeInfos={sortingOptions}
              label={sortingSelectLabel}
            />
          </Media>

          {!["error", "hasNone", "loadingNew"].includes(
            indexPageLoadingState.type,
          ) && <BlogPostList postPreviews={previews} />}

          <IndexPageLoadingUi
            css={indexPageLoadingUi}
            loadMoreLinkHref={loadMoreLinkHref}
            loadMoreLinkText={sharedStrings.button.more}
            loadingState={indexPageLoadingState}
          />
        </PageSegment>
        <A11yShortcutPreset preset="skipToNavigation" />
      </PageContainer>
    </BlogPageContext.Provider>
  );
};

export default BlogPage;
