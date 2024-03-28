import { StylableFC } from "@asl-19/react-dom-utils";
import { SerializedStyles } from "@emotion/react";

export type ButtonSize = "small" | "medium" | "large";

export type ButtonVariant = "primary" | "secondary";

export type ButtonProps = {
  IconComponent?: StylableFC;

  /**
   * This CSS is applied to the icon.
   *
   * This can be used to customize the fill color or rotation, for example.
   */
  iconCss?: SerializedStyles;
  iconPosition?: "start" | "end";
  size?: ButtonSize;
  text: string;
  textCss?: SerializedStyles;
  variant: ButtonVariant;
};
