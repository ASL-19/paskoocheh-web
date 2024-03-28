// This is actually an import from @types/web-app-manifest; there is no
// corresponding web-app-manifest package.
//
// https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/web-app-manifest/index.d.ts
import { WebAppManifest } from "web-app-manifest";

import androidChrome192Png from "src/static/favicons/android-chrome-192x192.png";
import androidChrome512Png from "src/static/favicons/android-chrome-512x512.png";
import maskableIconPng from "src/static/favicons/maskable-icon-192x192.png";
import getLocaleMetadata from "src/utils/getLocaleMetadata";
import getServerLocaleStrings from "src/utils/getServerLocaleStrings";
import colors from "src/values/colors";
import { LocaleCode } from "src/values/localeValues";
const getManifestDataUrl = ({
  localeCode,
  webUrl,
}: {
  localeCode: LocaleCode;
  webUrl: string;
}) => {
  const strings = getServerLocaleStrings(localeCode);

  const localeMetadata = getLocaleMetadata(localeCode);

  const webManifestContent: WebAppManifest = {
    background_color: colors.shadesWhite,
    dir: localeMetadata.direction,
    display: "browser",
    icons: [
      {
        purpose: "maskable",
        sizes: "192x192",
        src: `${webUrl}${maskableIconPng.src}`,
        type: "image/png",
      },
      {
        sizes: "192x192",
        src: `${webUrl}${androidChrome192Png.src}`,
        type: "image/png",
      },
      {
        sizes: "512x512",
        src: `${webUrl}${androidChrome512Png.src}`,
        type: "image/png",
      },
    ],
    lang: localeMetadata.lang,
    name: strings.shared.siteTitle,
    orientation: "any",
    short_name: strings.shared.siteTitle,
    start_url: `${webUrl}/${localeCode}`,
    theme_color: colors.blue,
  };

  return `data:application/manifest+json,${encodeURIComponent(
    JSON.stringify(webManifestContent),
  )}`;
};

export default getManifestDataUrl;
