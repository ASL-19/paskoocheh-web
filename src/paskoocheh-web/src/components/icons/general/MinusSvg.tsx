import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const MinusSvg: StylableFC = memo((props) => (
  <svg viewBox="0 0 36 36" {...props}>
    <path d="M3 18.1h30.4" stroke="currentcolor" strokeWidth="2.8" />
  </svg>
));

MinusSvg.displayName = "MinusSvg";

export default MinusSvg;
