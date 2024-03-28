import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Image from "next/image";
import { memo } from "react";

import {
  GqlCaptionedImage,
  GqlCaptionedImageBlock,
} from "src/generated/graphQl";
import { paragraphP1Regular } from "src/styles/typeStyles";
import { SetNonNullable } from "src/types/utilTypes";

const img = css({
  height: "100%",
  width: "100%",
});

export const getCaptionedImageCaption = (image: GqlCaptionedImage) =>
  image.caption && image.credit
    ? `${image.caption} (${image.credit})`
    : image.caption ?? image.credit ?? null;

const CaptionedImageBlock: StylableFC<{
  block: SetNonNullable<GqlCaptionedImageBlock, "image">;
  imageSizes: string;
}> = memo(({ block, imageSizes, ...remainingProps }) => {
  const caption =
    block.image.caption && block.image.credit
      ? `${block.image.caption} (${block.image.credit})`
      : block.image.caption ?? block.image.credit ?? null;

  return (
    <div {...remainingProps}>
      <Image
        alt={block.image.caption}
        css={img}
        height={block.image.height}
        sizes={imageSizes}
        src={`${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${block.image.file}`}
        width={block.image.width}
      />
      {caption && <p css={paragraphP1Regular}>{caption}</p>}
    </div>
  );
});

CaptionedImageBlock.displayName = "CaptionedImageBlock";

export default CaptionedImageBlock;
