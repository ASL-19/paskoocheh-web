import HomePage from "src/pageComponents/HomePage/HomePage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/HomePage/getHomePageServerSideProps";

export default createLocalePageComponent({
  pageComponent: HomePage,
  strings: stringsFa,
});
