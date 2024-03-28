import { ActivateAccountPageProps } from "src/pageComponents/ActivateAccountPage/ActivateAccountPage";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

type ActivateAccountPageQuery = {
  token: string;
};

const getActivateAccountPageServerSideProps: PaskoochehGetServerSideProps<
  ActivateAccountPageProps,
  ActivateAccountPageQuery
> = async ({ query: { token }, res }) => {
  const graphQlSdk = await getGraphQlSdk({ method: "POST" });

  let didActivate = false;

  const verifiedToken = token && typeof token === "string" ? token : "";

  try {
    const verifyAccountResponse = await graphQlSdk.doVerifyAccount({
      token: verifiedToken,
    });

    didActivate = !!verifyAccountResponse.verifyAccount?.success;

    return pageProps({
      cacheDuration: "short",
      props: {
        didActivate,
        platforms: await getPlatforms({ graphQlSdk }),
      },
      res,
    });
  } catch (error) {
    return errorProps({ error, platforms: null, res, statusCode: 500 });
  }
};

export default getActivateAccountPageServerSideProps;
