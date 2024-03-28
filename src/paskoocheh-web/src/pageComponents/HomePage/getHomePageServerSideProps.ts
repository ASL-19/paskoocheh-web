import {
  getHomePageNormalizedQuery,
  getPopularAppsPreview,
  HomePageProps,
} from "src/pageComponents/HomePage/HomePage";
import { isValidVersionPreview } from "src/types/appTypes";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getReqInfo from "src/utils/getReqInfo";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

const getHomePageServerSideProps: PaskoochehGetServerSideProps<
  HomePageProps
> = async ({ query, req, res }) => {
  const normalizedQuery = getHomePageNormalizedQuery(query);
  const { platformSlug } = getReqInfo(req);

  try {
    const graphQlSdk = await getGraphQlSdk();

    const [
      platforms,
      featuredVersionPreviewsResponse,
      toolTypesResponse,
      featuredToolResponse,
      popularAppsInitialVersionPreviews,
    ] = await Promise.all([
      getPlatforms({ graphQlSdk }),
      graphQlSdk.getVersionPreviews({
        featured: true,
        first: 6,
        orderBy: "last_modified",
        platformSlug,
      }),
      graphQlSdk.getToolTypes(),
      graphQlSdk.getHomePageFeaturedTool(),
      getPopularAppsPreview({
        normalizedQuery,
      }),
    ]);

    const toolTypes = (toolTypesResponse.toolTypes?.edges || []).reduce(
      (acc, edge) => (edge?.node ? [...acc, edge.node] : acc),
      [],
    );

    const featuredVersionPreviews = (
      featuredVersionPreviewsResponse.versions?.edges || []
    ).reduce(
      (acc, edge) =>
        isValidVersionPreview(edge.node) ? [...acc, edge.node] : acc,
      [],
    );

    const featuredToolPreview = featuredToolResponse.homePageFeaturedTool;

    return pageProps({
      cacheDuration: "short",
      props: {
        featuredToolPreview,
        featuredVersionPreviews,
        normalizedQuery,
        platforms,
        popularAppsInitialVersionPreviews,
        toolTypes,
      },
      res,
    });
  } catch (error) {
    return errorProps({
      error,
      platforms: null,
      res,
      statusCode: 500,
    });
  }
};

export default getHomePageServerSideProps;
