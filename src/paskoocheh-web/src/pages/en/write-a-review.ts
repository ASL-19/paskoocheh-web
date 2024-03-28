import WriteAReviewPage from "src/pageComponents/WriteAReviewPage/WriteAReviewPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/WriteAReviewPage/getWriteAReviewPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: WriteAReviewPage,
  strings: stringsEn,
});
