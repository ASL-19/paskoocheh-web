import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const MacosSvg: StylableFC = memo((props) => (
  <svg fill="currentcolor" viewBox="0 0 24 24" {...props}>
    <g>
      <path d="M12 .873a11.128 11.128 0 1 0 0 22.255A11.128 11.128 0 0 0 12 .873Zm5.192 17.93h-.814l-4.364-6.21-4.364 6.21h-.814l4.771-6.79-4.771-6.79h.814l4.364 6.21 4.364-6.21h.814l-4.771 6.79 4.771 6.79Z" />
    </g>
  </svg>
));

MacosSvg.displayName = "MacosSvg";

export default MacosSvg;
