import { hoverStyles } from "@asl-19/emotion-utils";
import { css } from "@emotion/react";

import { captionRegular, paragraphP1Regular } from "src/styles/typeStyles";
import {
  headingH5SmallSemiBold,
  paragraphP2SemiBold,
} from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";
import { buttonHeights } from "src/values/layoutValues";

export const formButton = css(
  { minWidth: "13.25rem" },
  breakpointStyles({
    singleColumn: {
      lt: {
        width: "100%",
      },
    },
  }),
);

export const formContainer = css(
  {
    alignItems: "center",
    backgroundColor: colors.primary50,
    borderRadius: "0.5rem",
    display: "flex",
    flexDirection: "column",
    padding: "1.25rem",
    rowGap: "1.25rem",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        backgroundColor: "transparent",
        padding: "0",
      },
    },
  }),
);

/**
 * Form heading that becomes smaller (paragraphP2SemiBold) at < singleColumn.
 *
 * Used in contact forms.
 */
export const formHeadingSmall = css(
  headingH5SmallSemiBold,
  breakpointStyles({
    singleColumn: {
      lt: paragraphP2SemiBold,
    },
  }),
);

/**
 * Form heading that stays the same size at all viewport widths.
 *
 * Used in auth forms.
 */
export const formHeading = css(headingH5SmallSemiBold);

export const formInputAndLabelContainer = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "0.25rem",
});

export const inputGroup = css({ width: "100%" });

export const formInput = ({ disabled = false }: { disabled?: boolean }) =>
  css(
    paragraphP1Regular,
    {
      backgroundColor: colors.shadesWhite,
      border: `1px solid ${colors.neutral500}`,
      borderRadius: "0.25rem",
      color: colors.secondary500,
      height: buttonHeights.medium,
      lineHeight: buttonHeights.medium,
      textIndent: "1rem",
      width: "100%",
    },
    disabled && {
      "html.js &": {
        backgroundColor: colors.neutral50,
        borderColor: colors.neutral200,
        color: colors.neutral400,
        cursor: "not-allowed",
      },
    },
    {
      ":focus": {
        borderColor: colors.primary500,
      },
    },
  );

export const formLabel = css(paragraphP1Regular, {
  color: colors.neutral700,
});

export const formConfirmationMessage = css(paragraphP1Regular);

export const formDescription = css(captionRegular);

export const formDescriptionLink = css(
  captionRegular,
  {
    color: colors.primary500,
  },
  hoverStyles({
    textDecoration: "underline",
  }),
);
