import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const HamburgerSvg: StylableFC = memo((props) => (
  <svg viewBox="0 0 36 36" {...props}>
    <path strokeWidth="2.5" d="M1 18h34.27M1 31h34.27M1 5h34.27" />
  </svg>
));

HamburgerSvg.displayName = "HamburgerSvg";

export default HamburgerSvg;
