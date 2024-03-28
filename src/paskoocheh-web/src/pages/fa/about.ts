import AboutPage from "src/pageComponents/AboutPage/AboutPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/AboutPage/getAboutPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: AboutPage,
  strings: stringsEn,
});
