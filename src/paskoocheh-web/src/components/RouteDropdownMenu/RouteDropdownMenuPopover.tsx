import { Menu, MenuStore } from "@ariakit/react/menu";
import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

import MenuItemLink from "src/components/MenuItemLink";
import { dropdownMenu, dropdownMenuItem } from "src/styles/dropdownStyles";
import { RouteInfo } from "src/types/miscTypes";
import { dropdownGutterPx } from "src/values/layoutValues";

export type ProjectTypeMenuOption = {
  id: string;
  route: string;
  title: string;
};

const RouteDropdownMenuPopover: StylableFC<{
  menuStore: MenuStore;
  routeInfos: Array<RouteInfo>;
}> = memo(({ menuStore, routeInfos }) => (
  <Menu
    css={dropdownMenu}
    gutter={dropdownGutterPx}
    sameWidth
    store={menuStore}
  >
    {routeInfos.map((routeInfo) => (
      <MenuItemLink
        content={routeInfo.name}
        href={routeInfo.route}
        css={dropdownMenuItem}
        key={routeInfo.key}
      />
    ))}
  </Menu>
));

RouteDropdownMenuPopover.displayName = "RouteDropdownMenuPopover";

export default RouteDropdownMenuPopover;
