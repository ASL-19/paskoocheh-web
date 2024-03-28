import { asType } from "@asl-19/js-utils";

import { GqlRedemptionMethod } from "src/generated/graphQl";

const redemptionMethodsData = {
  rewardRecord1: asType<GqlRedemptionMethod>({
    id: "1",
    pk: 1,
    redemptionMethodEn: "Download App 1",
    redemptionMethodFa: "Download App 1",
    redemptionPoints: 20,
  }),
  rewardRecord2: asType<GqlRedemptionMethod>({
    id: "2",
    pk: 2,
    redemptionMethodEn: "Download App 2",
    redemptionMethodFa: "Download App 2",
    redemptionPoints: 10,
  }),
};

export default redemptionMethodsData;
