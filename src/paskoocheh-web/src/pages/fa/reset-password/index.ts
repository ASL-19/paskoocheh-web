import ResetPasswordRequestPage from "src/pageComponents/ResetPasswordRequestPage/ResetPasswordRequestPage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/ResetPasswordRequestPage/getResetPasswordRequestPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: ResetPasswordRequestPage,
  strings: stringsFa,
});
