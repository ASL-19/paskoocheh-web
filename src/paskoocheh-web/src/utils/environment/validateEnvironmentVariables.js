const { cleanEnv, email, str, url } = require("envalid");

const booleanString = require("./validatorFunctions/booleanString.js");
const integerString = require("./validatorFunctions/integerString.js");
const protocolAndHost = require("./validatorFunctions/protocolAndHost.js");
const googleAnalyticsMeasurementId = require("./validatorFunctions/googleAnalyticsMeasurementId.js");

const validateEnvironmentVariables = () => {
  // ----------------------------------
  // --- Validate env using Envalid ---
  // ----------------------------------

  const env = cleanEnv(process.env, {
    NEXT_INTERNAL_ENABLE_WEBPACK_BUNDLE_ANALYZER: booleanString({
      default: "",
    }),
    NEXT_PUBLIC_BACKEND_URL: url(),
    NEXT_PUBLIC_BUILD_NUM: str({ default: "" }),
    NEXT_PUBLIC_CONTACT_EMAIL_ADDRESS: email(),
    NEXT_PUBLIC_ENABLE_APP_CATEGORIES_NAV: booleanString({ default: "" }),
    NEXT_PUBLIC_ENABLE_MOCK_GRAPHQL_SDK: booleanString({ default: "" }),
    NEXT_PUBLIC_ENABLE_REFERRAL: booleanString({ default: "" }),
    NEXT_PUBLIC_ENABLE_SEARCH_ENGINE_INDEXING: booleanString({ default: "" }),

    NEXT_PUBLIC_ENABLE_STANDALONE_REACT_DEVTOOLS: booleanString({
      default: "",
    }),
    NEXT_PUBLIC_GIT_SHORT_SHA: str({ default: "" }),
    NEXT_PUBLIC_GOOGLE_ANALYTICS_MEASUREMENT_ID: googleAnalyticsMeasurementId(),
    NEXT_PUBLIC_MOCK_GRAPHQL_SDK_DELAY: integerString({ default: "" }),
    NEXT_PUBLIC_REWARD_REDEMPTION_EMAIL_ADDRESS: email(),
    NEXT_PUBLIC_S3_BUCKET_NAME: str({ default: "" }),
    NEXT_PUBLIC_VERSION_NUM: str({ default: "" }),
    NEXT_PUBLIC_WEB_URL: protocolAndHost(),
  });

  // ---------------------------------------------------------------------------
  // --- Ensure env conforms to NodeJS.ProcessEnv (declared in lsw-env.d.ts) ---
  // ---------------------------------------------------------------------------

  /**
   * @type {Omit<NodeJS.ProcessEnv, "NODE_ENV">}
   */
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const typedEnv = env;

  // ------------------------------------------------------
  // --- Return env (used by mw-env.d.ts ValidEnv type) ---
  // ------------------------------------------------------

  return env;
};

module.exports = validateEnvironmentVariables;
