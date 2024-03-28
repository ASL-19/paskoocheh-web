import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

import HtmlContent from "src/components/HtmlContent";
import { GqlTextBlock } from "src/generated/graphQl";

const TextBlock: StylableFC<{
  block: GqlTextBlock & { text: string };
}> = memo(({ block, ...remainingProps }) => (
  <HtmlContent dangerousHtml={block.text} {...remainingProps} />
));

TextBlock.displayName = "TextBlock";

export default TextBlock;
