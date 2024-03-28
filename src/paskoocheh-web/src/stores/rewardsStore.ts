import constate from "constate";
import { useReducer } from "react";
import { match } from "ts-pattern";

import {
  GqlGetUserPurchasedApps,
  GqlQuizPage,
  GqlRedemptionMethod,
  GqlRewardRecord,
} from "src/generated/graphQl";
import { ValidVersionPreview } from "src/types/appTypes";
import reducerLog from "src/utils/store/reducerLog";

export type RewardsState = {
  initialRewardRecordsHasNextPage: boolean;
  pointsBalance: number;
  purchasedVersionPreviews: Array<ValidVersionPreview>;
  quizCompletedEarningPoints: number;
  quizPage: GqlQuizPage | null;
  quizWonEarningPoints: number;
  redemptionMethods: Array<GqlRedemptionMethod>;
  reviewedVersionPreviews: Array<ValidVersionPreview>;
  rewardRecords: Array<GqlRewardRecord>;
  userPinCode: number;
};

type RewardsAction =
  | {
      rewardRecords: Array<GqlRewardRecord>;
      type: "olderRewardRecordsLoaded";
    }
  | {
      pointsBalance: number;
      rewardRecords: Array<GqlRewardRecord>;
      type: "newRewardRecordLoaded";
    }
  | {
      purchasedVersionPreviews: GqlGetUserPurchasedApps;
      type: "purchasedVersionPreviewsLoaded";
    }
  | {
      reviewedVersionPreviews: GqlGetUserPurchasedApps;
      type: "reviewedVersionPreviewsLoaded";
    };

function reducer(state: RewardsState, action: RewardsAction) {
  const newState: RewardsState = match(action)
    // Note: Not tested yet — revisit once we have the backend hooked up!
    .with({ type: "olderRewardRecordsLoaded" }, (action) => ({
      ...state,
      rewardRecords: [
        ...state.rewardRecords,
        ...action.rewardRecords.filter(
          (rewardRecord) =>
            !state.rewardRecords.some(
              (existingRewardRecord) =>
                rewardRecord.id === existingRewardRecord.id,
            ),
        ),
      ],
    }))
    .with({ type: "newRewardRecordLoaded" }, (action) => ({
      ...state,
      pointsBalance: action.pointsBalance ?? state.pointsBalance,
      rewardRecords: action.rewardRecords,
    }))
    .with({ type: "purchasedVersionPreviewsLoaded" }, () => ({
      ...state,
      purchasedVersionPreviews: state.purchasedVersionPreviews,
    }))
    .with({ type: "reviewedVersionPreviewsLoaded" }, () => ({
      ...state,
      reviewedVersionPreviews: state.reviewedVersionPreviews,
    }))
    .exhaustive();

  reducerLog({
    action,
    newState,
    state,
    storeName: "Rewards",
  });

  return newState;
}
const useRewards = ({ initialState }: { initialState: RewardsState }) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  return { dispatch, state };
};

export const [
  RewardsProvider,
  useRewardsDispatch,
  useRewardsInitialRewardRecordsHasNextPage,
  useRewardsPointsBalance,
  useRewardsPurchasedVersionPreviews,
  useRewardsQuizCompletedEarningPoints,
  useRewardsQuizPage,
  useRewardsQuizWonEarningPoints,
  useRewardsRedemptionMethods,
  useRewardsReviewedVersionPreviews,
  useRewardsRewardRecords,
  useRewardsUserPinCode,
] = constate(
  useRewards,
  (value) => value.dispatch,
  (value) => value.state.initialRewardRecordsHasNextPage,
  (value) => value.state.pointsBalance,
  (value) => value.state.purchasedVersionPreviews,
  (value) => value.state.quizCompletedEarningPoints,
  (value) => value.state.quizPage,
  (value) => value.state.quizWonEarningPoints,
  (value) => value.state.redemptionMethods,
  (value) => value.state.reviewedVersionPreviews,
  (value) => value.state.rewardRecords,
  (value) => value.state.userPinCode,
);
