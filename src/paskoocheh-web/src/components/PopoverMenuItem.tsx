import { MenuItem } from "@ariakit/react/menu";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { FC, memo } from "react";
import { match, P } from "ts-pattern";

import MenuItemLink from "src/components/MenuItemLink";
import { dropdownMenuItem } from "src/styles/dropdownStyles";

export type MenuItemInfo = {
  IconComponent?: FC<{ className?: string }>;
  text: string;
} & (
  | {
      href?: never;
      onClick: () => void;
    }
  | {
      href: string;
      onClick?: never;
    }
);
const icon = css({
  height: "0.875rem",
});

const PopoverMenuItem: StylableFC<{
  menuItemInfo: MenuItemInfo;
}> = memo(({ menuItemInfo, ...remainingProps }) => {
  const IconComponent = menuItemInfo.IconComponent;

  const content = (
    <>
      {menuItemInfo.text}
      {IconComponent && <IconComponent css={icon} />}
    </>
  );

  return match(menuItemInfo)
    .with({ href: P.string }, (menuItemInfo) => (
      <MenuItemLink
        href={menuItemInfo.href}
        key={menuItemInfo.text}
        content={content}
        css={dropdownMenuItem}
      />
    ))
    .with({ onClick: P.not(undefined) }, (menuItemInfo) => (
      <MenuItem
        css={dropdownMenuItem}
        onClick={menuItemInfo.onClick}
        {...remainingProps}
      >
        {content}
      </MenuItem>
    ))
    .exhaustive();
});

PopoverMenuItem.displayName = "PopoverMenuItem";

export default PopoverMenuItem;
