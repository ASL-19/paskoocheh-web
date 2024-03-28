import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

const getAccountSettingsPageServerSideProps: PaskoochehGetServerSideProps =
  async ({ res }) => {
    try {
      const graphQlSdk = await getGraphQlSdk();

      const platforms = await getPlatforms({ graphQlSdk });

      return pageProps({
        cacheDuration: "short",
        props: {
          platforms,
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

export default getAccountSettingsPageServerSideProps;
