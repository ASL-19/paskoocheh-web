import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const WindowsSvg: StylableFC = memo((props) => (
  <svg fill="currentcolor" viewBox="0 0 24 24" {...props}>
    <g>
      <path d="M23.084 11.65c.05-1.29.064-10.547.005-10.76-4.062.55-8.13 1.106-12.205 1.67v9.09h12.2ZM.915 3.924l-.02 7.726H10.2V2.652L.915 3.924ZM10.884 12.334v9.046l12.162 1.73c.052-.276.072-9.592.03-10.776H10.885ZM.897 12.334c-.034 2.474-.034 2.8.005 7.627l9.298 1.322v-8.949H.897Z" />
    </g>
  </svg>
));

WindowsSvg.displayName = "WindowsSvg";

export default WindowsSvg;
