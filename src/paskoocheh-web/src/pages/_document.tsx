import Document, { Head, Html, Main, NextScript } from "next/document";

import getBeforeRenderScriptContent from "src/utils/document/getBeforeRenderScriptContent";
import getGoogleTagScriptContent from "src/utils/document/getGoogleTagScriptContent";
import getLocaleMetadata from "src/utils/getLocaleMetadata";
import getManifestDataUrl from "src/utils/getManifestDataUrl";
import { mediaStyles } from "src/utils/media/media";
import colors from "src/values/colors";

// ==============================
// === Get environment config ===
// ==============================

// =================================
// === Get inline script content ===
// =================================

const beforeRenderScriptContent = getBeforeRenderScriptContent();

const googleTagScriptContent = getGoogleTagScriptContent();

// =======================
// === Custom document ===
// =======================

class EgDocument extends Document {
  render() {
    const { direction, lang, localeCode } = getLocaleMetadata(
      this.props.dangerousAsPath.slice(1, 3),
    );

    const manifestDataUrl = getManifestDataUrl({
      localeCode,
      webUrl: process.env.NEXT_PUBLIC_WEB_URL,
    });

    return (
      <Html
        className={`${localeCode} ${direction}`}
        dir={direction}
        lang={lang}
      >
        <Head>
          {!process.env.NEXT_PUBLIC_ENABLE_SEARCH_ENGINE_INDEXING && (
            <meta name="robots" content="none" />
          )}

          <meta name="msapplication-TileColor" content={colors.shadesWhite} />
          <meta name="theme-color" content={colors.blue} />

          <meta
            name="NEXT_PUBLIC_BUILD_NUM"
            content={process.env.NEXT_PUBLIC_BUILD_NUM}
          />
          <meta
            name="NEXT_PUBLIC_CONTACT_EMAIL_ADDRESS"
            content={process.env.NEXT_PUBLIC_CONTACT_EMAIL_ADDRESS}
          />
          <meta
            name="NEXT_PUBLIC_ENABLE_APP_CATEGORIES_NAV"
            content={process.env.NEXT_PUBLIC_ENABLE_APP_CATEGORIES_NAV}
          />
          <meta
            name="NEXT_PUBLIC_ENABLE_MOCK_GRAPHQL_SDK"
            content={process.env.NEXT_PUBLIC_ENABLE_MOCK_GRAPHQL_SDK}
          />
          <meta
            name="NEXT_PUBLIC_ENABLE_REFERRAL"
            content={process.env.NEXT_PUBLIC_ENABLE_REFERRAL}
          />
          <meta
            name="NEXT_PUBLIC_ENABLE_SEARCH_ENGINE_INDEXING"
            content={process.env.NEXT_PUBLIC_ENABLE_SEARCH_ENGINE_INDEXING}
          />
          <meta
            name="NEXT_PUBLIC_ENABLE_STANDALONE_REACT_DEVTOOLS"
            content={process.env.NEXT_PUBLIC_ENABLE_STANDALONE_REACT_DEVTOOLS}
          />
          <meta
            name="NEXT_PUBLIC_GIT_SHORT_SHA"
            content={process.env.NEXT_PUBLIC_GIT_SHORT_SHA}
          />
          <meta
            name="NEXT_PUBLIC_GOOGLE_ANALYTICS_MEASUREMENT_ID"
            content={process.env.NEXT_PUBLIC_GOOGLE_ANALYTICS_MEASUREMENT_ID}
          />
          <meta
            name="NEXT_PUBLIC_BACKEND_URL"
            content={process.env.NEXT_PUBLIC_BACKEND_URL}
          />
          <meta
            name="NEXT_PUBLIC_S3_BUCKET_NAME"
            content={process.env.NEXT_PUBLIC_S3_BUCKET_NAME}
          />
          <meta
            name="NEXT_PUBLIC_VERSION_NUM"
            content={process.env.NEXT_PUBLIC_VERSION_NUM}
          />
          <meta
            name="NEXT_PUBLIC_WEB_URL"
            content={process.env.NEXT_PUBLIC_WEB_URL}
          />

          <link rel="manifest" href={manifestDataUrl} />

          <style
            type="text/css"
            dangerouslySetInnerHTML={{ __html: mediaStyles }}
          />

          {googleTagScriptContent && (
            <script
              dangerouslySetInnerHTML={{
                __html: googleTagScriptContent,
              }}
            />
          )}

          <script
            dangerouslySetInnerHTML={{
              __html: beforeRenderScriptContent,
            }}
          />

          {process.env.NEXT_PUBLIC_ENABLE_STANDALONE_REACT_DEVTOOLS && (
            // eslint-disable-next-line @next/next/no-sync-scripts
            <script src="http://localhost:8097" />
          )}
          {/* Adapted from https://github.com/zeit/next.js/tree/canary/packages/next-plugin-google-analytics */}
          {process.env.NEXT_PUBLIC_GOOGLE_ANALYTICS_MEASUREMENT_ID && (
            <script
              async
              src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GOOGLE_ANALYTICS_MEASUREMENT_ID}`}
            />
          )}
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

export default EgDocument;
