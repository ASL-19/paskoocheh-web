import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";
import { match, P } from "ts-pattern";

import { useAppLocaleInfo } from "src/stores/appStore";
import { Direction } from "src/types/layoutTypes";

type ThumbsDirection = "up" | "down";

const ThumbsUpSvg: StylableFC<{
  direction?: ThumbsDirection;
}> = memo(({ direction = "up", ...props }) => {
  const { direction: localeDirection } = useAppLocaleInfo();

  const rotation = match<[ThumbsDirection, Direction]>([
    direction,
    localeDirection,
  ])
    .with(["up", P.union("ltr", "rtl")], () => "0")
    .with(["down", P.union("ltr", "rtl")], () => "180")
    .exhaustive();

  return (
    <svg
      fill="none"
      stroke="currentcolor"
      viewBox="0 0 24 24"
      transform={`rotate(${rotation})`}
      {...props}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
        d="M8.4 19.5h8.118a2 2 0 0 0 1.845-1.23l2.483-5.943c.102-.244.154-.506.154-.77v-.428a2 2 0 0 0-2-2h-5.65l1.104-4.241a1.229 1.229 0 0 0-.619-1.398v0a1.228 1.228 0 0 0-1.56.361l-3.487 4.75A2 2 0 0 0 8.4 9.783V19.5Zm0 0H3v-9.429h5.4V19.5Z"
      />
    </svg>
  );
});

ThumbsUpSvg.displayName = "ThumbsUpSvg";

export default ThumbsUpSvg;
