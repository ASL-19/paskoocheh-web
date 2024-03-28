import { StylableFC } from "@asl-19/react-dom-utils";
import { SerializedStyles } from "@emotion/react";
import { memo } from "react";
import { match, P } from "ts-pattern";

import CaptionedImageBlock from "src/components/Block/CaptionedImageBlock";
import CollapsibleBlock from "src/components/Block/CollapsibleBlock";
import EmailBlock from "src/components/Block/EmailBlock";
import LinkBlock from "src/components/Block/LinkBlock";
import MarkdownBlock from "src/components/Block/MarkdownBlock";
import TextBlock from "src/components/Block/TextBlock";
import { GqlPostBody, GqlStaticPageBody } from "src/generated/graphQl";

const Block: StylableFC<{
  block: GqlPostBody | GqlStaticPageBody;
  blockCss?: SerializedStyles;
  imageBlockCss?: SerializedStyles;
  imageSizes: string;
}> = memo(({ block, blockCss, imageBlockCss, imageSizes, ...remainingProps }) =>
  match(block)
    .with(
      { __typename: "CaptionedImageBlock", image: P.not(null) },
      (block) => (
        <CaptionedImageBlock
          block={block}
          css={imageBlockCss}
          imageSizes={imageSizes}
          {...remainingProps}
        />
      ),
    )
    .with(
      {
        __typename: "CollapsibleBlock",
        heading: P.string,
        slug: P.string,
        text: P.string,
      },
      (block) => (
        <CollapsibleBlock block={block} css={blockCss} {...remainingProps} />
      ),
    )
    .with({ __typename: "EmailBlock" }, (block) => (
      <EmailBlock block={block} css={blockCss} {...remainingProps} />
    ))
    .with({ __typename: "LinkBlock" }, (block) => (
      <LinkBlock block={block} css={blockCss} {...remainingProps} />
    ))
    .with({ __typename: "TextBlock", text: P.string }, (block) => (
      <TextBlock block={block} css={blockCss} {...remainingProps} />
    ))
    .with({ __typename: "MarkdownBlock", html: P.string }, (block) => (
      <MarkdownBlock block={block} css={blockCss} {...remainingProps} />
    ))
    .with({ __typename: P.string }, (block) => {
      console.warn(
        `${block.__typename} block not rendered because it isn't implemented or contained invalid data.`,
      );

      return null;
    })
    .exhaustive(),
);

Block.displayName = "Block";

export default Block;
