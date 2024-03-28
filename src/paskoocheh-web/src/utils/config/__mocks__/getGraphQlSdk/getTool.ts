import { getSdk } from "src/generated/graphQl";
import toolTestDataBySlug from "src/test/data/toolTestDataBySlug";

const getTool: ReturnType<typeof getSdk>["getTool"] = () => {
  if (global?.graphQlSdkOverrides?.getToolResponse) {
    return Promise.resolve(global?.graphQlSdkOverrides?.getToolResponse);
  }

  return Promise.resolve({
    tool: toolTestDataBySlug["beepass-vpn"] ?? null,
  });
};

export default getTool;
