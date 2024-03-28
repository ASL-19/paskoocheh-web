import SignInPage from "src/pageComponents/SignInPage/SignInPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/SignInPage/getSignInPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: SignInPage,
  strings: stringsEn,
});
