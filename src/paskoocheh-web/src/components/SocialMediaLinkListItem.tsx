import { hoverStyles } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { FC, memo, MouseEventHandler } from "react";

export type SocialMediaListItemStyleProps = {
  itemHoverIconColor?: string;
  itemIconColor: string;
  /**
   * Item size (as
   * {@link https://developer.mozilla.org/en-US/docs/Web/CSS/length| CSS length})
   */
  itemSize: string;
};

const link = ({
  itemHoverIconColor,
  itemIconColor,
}: {
  itemHoverIconColor?: string;
  itemIconColor: string;
}) =>
  css(
    hoverStyles({
      color: itemHoverIconColor ?? itemIconColor,
    }),
    {
      alignItems: "center",
      color: itemIconColor,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
    },
  );

const svgIcon = ({ itemSize }: { itemSize: string }) =>
  css({
    height: itemSize,
    width: itemSize,
  });

const SocialMediaLinkListItem: StylableFC<
  SocialMediaListItemStyleProps & {
    IconComponent: FC<{ className?: string }>;
    iconAriaLabel: string;
  } & (
      | {
          href: string;
          onClick?: MouseEventHandler;
        }
      | {
          href?: never;
          onClick: MouseEventHandler;
        }
    )
> = memo(
  ({
    IconComponent,
    href,
    iconAriaLabel,
    itemHoverIconColor,
    itemIconColor,
    itemSize,
    onClick,
    ...remainingProps
  }) => (
    <li {...remainingProps}>
      {href ? (
        // eslint-disable-next-line react/jsx-no-target-blank
        <a
          css={link({
            itemHoverIconColor,
            itemIconColor,
          })}
          href={href}
          title=""
          aria-label="link"
          aria-labelledby="link"
          onClick={onClick}
          rel={href.startsWith("http") ? "noopener noreferrer" : undefined}
          target={href.startsWith("http") ? "_blank" : undefined}
        >
          <IconComponent
            aria-label={iconAriaLabel}
            css={svgIcon({ itemSize })}
          />
        </a>
      ) : (
        <button
          css={link({
            itemHoverIconColor,
            itemIconColor,
          })}
          onClick={onClick}
        >
          <IconComponent
            aria-label={iconAriaLabel}
            css={svgIcon({ itemSize })}
          />
        </button>
      )}
    </li>
  ),
);

SocialMediaLinkListItem.displayName = "SocialMediaLinkListItem";

export default SocialMediaLinkListItem;
