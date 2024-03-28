import ResetPasswordRequestPage from "src/pageComponents/ResetPasswordRequestPage/ResetPasswordRequestPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/ResetPasswordRequestPage/getResetPasswordRequestPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: ResetPasswordRequestPage,
  strings: stringsEn,
});
