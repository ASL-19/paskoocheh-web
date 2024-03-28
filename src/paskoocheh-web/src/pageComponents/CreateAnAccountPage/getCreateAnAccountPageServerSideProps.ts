import { CreateAnAccountPageProps } from "src/pageComponents/CreateAnAccountPage/CreateAnAccountPage";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

type CreateAnAccountPageQuery = {
  referral: string;
};

const getCreateAnAccountPageServerSideProps: PaskoochehGetServerSideProps<
  CreateAnAccountPageProps,
  CreateAnAccountPageQuery
> = async ({ query, res }) => {
  try {
    const graphQlSdk = await getGraphQlSdk();

    return pageProps({
      cacheDuration: "short",
      props: {
        platforms: await getPlatforms({ graphQlSdk }),
        referralSlug: query.referral?.toString() ?? null,
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

export default getCreateAnAccountPageServerSideProps;
