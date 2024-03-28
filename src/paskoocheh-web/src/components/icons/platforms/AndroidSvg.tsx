import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const AndroidSvg: StylableFC = memo((props) => (
  <svg fill="currentcolor" viewBox="0 0 24 24" {...props}>
    <g>
      <path d="m17.43 9.52 1.84-3.2a.38.38 0 0 0-.41-.55.37.37 0 0 0-.23.18l-1.87 3.24a11.67 11.67 0 0 0-9.52 0L5.37 5.95a.37.37 0 0 0-.65.37l1.85 3.2a11.02 11.02 0 0 0-5.7 8.72h22.26a11.02 11.02 0 0 0-5.7-8.72Zm-10.54 5.6a.93.93 0 1 1 0-1.87.93.93 0 0 1 0 1.86Zm10.22 0a.93.93 0 1 1 0-1.87.93.93 0 0 1 0 1.86Z" />
    </g>
  </svg>
));

AndroidSvg.displayName = "AndroidSvg";

export default AndroidSvg;
