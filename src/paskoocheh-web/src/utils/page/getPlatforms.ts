import { SdkWithHasAccessToken } from "src/types/apiTypes";

/**
 * Get all `GqlPlatform`s. Takes `graphQlSdk` to avoid async waterfall (in most
 * places this is called there should already be a `graphQlSdk`).
 *
 * **Can throw an exception — make sure this is called in a try...catch block!**
 */
const getPlatforms = async ({
  graphQlSdk,
}: {
  graphQlSdk: SdkWithHasAccessToken;
}) => {
  const platformResponse = await graphQlSdk.getPlatforms();

  const platforms = (platformResponse.platforms?.edges || []).reduce(
    (acc, edge) => (edge?.node ? [...acc, edge.node] : acc),
    [],
  );

  return platforms;
};

export default getPlatforms;
