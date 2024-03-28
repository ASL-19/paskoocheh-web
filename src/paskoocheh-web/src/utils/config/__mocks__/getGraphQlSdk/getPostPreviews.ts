import { getSdk } from "src/generated/graphQl";
import postTestDataBySlug from "src/test/data/postTestDataBySlug";

const getPostPreviews: ReturnType<typeof getSdk>["getPostPreviews"] = () => {
  if (global?.graphQlSdkOverrides?.getPostPreviewsResponse) {
    return Promise.resolve(global.graphQlSdkOverrides.getPostPreviewsResponse);
  }
  const posts = Object.values(postTestDataBySlug);

  return Promise.resolve({
    posts: {
      edges: posts.map((post) => ({
        node: post,
      })),
      pageInfo: { endCursor: null, hasNextPage: false },
    },
  });
};

export default getPostPreviews;
