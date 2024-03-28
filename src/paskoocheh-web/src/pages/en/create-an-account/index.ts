import CreateAnAccountPage from "src/pageComponents/CreateAnAccountPage/CreateAnAccountPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/CreateAnAccountPage/getCreateAnAccountPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: CreateAnAccountPage,
  strings: stringsEn,
});
