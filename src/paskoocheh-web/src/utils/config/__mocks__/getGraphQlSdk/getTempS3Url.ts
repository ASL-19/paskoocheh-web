import type { getSdk } from "src/generated/graphQl";

const getTempS3Url: ReturnType<typeof getSdk>["getTempS3Url"] = () => {
  if (global?.graphQlSdkOverrides?.getTempS3Url) {
    return Promise.resolve(global?.graphQlSdkOverrides?.getTempS3Url);
  }

  return Promise.resolve({
    tempS3Url: "/mockTempS3Url",
  });
};

export default getTempS3Url;
