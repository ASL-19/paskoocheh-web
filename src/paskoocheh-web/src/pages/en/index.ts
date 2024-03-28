import HomePage from "src/pageComponents/HomePage/HomePage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/HomePage/getHomePageServerSideProps";

export default createLocalePageComponent({
  pageComponent: HomePage,
  strings: stringsEn,
});
