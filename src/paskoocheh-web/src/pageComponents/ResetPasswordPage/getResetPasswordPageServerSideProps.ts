import { ResetPasswordPageProps } from "src/pageComponents/ResetPasswordPage/ResetPasswordPage";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

const getResetPasswordPageServerSideProps: PaskoochehGetServerSideProps<
  ResetPasswordPageProps
> = async ({ res }) => {
  try {
    const graphQlSdk = await getGraphQlSdk();

    return pageProps({
      cacheDuration: "short",
      props: {
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

export default getResetPasswordPageServerSideProps;
