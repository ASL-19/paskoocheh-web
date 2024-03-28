import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const RewardSvg: StylableFC = memo((props) => (
  <svg fill="none" viewBox="0 0 24 24" {...props}>
    <path
      stroke="currentcolor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="2"
      d="M20 12v10H4V12M22 7H2v5h20V7ZM12 22V7M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7ZM12 7H7.5a2.5 2.5 0 1 1 0-5C11 2 12 7 12 7Z"
    />
  </svg>
));

RewardSvg.displayName = "RewardSvg";

export default RewardSvg;
