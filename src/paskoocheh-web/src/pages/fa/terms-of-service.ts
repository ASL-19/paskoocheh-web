import TermsOfServicePage from "src/pageComponents/TermsOfServicePage/TermsOfServicePage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/TermsOfServicePage/getTermsOfServicePageServerSideProps";

export default createLocalePageComponent({
  pageComponent: TermsOfServicePage,
  strings: stringsFa,
});
