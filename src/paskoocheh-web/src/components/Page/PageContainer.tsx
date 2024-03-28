import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, ReactNode } from "react";

import { fullWidthWrapper } from "src/styles/generalStyles";

const pageWrapper = css(fullWidthWrapper, {
  display: "flex",
  flex: "1 0 auto",
  flexFlow: "column wrap",
});

const PageContainer: StylableFC<{ as?: "div" | "main"; children: ReactNode }> =
  memo(({ as: WrapperComponent = "div", children, ...remainingProps }) => (
    <WrapperComponent css={pageWrapper} {...remainingProps}>
      {children}
    </WrapperComponent>
  ));

PageContainer.displayName = "PageContainer";

export default PageContainer;
