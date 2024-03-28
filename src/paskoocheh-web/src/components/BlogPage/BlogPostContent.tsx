import { getAbsoluteUrl } from "@asl-19/js-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Image from "next/image";
import { memo } from "react";

import Blocks from "src/components/Block/Blocks";
import {
  blogPostContentMaxWidth,
  blogPostFullWidthImageSizes,
} from "src/components/BlogPage/blogPageValues";
import BlogPostSummarySection from "src/components/BlogPage/BlogPostSummarySection";
import FormattedDate from "src/components/FormattedDate";
import SocialMediaShareLinkList from "src/components/SocialMediaShareLinkList";
import { GqlPost } from "src/generated/graphQl";
import useDateInfo from "src/hooks/useDateInfo";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import {
  captionRegular,
  captionSemiBold,
  headingH3SemiBold,
  paragraphP1SemiBold,
} from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

export type BlogPostContentStrings = {
  /**
   * text for published date
   */
  published: string;
  /**
   * Text for summary section title
   */
  summary: string;
};

// ==============
// === Styles ===
// ==============

const container = css({
  display: "flex",
  flexDirection: "column",
  gap: "2rem",
  margin: "0 auto",
  maxWidth: blogPostContentMaxWidth,
  padding: "2rem 0",
});

const dateAndLinksContainer = css({
  display: "flex",
  justifyContent: "space-between",
});

const categoryAndDateContainer = css({
  display: "flex",
  flexDirection: "column",
  gap: "0.5rem",
});

const category = css(
  captionSemiBold,
  {
    backgroundColor: colors.primary500,
    borderRadius: "2px",
    color: colors.shadesWhite,
    height: "1.375rem",
    lineHeight: "1.375rem",
    maxWidth: "max-content",
    padding: "0 1rem",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        borderRadius: "4px",
      },
    },
  }),
);

const date = css(captionRegular, { color: colors.secondary400 });

const title = css(
  headingH3SemiBold,
  {},
  breakpointStyles({
    singleColumn: {
      lt: paragraphP1SemiBold,
    },
  }),
);

const fullWidth = css({ width: "100%" });

const constrainedWidth = css({
  alignSelf: "center",
  maxWidth: "42.375rem",
});

const image = css(
  fullWidth,
  {
    borderRadius: "0.5rem",
    height: "31.25rem",
  },
  {
    "@supports (aspect-ratio: 9/4)": {
      aspectRatio: "9/4",

      height: "auto",
      maxHeight: "31.25rem",
    },
  },
);

const BlogPostContent: StylableFC<{
  post: GqlPost;
}> = memo(({ post, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();
  const { BlogPostContent: strings } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const absoluteUrl = getAbsoluteUrl({
    protocolAndHost: process.env.NEXT_PUBLIC_WEB_URL,
    rootRelativeUrl: routeUrls.blogPost({
      localeCode,
      platform: queryOrDefaultPlatformSlug,
      slug: post.slug,
    }),
  });

  const dateInfo = useDateInfo({ dateString: post.published });
  const imageUrl = `${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${post.featuredImage.file}`;

  const postMainTopic = post.topics?.[0];
  /* eslint-disable react/jsx-key */
  const postCategoryElements = [
    ...(postMainTopic
      ? [
          <div css={category} key={post.id}>
            {postMainTopic.name}
          </div>,
        ]
      : []),
  ];

  return (
    <div css={container} {...remainingProps}>
      <div css={dateAndLinksContainer}>
        <div css={categoryAndDateContainer}>
          {postCategoryElements}
          <p css={date}>
            {strings.published}

            {dateInfo && (
              <>
                &nbsp;
                <FormattedDate dateInfo={dateInfo} />
              </>
            )}
          </p>
        </div>

        <SocialMediaShareLinkList
          itemIconColor={colors.greyDark}
          itemSize="1.125rem"
          title={post.title}
          url={absoluteUrl}
        />
      </div>

      <h1 css={title} id="main-heading">
        {post.title}
      </h1>

      <Image
        src={imageUrl}
        alt=""
        css={image}
        width={post.featuredImage.width}
        height={post.featuredImage.height}
        sizes={blogPostFullWidthImageSizes}
        placeholder="blur"
        blurDataURL={imageUrl}
      />

      {post.summary && (
        <BlogPostSummarySection css={constrainedWidth} summary={post.summary} />
      )}

      {post.body && (
        <Blocks
          blockCss={constrainedWidth}
          imageBlockCss={fullWidth}
          blocks={post.body}
          imageSizes={blogPostFullWidthImageSizes}
        />
      )}
    </div>
  );
});

BlogPostContent.displayName = "BlogPostContent";

export default BlogPostContent;
