import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Link from "next/link";
import { Dispatch, memo, RefObject, SetStateAction } from "react";

import useOnSectionLinkClick from "src/hooks/useOnSectionLinkClick";
import { navMenuText, navTopLevelItem } from "src/styles/navStyles";
import { paragraphP3SemiBold } from "src/styles/typeStyles";
import colors from "src/values/colors";

export type AppNavLinkInfo<SectionId extends string = string> = {
  id: SectionId;
  navItemRef: RefObject<HTMLLIElement>;
  sectionRef: RefObject<HTMLElement>;
  text: string;
  url: string;
};

const listItem = css(navTopLevelItem, navMenuText, paragraphP3SemiBold, {
  alignItems: "center",

  display: "flex",
  flex: "0 0 auto",
  justifyContent: "center",
});

const link = ({ isActive }: { isActive: boolean }) =>
  css({
    "::before": {
      borderBottom: isActive ? `solid 2px ${colors.primary500}` : "none",
      borderRadius: "10px",
      bottom: "0",
      content: '""',
      display: "block",
      height: "2px",
      position: "absolute",
      width: "100%",
      zIndex: "1",
    },
    color: colors.secondary500,
    display: "flex",
    flexDirection: "column",
    height: "2rem",
    lineHeight: "1.75rem",
    position: "relative",
  });

const AppNavLinkListItem: StylableFC<{
  activeSectionId: string;
  linkInfo: AppNavLinkInfo;
  setActiveSectionId: Dispatch<SetStateAction<string>>;
}> = memo(
  ({ activeSectionId, linkInfo, setActiveSectionId, ...remainingProps }) => {
    const isActive = linkInfo.id === activeSectionId;

    const onClick = useOnSectionLinkClick({ linkInfo, setActiveSectionId });

    return (
      <li css={listItem} ref={linkInfo.navItemRef} {...remainingProps}>
        <Link href={linkInfo.url} css={link({ isActive })} onClick={onClick}>
          {linkInfo.text}
        </Link>
      </li>
    );
  },
);

AppNavLinkListItem.displayName = "AppNavLinkListItem";

export default AppNavLinkListItem;
