import { focusElement } from "@asl-19/js-dom-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, MouseEvent, useCallback } from "react";

import colors from "src/values/colors";

const link = css(
  {
    backgroundColor: colors.black,
    clip: "rect(1px, 1px, 1px, 1px)",
    clipPath: "inset(50%)",
    color: `${colors.shadesWhite} !important`,
    fontSize: "1.25rem",
    height: "1px",
    lineHeight: "2rem",
    margin: "-1px",
    overflow: "hidden",
    position: "absolute",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  },
  {
    "&:active, &:focus, &:hover": {
      clip: "auto !important",
      clipPath: "none",
      height: "2rem",
      margin: "0",
      padding: "0 1rem",
    },
  },
);

const A11yShortcut: StylableFC<{
  targetId: string;
  text: string;
}> = memo(({ className, targetId, text }) => {
  const onClick = useCallback(
    (event: MouseEvent) => {
      event.preventDefault();

      focusElement(document.getElementById(targetId));
    },
    [targetId],
  );

  return (
    <a className={className} css={link} href={`#${targetId}`} onClick={onClick}>
      {text}
    </a>
  );
});

A11yShortcut.displayName = "A11yShortcut";

export default A11yShortcut;
