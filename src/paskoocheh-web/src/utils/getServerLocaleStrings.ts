import { match } from "ts-pattern";

import stringsEn from "src/strings/stringsEn";
import stringsFa from "src/strings/stringsFa";
import { LocaleCode } from "src/values/localeValues";

/**
 * __Important__: This should only be used on the server to avoid bundling every
 * locale’s strings in every locale’s bundle!
 */
const getServerLocaleStrings = (localeCode: LocaleCode) => {
  if (process.env.NODE_ENV !== "test" && typeof window !== "undefined") {
    console.warn(
      "getServerLocaleStrings called in browser! Replace with useAppLocaleInfo().strings or every locale’s strings will be bundled with every page.",
    );
  }

  return match(localeCode)
    .with("en", () => stringsEn)
    .with("fa", () => stringsFa)
    .exhaustive();
};

export default getServerLocaleStrings;
