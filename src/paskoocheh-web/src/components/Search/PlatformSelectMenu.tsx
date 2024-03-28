import { Menu, MenuStore } from "@ariakit/react/menu";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import { PlatformSelectGroupInfo } from "src/components/Search/PlatformSelect";
import PlatformSelectMenuGroup from "src/components/Search/PlatformSelectMenuGroup";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

const dropdownContainer = css(
  {
    backgroundColor: colors.shadesWhite,
    border: `1px solid ${colors.neutral100}`,
    borderRadius: "0.5rem",
    boxShadow: "0px 12px 24px rgba(0, 0, 0, 0.1)",
    display: "flex",
    gap: "1.5rem",

    // width: "33rem",
    maxHeight: "var(--popover-available-height)",

    overflowY: "auto",
    // inset: 0,
    padding: "1.25rem 1.5rem",
    // position: "absolute",
    zIndex: 100,
  },
  breakpointStyles({
    singleColumn: {
      gte: {
        width: "33rem",
      },
      lt: {
        flexDirection: "column",
        width: "10rem",
      },
    },
  }),
);

const searchSelectList = css({
  // Flex-basis is 0 so the SearchSelectList items have grow at the same ratio
  // (regardless of content)
  flex: "1 1 0",
});

const PlatformSelectMenu: StylableFC<{
  groupInfos: Array<PlatformSelectGroupInfo>;
  menuStore: MenuStore;
}> = memo(({ groupInfos, menuStore, ...remainingProps }) => (
  <Menu
    css={dropdownContainer}
    store={menuStore}
    gutter={16}
    fitViewport
    {...remainingProps}
  >
    {groupInfos.map((groupInfo) => (
      <PlatformSelectMenuGroup
        css={searchSelectList}
        heading={groupInfo.heading}
        key={groupInfo.heading}
        platforms={groupInfo.platforms || null}
      />
    ))}
  </Menu>
));

PlatformSelectMenu.displayName = "PlatformSelectMenu";

export default PlatformSelectMenu;
