import { StylableFC } from "@asl-19/react-dom-utils";
import { memo, MouseEventHandler } from "react";

import HowPointsWork from "src/components/RewardsPage/HowPointsWork";
import PointsBalance from "src/components/RewardsPage/PointsBalance";
import { dashboardGridContainer } from "src/styles/dashboardStyles";
import { Media } from "src/utils/media/media";

const RewardsPointsSection: StylableFC<{
  onRedemptionLinkClick: MouseEventHandler;
}> = memo(({ onRedemptionLinkClick, ...remainingProps }) => (
  <div css={dashboardGridContainer} {...remainingProps}>
    <PointsBalance onRedemptionLinkClick={onRedemptionLinkClick} />

    <Media greaterThanOrEqual="singleColumn">
      <HowPointsWork />
    </Media>
  </div>
));

RewardsPointsSection.displayName = "RewardsPointsSection";

export default RewardsPointsSection;
