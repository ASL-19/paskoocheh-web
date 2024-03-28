import { Select, SelectStore } from "@ariakit/react/select";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import DropdownChevronSvg from "src/components/DropdownChevronSvg";
import { useAppStrings } from "src/stores/appStore";
import { dropdownButtonWhiteRect } from "src/styles/dropdownStyles";

const select = css(dropdownButtonWhiteRect, {
  maxWidth: "17.5rem",
  width: "100%",
});

const AppInstallSelect: StylableFC<{
  label: string;
  selectStore: SelectStore;
}> = memo(({ className, label, selectStore }) => {
  const strings = useAppStrings();

  return (
    <Select
      className={className}
      css={select}
      store={selectStore}
      title={strings.AppOverviewSection.availableOptions}
    >
      {label}

      <DropdownChevronSvg />
    </Select>
  );
});

AppInstallSelect.displayName = "AppInstallSelect";

export default AppInstallSelect;
