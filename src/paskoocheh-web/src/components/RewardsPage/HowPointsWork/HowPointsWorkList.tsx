import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import HowPointsWorkListItem, {
  HowPointsWorkListItemInfo,
} from "src/components/RewardsPage/HowPointsWork/HowPointsWorkListItem";
import {
  dashboardItemContainer,
  dashboardItemTitle,
} from "src/styles/dashboardStyles";
import { breakpointStyles } from "src/utils/media/media";

const container = css(
  {
    gridColumn: "span 6",
  },
  breakpointStyles({
    desktopNarrow: {
      lt: { gridColumn: "span 12" },
    },
  }),
);

const listContainer = css(dashboardItemContainer, {
  alignItems: "start",
  justifyContent: "start",
});

const HowPointsWorkList: StylableFC<{
  label: string;
  list: Array<HowPointsWorkListItemInfo>;
}> = memo(({ className, label, list }) => (
  <div className={className} css={container}>
    <div css={listContainer}>
      <h2 css={dashboardItemTitle}>{label}</h2>
      {list.map((item, index) => (
        <HowPointsWorkListItem key={index} item={item} />
      ))}
    </div>
  </div>
));

HowPointsWorkList.displayName = "HowPointsWorkList";

export default HowPointsWorkList;
