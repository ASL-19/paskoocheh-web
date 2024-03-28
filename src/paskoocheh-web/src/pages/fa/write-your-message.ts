import WriteYourMessagePage from "src/pageComponents/WriteYourMessagePage/WriteYourMessagePage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/WriteYourMessagePage/getWriteYourMessagePageServerSideProps";

export default createLocalePageComponent({
  pageComponent: WriteYourMessagePage,
  strings: stringsFa,
});
