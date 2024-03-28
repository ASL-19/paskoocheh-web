import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const TelegramSvg: StylableFC = memo((props) => (
  <svg fill="currentcolor" viewBox="0 0 36 36" {...props}>
    <g transform="translate(2 4)">
      <path d="M27.06 25.48c-.2.82-.51 1.34-.97 1.55-.45.22-1 .14-1.67-.25l-7.36-5.49-3.56 3.47c-.24.24-.43.4-.58.5-.23.15-.54.22-.92.22l.57-7.58L26.2 5.4c.2-.14.25-.27.18-.4-.07-.11-.21-.16-.43-.14-.21.03-.44.11-.68.26L8.43 15.88l-7.29-2.31c-.8-.24-1.18-.6-1.14-1.09.05-.48.55-.91 1.5-1.3L29.84.13c.72-.24 1.29-.15 1.72.26.42.4.54 1.12.35 2.13l-4.85 22.96z" />
    </g>
  </svg>
));

TelegramSvg.displayName = "TelegramSvg";

export default TelegramSvg;
