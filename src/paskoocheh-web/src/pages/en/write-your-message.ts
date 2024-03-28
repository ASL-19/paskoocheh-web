import WriteYourMessagePage from "src/pageComponents/WriteYourMessagePage/WriteYourMessagePage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/WriteYourMessagePage/getWriteYourMessagePageServerSideProps";

export default createLocalePageComponent({
  pageComponent: WriteYourMessagePage,
  strings: stringsEn,
});
