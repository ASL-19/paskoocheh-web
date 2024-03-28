import ContactPage from "src/pageComponents/ContactPage/ContactPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/ContactPage/getContactPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: ContactPage,
  strings: stringsEn,
});
