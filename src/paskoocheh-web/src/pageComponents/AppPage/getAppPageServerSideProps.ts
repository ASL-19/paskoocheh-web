import { AppPageProps } from "src/pageComponents/AppPage/AppPage";
import routeUrls from "src/routeUrls";
import { isValidVersion } from "src/types/appTypes";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getReqInfo from "src/utils/getReqInfo";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getValidToolPrimaryToolType from "src/utils/getValidToolPrimaryToolType";
import getPlatforms from "src/utils/page/getPlatforms";
import { paskoochehAppSlug } from "src/values/apiValues";

type AppPageParams = {
  slug: string;
  toolType: string;
};

const getAppPageServerSideProps: PaskoochehGetServerSideProps<
  AppPageProps,
  AppPageParams
> = async ({ params, req, res }) => {
  const { localeCode, platformSlug } = getReqInfo(req);

  try {
    const graphQlSdk = await getGraphQlSdk();

    const platforms = await getPlatforms({ graphQlSdk });

    const [currentPlatformVersionResponse, paskoochehPlatformVersionResponse] =
      await Promise.all([
        graphQlSdk.getVersion({
          platformSlug,
          toolSlug: params.slug,
        }),
        graphQlSdk.getVersion({
          platformSlug,
          toolSlug: paskoochehAppSlug,
        }),
      ]);

    const currentPlatformVersion = currentPlatformVersionResponse.version;

    if (!currentPlatformVersion || !isValidVersion(currentPlatformVersion)) {
      return errorProps({ platforms, res, statusCode: 404 });
    }

    const platformPaskoochehAppPath = (() => {
      const paskoochehVersion =
        paskoochehPlatformVersionResponse.version &&
        isValidVersion(paskoochehPlatformVersionResponse.version)
          ? paskoochehPlatformVersionResponse.version
          : null;

      if (!paskoochehVersion) {
        return null;
      }

      return routeUrls.app({
        localeCode,
        platform: platformSlug,
        slug: paskoochehVersion.tool.slug,
        toolType: getValidToolPrimaryToolType(paskoochehVersion.tool).slug,
      });
    })();

    return pageProps({
      cacheDuration: "short",
      props: {
        currentPlatformVersion,
        platformPaskoochehAppPath,
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

export default getAppPageServerSideProps;
