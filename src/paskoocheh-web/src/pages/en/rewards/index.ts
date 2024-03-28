import RewardsPage from "src/pageComponents/RewardsPage/RewardsPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/RewardsPage/getRewardsPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: RewardsPage,
  strings: stringsEn,
});
