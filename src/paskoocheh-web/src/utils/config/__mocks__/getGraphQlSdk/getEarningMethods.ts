import { getSdk } from "src/generated/graphQl";
import earningMethodsData from "src/test/data/earningMethodsData";

const getEarningMethods: ReturnType<
  typeof getSdk
>["getEarningMethods"] = () => {
  if (global.graphQlSdkOverrides?.getEarningMethodsResponse) {
    return Promise.resolve(
      global.graphQlSdkOverrides.getEarningMethodsResponse,
    );
  }

  const earningMethods = Object.values(earningMethodsData);

  return Promise.resolve({
    earningMethods,
  });
};

export default getEarningMethods;
