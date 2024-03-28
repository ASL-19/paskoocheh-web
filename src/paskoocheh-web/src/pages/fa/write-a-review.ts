import WriteAReviewPage from "src/pageComponents/WriteAReviewPage/WriteAReviewPage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/WriteAReviewPage/getWriteAReviewPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: WriteAReviewPage,
  strings: stringsFa,
});
