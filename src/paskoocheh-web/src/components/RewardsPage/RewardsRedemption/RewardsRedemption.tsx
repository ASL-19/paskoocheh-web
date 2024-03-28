import { gridContainer } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import RewardsRedemptionListItem from "src/components/RewardsPage/RewardsRedemption/RewardsRedemptionListItem";
import { useRewardsRedemptionMethods } from "src/stores/rewardsStore";
import { breakpointStyles } from "src/utils/media/media";

const container = gridContainer({ columns: 2, gap: "1.25rem" });

const item = css(
  breakpointStyles({
    desktopNarrow: {
      lt: {
        gridColumn: "span 2",
      },
    },
  }),
);

const RewardsRedemption: StylableFC<{}> = memo(({ ...remainingProps }) => {
  const redemptionMethods = useRewardsRedemptionMethods();

  return (
    <div {...remainingProps}>
      <div css={container}>
        {redemptionMethods.map((redemption) => (
          <RewardsRedemptionListItem
            css={item}
            key={redemption.id}
            redemption={redemption}
          />
        ))}
      </div>
    </div>
  );
});

RewardsRedemption.displayName = "RewardsRedemption";

export default RewardsRedemption;
