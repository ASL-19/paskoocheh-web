const normalizeHtmlWhitespace = require("normalize-html-whitespace");

const getGoogleTagScriptContent = () =>
  process.env.NEXT_PUBLIC_GOOGLE_ANALYTICS_MEASUREMENT_ID
    ? /** @type {string} */ (
        normalizeHtmlWhitespace(`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', '${process.env.NEXT_PUBLIC_GOOGLE_ANALYTICS_MEASUREMENT_ID}');
        `)
      )
    : null;

module.exports = getGoogleTagScriptContent;
