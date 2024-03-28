import HowPointsWorkPage from "src/pageComponents/HowPointsWorkPage/HowPointsWorkPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/HowPointsWorkPage/getHowPointsWorkPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: HowPointsWorkPage,
  strings: stringsEn,
});
