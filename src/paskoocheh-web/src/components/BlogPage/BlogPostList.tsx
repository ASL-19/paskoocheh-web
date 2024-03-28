import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

import BlogPostListItem from "src/components/BlogPage/BlogPostListItem";
import { GqlPostPreview } from "src/generated/graphQl";
import { threeColumnGridContainer } from "src/styles/generalStyles";

const BlogPostList: StylableFC<{
  postPreviews: Array<GqlPostPreview>;
}> = memo(({ postPreviews, ...remainingProps }) => (
  <ul css={threeColumnGridContainer} {...remainingProps}>
    {postPreviews.map((postPreview) => (
      <BlogPostListItem postPreview={postPreview} key={postPreview.id} />
    ))}
  </ul>
));

BlogPostList.displayName = "BlogPostList";

export default BlogPostList;
