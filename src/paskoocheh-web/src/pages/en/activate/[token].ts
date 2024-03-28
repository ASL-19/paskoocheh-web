import ActivateAccountPage from "src/pageComponents/ActivateAccountPage/ActivateAccountPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/ActivateAccountPage/getActivateAccountPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: ActivateAccountPage,
  strings: stringsEn,
});
