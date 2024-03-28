import { css, SerializedStyles } from "@emotion/react";
import { FC, memo, ReactNode, useMemo } from "react";

export const pageSegmentMaxWidth = "77rem";

export const pageSegmentPaddingInline = "1rem";

const pageSegment = css({
  width: "100%",
});

const centeredContainer = css({
  margin: "0 auto",
  maxWidth: pageSegmentMaxWidth,
  padding: `0 ${pageSegmentPaddingInline}`,
  position: "relative",
  width: "100%",
});

const PageSegment: FC<{
  // Add any tag names we need here (avoiding `keyof JSX.IntrinsicElements` for performance)
  as?: "div" | "header" | "main" | "section";
  centeredContainerCss?: SerializedStyles;
  children: ReactNode;
  className?: string;
  id?: string;
}> = memo(
  ({
    as: WrapperComponent = "div",
    centeredContainerCss,
    children,
    className,
    id,
  }) => {
    const centredContainerCombinedCss = useMemo(
      () => [centeredContainer, centeredContainerCss],
      [centeredContainerCss],
    );

    return (
      <WrapperComponent className={className} css={pageSegment} id={id}>
        <div css={centredContainerCombinedCss}>{children}</div>
      </WrapperComponent>
    );
  },
);

PageSegment.displayName = "PageSegment";

export default PageSegment;
