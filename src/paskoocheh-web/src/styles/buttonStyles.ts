import { hoverStyles } from "@asl-19/emotion-utils";
import { css } from "@emotion/react";

import { paragraphP1SemiBold } from "src/styles/typeStyles";
import { ButtonSize } from "src/types/buttonTypes";
import colors from "src/values/colors";
import { buttonHeights } from "src/values/layoutValues";

const button = ({
  disabled,
  size,
}: {
  disabled?: boolean;
  size: ButtonSize;
}) => {
  const buttonHeight = buttonHeights[size];

  return css(
    paragraphP1SemiBold,
    {
      borderRadius: "6.25rem",
      borderStyle: "solid",
      borderWidth: "1px",
      columnGap: "0.5rem",
      display: "flex",
      flex: "0 0 auto",
      flexDirection: "row",
      height: buttonHeight,
      justifyContent: "center",
      lineHeight: `calc(${buttonHeight} - 2px)`,
      overflow: "hidden",
      padding: "0 1rem",
      textAlign: "center",
      textOverflow: "ellipsis",
      transitionDuration: "0.3s",
      transitionProperty: "background-color, border-color",
      whiteSpace: "nowrap",
      width: "max-content",
    },
    disabled && {
      "html.js &": {
        cursor: "not-allowed",
      },
    },
  );
};

export const buttonPrimary = ({
  disabled,
  size,
}: {
  disabled?: boolean;
  size: ButtonSize;
}) =>
  css(
    button({ disabled, size }),
    {
      backgroundColor: disabled ? colors.grey : colors.primary500,
      borderColor: disabled ? colors.grey : colors.primary500,
      color: disabled ? colors.black : colors.shadesWhite,
    },
    hoverStyles({
      backgroundColor: disabled ? colors.grey : colors.primary400,
      borderColor: disabled ? colors.grey : colors.primary400,
    }),
  );

export const buttonSecondary = ({
  disabled,
  size,
}: {
  disabled?: boolean;
  size: ButtonSize;
}) =>
  css(button({ disabled, size }), {
    backgroundColor: disabled ? colors.neutral200 : "transparent",
    borderColor: disabled ? colors.neutral500 : colors.primary500,
    color: disabled ? colors.neutral500 : colors.primary500,
  });

export const buttonIcon = css({
  alignSelf: "center",
  flex: "0 0 auto",
  height: "1.25rem",
});
