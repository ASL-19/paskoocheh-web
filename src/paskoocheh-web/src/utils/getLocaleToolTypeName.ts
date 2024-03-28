import { GqlToolType } from "src/generated/graphQl";
import { LocaleCode } from "src/values/localeValues";

/**
 * Given a toolType returns nameFa if `localeCode === "fa"` and the `nameFa`
 * field is set; otherwise `name`.
 */
const getLocaleToolTypeName = ({
  localeCode,
  toolType,
}: {
  localeCode: LocaleCode;
  toolType: GqlToolType;
}) =>
  localeCode === "fa" && toolType.nameFa ? toolType.nameFa : toolType.name;

export default getLocaleToolTypeName;
