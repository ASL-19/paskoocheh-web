import { getSdk } from "src/generated/graphQl";
import rewardRecordData from "src/test/data/rewardRecordData";

// TODO: Is there a good way for us to keep records in memory for testing new
// records created at run/test time? Currently it can’t know about new records
// so e.g. pagination won’t work.
const getRewardRecords: ReturnType<typeof getSdk>["getRewardRecords"] = () => {
  if (global.graphQlSdkOverrides?.getRewardRecordsResponse) {
    return Promise.resolve(global.graphQlSdkOverrides.getRewardRecordsResponse);
  }

  const rewardRecords = Object.values(rewardRecordData);

  return Promise.resolve({
    me: {
      rewardsRecords: {
        edges: rewardRecords.map((rewardRecord) => ({
          node: rewardRecord,
        })),
        pageInfo: { endCursor: null, hasNextPage: false },
      },
    },
  });
};

export default getRewardRecords;
