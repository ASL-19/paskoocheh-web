import ContactPage from "src/pageComponents/ContactPage/ContactPage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/ContactPage/getContactPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: ContactPage,
  strings: stringsFa,
});
