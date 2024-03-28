import { StylableFC } from "@asl-19/react-dom-utils";
import { ButtonHTMLAttributes, memo, MouseEventHandler, useMemo } from "react";

import { buttonIcon } from "src/styles/buttonStyles";
import { ButtonProps } from "src/types/buttonTypes";
import getButtonCss from "src/utils/getButtonCss";

/**
 * Button-shaped button.
 */
const ButtonButton: StylableFC<
  ButtonProps & {
    disabled?: boolean;
    onClick?: MouseEventHandler<HTMLButtonElement>;
    type?: ButtonHTMLAttributes<HTMLButtonElement>["type"];
  }
> = memo(
  ({
    IconComponent,
    className,
    disabled,
    iconCss,
    onClick,
    size = "medium",
    text,
    textCss,
    type,
    variant,
    ...otherProps
  }) => {
    const iconComponentCss = useMemo(() => [buttonIcon, iconCss], [iconCss]);

    return (
      <button
        className={className}
        css={getButtonCss({ disabled, size, variant })}
        disabled={disabled}
        onClick={onClick}
        type={type}
        {...otherProps}
      >
        {IconComponent && <IconComponent aria-hidden css={iconComponentCss} />}

        <span css={textCss}>{text}</span>
      </button>
    );
  },
);

ButtonButton.displayName = "ButtonButton";

export default ButtonButton;
