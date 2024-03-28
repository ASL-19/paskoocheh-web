import BlogPostPage from "src/pageComponents/BlogPostPage/BlogPostPage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/BlogPostPage/getBlogPostPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: BlogPostPage,
  strings: stringsFa,
});
