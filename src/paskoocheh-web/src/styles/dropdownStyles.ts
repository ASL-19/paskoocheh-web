import { hoverStyles } from "@asl-19/emotion-utils";
import { css } from "@emotion/react";

import { paragraphP1Regular } from "src/styles/typeStyles";
import colors from "src/values/colors";
import zIndexes from "src/values/zIndexes";

const dropdownButton = css(paragraphP1Regular, {
  alignItems: "center",
  borderStyle: "solid",
  borderWidth: "1px",
  columnGap: "0.5rem",
  display: "flex",
  flexDirection: "row",
  height: "2rem",
  justifyContent: "space-between",
  padding: "0.5rem 1rem",
});

export const dropdownButtonGreyRect = css(dropdownButton, {
  backgroundColor: colors.neutral50,
  borderColor: colors.neutral200,
  borderRadius: "0.5rem",
});

export const dropdownButtonWhiteRect = css(dropdownButton, {
  backgroundColor: colors.shadesWhite,
  borderColor: colors.neutral400,
  borderRadius: "0.25rem",
});

export const dropdownButtonWhitePill = css(dropdownButton, {
  backgroundColor: colors.shadesWhite,
  borderColor: colors.secondary100,
  borderRadius: "1rem",
});

export const dropdownMenu = css({
  backgroundColor: colors.shadesWhite,
  borderRadius: "0.5rem",
  boxShadow: "0px 12px 24px rgba(0, 0, 0, 0.1)",
  padding: "1rem 0.5rem",
  position: "relative",
  zIndex: zIndexes.InstallOptionsDropdownMenu_item,
});

export const dropdownLabelText = css({
  overflow: "hidden",
  textOverflow: "ellipsis",
  whiteSpace: "nowrap",
});

const dropdownActiveItemBackground = css({
  backgroundColor: colors.secondary50,
});

export const dropdownBackgroundWhenActiveItem = css({
  "&[data-active-item]": dropdownActiveItemBackground,
});

export const dropdownMenuItem = css(
  paragraphP1Regular,
  dropdownBackgroundWhenActiveItem,
  {
    alignItems: "center",
    color: colors.secondary400,
    cursor: "pointer",
    display: "flex",
    height: "2.25rem",
    justifyContent: "space-between",
    lineHeight: "2.25rem",
    paddingInline: "0.5rem",
    whiteSpace: "nowrap",
    width: "100%",
  },
  hoverStyles({
    backgroundColor: colors.secondary50,
  }),
);
