/* eslint-disable no-param-reassign */

const fs = require("fs");
const path = require("path");

const { getNextJsHeaders } = require("@asl-19/next-utils");

const getContentSecurityPolicyContent = require("./src/utils/document/getContentSecurityPolicyContent");
const validateEnvironmentVariables = require("./src/utils/environment/validateEnvironmentVariables");

const isTestBuild = (process.env.npm_lifecycle_event ?? "").startsWith("test");

// ======================================================================
// === Read src/revision.txt into process.env.NEXT_PUBLIC_VERSION_NUM ===
// ======================================================================
//
try {
  process.env.NEXT_PUBLIC_VERSION_NUM = fs
    .readFileSync(path.join(__dirname, "../revision.txt"), "utf8")
    .trim();
} catch {
  /* empty */
}

// ============================
// === Validate process.env ===
// ============================
//
// Will stop build if any process.env.NEXT_ values are missing or invalid.

validateEnvironmentVariables();

// ======================
// === Next.js config ===
// ======================

/** @typedef {import('next/dist/server/config').NextConfig} NextConfig */

/* eslint-disable sort-keys-fix/sort-keys-fix */

/** @type {NextConfig["headers"]} */
const headers = async () => [
  {
    source: "/(.*)",
    headers: getNextJsHeaders({
      "Cache-Control": "public, max-age=0, s-maxage=315360000",
      "Content-Security-Policy": getContentSecurityPolicyContent(),
      // TODO: Enable once dev server media files are behind CloudFront
      // "Cross-Origin-Embedder-Policy": NEXT_PUBLIC_WEB_URL.startsWith("https")
      //   ? "require-corp"
      //   : "unsafe-none",
      "Cross-Origin-Opener-Policy": "same-origin",
      "Cross-Origin-Resource-Policy": "same-origin",
      "Permissions-Policy":
        "accelerometer=(), camera=(), display-capture=(), gamepad=(), geolocation=(), gyroscope=(), hid=(), idle-detection=(), magnetometer=(), microphone=(), midi=(), payment=(), publickey-credentials-get=(), screen-wake-lock=(), serial=(), usb=(), xr-spatial-tracking=()",
      "Referrer-Policy": "same-origin",
      "Strict-Transport-Security": "max-age=15724800; includeSubDomains",
      "X-Content-Type-Options": "nosniff",
      "X-Frame-Options": "DENY",
      "X-XSS-Protection": "1; mode=block",
    }),
  },
];

/** @type {import('next/dist/server/config').NextConfig["images"]} */
const images = {
  // Without this Playwright tests fail with "[WebServer] TypeError: fetch
  // failed […] at async imageOptimizer"
  //
  // This seems to be related to https://github.com/vercel/next.js/issues/44062
  unoptimized: isTestBuild,
  minimumCacheTTL: 315360000,
  remotePatterns: [
    process.env.NEXT_PUBLIC_WEB_URL,
    `${process.env.NEXT_PUBLIC_BACKEND_URL}/media/`,
  ].map((imageSource) => {
    const imageSourceUrl = new URL(imageSource);

    return {
      hostname: imageSourceUrl.hostname,
      protocol: imageSourceUrl.protocol.startsWith("https") ? "https" : "http",
    };
  }),
};

/** @type {import('next/dist/server/config').NextConfig["redirects"]} */
const redirects = async () => [
  // -------------------
  // --- Legacy URLs ---
  // -------------------
  // TODO: is anything missing?
  {
    source: "/about.html",
    destination: "/fa/about",
    statusCode: 301,
  },
  {
    source: "/blog/posts/",
    destination: "/fa/blog",
    statusCode: 301,
  },
  {
    source: "/blog/posts/:slug*.html",
    destination: "/fa/blog/:slug*",
    statusCode: 301,
  },
  {
    source: "/contact.html",
    destination: "/fa/write-your-message",
    statusCode: 301,
  },
  {
    source: "/privacy-policy.html",
    destination: "/fa/privacy-policy",
    statusCode: 301,
  },
  {
    source: "/terms-of-service.html",
    destination: "/fa/terms-of-service",
    statusCode: 301,
  },
  // -------------------------
  // --- General redirects ---
  // -------------------------
  {
    source: "/",
    destination: "/fa",
    statusCode: 301,
  },
  {
    source: "/index.html",
    destination: "/",
    statusCode: 301,
  },
  {
    source: "/:path*/index.html",
    destination: "/:path*",
    statusCode: 301,
  },
];

/** @type {import('next/dist/server/config').NextConfig["rewrites"]} */
const rewrites = async () => [
  // Some browsers will look for /apple-touch-icon.png and /favicon.ico in some
  // scenarios, so they need to be accessible from the root. (Most modern
  // browsers will use the icons specified in the _document.tsx’s manifest data
  // URL or <link> tags.)
  {
    source: "/apple-touch-icon.png",
    destination: "/api/apple-touch-icon-png",
  },
  {
    source: "/favicon.ico",
    destination: "/api/favicon-ico",
  },
];

/* eslint-enable sort-keys-fix/sort-keys-fix */

/** @type {NextConfig["webpack"]} */
const webpack = (config, options) => {
  config.resolve.alias = {
    ...config.resolve.alias,
    // Remove unused parts of the graphql-request package from our bundle
    "./graphql-ws.js": false,
    "cross-fetch$": false,
    graphql$: false,
    // Replace getGraphQlSdk with mock if NEXT_PUBLIC_ENABLE_MOCK_GRAPHQL_SDK
    ...(process.env.NEXT_PUBLIC_ENABLE_MOCK_GRAPHQL_SDK
      ? {
          "src/utils/config/getGraphQlSdk":
            "src/utils/config/__mocks__/getGraphQlSdk",
        }
      : {}),
  };

  if (!options.isServer) {
    if (process.env.NEXT_INTERNAL_ENABLE_WEBPACK_BUNDLE_ANALYZER) {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore (webpack-bundle-analyzer is in devDependencies so
      // won’t exist on CI)
      const { BundleAnalyzerPlugin } = require("webpack-bundle-analyzer");

      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: "static",
          reportFilename: options.isServer
            ? "../analyze/server.html"
            : "./analyze/client.html",
        }),
      );
    }

    if (config.optimization.splitChunks) {
      /**
       * @type {typeof import("src/values/localeValues").localeCodes}
       */
      const localeCodes = /** @type {const} */ (["en", "fa"]);

      localeCodes.forEach((localeCode) => {
        const stringsFileName = `strings${(localeCode[0] || "").toUpperCase()}${
          localeCode[1] || ""
        }`;

        config.optimization.splitChunks.cacheGroups[stringsFileName] = {
          chunks: "all",
          enforce: true,
          name: stringsFileName,
          test: RegExp(`src/strings/${stringsFileName}.*`),
        };
      });
    }
  }

  return config;
};

/** @type {NextConfig} */
const nextConfig = {
  compiler: {
    emotion: true,
  },
  // Build test builds into ".next-test" to keep test builds separate from
  // regular builds, and to allow E2E tests to run while regular server is
  // running.
  distDir: isTestBuild ? ".next-test" : ".next",
  eslint: {
    ignoreDuringBuilds: true,
  },
  experimental: {
    scrollRestoration: true,
  },
  headers,
  images,
  output: "standalone",
  redirects,
  rewrites,
  webpack,
};

module.exports = nextConfig;
