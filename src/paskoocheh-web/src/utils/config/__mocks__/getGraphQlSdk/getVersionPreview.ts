import { getSdk } from "src/generated/graphQl";
import versionPreviewTestDataBySlug from "src/test/data/versionPreviewTestDataBySlug";

const getVersionPreview: ReturnType<
  typeof getSdk
>["getVersionPreview"] = () => {
  if (global?.graphQlSdkOverrides?.getVersionPreviewResponse) {
    return Promise.resolve(
      global?.graphQlSdkOverrides?.getVersionPreviewResponse,
    );
  }

  return Promise.resolve({
    version: versionPreviewTestDataBySlug["beepass-vpn"] ?? null,
  });
};

export default getVersionPreview;
