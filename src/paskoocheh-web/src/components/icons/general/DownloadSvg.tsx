import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const DownloadSvg: StylableFC = memo((props) => (
  <svg viewBox="0 0 13.79 14.69" {...props}>
    <path fill="none" strokeWidth="2" d="M7.1 0v12.34" />
    <path fill="none" strokeWidth="2" d="M0 13.7h13.8" />
    <path
      fill="none"
      strokeLinejoin="bevel"
      strokeWidth="2"
      d="m.96 6.89 6.14 5.45 5.73-5.45"
    />
  </svg>
));

DownloadSvg.displayName = "DownloadSvg";

export default DownloadSvg;
