import { StylableFC } from "@asl-19/react-dom-utils";
import Link from "next/link";
import { memo } from "react";

import { GqlLinkBlock } from "src/generated/graphQl";
import { blockLink } from "src/styles/blockStyles";

const LinkBlock: StylableFC<{
  block: GqlLinkBlock;
}> = memo(({ block, className }) => (
  <Link className={className} href={block.value} css={blockLink}>
    {block.value}
  </Link>
));

LinkBlock.displayName = "LinkBlock";

export default LinkBlock;
