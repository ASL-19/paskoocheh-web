/* eslint-disable @typescript-eslint/consistent-type-definitions, @typescript-eslint/no-unused-vars, no-var */

type ValidEnv = ReturnType<
  typeof import("src/utils/environment/validateEnvironmentVariables.js")
>;

declare namespace globalThis {
  var asl19StoreStates;

  var graphQlSdkOverrides:
    | undefined
    | {
        doSendPasswordResetEmail?: import("src/generated/graphQl").GqlDoSendPasswordResetEmail;
        doSignUp?: import("src/generated/graphQl").GqlDoSignUp;
        doTokenAuth?: import("src/generated/graphQl").GqlDoTokenAuth;
        getEarningMethodsResponse?: import("src/generated/graphQl").GqlGetEarningMethods;
        getHasFinishedQuizResponse?: import("src/generated/graphQl").GqlGetHasFinishedQuiz;
        getHomePageFeaturedToolResponse?: import("src/generated/graphQl").GqlGetHomePageFeaturedTool;
        getPlatformsResponse?: import("src/generated/graphQl").GqlGetPlatforms;
        getPostPreviewsResponse?: import("src/generated/graphQl").GqlGetPostPreviews;
        getPostResponse?: import("src/generated/graphQl").GqlGetPost;
        getQuizzesResponse?: import("src/generated/graphQl").GqlGetQuizzes;
        getRedemptionMethodsResponse?: import("src/generated/graphQl").GqlGetRedemptionMethods;
        getRewardRecordsResponse?: import("src/generated/graphQl").GqlGetRewardsRecords;
        getStaticPageResponse?: import("src/generated/graphQl").GqlGetStaticPage;
        getTempS3Url?: import("src/generated/graphQl").GqlGetTempS3Url;
        getToolResponse?: import("src/generated/graphQl").GqlGetTool;
        getToolTypesResponse?: import("src/generated/graphQl").GqlGetToolTypes;
        getTopicsResponse?: import("src/generated/graphQl").GqlGetTopics;
        getUserBalance?: import("src/generated/graphQl").GqlGetUserBalance;
        getUserPurchasedAppsResponse?: import("src/generated/graphQl").GqlGetUserPurchasedApps;
        getVersionPreviewResponse?: import("src/generated/graphQl").GqlGetVersionPreview;
        getVersionPreviewsResponse?: import("src/generated/graphQl").GqlGetVersionPreviews;
        getVersionResponse?: import("src/generated/graphQl").GqlGetVersion;
      };
}

declare namespace NodeJS {
  type ProcessEnv = {
    /**
     * Set to "true" if running in a CI environment. Don’t use this in
     * application code!
     *
     * We use this to increase Jest timeouts in CI.
     */
    CI?: "true";

    /**
     * [OPTIONAL] Should Webpack Bundle Analyzer run during build?
     *
     * If enabled a browser window will open with a bundle visualization.
     *
     * Must be set to "true" or "" if provided.
     */
    NEXT_INTERNAL_ENABLE_WEBPACK_BUNDLE_ANALYZER?: ValidEnv["NEXT_INTERNAL_ENABLE_WEBPACK_BUNDLE_ANALYZER"];

    /**
     * BACKEND URL.
     *
     * e.g. "http://example.com/BACKEND/"
     */
    NEXT_PUBLIC_BACKEND_URL: ValidEnv["NEXT_PUBLIC_BACKEND_URL"];

    /**
     * [OPTIONAL] Unique build number.
     *
     * Exists purely to expose in page <head>; not used in any app logic.
     *
     * e.g. "123456"
     */
    NEXT_PUBLIC_BUILD_NUM: ValidEnv["NEXT_PUBLIC_BUILD_NUM"];

    /**
     * Contact email address, used in the footer.
     *
     * e.g. "bia\@paskoocheh.com"
     */
    NEXT_PUBLIC_CONTACT_EMAIL_ADDRESS: string;

    /**
     * [OPTIONAL] Should the app categories navigation be displayed?
     *
     * This is a temporary flag that can be removed once !667 is merged.
     *
     * Must be set to "true" or "" if provided.
     */
    NEXT_PUBLIC_ENABLE_APP_CATEGORIES_NAV: ValidEnv["NEXT_PUBLIC_ENABLE_APP_CATEGORIES_NAV"];

    /**
     * [OPTIONAL] Should app be built with the mock GraphQL SDK?
     *
     * If enabled getGraphQlSdk() will return a mock version that returns local
     * static test data.
     *
     * Must be set to "true" or "" if provided.
     */
    NEXT_PUBLIC_ENABLE_MOCK_GRAPHQL_SDK?: ValidEnv["NEXT_PUBLIC_ENABLE_MOCK_GRAPHQL_SDK"];

    /**
     * [OPTIONAL] Should referral link be enabled?
     *
     * If enabled the front end will allow user to create new account from
     * referral link
     *
     * Must be set to "true" or "" if provided.
     */
    NEXT_PUBLIC_ENABLE_REFERRAL?: ValidEnv["NEXT_PUBLIC_ENABLE_REFERRAL"];

    /**
     * [OPTIONAL] Should the site be indexable by Google (and other search
     * engines)?
     *
     * If not set the frontend will send `<meta name="robots" content="none" />`
     * to prevent search indexing.
     *
     * Must be set to "true" or "" if provided.
     */
    NEXT_PUBLIC_ENABLE_SEARCH_ENGINE_INDEXING?: ValidEnv["NEXT_PUBLIC_ENABLE_SEARCH_ENGINE_INDEXING"];

    /**
     * [OPTIONAL] Should app connect to standalone React DevTools?
     *
     * Should only be used in development.
     *
     * Must be set to "true" or "" if provided.
     *
     * @see
     * https://github.com/facebook/react/tree/master/packages/react-devtools#usage-with-react-dom
     */
    NEXT_PUBLIC_ENABLE_STANDALONE_REACT_DEVTOOLS?: ValidEnv["NEXT_PUBLIC_ENABLE_STANDALONE_REACT_DEVTOOLS"];

    /**
     * [OPTIONAL] Git short SHA of commit that triggered release.
     *
     * Exists purely to expose in page <head>; not used in any app logic.
     *
     * e.g. "0a1b2c3d"
     */
    NEXT_PUBLIC_GIT_SHORT_SHA: ValidEnv["NEXT_PUBLIC_GIT_SHORT_SHA"];

    /**
     * Google Analytics Measurement ID.
     *
     * e.g. "G-XXXXXXXXXX"
     */
    NEXT_PUBLIC_GOOGLE_ANALYTICS_MEASUREMENT_ID: ValidEnv["NEXT_PUBLIC_GOOGLE_ANALYTICS_MEASUREMENT_ID"];

    /**
     * [OPTIONAL] Artificial delay (in ms) of mock getGraphQlSdk.
     *
     * If provided the getGraphQlSdk promise will resolve in the provided time
     * +/- 50%.
     *
     * Useful for testing e.g. loading behaviour while using mock API.
     */
    NEXT_PUBLIC_MOCK_GRAPHQL_SDK_DELAY?: ValidEnv["NEXT_PUBLIC_MOCK_GRAPHQL_SDK_DELAY"];

    /**
     * Rewards Contact email address, used in RewardsPage Redemption.
     *
     * e.g. "reward\@paskoocheh.com"
     */
    NEXT_PUBLIC_REWARD_REDEMPTION_EMAIL_ADDRESS: string;

    /**
     * [OPTIONAL] S3 bucket name (used for S3 downloads).
     *
     * This may be removed in the future
     *
     * e.g. "1.0.0"
     */
    NEXT_PUBLIC_S3_BUCKET_NAME: ValidEnv["NEXT_PUBLIC_S3_BUCKET_NAME"];

    /**
     * [OPTIONAL] Version number.
     *
     * This is set to the content of src/revision.txt during the frontend build
     * (should not be set from the outside).
     *
     * e.g. "1.0.0"
     */
    NEXT_PUBLIC_VERSION_NUM: ValidEnv["NEXT_PUBLIC_VERSION_NUM"];

    /**
     * Web URL
     *
     * Web front-end public URL (without trailing slash).
     *
     * e.g. "https://example.com"
     */
    NEXT_PUBLIC_WEB_URL: ValidEnv["NEXT_PUBLIC_WEB_URL"];

    NODE_ENV: "development" | "test" | "production";

    /**
     * Name of the current NPM script. Don’t use this in application code!
     *
     * Note that this isn’t necessarily the script you called because
     * `npm-run-all`/`run-s`/`run-p` start sub-scripts/shells.
     *
     * @see
     * https://docs.npmjs.com/cli/v9/using-npm/scripts#current-lifecycle-event
     */
    npm_lifecycle_event?: string;
  };
}

let gtag: Gtag.Gtag | undefined;
