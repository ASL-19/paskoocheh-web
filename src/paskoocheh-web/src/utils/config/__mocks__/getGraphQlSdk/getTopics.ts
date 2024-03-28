import { getSdk } from "src/generated/graphQl";
import topicTestDataBySlug from "src/test/data/topicTestDataBySlug";

const getTopics: ReturnType<typeof getSdk>["getTopics"] = () => {
  if (global?.graphQlSdkOverrides?.getTopicsResponse) {
    return Promise.resolve(global.graphQlSdkOverrides.getTopicsResponse);
  }

  const topics = Object.values(topicTestDataBySlug);

  return Promise.resolve({
    topics: {
      edges: topics.map((topic) => ({
        node: topic,
      })),
      pageInfo: { endCursor: null, hasNextPage: false },
    },
  });
};

export default getTopics;
