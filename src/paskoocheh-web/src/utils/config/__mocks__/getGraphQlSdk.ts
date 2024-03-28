import { SdkWithHasAccessToken } from "src/types/apiTypes";
import getRefreshToken from "src/utils/api/getRefreshToken";
import doTokenAuth from "src/utils/config/__mocks__/getGraphQlSdk/doTokenAuth";
import getEarningMethods from "src/utils/config/__mocks__/getGraphQlSdk/getEarningMethods";
import getHasFinishedQuiz from "src/utils/config/__mocks__/getGraphQlSdk/getHasFinishedQuiz";
import getHomePageFeaturedTool from "src/utils/config/__mocks__/getGraphQlSdk/getHomePageFeaturedTool";
import getMe from "src/utils/config/__mocks__/getGraphQlSdk/getMe";
import getPlatforms from "src/utils/config/__mocks__/getGraphQlSdk/getPlatforms";
import getPost from "src/utils/config/__mocks__/getGraphQlSdk/getPost";
import getPostPreviews from "src/utils/config/__mocks__/getGraphQlSdk/getPostPreviews";
import getQuizzes from "src/utils/config/__mocks__/getGraphQlSdk/getQuizzes";
import getRedemptionMethods from "src/utils/config/__mocks__/getGraphQlSdk/getRedemptionMethods";
import getRewardRecords from "src/utils/config/__mocks__/getGraphQlSdk/getRewardRecords";
import getStaticPage from "src/utils/config/__mocks__/getGraphQlSdk/getStaticPage";
import getTempS3Url from "src/utils/config/__mocks__/getGraphQlSdk/getTempS3Url";
import getTool from "src/utils/config/__mocks__/getGraphQlSdk/getTool";
import getToolTypes from "src/utils/config/__mocks__/getGraphQlSdk/getToolTypes";
import getTopics from "src/utils/config/__mocks__/getGraphQlSdk/getTopics";
import getUserPurchasedApps from "src/utils/config/__mocks__/getGraphQlSdk/getUserPurchasedApps";
import getVersion from "src/utils/config/__mocks__/getGraphQlSdk/getVersion";
import getVersionPreview from "src/utils/config/__mocks__/getGraphQlSdk/getVersionPreview";
import getVersionPreviews from "src/utils/config/__mocks__/getGraphQlSdk/getVersionPreviews";
const envDelay = process.env.NEXT_PUBLIC_MOCK_GRAPHQL_SDK_DELAY
  ? parseInt(process.env.NEXT_PUBLIC_MOCK_GRAPHQL_SDK_DELAY) || 0
  : 0;

const getGraphQlSdk = (): Promise<Partial<SdkWithHasAccessToken>> => {
  /**
   * The value of delay +/- 50%
   */
  const semiRandomizedDelay =
    envDelay + envDelay * 0.5 * (Math.random() * 2 - 1);

  return new Promise((resolve) =>
    setTimeout(
      () =>
        resolve({
          doTokenAuth,
          getEarningMethods,
          getHasFinishedQuiz,
          getHomePageFeaturedTool,
          getMe,
          getPlatforms,
          getPost,
          getPostPreviews,
          getQuizzes,
          getRedemptionMethods,
          getRewardRecords,
          getStaticPage,
          getTempS3Url,
          getTool,
          getToolTypes,
          getTopics,
          getUserPurchasedApps,
          getVersion,
          getVersionPreview,
          getVersionPreviews,
          hasAccessToken: !!getRefreshToken(),
        }),
      semiRandomizedDelay,
    ),
  );
};

export default getGraphQlSdk;
