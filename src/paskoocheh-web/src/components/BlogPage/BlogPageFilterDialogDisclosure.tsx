import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import DropdownChevronSvg from "src/components/DropdownChevronSvg";
import {
  dropdownButtonWhitePill,
  dropdownLabelText,
} from "src/styles/dropdownStyles";

const dropdownButton = css(dropdownButtonWhitePill, {
  width: "11.25rem",
});

const BlogPageFilterDialogDisclosure: StylableFC<{
  label: string;
}> = memo(({ label, ...props }) => (
  <div css={dropdownButton} {...props}>
    <span css={dropdownLabelText}>{label}</span>

    <DropdownChevronSvg />
  </div>
));

BlogPageFilterDialogDisclosure.displayName = "BlogPageFilterDialogDisclosure";

export default BlogPageFilterDialogDisclosure;
