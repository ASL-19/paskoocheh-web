import SearchResultsPage from "src/pageComponents/SearchResultsPage/SearchResultsPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/SearchResultsPage/getSearchResultsPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: SearchResultsPage,
  strings: stringsEn,
});
