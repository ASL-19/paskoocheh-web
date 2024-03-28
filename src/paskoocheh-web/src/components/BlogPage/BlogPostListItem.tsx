import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Image from "next/image";
import Link from "next/link";
import { memo } from "react";

import BlogPostMetadata from "src/components/BlogPage/BlogPostMetadata";
import LinkOverlay from "src/components/LinkOverlay";
import { GqlPostPreview } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo } from "src/stores/appStore";
import { paragraphP1Regular, paragraphP3SemiBold } from "src/styles/typeStyles";
import colors from "src/values/colors";
import { threeColumnGridContainerImageSizes } from "src/values/layoutValues";

const container = css({
  display: "flex",
  flexDirection: "column",
  gap: "1rem",
  position: "relative",
});

const image = css(
  {
    borderRadius: "0.5rem",
    width: "100%",
  },
  {
    "@supports (aspect-ratio: 9/4)": {
      aspectRatio: "9/4",
      height: "auto",
      maxWidth: "100%",
    },
  },
);

const blogDetails = css({
  display: "flex",
  flexDirection: "column",
  gap: "0.5rem",
});

const linkText = css(paragraphP3SemiBold, { color: colors.secondary500 });

export const getBlogPostListItemElementId = (postPreview: GqlPostPreview) =>
  `BlogPostPreviewListItem-${postPreview.id}`;

const BlogPostListItem: StylableFC<{
  postPreview: GqlPostPreview;
}> = memo(({ postPreview, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const postUrl = routeUrls.blogPost({
    localeCode,
    platform: queryOrDefaultPlatformSlug,
    slug: postPreview.slug,
  });

  const imageUrl = `${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${postPreview.featuredImage.file}`;

  return (
    <li
      css={container}
      id={getBlogPostListItemElementId(postPreview)}
      {...remainingProps}
    >
      <Image
        src={imageUrl}
        alt=""
        css={image}
        width={postPreview.featuredImage.width}
        height={postPreview.featuredImage.height}
        sizes={threeColumnGridContainerImageSizes}
        placeholder="blur"
        blurDataURL={imageUrl}
      />

      <div css={blogDetails}>
        <BlogPostMetadata post={postPreview} />

        <Link href={postUrl} css={linkText}>
          <h2>{postPreview.title}</h2>
        </Link>

        <p css={paragraphP1Regular}>{postPreview.synopsis}</p>
      </div>

      <LinkOverlay url={postUrl} />
    </li>
  );
});

BlogPostListItem.displayName = "BlogPostListItem";

export default BlogPostListItem;
