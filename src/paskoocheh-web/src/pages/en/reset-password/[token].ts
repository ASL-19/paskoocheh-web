import ResetPasswordPage from "src/pageComponents/ResetPasswordPage/ResetPasswordPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/ResetPasswordPage/getResetPasswordPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: ResetPasswordPage,
  strings: stringsEn,
});
