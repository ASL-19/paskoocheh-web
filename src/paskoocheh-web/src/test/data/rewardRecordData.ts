import { asType } from "@asl-19/js-utils";

import { GqlRewardRecord } from "src/generated/graphQl";

const rewardRecordData = {
  rewardRecord1: asType<GqlRewardRecord>({
    date: "2020-09-30T10:40:16.997604+00:00",
    description: "quiz",
    id: "1",
    points: 3,
    recordType: "REDEEMED",
  }),
  rewardRecord2: asType<GqlRewardRecord>({
    date: "2020-09-30T10:40:16.997604+00:00",
    description: "referral",
    id: "2",
    points: 2,
    recordType: "EARNED",
  }),
};

export default rewardRecordData;
