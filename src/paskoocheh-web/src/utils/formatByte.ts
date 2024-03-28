import { replaceArabicNumeralsWithPersianNumerals } from "@asl-19/js-utils";
import { match } from "ts-pattern";

import { LocaleCode } from "src/values/localeValues";

const formatByte = ({
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
      (absoluteNumber) => absoluteNumber < 1024,
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
      (absoluteNumber) =>
        absoluteNumber >= 1024 && absoluteNumber < 1024 * 1024,
      (absoluteNumber) => {
        const fixedNumber = (absoluteNumber / 1024).toFixed(decimalPoints);

        return match(localeCode)
          .with("en", () => `${fixedNumber}KB`)
          .with("fa", () =>
            // cSpell:disable-next-line
            replaceArabicNumeralsWithPersianNumerals(`${fixedNumber}کیلوبایت`),
          )
          .exhaustive();
      },
    )
    .when(
      (absoluteNumber) =>
        absoluteNumber >= 1024 * 1024 && absoluteNumber < 1024 * 1024 * 1024,
      (absoluteNumber) => {
        const fixedNumber = (absoluteNumber / (1024 * 1024)).toFixed(
          decimalPoints,
        );

        return match(localeCode)
          .with("en", () => `${fixedNumber}MB`)
          .with("fa", () =>
            // cSpell:disable-next-line
            replaceArabicNumeralsWithPersianNumerals(`${fixedNumber}مگابایت`),
          )
          .exhaustive();
      },
    )
    .otherwise((absoluteNumber) => absoluteNumber);

export default formatByte;
