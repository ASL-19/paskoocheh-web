import { getFirstStringOrString } from "@asl-19/js-utils";
import { match, P } from "ts-pattern";

import { ContactPageProps } from "src/pageComponents/ContactPage/ContactPage";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getReqInfo from "src/utils/getReqInfo";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

const getContactPageServerSideProps: PaskoochehGetServerSideProps<
  ContactPageProps
> = async ({ query, req, res }) => {
  const { platformSlug } = getReqInfo(req);

  try {
    const graphQlSdk = await getGraphQlSdk();

    const toolPk = match(Number(getFirstStringOrString(query.tool)))
      .with(P.not(NaN), (toolPk) => toolPk)
      .otherwise(() => null);

    const [platforms, toolPreviewResponse] = await Promise.all([
      getPlatforms({ graphQlSdk }),
      ...(toolPk
        ? [
            graphQlSdk.getVersionPreview({
              platformSlug,
              // TODO: Change tool argument to tool slug and replace with toolSlug once
              // #559 is done
              toolPk,
            }),
          ]
        : []),
    ]);
    const versionPreview = toolPreviewResponse
      ? toolPreviewResponse.version
      : null;

    if (toolPk && !versionPreview) {
      return errorProps({
        platforms: null,
        res,
        statusCode: 404,
      });
    }

    return pageProps({
      cacheDuration: "short",
      props: {
        platforms,
        toolPk,
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

export default getContactPageServerSideProps;
