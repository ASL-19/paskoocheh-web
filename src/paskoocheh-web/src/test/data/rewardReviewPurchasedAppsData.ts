import { asType } from "@asl-19/js-utils";

import { GqlGetUserPurchasedApps } from "src/generated/graphQl";
import platformTestDataBySlug from "src/test/data/platformTestDataBySlug";
import toolPreviewTestDataBySlug from "src/test/data/toolPreviewTestDataBySlug";

const rewardReviewPurchasedAppsData = {
  node: asType<GqlGetUserPurchasedApps>({
    me: {
      purchasedApps: [
        {
          // cSpell:disable
          averageRating: {
            ratingCount: 5,
            starRating: 0,
          },
          downloadCount: 3998,
          id: "VmVyc2lvbk5vZGU6Mzgz",
          pk: 383,
          platform: platformTestDataBySlug["android"],
          tool: toolPreviewTestDataBySlug["beepass-vpn"],
          // cSpell:enable
        },
      ],
    },
  }),
};

export default rewardReviewPurchasedAppsData;
