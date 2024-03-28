import RewardsPage from "src/pageComponents/RewardsPage/RewardsPage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/RewardsPage/getRewardsPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: RewardsPage,
  strings: stringsFa,
});
