import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const InfoSvg: StylableFC = memo((props) => (
  <svg fill="none" viewBox="0 0 24 24" {...props}>
    <path
      stroke="currentcolor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="2"
      d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10ZM12 16v-4M12 8h.01"
    />
  </svg>
));

InfoSvg.displayName = "InfoSvg";

export default InfoSvg;
