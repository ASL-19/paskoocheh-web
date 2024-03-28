import AppPage from "src/pageComponents/AppPage/AppPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/AppPage/getAppPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: AppPage,
  strings: stringsEn,
});
