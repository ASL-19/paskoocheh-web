import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const PlusSvg: StylableFC = memo((props) => (
  <svg viewBox="0 0 36 36" {...props}>
    <path
      d="M3 18.1h30.4M18.5 33V3.8"
      stroke="currentcolor"
      strokeWidth="2.8"
    />
  </svg>
));

PlusSvg.displayName = "PlusSvg";

export default PlusSvg;
