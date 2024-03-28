import CreateAnAccountPage from "src/pageComponents/CreateAnAccountPage/CreateAnAccountPage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/CreateAnAccountPage/getCreateAnAccountPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: CreateAnAccountPage,
  strings: stringsFa,
});
