import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

import HtmlContent from "src/components/HtmlContent";
import { GqlMarkdownBlock } from "src/generated/graphQl";

const MarkdownBlock: StylableFC<{
  block: GqlMarkdownBlock & { html: string };
}> = memo(({ block, ...remainingProps }) => (
  <HtmlContent dangerousHtml={block.html} {...remainingProps} />
));

MarkdownBlock.displayName = "MarkdownBlock";

export default MarkdownBlock;
