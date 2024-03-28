const normalizeHtmlWhitespace = require("normalize-html-whitespace");

/**
 * This code checks if the browser supports the following required features, and
 * prevents  JS from loading if it doesn’t:
 *
 * - AbortController
 *
 * If the JS will be allowed to load, a `js` className is added to the
 * <html> element. This should be used in CSS to display no-JS
 * fallbacks/adaptations.
 *
 * This method is supported in browsers released since ~September 2015, and
 * notably not any version of Internet Explorer or the pre-Chrome Android
 * browser/webview.
 *
 * For incompatible browsers, it’s better if the client-side doesn’t attempt to
 * rehydrate the page since this could leave the page in a broken or empty
 * state. JS-free browsing will likely also lead to better perceived performance
 * since anyone running an outdated browser is probably also on outdated
 * hardware.
 *
 * Setting window.webpackJsonp to break the JS is an ugly hack -- it would be
 * preferable if Next.js had an official mechanism to preclude client-side
 * hydration, but as of 2019-10-30 it doesn’t.
 *
 * Note: This script isn’t transpiled, and therefore needs to be written in ES5
 * and widely-supported syntax (e.g. no trailing commas!) for browser
 * compatibility.
 *
 * @return string
 */
const getBeforeRenderScriptContent = () =>
  normalizeHtmlWhitespace(`
    (function () {
      var userAgent = window.navigator.userAgent;

      if (
        /iPad|iPhone|iPod/.test(userAgent) &&
        typeof window.MSStream === 'undefined'
      ) {
        document.documentElement.classList.add('userAgentIsIos');
      }

      if (
        typeof AbortController === "undefined" ||
        typeof URLSearchParams === "undefined"
      ) {
        window.webpackChunk_N_E = {
          0: [],
          length: 0,
          push: function () { },
          slice: function () { return [] }
        };

        return;
      }

      document.documentElement.classList.add("js");
    })();
  `);

module.exports = getBeforeRenderScriptContent;
