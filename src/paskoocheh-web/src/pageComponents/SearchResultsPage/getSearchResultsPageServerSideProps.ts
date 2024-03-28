import { getFirstStringOrString } from "@asl-19/js-utils";

import { SearchResultsPageProps } from "src/pageComponents/SearchResultsPage/SearchResultsPage";
import routeUrls from "src/routeUrls";
import { isValidVersionPreview } from "src/types/appTypes";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getReqInfo from "src/utils/getReqInfo";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

const getSearchResultsPageServerSideProps: PaskoochehGetServerSideProps<
  SearchResultsPageProps
> = async ({ query, req, res }) => {
  const { platformSlug } = getReqInfo(req);

  const queryQuery = getFirstStringOrString(query.query);

  // Redirect to homepage if query empty (helps no-JS users change platforms)
  if (!queryQuery) {
    const { localeCode } = getReqInfo(req);

    return {
      redirect: {
        destination: routeUrls.home({
          localeCode,
          platform: platformSlug,
        }),
        permanent: false,
      },
    };
  }

  try {
    const graphQlSdk = await getGraphQlSdk();

    const [platforms, versionPreviewsResponse] = await Promise.all([
      getPlatforms({ graphQlSdk }),
      graphQlSdk.getVersionPreviews({
        first: 99,
        orderBy: "last_modified",
      }),
    ]);

    const versionPreviews = (
      versionPreviewsResponse.versions?.edges || []
    ).reduce(
      (acc, edge) =>
        isValidVersionPreview(edge.node) ? [...acc, edge.node] : acc,
      [],
    );

    const searchResults = versionPreviews.filter((appPreview) =>
      appPreview.tool?.name.toLowerCase().includes(queryQuery.toLowerCase()),
    );

    return pageProps({
      cacheDuration: "short",
      props: {
        platforms,
        query: queryQuery,
        searchResults,
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

export default getSearchResultsPageServerSideProps;
