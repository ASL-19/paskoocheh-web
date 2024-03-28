import { getSdk } from "src/generated/graphQl";
import redemptionMethodsData from "src/test/data/redemptionMethodsData";

const getRedemptionMethods: ReturnType<
  typeof getSdk
>["getRedemptionMethods"] = () => {
  if (global.graphQlSdkOverrides?.getRedemptionMethodsResponse) {
    return Promise.resolve(
      global.graphQlSdkOverrides.getRedemptionMethodsResponse,
    );
  }

  const redemptionMethods = Object.values(redemptionMethodsData);

  return Promise.resolve({
    redemptionMethods: {
      edges: redemptionMethods.map((redemptionMethod) => ({
        node: redemptionMethod,
      })),
      pageInfo: { endCursor: null, hasNextPage: false },
    },
  });
};

export default getRedemptionMethods;
