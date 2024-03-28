import { constructUrl } from "@asl-19/js-utils";

import { postsPerPage } from "src/values/indexPageValues";
import { LocaleCode } from "src/values/localeValues";

const getNormalizedBlogItemsCount = (count?: number) =>
  count === undefined || count === postsPerPage ? undefined : count;

const routeUrls = {
  about: ({
    localeCode,
    platform,
  }: {
    localeCode: LocaleCode;
    platform: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/about`,
      querySegments: {
        platform,
      },
    }),

  account: ({
    localeCode,
    platform,
  }: {
    localeCode: LocaleCode;
    platform: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/account-settings`,
      querySegments: {
        platform,
      },
    }),

  accountSettingsSuccess: ({
    localeCode,
    platform,
  }: {
    localeCode: LocaleCode;
    platform: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/account-settings/success`,
      querySegments: {
        platform,
      },
    }),

  activate: ({
    localeCode,
    token,
  }: {
    localeCode: LocaleCode;
    token: string;
  }) => `/${localeCode}/activate/${token}`,

  app: ({
    localeCode,
    platform,
    slug,
    toolType,
  }: {
    localeCode: LocaleCode;
    platform: string;
    slug: string;
    toolType: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/${toolType}/${slug}`,
      querySegments: {
        platform,
      },
    }),

  blog: ({
    count,
    localeCode,
    order,
    platform,
    topic,
  }: {
    count?: number;
    localeCode: LocaleCode;
    order?: string;
    platform: string;
    topic?: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/blog`,
      querySegments: {
        count: getNormalizedBlogItemsCount(count),
        order: order === "-published" ? undefined : order,
        platform,
        topic: topic === "all" ? undefined : topic,
      },
    }),

  blogPost: ({
    localeCode,
    platform,
    slug,
  }: {
    localeCode: LocaleCode;
    platform: string;
    slug: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/blog/${slug}`,
      querySegments: {
        platform,
      },
    }),

  contact: ({
    localeCode,
    platform,
    tool,
  }: {
    localeCode: LocaleCode;
    platform: string;
    tool?: number | null;
  }) =>
    constructUrl({
      path: `/${localeCode}/contact`,
      querySegments: {
        platform,
        tool,
      },
    }),

  contactEmail: ({
    appId,
    localeCode,
    platform,
  }: {
    appId?: string;
    localeCode: LocaleCode;
    platform: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/contact/email`,
      querySegments: {
        appId,
        platform,
      },
    }),

  createAnAccount: ({
    localeCode,
    platform,
    referral,
  }: {
    localeCode: LocaleCode;
  } & (
    | {
        platform: string;
        referral?: never;
      }
    | {
        platform?: never;
        referral?: string;
      }
  )) =>
    constructUrl({
      path: `/${localeCode}/create-an-account`,
      querySegments: {
        platform,
        referral,
      },
    }),

  home: ({
    category,
    localeCode,
    platform,
  }: {
    category?: string;
    localeCode: LocaleCode;
    platform: string;
  }) =>
    constructUrl({
      path: `/${localeCode}`,
      querySegments: {
        category: category === "all" ? undefined : category,
        platform,
      },
    }),

  privacyPolicy: ({
    localeCode,
    platform,
  }: {
    localeCode: LocaleCode;
    platform: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/privacy-policy`,
      querySegments: {
        platform,
      },
    }),

  resetPassword: ({
    localeCode,
    platform,
    token,
  }: {
    localeCode: LocaleCode;
    platform: string;
    token: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/reset-password/${token}`,
      querySegments: {
        platform,
      },
    }),

  resetPasswordRequest: ({
    localeCode,
    platform,
  }: {
    localeCode: LocaleCode;
    platform: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/reset-password`,
      querySegments: {
        platform,
      },
    }),

  rewards: ({
    localeCode,
    platform,
  }: {
    localeCode: LocaleCode;
    platform: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/rewards`,
      querySegments: {
        platform,
      },
    }),

  rewardsHowPointsWork: ({
    localeCode,
    platform,
  }: {
    localeCode: LocaleCode;
    platform: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/rewards/how-points-work`,
      querySegments: {
        platform,
      },
    }),

  searchResults: ({
    category,
    localeCode,
    platform,
    query,
  }: {
    category?: string;
    localeCode: LocaleCode;
    platform: string;
    query?: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/search-results`,
      querySegments: {
        category,
        platform,
        query,
      },
    }),

  signIn: ({
    localeCode,
    platform,
    returnPath,
  }: {
    localeCode: LocaleCode;
    platform: string;
    returnPath?: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/sign-in`,
      querySegments: {
        platform,
        returnPath,
      },
    }),

  termsOfService: ({
    localeCode,
    platform,
  }: {
    localeCode: LocaleCode;
    platform: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/terms-of-service`,
      querySegments: {
        platform,
      },
    }),

  writeAReview: ({
    appId,
    localeCode,
    platform,
  }: {
    appId: string;
    localeCode: LocaleCode;
    platform: string;
  }) =>
    constructUrl({
      path: `/${localeCode}/write-a-review`,
      querySegments: {
        appId,
        platform,
      },
    }),

  writeYourMessage: ({
    localeCode,
    platform,
    tool,
  }: {
    localeCode: LocaleCode;
    platform: string;
    // TODO: Change to toolSlug once #559 is done
    tool?: number | null;
  }) =>
    constructUrl({
      path: `/${localeCode}/write-your-message`,
      querySegments: { platform, tool },
    }),
} satisfies {
  [routeName: string]: (routeArgs: {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    [routeArgument: string]: any;
    localeCode: LocaleCode;
  }) => string;
};

export default routeUrls;
