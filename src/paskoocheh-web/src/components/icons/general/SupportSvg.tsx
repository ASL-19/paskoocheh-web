import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const SupportSvg: StylableFC = memo((props) => (
  <svg fill="none" viewBox="0 0 24 24" {...props}>
    <path
      fill="#2D2D2D"
      d="M22 17.002a6.001 6.001 0 0 1-4.477 5.803.894.894 0 0 1-.47-.009.969.969 0 0 1-.63-1.306l.013-.031c.132-.318.422-.536.751-.638A4.002 4.002 0 0 0 19.465 19H18a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h1.938a8 8 0 0 0-15.876 0H6a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-5C2 6.477 6.477 2 12 2s10 4.477 10 10v5.002Z"
    />
  </svg>
));

SupportSvg.displayName = "SupportSvg";

export default SupportSvg;
