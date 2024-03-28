import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const PlaySvg: StylableFC = memo((props) => (
  <svg fill="currentColor" viewBox="0 0 36 36" {...props}>
    <g transform="matrix(-1 0 0 1 40 0)">
      <path d="M28 7v21a1 1 0 01-1.6.9L13 18.4a1 1 0 010-1.6L26.4 6.3A1 1 0 0128 7z" />
    </g>
  </svg>
));

PlaySvg.displayName = "PlaySvg";

export default PlaySvg;
