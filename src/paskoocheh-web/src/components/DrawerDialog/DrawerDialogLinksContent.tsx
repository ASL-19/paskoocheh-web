import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Link from "next/link";
import { memo, useCallback } from "react";

import { AnimatedDialogStore } from "src/hooks/useAnimatedDialogState";
import { paragraphP1Regular } from "src/styles/typeStyles";
import { RouteInfo } from "src/types/miscTypes";
import colors from "src/values/colors";

const list = css({
  alignItems: "start",
  display: "flex",
  flexDirection: "column",
  rowGap: "0.5rem",
  width: "100%",
});

const link = css(paragraphP1Regular, {
  color: colors.secondary400,
  lineHeight: "2.25rem",
});

const DrawerDialogLinksContent: StylableFC<{
  animatedDialogState: AnimatedDialogStore;
  routeInfos: Array<RouteInfo>;
}> = memo(({ animatedDialogState, className, routeInfos }) => {
  const onClick = useCallback(() => {
    animatedDialogState?.hide();
  }, [animatedDialogState]);

  return (
    <ul className={className} css={list}>
      {routeInfos?.map((option) => (
        <Link
          shallow
          href={option.route}
          css={link}
          key={option.key}
          onClick={onClick}
        >
          {option.name}
        </Link>
      ))}
    </ul>
  );
});

DrawerDialogLinksContent.displayName = "DrawerDialogLinksContent";

export default DrawerDialogLinksContent;
