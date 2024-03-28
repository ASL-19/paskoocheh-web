import BlogPage from "src/pageComponents/BlogPage/BlogPage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/BlogPage/getBlogPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: BlogPage,
  strings: stringsFa,
});
