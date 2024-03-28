const { createHash } = require("crypto");
const {
  DATA,
  NONE,
  SELF,
  UNSAFE_EVAL,
  UNSAFE_INLINE,
  getCSP,
} = require("csp-header");

const getBeforeRenderScriptContent = require("./getBeforeRenderScriptContent");
const { P, match } = require("ts-pattern");
const getGoogleTagScriptContent = require("./getGoogleTagScriptContent");

/**
 * Get Content-Security-Policy (CSP) header content.
 */
const getContentSecurityPolicyContent = () => {
  const graphQlUrlOrigin = new URL(
    `${process.env.NEXT_PUBLIC_BACKEND_URL}/graphql/`,
  ).origin;
  const storageUrlOrigin = new URL(
    `${process.env.NEXT_PUBLIC_BACKEND_URL}/media/`,
  ).origin;

  const beforeRenderScriptContentSha256Hash = createHash("sha256")
    .update(getBeforeRenderScriptContent())
    .digest("base64");

  const googleTagScriptContentSha256Hash = match(getGoogleTagScriptContent())
    .with(P.string, (googleTagScriptContent) =>
      createHash("sha256").update(googleTagScriptContent).digest("base64"),
    )
    .otherwise(() => null);

  /**
   * This is the hash of `<script crossorigin="anonymous" nomodule>` injected by
   * Next.js near the bottom of <body>
   *
   * See https://cli.vuejs.org/guide/browser-compatibility.html#modern-mode (Vue
   * uses the same approach)
   */
  const nextJsNomoduleScriptContentSha256Hash =
    "4RS22DYeB7U14dra4KcQYxmwt5HkOInieXK1NUMBmQI=";

  return getCSP({
    directives: {
      "base-uri": [SELF],
      "connect-src": [
        SELF,
        graphQlUrlOrigin,
        "https://www.google-analytics.com",
        ...(process.env.NODE_ENV === "development"
          ? [process.env.NEXT_PUBLIC_WEB_URL.replace("http://", "ws://")]
          : []),
        ...(process.env.NEXT_PUBLIC_ENABLE_STANDALONE_REACT_DEVTOOLS === "true"
          ? ["ws://localhost:8097"]
          : []),
      ],
      "default-src": [
        SELF,
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/media/`,
        "https://www.youtube.com/",
      ],
      "frame-ancestors": [NONE],
      "frame-src": [
        "https://www.youtube.com",
        "https://www.youtube-nocookie.com",
      ],
      "img-src": [
        SELF,
        DATA,
        graphQlUrlOrigin,
        storageUrlOrigin,
        "https://www.google-analytics.com",
        // Dev server returns S3 URLs so we add an exception here (using a
        // workaround to avoid including our internal server URLs in the code)
        //
        // TODO: Can we remove this later? Seems like the referenced files don’t
        // exist, at least on dev
        ...((`${process.env.NEXT_PUBLIC_BACKEND_URL}/media/`.match(/\./g) || [])
          .length > 1
          ? ["https://s3.amazonaws.com"]
          : []),
      ],
      "manifest-src": [DATA],
      "media-src": [storageUrlOrigin],
      "object-src": [NONE],
      "script-src": [
        SELF,
        "https://www.google-analytics.com",
        "https://www.googletagmanager.com",
        ...(process.env.NODE_ENV !== "development"
          ? [
              `'sha256-${beforeRenderScriptContentSha256Hash}'`,
              `'sha256-${nextJsNomoduleScriptContentSha256Hash}'`,
              ...(googleTagScriptContentSha256Hash
                ? [`'sha256-${googleTagScriptContentSha256Hash}'`]
                : []),
            ]
          : [UNSAFE_EVAL, UNSAFE_INLINE]), // required for Next.js hot code reloading
        ...(process.env.NEXT_PUBLIC_ENABLE_STANDALONE_REACT_DEVTOOLS === "true"
          ? ["http://localhost:8097"]
          : []),
      ],
      "style-src": [SELF, UNSAFE_INLINE],
      "upgrade-insecure-requests":
        process.env.NEXT_PUBLIC_WEB_URL.startsWith("https"),
    },
  });
};

module.exports = getContentSecurityPolicyContent;
