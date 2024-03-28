import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

/**
 * Rating star icon.
 */
const StarSvg: StylableFC = memo((props) => (
  <svg fill="none" viewBox="0 0 16 16" {...props}>
    <path
      fill="currentcolor"
      d="m8 1.333 1.854 4.458 4.812.386L11 9.317l1.12 4.697L8 11.497l-4.12 2.517L5 9.318 1.333 6.177l4.813-.386L8 1.333Z"
    />
  </svg>
));

StarSvg.displayName = "StarSvg";

export default StarSvg;
