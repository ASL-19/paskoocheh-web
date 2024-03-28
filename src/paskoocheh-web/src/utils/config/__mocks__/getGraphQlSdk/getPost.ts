import { getSdk } from "src/generated/graphQl";
import postTestDataBySlug from "src/test/data/postTestDataBySlug";

const getPost: ReturnType<typeof getSdk>["getPost"] = (variables) => {
  if (global?.graphQlSdkOverrides?.getPostResponse) {
    return Promise.resolve(global?.graphQlSdkOverrides?.getPostResponse);
  }

  return Promise.resolve({ post: postTestDataBySlug[variables.slug] ?? null });
};

export default getPost;
