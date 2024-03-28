import { Disclosure, DisclosureProps } from "@ariakit/react/disclosure";
import { StylableFC } from "@asl-19/react-dom-utils";
import { memo, useMemo } from "react";

import { ButtonProps } from "src/types/buttonTypes";
import getButtonCss from "src/utils/getButtonCss";

/**
 * Button-shaped button.
 */
const ButtonDisclosure: StylableFC<ButtonProps & DisclosureProps> = memo(
  ({
    IconComponent,
    className,
    disabled,
    iconCss,
    size = "medium",
    store,
    text,
    textCss,
    type,
    variant,
    ...otherProps
  }) => {
    const iconComponentCss = useMemo(() => [iconCss], [iconCss]);

    return (
      <Disclosure
        className={className}
        css={getButtonCss({ disabled, size, variant })}
        store={store}
        type={type}
        disabled={disabled}
        {...otherProps}
      >
        {IconComponent && <IconComponent aria-hidden css={iconComponentCss} />}
        <span css={textCss}>{text}</span>
      </Disclosure>
    );
  },
);

ButtonDisclosure.displayName = "ButtonButton";

export default ButtonDisclosure;
