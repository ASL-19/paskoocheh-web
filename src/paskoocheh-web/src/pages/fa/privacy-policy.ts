import PrivacyPolicyPage from "src/pageComponents/PrivacyPolicyPage/PrivacyPolicyPage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/PrivacyPolicyPage/getPrivacyPolicyPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: PrivacyPolicyPage,
  strings: stringsFa,
});
