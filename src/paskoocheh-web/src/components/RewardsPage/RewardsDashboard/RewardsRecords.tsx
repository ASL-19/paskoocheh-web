import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useCallback, useState } from "react";

import IndexPageLoadingUi from "src/components/IndexPageLoadingUi";
import RewardsRecordsListItem from "src/components/RewardsPage/RewardsDashboard/RewardsRecordsListItem";
import useAnnounceLoadingNewItemsComplete from "src/hooks/a11y/useAnnounceLoadingNewItemsComplete";
import { IndexPageLoadingState } from "src/hooks/useIndexPageLoadingAndQueryLogic";
import { useAppStrings } from "src/stores/appStore";
import {
  useRewardsDispatch,
  useRewardsInitialRewardRecordsHasNextPage,
  useRewardsRewardRecords,
} from "src/stores/rewardsStore";
import {
  dashboardItemContainer,
  dashboardItemTitle,
} from "src/styles/dashboardStyles";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import { rewardRecordsPerPage } from "src/values/indexPageValues";

const container = css(dashboardItemContainer, {
  justifyContent: "flex-start",
});
const recordContainer = css({
  width: "100%",
});

const RewardsRecords: StylableFC = memo(({ className }) => {
  const { RewardsPageContent: strings, shared: sharedStrings } =
    useAppStrings();
  const [currentOffset, setCurrentOffset] = useState(rewardRecordsPerPage);
  const rewardsDispatch = useRewardsDispatch();
  const announceLoadingNewItemsComplete = useAnnounceLoadingNewItemsComplete();
  const initialRewardRecordsHasNextPage =
    useRewardsInitialRewardRecordsHasNextPage();
  const rewardRecords = useRewardsRewardRecords();

  //DashboardTab - Records
  const [rewardRecordsLoadingState, setRewardRecordsLoadingState] =
    useState<IndexPageLoadingState>(
      rewardRecords.length === 0
        ? { type: "hasNone" }
        : initialRewardRecordsHasNextPage
          ? { type: "hasMore" }
          : { type: "hasNoMore" },
    );

  const loadMoreRewardRecords = useCallback(async () => {
    try {
      const graphQlSdk = await getGraphQlSdk();
      setRewardRecordsLoadingState({ type: "loadingMore" });

      const moreRewardRecordsResponse = await graphQlSdk.getRewardRecords({
        count: rewardRecordsPerPage,
        offset: currentOffset,
      });

      const moreRewardRecords = (
        moreRewardRecordsResponse.me?.rewardsRecords?.edges ?? []
      ).reduce(
        (acc, rewardRecords) =>
          rewardRecords.node ? [...acc, rewardRecords.node] : acc,
        [],
      );

      if (moreRewardRecordsResponse?.me?.rewardsRecords?.pageInfo.hasNextPage) {
        setRewardRecordsLoadingState({ type: "hasMore" });
      } else {
        setRewardRecordsLoadingState({ type: "hasNoMore" });
      }

      setCurrentOffset(currentOffset + rewardRecordsPerPage);

      if (moreRewardRecords.length > 0) {
        rewardsDispatch({
          rewardRecords: moreRewardRecords,
          type: "olderRewardRecordsLoaded",
        });

        announceLoadingNewItemsComplete({
          count: moreRewardRecords.length,
        });
      }
    } catch (error) {
      console.error(error);
      setRewardRecordsLoadingState({ type: "error" });
    }
  }, [announceLoadingNewItemsComplete, currentOffset, rewardsDispatch]);

  return (
    <div className={className} css={container}>
      <p css={dashboardItemTitle}>{strings.records}</p>
      {!["error", "hasNone", "loadingNew"].includes(
        rewardRecordsLoadingState.type,
      ) && (
        <ul css={recordContainer}>
          {rewardRecords.map((record) => (
            <RewardsRecordsListItem key={record.id} record={record} />
          ))}
        </ul>
      )}
      <IndexPageLoadingUi
        loadMoreLinkText={sharedStrings.button.more}
        loadingState={rewardRecordsLoadingState}
        onClick={loadMoreRewardRecords}
        buttonType="button"
      />
    </div>
  );
});

RewardsRecords.displayName = "RewardsRecords";

export default RewardsRecords;
