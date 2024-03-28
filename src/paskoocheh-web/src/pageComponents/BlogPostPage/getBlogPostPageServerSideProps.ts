import { GqlPost } from "src/generated/graphQl";
import { BlogPostPageProps } from "src/pageComponents/BlogPostPage/BlogPostPage";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getReqInfo from "src/utils/getReqInfo";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

type BlogPostPageParams = {
  slug: string;
};

const getBlogPostPageServerSideProps: PaskoochehGetServerSideProps<
  BlogPostPageProps,
  BlogPostPageParams
> = async ({ params, req, res }) => {
  const { localeCode } = getReqInfo(req);

  try {
    const graphQlSdk = await getGraphQlSdk();

    const [platforms, postResponse] = await Promise.all([
      getPlatforms({ graphQlSdk }),
      graphQlSdk.getPost({
        localeCode,
        slug: params.slug,
      }),
    ]);

    const post = postResponse.post as GqlPost;

    if (!post) {
      return errorProps({ platforms, res, statusCode: 404 });
    }

    return pageProps({
      cacheDuration: "short",
      props: {
        platforms,
        post,
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

export default getBlogPostPageServerSideProps;
