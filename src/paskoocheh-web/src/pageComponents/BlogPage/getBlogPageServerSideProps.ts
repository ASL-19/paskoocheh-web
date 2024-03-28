import {
  BlogPageProps,
  getBlogPageNormalizedQuery,
  getBlogPagePreviewAndHasNextPage,
} from "src/pageComponents/BlogPage/BlogPage";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getReqInfo from "src/utils/getReqInfo";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

const getBlogPageServerSideProps: PaskoochehGetServerSideProps<
  BlogPageProps
> = async ({ query, req, res }) => {
  const { localeCode } = getReqInfo(req);
  const normalizedQuery = getBlogPageNormalizedQuery(query);

  try {
    const graphQlSdk = await getGraphQlSdk();

    const [
      {
        filteredHashtag: initialFilteredHashtag,
        hasNextPage: initialHasNextPage,
        previews: initialPreviews,
      },
      platforms,
      topicResponse,
    ] = await Promise.all([
      getBlogPagePreviewAndHasNextPage({
        isLoadMoreQuery: false,
        localeCode,
        normalizedQuery,
      }),
      getPlatforms({ graphQlSdk }),
      graphQlSdk.getTopics({ localeCode }),
    ]);

    const topics = (topicResponse.topics?.edges || []).reduce(
      (acc, edge) => (edge?.node ? [...acc, edge.node] : acc),
      [],
    );

    return pageProps({
      cacheDuration: "short",
      props: {
        initialFilteredHashtag,
        initialHasNextPage,
        initialPreviews,
        platforms,
        topics,
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

export default getBlogPageServerSideProps;
