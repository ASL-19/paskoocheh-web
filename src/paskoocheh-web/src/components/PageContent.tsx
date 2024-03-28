import { css } from "@emotion/react";
import { FC, memo } from "react";

import Blocks from "src/components/Block/Blocks";
import PageSegment from "src/components/Page/PageSegment";
import { GqlStaticPage } from "src/generated/graphQl";
import { headingH3SemiBold } from "src/styles/typeStyles";

const container = css({
  display: "flex",
  flexDirection: "column",
  paddingBlock: "3rem",
  rowGap: "2rem",
});

const PageContent: FC<{
  staticPage: GqlStaticPage;
}> = memo(({ staticPage }) => (
  <PageSegment centeredContainerCss={container}>
    <h1 css={headingH3SemiBold} id="main-heading">
      {staticPage.title}
    </h1>

    {staticPage.body && <Blocks blocks={staticPage.body} />}
  </PageSegment>
));

PageContent.displayName = "PageContent";

export default PageContent;
