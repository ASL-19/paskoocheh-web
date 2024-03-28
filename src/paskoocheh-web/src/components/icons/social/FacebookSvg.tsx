import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const FacebookSvg: StylableFC = memo((props) => (
  <svg fill="currentcolor" viewBox="0 0 36 36" {...props}>
    <g transform="translate(2 2)">
      <path d="M32 28.57A3.3 3.3 0 0131 31a3.3 3.3 0 01-2.43 1H22.5V19.36h4.29l.64-4.86H22.5v-3.07c0-.76.14-1.34.43-1.72.38-.43 1.02-.64 1.93-.64h2.57V4.8c-1-.15-2.24-.22-3.72-.22-1.9 0-3.41.56-4.53 1.68-1.12 1.12-1.68 2.68-1.68 4.68v3.57h-4.36v4.86h4.36V32H3.43A3.3 3.3 0 011 31a3.3 3.3 0 01-1-2.43V3.43C0 2.48.33 1.67 1 1a3.3 3.3 0 012.43-1h25.14c.95 0 1.76.33 2.43 1 .67.67 1 1.48 1 2.43v25.14z" />
    </g>
  </svg>
));

FacebookSvg.displayName = "FacebookSvg";

export default FacebookSvg;
