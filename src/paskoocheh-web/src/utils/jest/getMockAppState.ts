import { GqlPlatform } from "src/generated/graphQl";
import { AppState } from "src/stores/appStore";
import stringsEn from "src/strings/stringsEn";
import platformTestDataBySlug from "src/test/data/platformTestDataBySlug";
import getRefreshToken from "src/utils/api/getRefreshToken";
import getLocaleMetadata from "src/utils/getLocaleMetadata";
import { LocaleCode } from "src/values/localeValues";

const getMockAppState = ({
  localeCode,
  platforms,
}: {
  localeCode: LocaleCode;
  platforms?: Array<GqlPlatform>;
}): AppState => ({
  localeInfo: getLocaleMetadata(localeCode),
  platforms: platforms ?? Object.values(platformTestDataBySlug),
  routeChangeInfo: {
    routeChangeIsInProgress: false,
    routeChangeTimestamp: 0,
  },
  strings: stringsEn,
  username: getRefreshToken(),
});

export default getMockAppState;
