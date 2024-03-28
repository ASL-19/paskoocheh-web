import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const MailSvg: StylableFC = memo((props) => (
  <svg fill="currentcolor" viewBox="0 0 24 25" {...props}>
    <g transform="translate(-1328 -240)">
      <g transform="translate(1330 244.67)">
        <path d="M17.27 0A2.7 2.7 0 0120 2.67v10.66A2.7 2.7 0 0117.27 16H2.73A2.7 2.7 0 010 13.33V2.67A2.7 2.7 0 012.74 0h14.54zM4.8 3.5a.95.95 0 00-1.3.33.99.99 0 00.33 1.35l5.82 3.59.11.23.14-.08.13.08.14-.24 5.43-3.2a.83.83 0 00.28-1.15.88.88 0 00-1.18-.3L10.12 6.8 4.8 3.5z" />
      </g>
    </g>
  </svg>
));

MailSvg.displayName = "MailSvg";

export default MailSvg;
