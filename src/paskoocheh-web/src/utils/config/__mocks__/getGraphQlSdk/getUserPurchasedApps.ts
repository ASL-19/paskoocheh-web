import { getSdk } from "src/generated/graphQl";
import rewardReviewPurchasedAppsData from "src/test/data/rewardReviewPurchasedAppsData";

const getUserPurchasedApps: ReturnType<
  typeof getSdk
>["getUserPurchasedApps"] = () => {
  if (global.graphQlSdkOverrides?.getUserPurchasedAppsResponse) {
    return Promise.resolve(
      global.graphQlSdkOverrides.getUserPurchasedAppsResponse,
    );
  }

  const purchasedVersionPreviews = rewardReviewPurchasedAppsData.node;

  return Promise.resolve(purchasedVersionPreviews);
};

export default getUserPurchasedApps;
