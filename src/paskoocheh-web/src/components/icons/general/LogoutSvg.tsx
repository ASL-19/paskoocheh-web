import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

/**
 * Header user dropdown - logout icon.
 */
const LogoutSvg: StylableFC = memo((props) => (
  <svg fill="none" viewBox="0 0 16 16" {...props}>
    <path
      stroke="currentcolor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="2"
      d="M10.667 11.333 14 8l-3.333-3.333M14 8H6M6 14H3.333A1.334 1.334 0 0 1 2 12.667V3.333A1.333 1.333 0 0 1 3.333 2H6"
    />
  </svg>
));

LogoutSvg.displayName = "LogoutSvg";

export default LogoutSvg;
