import { css } from "@emotion/react";
import Link from "next/link";
import { FC, memo } from "react";

import zIndexes from "src/values/zIndexes";

const linkOverlay = css({
  height: "100%",
  // It’s sometimes useful to enable this declaration during development to make
  // it easier to select elements in browser dev tools.
  // pointer-events: none;
  position: "absolute",
  right: "0",
  top: "0",
  width: "100%",
  zIndex: zIndexes.LinkOverlay_linkOverlay,
});

const LinkOverlay: FC<{
  className?: string;
  url: string;
}> = memo(({ className, url }) => (
  <Link
    href={url}
    aria-hidden="true"
    className={className}
    css={linkOverlay}
    tabIndex={-1}
  />
));

LinkOverlay.displayName = "LinkOverlay";

export default LinkOverlay;
