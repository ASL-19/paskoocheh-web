import { css } from "@emotion/react";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import BlogPostContent from "src/components/BlogPage/BlogPostContent";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import { GqlPost } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo } from "src/stores/appStore";
import {
  PaskoochehNextPage,
  PaskoochehPageRequiredProps,
} from "src/types/pageTypes";

// =============
// === Types ===
// =============
export type BlogPostPageProps = PaskoochehPageRequiredProps & {
  post: GqlPost;
};

export type BlogPostPageStrings = {
  pageDescription: string;
};

// ==============
// === Styles ===
// ==============
const pageContainer = css({
  display: "flex",
  flexDirection: "column",
});

// ==============================
// === Next.js page component ===
// ==============================
const BlogPostPage: PaskoochehNextPage<BlogPostPageProps> = ({ post }) => {
  const { localeCode } = useAppLocaleInfo();

  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  return (
    <PageContainer css={pageContainer}>
      <PageMeta
        canonicalPath={routeUrls.blogPost({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
          slug: post.slug,
        })}
        description={post.searchDescription}
        image={null}
        isAvailableInAlternateLocales={true}
        title={post.seoTitle || post.title}
      />

      <PageSegment as="main">
        <BlogPostContent post={post} />

        <A11yShortcutPreset preset="skipToNavigation" />
      </PageSegment>
    </PageContainer>
  );
};

export default BlogPostPage;
