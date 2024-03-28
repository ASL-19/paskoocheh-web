import { StylableFC } from "@asl-19/react-dom-utils";
import Link from "next/link";
import { memo, useMemo } from "react";

import { buttonIcon } from "src/styles/buttonStyles";
import { ButtonProps } from "src/types/buttonTypes";
import getButtonCss from "src/utils/getButtonCss";

/**
 * Button-shaped link.
 */
const ButtonLink: StylableFC<
  ButtonProps & {
    href: string;
    replace?: boolean;
    scroll?: boolean;
    shallow?: boolean;
    type?: string;
  }
> = memo(
  ({
    IconComponent,
    className,
    href,
    iconCss,
    replace,
    scroll,
    shallow,
    size = "medium",
    text,
    textCss,
    type,
    variant,
    ...otherProps
  }) => {
    const iconComponentCss = useMemo(() => [buttonIcon, iconCss], [iconCss]);

    return (
      <Link
        href={href}
        replace={replace}
        shallow={shallow}
        className={className}
        css={getButtonCss({ size, variant })}
        type={type}
        scroll={scroll}
        {...otherProps}
      >
        <span css={textCss}>{text}</span>
        {IconComponent && <IconComponent aria-hidden css={iconComponentCss} />}
      </Link>
    );
  },
);

ButtonLink.displayName = "ButtonLink";

export default ButtonLink;
