import ActivateAccountPage from "src/pageComponents/ActivateAccountPage/ActivateAccountPage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/ActivateAccountPage/getActivateAccountPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: ActivateAccountPage,
  strings: stringsFa,
});
