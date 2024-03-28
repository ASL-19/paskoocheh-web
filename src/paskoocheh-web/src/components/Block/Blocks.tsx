import { SerializedStyles } from "@emotion/react";
import { FC, memo } from "react";

import Block from "src/components/Block/Block";
import { pageSegmentPaddingInline } from "src/components/Page/PageSegment";
import { GqlPostBody, GqlStaticPageBody } from "src/generated/graphQl";

const Blocks: FC<{
  /**
   * Styles to apply to block elements.
   */
  blockCss?: SerializedStyles;
  blocks: Array<GqlPostBody | GqlStaticPageBody | null>;
  /**
   * Styles to apply to `CaptionedImageBlock`.
   *
   * (Will fall back to `blockCss` prop if not provided).
   */
  imageBlockCss?: SerializedStyles;
  /**
   * `CaptionedImageBlock` `Image` `sizes` prop.
   *
   * (Uses value appropriate for full-width images if not provided.)
   *
   * @see https://nextjs.org/docs/pages/api-reference/components/image#sizes
   */
  imageSizes?: string;
}> = memo(
  ({
    blockCss,
    blocks,
    imageBlockCss,
    imageSizes = `calc(100vw - ${pageSegmentPaddingInline} * 2)`,
  }) => (
    <>
      {blocks.map((block, index) =>
        block ? (
          <Block
            block={block}
            blockCss={blockCss}
            imageBlockCss={imageBlockCss ?? blockCss}
            imageSizes={imageSizes}
            key={index}
          />
        ) : null,
      )}
    </>
  ),
);

Blocks.displayName = "Blocks";

export default Blocks;
