import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import ChevronSvg from "src/components/icons/general/ChevronSvg";
import colors from "src/values/colors";

const dropdownChevronSvg = css({
  fill: colors.secondary500,
  height: "0.75rem",
  width: "0.75rem",
});

const DropdownChevronSvg: StylableFC = memo(() => (
  <ChevronSvg css={dropdownChevronSvg} direction="down" />
));

DropdownChevronSvg.displayName = "DropdownChevronSvg";

export default DropdownChevronSvg;
