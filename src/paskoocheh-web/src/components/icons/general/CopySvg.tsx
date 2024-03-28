import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const CopySvg: StylableFC = memo((props) => (
  <svg fill="none" viewBox="0 0 24 24" {...props}>
    <path
      stroke="currentcolor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="2"
      d="M20 9h-9a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2Z"
    />
    <path
      stroke="currentcolor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="2"
      d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"
    />
  </svg>
));

CopySvg.displayName = "CopySvg";

export default CopySvg;
