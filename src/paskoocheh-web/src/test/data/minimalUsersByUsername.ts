import { asType } from "@asl-19/js-utils";

import { GqlMinimalUser } from "src/generated/graphQl";
import rewardRecordData from "src/test/data/rewardRecordData";

const minimalUsersByUsername = {
  mockuser: asType<GqlMinimalUser>({
    email: "mockuser@paskoocheh.com",
    id: "1",
    pin: 111111,
    pointsBalance: 50,
    referralSlug: "referral",
    rewardsRecords: {
      edges: [
        {
          node: rewardRecordData.rewardRecord1,
        },
      ],
      pageInfo: {
        hasNextPage: false,
      },
    },
    username: "mockuser",
  }),
};

export default minimalUsersByUsername;
