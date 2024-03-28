import { PrivacyPolicyPageProps } from "src/pageComponents/PrivacyPolicyPage/PrivacyPolicyPage";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getReqInfo from "src/utils/getReqInfo";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

const getPrivacyPolicyPageServerSideProps: PaskoochehGetServerSideProps<
  PrivacyPolicyPageProps
> = async ({ req, res }) => {
  const { localeCode } = getReqInfo(req);

  try {
    const graphQlSdk = await getGraphQlSdk();

    const [platforms, staticPageResponse] = await Promise.all([
      getPlatforms({ graphQlSdk }),
      graphQlSdk.getStaticPage({
        localeCode,
        staticPageSlug: "privacy-policy",
      }),
    ]);

    const staticPage = staticPageResponse.staticPage;

    if (!staticPage) {
      return errorProps({ platforms, res, statusCode: 404 });
    }

    return pageProps({
      cacheDuration: "short",
      props: { platforms, staticPage },
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

export default getPrivacyPolicyPageServerSideProps;
