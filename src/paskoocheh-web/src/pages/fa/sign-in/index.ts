import SignInPage from "src/pageComponents/SignInPage/SignInPage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/SignInPage/getSignInPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: SignInPage,
  strings: stringsFa,
});
