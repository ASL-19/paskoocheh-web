import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

const SearchSvg: StylableFC = memo((props) => (
  <svg stroke="none" viewBox="0 0 16 16" fill="none" {...props}>
    <path
      d="M7.33333 12.6667C10.2789 12.6667 12.6667 10.2789 12.6667 7.33333C12.6667 4.38781 10.2789 2 7.33333 2C4.38781 2 2 4.38781 2 7.33333C2 10.2789 4.38781 12.6667 7.33333 12.6667Z"
      stroke="currentcolor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path
      d="M13.9996 13.9996L11.0996 11.0996"
      stroke="currentcolor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
));

SearchSvg.displayName = "SearchSvg";

export default SearchSvg;
