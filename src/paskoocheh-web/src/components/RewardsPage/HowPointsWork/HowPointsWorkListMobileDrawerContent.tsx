import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import useHowPointsWorkListItemInfos from "src/hooks/useHowPointsWorkListItemInfos";
import { useAppStrings } from "src/stores/appStore";
import { dashboardItemDescription } from "src/styles/dashboardStyles";
import { paragraphP1SemiBold } from "src/styles/typeStyles";

const container = css({
  display: "flex",
  flexDirection: "column",
  gap: "1rem",
});
const listContainer = css({
  display: "flex",
  flexDirection: "column",
  gap: "0.75rem",
});

const HowPointsWorkListMobileDrawerContent: StylableFC = memo((props) => {
  const strings = useAppStrings();

  const { earnPointsListItemInfos, redeemPointsListItemInfos } =
    useHowPointsWorkListItemInfos();

  return (
    <div css={container} {...props}>
      <h3 css={paragraphP1SemiBold}>
        {strings.HowPointsWorkPage.lists.earnPoints.heading}
      </h3>

      <ul css={listContainer}>
        {earnPointsListItemInfos.map((item, index) => (
          <li css={dashboardItemDescription} key={index}>
            {item.description}
          </li>
        ))}
      </ul>

      <h3 css={paragraphP1SemiBold}>
        {strings.HowPointsWorkPage.lists.redeemPoints.heading}
      </h3>

      <ul css={listContainer}>
        {redeemPointsListItemInfos.map((item, index) => (
          <li css={dashboardItemDescription} key={index}>
            {item.description}
          </li>
        ))}
      </ul>
    </div>
  );
});

HowPointsWorkListMobileDrawerContent.displayName =
  "HowPointsWorkListMobileDrawerContent";

export default HowPointsWorkListMobileDrawerContent;
