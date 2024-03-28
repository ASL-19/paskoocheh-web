import { getSdk } from "src/generated/graphQl";
import toolTypesTestDataBySlug from "src/test/data/toolTypeTestDataBySlug";

const getToolTypes: ReturnType<typeof getSdk>["getToolTypes"] = () => {
  if (global?.graphQlSdkOverrides?.getToolTypesResponse) {
    return Promise.resolve(global.graphQlSdkOverrides.getToolTypesResponse);
  }

  const toolTypes = Object.values(toolTypesTestDataBySlug);

  return Promise.resolve({
    toolTypes: {
      edges: toolTypes.map((toolType) => ({
        node: toolType,
      })),
      pageInfo: { endCursor: null, hasNextPage: false },
    },
  });
};

export default getToolTypes;
