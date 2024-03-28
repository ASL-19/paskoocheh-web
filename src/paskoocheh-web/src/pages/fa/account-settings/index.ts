import AccountSettingPage from "src/pageComponents/AccountSettingsPage/AccountSettingsPage";
import stringsFa from "src/strings/stringsFa";
import createLocalePageComponent from "src/utils/createLocalePageComponent";

export { default as getServerSideProps } from "src/pageComponents/AccountSettingsPage/getAccountSettingsPageServerSideProps";

export default createLocalePageComponent({
  pageComponent: AccountSettingPage,
  strings: stringsFa,
});
