import { GqlPlatform } from "src/generated/graphQl";
import { LocaleCode } from "src/values/localeValues";

const getPlatformDisplayNames = (platform: GqlPlatform, locale: LocaleCode) => {
  const platformDisplayName: string =
    locale === "fa" && platform.displayNameFa
      ? platform.displayNameFa
      : platform.displayName;

  return platformDisplayName;
};

export default getPlatformDisplayNames;
