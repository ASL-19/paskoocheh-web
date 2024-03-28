import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

/**
 * Cross (✕) icon.
 *
 * Note: Color needs to be styled using stroke, not fill!
 */
const CrossSvg: StylableFC = memo((props) => (
  <svg viewBox="0 0 36 36" {...props}>
    <path
      d="M6.126 5.626l24.233 24.233M5.707 30.457L29.94 6.223"
      stroke="currentcolor"
      strokeWidth="2.8"
    />
  </svg>
));

CrossSvg.displayName = "CrossSvg";

export default CrossSvg;
