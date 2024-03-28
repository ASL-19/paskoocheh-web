import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

/**
 * Header user icon.
 */
const UserSvg: StylableFC = memo((props) => (
  <svg fill="none" viewBox="0 0 24 24" {...props}>
    <path
      stroke="currentcolor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="2"
      d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z"
    />
  </svg>
));

UserSvg.displayName = "UserSvg";

export default UserSvg;
