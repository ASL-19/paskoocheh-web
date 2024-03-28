import { getSdk } from "src/generated/graphQl";
import versionTestDataBySlug from "src/test/data/versionTestDataBySlug";

const getVersion: ReturnType<typeof getSdk>["getVersion"] = () => {
  if (global?.graphQlSdkOverrides?.getVersionResponse) {
    return Promise.resolve(global?.graphQlSdkOverrides?.getVersionResponse);
  }

  return Promise.resolve({
    version: versionTestDataBySlug["beepass-vpn"] ?? null,
  });
};

export default getVersion;
