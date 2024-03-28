import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import HeaderNavLinkListItem, {
  HeaderNavLinkListItemLinkInfo,
} from "src/components/Header/HeaderNavLinkListItem";
import { headingH6SemiBold, paragraphP1Regular } from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";

const container = ({ isMobile }: { isMobile: boolean }) =>
  css(
    {
      alignItems: isMobile ? "start" : "center",
      display: "flex",
      flexDirection: isMobile ? "column" : "row",
      gap: "1.5rem",
      justifyContent: "space-between",
      width: "100%",
    },
    isMobile ? headingH6SemiBold : paragraphP1Regular,
    breakpointStyles({
      desktopNarrow: {
        lt: {
          "html:not(.js) &": {
            flexDirection: "column",
          },
        },
      },
    }),
  );

const HeaderNavLinkList: StylableFC<{
  activeUrlComparisonQueryKeys?: Array<string>;
  isMobile: boolean;
  navLinkInfos: Array<HeaderNavLinkListItemLinkInfo>;
}> = memo(
  ({
    activeUrlComparisonQueryKeys = [],
    className,
    isMobile,
    navLinkInfos,
  }) => (
    <nav className={className}>
      <ul css={container({ isMobile })}>
        {navLinkInfos.map((navLinkInfo) => (
          <HeaderNavLinkListItem
            activeUrlComparisonQueryKeys={activeUrlComparisonQueryKeys}
            key={`${navLinkInfo.text ?? navLinkInfo.label ?? ""}-${
              navLinkInfo.href ?? ""
            }`}
            linkInfo={navLinkInfo}
            isMobile={isMobile}
          />
        ))}
      </ul>
    </nav>
  ),
);

HeaderNavLinkList.displayName = "HeaderNavLinkList";

export default HeaderNavLinkList;
