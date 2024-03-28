import { hoverStyles } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import DownloadSvg from "src/components/icons/general/DownloadSvg";
import { GqlDocumentBlock } from "src/generated/graphQl";
import { SetNonNullable } from "src/types/utilTypes";
import colors from "src/values/colors";

const icon = css({
  height: "1rem",
  stroke: colors.black,
});

const container = css(
  {
    color: colors.black,
    display: "block",
  },
  hoverStyles({
    textDecoration: "underline",
  }),
);

const DocumentBlock: StylableFC<{
  block: SetNonNullable<GqlDocumentBlock, "document">;
}> = memo(({ block, className }) => (
  <a
    className={className}
    css={container}
    download
    href={`${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${block.document.url}`}
  >
    <DownloadSvg css={icon} /> &nbsp;
    {block?.document?.title}
  </a>
));

DocumentBlock.displayName = "DocumentBlock";

export default DocumentBlock;
