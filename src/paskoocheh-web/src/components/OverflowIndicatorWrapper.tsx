import useOverflowState from "@asl-19/use-overflow-state";
import { css, SerializedStyles } from "@emotion/react";
import { cloneElement, FC, memo, ReactElement, useMemo, useRef } from "react";

import {
  overflowIndicatorContainer,
  overflowIndicatorContainerLeftActive,
  overflowIndicatorContainerRightActive,
} from "src/styles/overflowIndicatorStyles";

const container = css(
  overflowIndicatorContainer,
  {
    "> *:only-child": {
      WebkitOverflowScrolling: "touch",
    },
  },
  {
    "&.overflowIndicatorLeft": overflowIndicatorContainerLeftActive,
    "&.overflowIndicatorRight": overflowIndicatorContainerRightActive,
  },
);

const OverflowIndicatorWrapper: FC<{
  children: ReactElement;
  className?: string;
  containerCss?: SerializedStyles;
}> = memo(({ children, className, containerCss }) => {
  const scrollableElementRef = useRef<HTMLElement>(null);
  const wrapperElementRef = useRef<HTMLDivElement>(null);

  const { leftHasOverflow, rightHasOverflow } = useOverflowState({
    scrollableElementRef,
    wrapperElementRef,
  });

  const containerClassName = `${className ? `${className} ` : ""}${
    leftHasOverflow ? "overflowIndicatorLeft" : ""
  } ${rightHasOverflow ? "overflowIndicatorRight" : ""} `.trim();

  const containerCssCombined = useMemo(
    () => [container, containerCss],
    [containerCss],
  );

  return (
    <div
      className={containerClassName}
      css={containerCssCombined}
      ref={wrapperElementRef}
    >
      {cloneElement(children, { ref: scrollableElementRef })}
    </div>
  );
});

OverflowIndicatorWrapper.displayName = "OverflowIndicatorWrapper";

export default OverflowIndicatorWrapper;
