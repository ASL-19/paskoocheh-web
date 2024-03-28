import { SignInPageProps } from "src/pageComponents/SignInPage/SignInPage";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

const getSignInPageServerSideProps: PaskoochehGetServerSideProps<
  SignInPageProps
> = async ({ query, res }) => {
  try {
    const graphQlSdk = await getGraphQlSdk();

    const decodedReturnPath =
      typeof query.returnPath === "string" ? query.returnPath : null;

    return pageProps({
      cacheDuration: "short",
      props: {
        decodedReturnPath,
        platforms: await getPlatforms({ graphQlSdk }),
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

export default getSignInPageServerSideProps;
