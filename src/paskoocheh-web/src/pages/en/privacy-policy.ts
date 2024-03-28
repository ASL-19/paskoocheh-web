import PrivacyPolicyPage from "src/pageComponents/PrivacyPolicyPage/PrivacyPolicyPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/PrivacyPolicyPage/getPrivacyPolicyPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: PrivacyPolicyPage,
  strings: stringsEn,
});
