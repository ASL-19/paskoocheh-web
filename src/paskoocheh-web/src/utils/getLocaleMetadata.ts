import { match } from "ts-pattern";

import { Direction } from "src/types/layoutTypes";
import { LocaleCode } from "src/values/localeValues";

// We may need to tweak this on a per-language basis
const dateTimeFormatOptions: Intl.DateTimeFormatOptions = {
  day: "numeric",
  month: "short",
  year: "numeric",
};

const getLocaleMetadata = (locale: LocaleCode | string) =>
  match<
    string,
    {
      /**
       * Intl.DateTimeFormat for locale.
       *
       * In some cases the DateTimeFormat is constructed with custom options
       * (e.g. for numbering system).
       */
      dateTimeFormatter: Intl.DateTimeFormat;
      /**
       * Writing direction ("ltr"/"rtl")
       */
      direction: Direction;
      /**
       * Language tags by localeCode.
       *
       * In some cases (e.g. Persian) we should specify a country-specific
       * dialect; in others (e.g. English) it doesn’t make sense to unless the
       * site is targeting a specific country).
       *
       * @see
       * https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/lang#language_tag_syntax
       */
      lang: string;
      /**
       * Two-letter LocaleCode
       */
      localeCode: LocaleCode;
      /**
       * Locale name in native language.
       *
       * These don’t need to be localized since they’re used for alternate
       * language links (e.g. on Persian site English link says "English")
       */
      nativeName: string;
      /**
       * Intl.NumberFormat for locale.
       */
      numberFormatter: Intl.NumberFormat;
    }
  >(locale)
    .with("fa", () => {
      const lang = "fa-IR";

      return {
        dateTimeFormatter: new Intl.DateTimeFormat(lang, dateTimeFormatOptions),
        direction: "rtl",
        lang,
        localeCode: "fa",
        nativeName: "فارسی", // cSpell:disable-line
        numberFormatter: new Intl.NumberFormat("en-US"),
      };
    })
    .otherwise(() => {
      const lang = "en";

      return {
        dateTimeFormatter: new Intl.DateTimeFormat(lang, dateTimeFormatOptions),
        direction: "ltr",
        lang,
        localeCode: "en",
        nativeName: "English",
        numberFormatter: new Intl.NumberFormat("en-US"),
      };
    });

export default getLocaleMetadata;
