import { getAbsoluteUrl } from "@asl-19/js-utils";
import Head from "next/head";
import { StaticImageData } from "next/image";
import { FC, memo } from "react";

import logoPrimaryOpenGraphPng from "src/static/pageMetaImages/logoPrimaryOpenGraph.png";
import logoPrimaryTwitterPng from "src/static/pageMetaImages/logoPrimaryTwitter.png";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import getLocaleMetadata from "src/utils/getLocaleMetadata";
import getPageMetaTitle from "src/utils/getPageMetaTitle";
import { LocaleCode, localeCodes } from "src/values/localeValues";

export type PageMetaStrings = {
  /**
   * Page title + site title (e.g. About us — Paskoocheh).
   *
   * Used if the page has a title.
   *
   * @param pageTitle - Title of page (e.g. “Events”)
   * @param siteTitle - Title of page (e.g. “Paskoocheh”)
   */
  pageTitleAndSiteTitle: string;

  /**
   * Description of entire site.
   *
   * Used for pages that don’t have a dedicated description, and for the
   * homepage.
   */
  siteDescription: string;
};

const PageMeta: FC<
  {
    description: string | null;
    image: StaticImageData | null;
    title: string | null;
  } & ( // isAvailableInAlternateLocales can only be true if canonicalPath is set
    | {
        canonicalPath: string;
        isAvailableInAlternateLocales: true | false;
      }
    | {
        canonicalPath: null;
        isAvailableInAlternateLocales: false;
      }
  )
> = memo(
  ({
    canonicalPath,
    description,
    image,
    isAvailableInAlternateLocales,
    title,
  }) => {
    const { localeCode } = useAppLocaleInfo();
    const strings = useAppStrings();

    const renderedDescription = description || strings.PageMeta.siteDescription;
    const renderedTitle = getPageMetaTitle({ strings, title });

    const openGraphImage = image ?? logoPrimaryOpenGraphPng;
    const twitterImage = image ?? logoPrimaryTwitterPng;

    const canonicalUrl = canonicalPath
      ? getAbsoluteUrl({
          protocolAndHost: process.env.NEXT_PUBLIC_WEB_URL,
          rootRelativeUrl: canonicalPath,
        })
      : null;

    /**
     * Alternate locale `<link>`s
     *
     * See https://developers.google.com/search/docs/advanced/crawling/localized-versions
     */
    const alternateLocaleLinks = isAvailableInAlternateLocales
      ? localeCodes
          .filter((localeCodesItem) => localeCodesItem !== localeCode)
          .map((alternateLocaleCode, index) => {
            const canonicalUrl = getAbsoluteUrl({
              protocolAndHost: process.env.NEXT_PUBLIC_WEB_URL,
              rootRelativeUrl: canonicalPath.replace(
                new RegExp(`^/${localeCode}`),
                `/${alternateLocaleCode}`,
              ),
            });
            const { lang } = getLocaleMetadata(
              localeCodes[index] as LocaleCode,
            );
            return (
              <link
                rel="alternate"
                href={canonicalUrl}
                hrefLang={lang}
                key={alternateLocaleCode}
              />
            );
          })
      : [];

    return (
      <Head>
        <title>{renderedTitle}</title>
        <meta property="og:title" content={title || strings.shared.siteTitle} />
        <meta
          name="twitter:title"
          content={title || strings.shared.siteTitle}
        />

        <meta name="description" content={renderedDescription} />
        <meta name="twitter:description" content={renderedDescription} />
        <meta property="og:description" content={renderedDescription} />

        {/* Image */}
        <meta
          property="og:image"
          content={`${process.env.NEXT_PUBLIC_WEB_URL}${openGraphImage.src}`}
        />
        <meta property="og:image:width" content={`${openGraphImage.width}`} />
        <meta property="og:image:height" content={`${openGraphImage.height}`} />
        <meta
          name="twitter:image"
          content={`${process.env.NEXT_PUBLIC_WEB_URL}${twitterImage.src}`}
        />

        {/* --------------------------------
        --- Canonical and alternate URLs ---
        -------------------------------- */}
        {canonicalUrl && (
          <>
            <link rel="canonical" href={canonicalUrl} />
            <meta property="og:url" content={canonicalUrl} />
          </>
        )}

        {alternateLocaleLinks}
      </Head>
    );
  },
);

PageMeta.displayName = "PageMeta";

export default PageMeta;
