import BlogPage from "src/pageComponents/BlogPage/BlogPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/BlogPage/getBlogPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: BlogPage,
  strings: stringsEn,
});
