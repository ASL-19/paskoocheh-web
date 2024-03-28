import { getSdk } from "src/generated/graphQl";
import versionPreviewTestDataBySlug from "src/test/data/versionPreviewTestDataBySlug";

const getVersionPreviews: ReturnType<
  typeof getSdk
>["getVersionPreviews"] = () => {
  if (global?.graphQlSdkOverrides?.getVersionPreviewsResponse) {
    return Promise.resolve(
      global.graphQlSdkOverrides.getVersionPreviewsResponse,
    );
  }
  const tools = Object.values(versionPreviewTestDataBySlug);

  return Promise.resolve({
    versions: {
      edges: tools.map((tool) => ({
        node: tool,
      })),
      pageInfo: { endCursor: null, hasNextPage: false },
    },
  });
};

export default getVersionPreviews;
