import { useMenuStore } from "@ariakit/react/menu";
import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

import RouteDropdownMenuDisclosure from "src/components/RouteDropdownMenu/RouteDropdownMenuDisclosure";
import RouteDropdownMenuPopover from "src/components/RouteDropdownMenu/RouteDropdownMenuPopover";
import { RouteInfo } from "src/types/miscTypes";

/**
 * Dropdown menu that renders a list of route links.
 */
const RouteDropdownMenu: StylableFC<{
  label: string;
  routeInfos: Array<RouteInfo>;
}> = memo(({ label, routeInfos }) => {
  const menuStore = useMenuStore();
  const menuIsMounted = menuStore.useState("mounted");

  return (
    <>
      <RouteDropdownMenuDisclosure menuStore={menuStore} label={label} />

      {menuIsMounted && (
        <RouteDropdownMenuPopover
          menuStore={menuStore}
          routeInfos={routeInfos}
        />
      )}
    </>
  );
});

RouteDropdownMenu.displayName = "RouteDropdownMenu";

export default RouteDropdownMenu;
