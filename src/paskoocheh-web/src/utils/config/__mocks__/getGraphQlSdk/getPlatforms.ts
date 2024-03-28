import { getSdk } from "src/generated/graphQl";
import platformTestDataBySlug from "src/test/data/platformTestDataBySlug";

const getPlatforms: ReturnType<typeof getSdk>["getPlatforms"] = () => {
  if (global?.graphQlSdkOverrides?.getPlatformsResponse) {
    return Promise.resolve(global.graphQlSdkOverrides.getPlatformsResponse);
  }

  const platforms = Object.values(platformTestDataBySlug);

  return Promise.resolve({
    platforms: {
      edges: platforms.map((platform) => ({
        node: platform,
      })),
    },
  });
};

export default getPlatforms;
