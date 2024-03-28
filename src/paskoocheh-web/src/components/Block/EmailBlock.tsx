import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

import { GqlEmailBlock } from "src/generated/graphQl";
import { blockLink } from "src/styles/blockStyles";

const EmailBlock: StylableFC<{
  block: GqlEmailBlock;
}> = memo(({ block, className }) => (
  <a className={className} href={`mailto:${block.value}`} css={blockLink}>
    {block.value}
  </a>
));

EmailBlock.displayName = "EmailBlock";

export default EmailBlock;
