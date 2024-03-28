import { getSdk } from "src/generated/graphQl";
import toolTestDataBySlug from "src/test/data/toolTestDataBySlug";

const getHomePageFeaturedTool: ReturnType<
  typeof getSdk
>["getHomePageFeaturedTool"] = () => {
  if (global?.graphQlSdkOverrides?.getHomePageFeaturedToolResponse) {
    return Promise.resolve(
      global?.graphQlSdkOverrides?.getHomePageFeaturedToolResponse,
    );
  }

  return Promise.resolve({
    homePageFeaturedTool: toolTestDataBySlug["beepass-vpn"] ?? null,
  });
};

export default getHomePageFeaturedTool;
