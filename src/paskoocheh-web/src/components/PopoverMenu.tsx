import { Menu, MenuStore } from "@ariakit/react/menu";
import { FC, memo } from "react";

import PopoverMenuItem, { MenuItemInfo } from "src/components/PopoverMenuItem";
import { dropdownMenu } from "src/styles/dropdownStyles";
import { dropdownGutterPx } from "src/values/layoutValues";

const PopoverMenu: FC<{
  menuItemInfos: Array<MenuItemInfo>;
  menuStore: MenuStore;
}> = memo(({ menuItemInfos, menuStore }) => (
  <Menu css={dropdownMenu} gutter={dropdownGutterPx} store={menuStore}>
    {menuItemInfos.map((menuItemInfo, index) => (
      <PopoverMenuItem menuItemInfo={menuItemInfo} key={index} />
    ))}
  </Menu>
));

PopoverMenu.displayName = "PopoverMenu";

export default PopoverMenu;
