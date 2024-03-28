import { MenuButton, MenuStore } from "@ariakit/react/menu";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import DropdownChevronSvg from "src/components/DropdownChevronSvg";
import {
  dropdownButtonGreyRect,
  dropdownLabelText,
} from "src/styles/dropdownStyles";

const dropdownButton = css(dropdownButtonGreyRect, {
  width: "11.25rem",
});

const RouteDropdownMenuDisclosure: StylableFC<{
  label: string;
  menuStore: MenuStore;
}> = memo(({ label, menuStore }) => (
  <MenuButton css={dropdownButton} store={menuStore} aria-label={label}>
    <span css={dropdownLabelText}>{label}</span>

    <DropdownChevronSvg />
  </MenuButton>
));

RouteDropdownMenuDisclosure.displayName = "RouteDropdownMenuDisclosure";

export default RouteDropdownMenuDisclosure;
