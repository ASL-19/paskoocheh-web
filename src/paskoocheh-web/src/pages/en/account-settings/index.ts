import AccountSettingPage from "src/pageComponents/AccountSettingsPage/AccountSettingsPage";
import stringsEn from "src/strings/stringsEn";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/AccountSettingsPage/getAccountSettingsPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: AccountSettingPage,
  strings: stringsEn,
});
