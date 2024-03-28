import BlogPostPage from "src/pageComponents/BlogPostPage/BlogPostPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/BlogPostPage/getBlogPostPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: BlogPostPage,
  strings: stringsEn,
});
