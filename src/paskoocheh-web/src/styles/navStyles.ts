import { css } from "@emotion/react";

import { paragraphP1Regular } from "src/styles/typeStyles";

export const navTopLevelItem = css(paragraphP1Regular, {
  alignItems: "center",
  display: "flex",
  height: "2.5rem",
  justifyContent: "center",
  lineHeight: "2.5rem",
  textOverflow: "ellipsis",
  whiteSpace: "nowrap",
});

export const navMenuText = css(paragraphP1Regular, {
  lineHeight: "2rem",
  textOverflow: "ellipsis",
  whiteSpace: "nowrap",
});
