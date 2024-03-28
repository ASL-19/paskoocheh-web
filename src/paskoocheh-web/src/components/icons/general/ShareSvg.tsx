import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const ShareSvg: StylableFC = memo((props) => (
  <svg fill="none" viewBox="0 0 16 16" {...props}>
    <path
      stroke="#2D2D2D"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="2"
      d="M12 14.667a2 2 0 1 0 0-4 2 2 0 0 0 0 4ZM4 10a2 2 0 1 0 0-4 2 2 0 0 0 0 4ZM5.727 9.007l4.553 2.653M12 5.333a2 2 0 1 0 0-4 2 2 0 0 0 0 4ZM10.273 4.34 5.727 6.993"
    />
  </svg>
));

ShareSvg.displayName = "ShareSvg";

export default ShareSvg;
