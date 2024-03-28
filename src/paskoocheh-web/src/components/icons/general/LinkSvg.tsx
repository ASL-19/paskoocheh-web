import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const LinkSvg: StylableFC = memo((props) => (
  <svg fill="currentcolor" viewBox="0 0 24 24" {...props}>
    <path d="M3.9 12A3.1 3.1 0 0 1 7 8.9h4V7H7a5 5 0 0 0 0 10h4v-1.9H7A3.1 3.1 0 0 1 3.9 12ZM8 13h8v-2H8v2Zm9-6h-4v1.9h4a3.1 3.1 0 0 1 0 6.2h-4V17h4a5 5 0 0 0 0-10Z" />
  </svg>
));

LinkSvg.displayName = "LinkSvg";

export default LinkSvg;
