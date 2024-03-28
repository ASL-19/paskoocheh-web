import { useMemo } from "react";

import { HowPointsWorkListItemInfo } from "src/components/RewardsPage/HowPointsWork/HowPointsWorkListItem";
import earnPointsPng from "src/static/images/earnPointsPng.png";
import redeemPointsPng from "src/static/images/redeemPoints.png";
import { useAppStrings } from "src/stores/appStore";

const useHowPointsWorkListItemInfos = () => {
  const strings = useAppStrings();

  const earnPointsListItemInfos = useMemo<Array<HowPointsWorkListItemInfo>>(
    () => [
      {
        ...strings.HowPointsWorkPage.lists.earnPoints.items.rateAndReviewApps,
        image: earnPointsPng,
      },
      {
        ...strings.HowPointsWorkPage.lists.earnPoints.items.weeklyChallenge,
        image: earnPointsPng,
      },
      {
        ...strings.HowPointsWorkPage.lists.earnPoints.items.updateApps,
        image: earnPointsPng,
      },
      {
        ...strings.HowPointsWorkPage.lists.earnPoints.items.referFriends,
        image: earnPointsPng,
      },
    ],
    [strings],
  );

  const redeemPointsListItemInfos = useMemo<Array<HowPointsWorkListItemInfo>>(
    () => [
      {
        ...strings.HowPointsWorkPage.lists.redeemPoints.items.redeemPaidVpnApps,
        image: redeemPointsPng,
      },
    ],
    [strings],
  );

  return {
    earnPointsListItemInfos,
    redeemPointsListItemInfos,
  };
};

export default useHowPointsWorkListItemInfos;
