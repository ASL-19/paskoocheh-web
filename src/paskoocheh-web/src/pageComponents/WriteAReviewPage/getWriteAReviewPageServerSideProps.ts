import { getFirstStringOrString } from "@asl-19/js-utils";

import { WriteAReviewPageProps } from "src/pageComponents/WriteAReviewPage/WriteAReviewPage";
import { PaskoochehGetServerSideProps } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getReqInfo from "src/utils/getReqInfo";
import errorProps from "src/utils/getServerSideProps/errorProps";
import pageProps from "src/utils/getServerSideProps/pageProps";
import getPlatforms from "src/utils/page/getPlatforms";

const getWriteAReviewPageServerSideProps: PaskoochehGetServerSideProps<
  WriteAReviewPageProps
> = async ({ query, req, res }) => {
  const { platformSlug } = getReqInfo(req);
  const graphQlSdk = await getGraphQlSdk();

  const queryTool = getFirstStringOrString(query.tool);

  try {
    const toolPreviewResponse = await graphQlSdk.getVersionPreview({
      platformSlug,
      // TODO: Change tool argument to tool slug and replace with toolSlug once
      // #559 is done
      toolPk: Number(queryTool) || 0,
    });

    const versionPreview = toolPreviewResponse.version;

    if (!versionPreview) {
      return errorProps({
        platforms: null,
        res,
        statusCode: 404,
      });
    }

    return pageProps({
      cacheDuration: "short",
      props: {
        platforms: await getPlatforms({ graphQlSdk }),
        versionPreview,
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

export default getWriteAReviewPageServerSideProps;
