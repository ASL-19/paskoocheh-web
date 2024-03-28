import { SelectItem, SelectPopover, SelectStore } from "@ariakit/react/select";
import { FC, memo } from "react";

import { dropdownMenu, dropdownMenuItem } from "src/styles/dropdownStyles";
import { InstallationOption } from "src/types/miscTypes";
import { dropdownGutterPx } from "src/values/layoutValues";

const AppInstallSelectPopover: FC<{
  installationOptions: Array<InstallationOption>;
  selectStore: SelectStore;
}> = memo(({ installationOptions, selectStore }) => (
  <SelectPopover
    css={dropdownMenu}
    gutter={dropdownGutterPx}
    sameWidth
    store={selectStore}
  >
    {installationOptions.map((option) => (
      <SelectItem
        css={dropdownMenuItem}
        key={option.downloadUrl}
        value={option.downloadUrl}
      >
        {option.name}
      </SelectItem>
    ))}
  </SelectPopover>
));

AppInstallSelectPopover.displayName = "AppInstallSelectPopover";

export default AppInstallSelectPopover;
