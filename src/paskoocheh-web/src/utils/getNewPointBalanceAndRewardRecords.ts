import { GqlRewardRecord } from "src/generated/graphQl";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";

const getNewPointBalanceAndRewardRecords = async () => {
  const graphQlSdk = await getGraphQlSdk({ method: "POST" });
  let newPointsBalance: number;
  let newRewardRecords: Array<GqlRewardRecord>;
  try {
    const newMeResponse = await graphQlSdk.getMe();

    newPointsBalance = newMeResponse.me?.pointsBalance ?? 0;

    newRewardRecords = (newMeResponse.me?.rewardsRecords?.edges ?? []).reduce(
      (acc, userRewardRecords) =>
        userRewardRecords.node ? [...acc, userRewardRecords.node] : acc,
      [],
    );
  } catch (error) {
    console.error(error);
    return { newPointsBalance: null, newRewardRecords: null };
  }

  return { newPointsBalance, newRewardRecords };
};

export default getNewPointBalanceAndRewardRecords;
