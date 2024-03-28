import { replaceArabicNumeralsWithPersianNumerals } from "@asl-19/js-utils";

import { useAppLocaleInfo } from "src/stores/appStore";

const useStringWithLocalizedNumerals = (input: string | number) => {
  const { localeCode } = useAppLocaleInfo();

  const inputAsString = input.toString();

  return localeCode === "fa"
    ? replaceArabicNumeralsWithPersianNumerals(inputAsString)
    : inputAsString;
};

export default useStringWithLocalizedNumerals;
