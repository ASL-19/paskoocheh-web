import { MenuButton, MenuStore } from "@ariakit/react/menu";
import { hoverStyles } from "@asl-19/emotion-utils";
import { useHrefIsActive } from "@asl-19/next-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Link from "next/link";
import { FC, memo, MouseEventHandler } from "react";
import { match, P } from "ts-pattern";

import { navMenuText, navTopLevelItem } from "src/styles/navStyles";
import {
  headingH6SemiBold,
  paragraphP1Regular,
  paragraphP1SemiBold,
} from "src/styles/typeStyles";
import colors from "src/values/colors";

export type HeaderNavLinkListItemLinkInfo = {
  IconComponent?: FC<{ className?: string }>;
} & (
  | {
      href: string;
      menuStore?: never;
      onClick?: never;
    }
  | {
      href?: never;
      menuStore?: never;
      onClick: MouseEventHandler<HTMLButtonElement>;
    }
  | {
      href?: never;
      menuStore: MenuStore;
      onClick?: never;
    }
) &
  (
    | {
        label: string;
        text?: never;
      }
    | {
        label?: never;
        text: string;
      }
  );

const listItem = css(navTopLevelItem, navMenuText, {
  alignItems: "center",
  display: "flex",
  flex: "0 0 auto",
  height: "auto",
  justifyContent: "center",
});

const link = ({
  isActive,
  isMobile,
  isText,
}: {
  isActive: boolean;
  isMobile: boolean;
  isText: boolean;
}) =>
  css(
    {
      alignItems: "center",
      color: colors.secondary500,
      display: "flex",
      flexDirection: "column",
      height: "1.75rem",
      lineHeight: "1.75rem",
      position: "relative",
    },
    isMobile
      ? headingH6SemiBold
      : isActive
        ? paragraphP1SemiBold
        : paragraphP1Regular,
    {
      "::after": {
        background: colors.primary500,
        bottom: 0,
        color: "transparent",
        content: '""',
        display: "block",
        height: "2px",
        margin: "auto",

        position: "absolute",
        transform: isActive && isText ? "scaleX(1)" : "scaleX(0)",
        transition: "transform 0.3s ease",
        visibility: "visible",
        width: "100%",
      },
    },
    hoverStyles({
      "::after": {
        transform: isText ? "scaleX(1)" : "scaleX(0)",
      },
    }),
  );

const icon = ({ isActive }: { isActive: boolean }) =>
  css({
    color: isActive ? colors.primary500 : colors.secondary500,
    height: "1.5rem",
  });

const HeaderNavLinkListItem: StylableFC<{
  activeUrlComparisonQueryKeys: Array<string>;
  isMobile: boolean;
  linkInfo: HeaderNavLinkListItemLinkInfo;
}> = memo(({ activeUrlComparisonQueryKeys, isMobile, linkInfo }) => {
  const isActive = useHrefIsActive({
    activeUrlComparisonQueryKeys,
    href: linkInfo.href ?? "",
    webPublicUrl: process.env.NEXT_PUBLIC_WEB_URL,
  });

  const IconComponent = linkInfo.IconComponent;

  return (
    <li css={listItem}>
      {match(linkInfo)
        .with({ href: P.string }, (linkInfo) => (
          <Link
            href={linkInfo.href}
            css={link({ isActive, isMobile, isText: !IconComponent })}
            aria-label={IconComponent ? linkInfo.label : linkInfo.text}
          >
            {IconComponent && !isMobile ? (
              <IconComponent css={icon({ isActive })} />
            ) : (
              linkInfo.text
            )}
          </Link>
        ))
        .with({ onClick: P.not(undefined) }, (linkInfo) => (
          <button
            css={link({ isActive, isMobile, isText: !IconComponent })}
            onClick={linkInfo.onClick}
          >
            {IconComponent && !isMobile ? (
              <IconComponent css={icon({ isActive })} />
            ) : (
              linkInfo.text
            )}
          </button>
        ))
        .with({ menuStore: P.not(undefined) }, (linkInfo) => (
          <MenuButton
            css={link({ isActive, isMobile, isText: !IconComponent })}
            store={linkInfo.menuStore}
            aria-label={IconComponent ? linkInfo.label : linkInfo.text}
          >
            {IconComponent && !isMobile ? (
              <IconComponent css={icon({ isActive })} />
            ) : (
              linkInfo.text
            )}
          </MenuButton>
        ))
        .exhaustive()}
    </li>
  );
});

HeaderNavLinkListItem.displayName = "HeaderNavLinkListItem";

export default HeaderNavLinkListItem;
