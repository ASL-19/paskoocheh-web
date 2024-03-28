import { Strings } from "src/types/stringTypes";

/**
 * Get `PageMeta` rendered title.
 */
const getPageMetaTitle = ({
  strings,
  title,
}: {
  strings: Strings;
  title: string | null;
}) =>
  title
    ? strings.PageMeta.pageTitleAndSiteTitle
        .replace("{pageTitle}", title)
        .replace("{siteTitle}", strings.shared.siteTitle)
    : strings.shared.siteTitle;

export default getPageMetaTitle;
