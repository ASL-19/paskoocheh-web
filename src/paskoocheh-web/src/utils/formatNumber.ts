import { replaceArabicNumeralsWithPersianNumerals } from "@asl-19/js-utils";
import { match } from "ts-pattern";

import { LocaleCode } from "src/values/localeValues";

const formatNumber = ({
  decimalPoints = 0,
  localeCode,
  number,
  renderPositiveSign,
}: {
  decimalPoints?: number;
  localeCode: LocaleCode;
  number: number;
  renderPositiveSign?: boolean;
}) =>
  (number > 0 && renderPositiveSign ? "+" : number < 0 ? "-" : "") +
  match(Math.abs(number))
    .when(
      (absoluteNumber) => absoluteNumber < 1e3,
      (absoluteNumber) => {
        const fixedNumber = absoluteNumber.toFixed(decimalPoints);

        return match(localeCode)
          .with("en", () => fixedNumber)
          .with("fa", () =>
            replaceArabicNumeralsWithPersianNumerals(fixedNumber),
          )
          .exhaustive();
      },
    )
    .when(
      (absoluteNumber) => absoluteNumber >= 1e3 && absoluteNumber < 1e6,
      (absoluteNumber) => {
        const fixedNumber = (absoluteNumber / 1e3).toFixed(decimalPoints);

        return match(localeCode)
          .with("en", () => `${fixedNumber}K`)
          .with("fa", () =>
            // cSpell:disable-next-line
            replaceArabicNumeralsWithPersianNumerals(`${fixedNumber}هزار`),
          )
          .exhaustive();
      },
    )
    .when(
      (absoluteNumber) => absoluteNumber >= 1e6 && absoluteNumber < 1e9,
      (absoluteNumber) => {
        const fixedNumber = (absoluteNumber / 1e6).toFixed(decimalPoints);

        return match(localeCode)
          .with("en", () => `${fixedNumber}M`)
          .with("fa", () =>
            // cSpell:disable-next-line
            replaceArabicNumeralsWithPersianNumerals(`${fixedNumber}میلیون`),
          )
          .exhaustive();
      },
    )
    .otherwise((absoluteNumber) => absoluteNumber);

export default formatNumber;
