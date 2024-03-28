import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Image, { StaticImageData } from "next/image";
import { memo } from "react";

import {
  dashboardItemDescription,
  dashboardItemTitle,
} from "src/styles/dashboardStyles";
import colors from "src/values/colors";

export type HowPointsWorkListItemInfoText = {
  description: string;
  heading: string;
};

export type HowPointsWorkListItemInfo = HowPointsWorkListItemInfoText & {
  image: StaticImageData;
};

const container = css({
  display: "flex",
  gap: "1rem",
});
const svg = css({
  borderRadius: "100%",
  height: "4rem",
  minWidth: "4rem",
  width: "4rem",
});
const nameAndDescription = css({
  display: "flex",
  flexDirection: "column",
  gap: "1rem",
});
const description = css(dashboardItemDescription, {
  color: colors.secondary300,
});
const HowPointsWorkListItem: StylableFC<{
  item: HowPointsWorkListItemInfo;
}> = memo(({ className, item }) => (
  <div className={className} css={container}>
    <Image alt="" src={item.image} css={svg} width="100" height="100" />

    <div css={nameAndDescription}>
      <h3 css={dashboardItemTitle}>{item.heading}</h3>
      <p css={description}>{item.description}</p>
    </div>
  </div>
));

HowPointsWorkListItem.displayName = "HowPointsWorkListItem";

export default HowPointsWorkListItem;
