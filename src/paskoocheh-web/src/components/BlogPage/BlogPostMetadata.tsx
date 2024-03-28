import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { Fragment, memo, useContext } from "react";

import FormattedDate from "src/components/FormattedDate";
import BlogPageContext from "src/contexts/BlogPageContext";
import { GqlPost, GqlPostPreview } from "src/generated/graphQl";
import useDateInfo from "src/hooks/useDateInfo";
import { captionRegular, captionSemiBold } from "src/styles/typeStyles";
import colors from "src/values/colors";

const topicAndDate = css({
  alignItems: "center",
  columnGap: "1rem",
  display: "flex",
  justifyContent: "space-between",
});

const topicAndDateOneChild = css(topicAndDate, {
  justifyContent: "end",
});
const topicAndDateMultipleChildren = css(topicAndDate, {
  justifyContent: "space-between",
});

const topic = css(captionSemiBold, {
  backgroundColor: colors.primary500,
  borderRadius: "0.125rem",
  color: colors.shadesWhite,
  flex: "0 1 auto",
  height: "1.375rem",
  lineHeight: "1.375rem",
  minWidth: 0,
  overflow: "hidden",
  padding: "0 0.5rem",
  textOverflow: "ellipsis",
  whiteSpace: "nowrap",
});
const formattedDate = css(captionRegular, {
  flex: "0 0 auto",
});

/**
 * Blog post date and main topic.
 */
const BlogPostMetadata: StylableFC<{
  post: GqlPost | GqlPostPreview;
}> = memo(({ post, ...remainingProps }) => {
  const { topic: topicSlug } = useContext(BlogPageContext);

  const postDateInfo = useDateInfo({ dateString: post.published });
  const postMainTopic = topic
    ? post.topics?.find((topic) => topic?.slug === topicSlug)
    : post.topics?.[0];

  /* eslint-disable react/jsx-key */
  const segmentElements = [
    ...(postMainTopic ? [<span css={topic}>{postMainTopic.name}</span>] : []),
    ...(postDateInfo
      ? [<FormattedDate css={formattedDate} dateInfo={postDateInfo} />]
      : []),
  ];
  /* eslint-enable react/jsx-key */

  return (
    <footer
      css={
        segmentElements.length > 1
          ? topicAndDateMultipleChildren
          : topicAndDateOneChild
      }
      {...remainingProps}
    >
      {segmentElements.map((segmentElement, index) => (
        <Fragment key={index}>{segmentElement}</Fragment>
      ))}
    </footer>
  );
});

BlogPostMetadata.displayName = "BlogPostMetadata";

export default BlogPostMetadata;
