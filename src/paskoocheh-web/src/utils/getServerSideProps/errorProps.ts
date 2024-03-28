import { serverLog } from "@asl-19/js-utils";
import type { ServerResponse } from "http";

import { ErrorPageContentProps } from "src/components/ErrorPageContent";
import { GqlPlatform } from "src/generated/graphQl";
import stringsEn from "src/strings/stringsEn";
import { StringKey } from "src/types/stringTypes";
import getStringByDotSeparatedKey from "src/utils/getStringByDotSeparatedKey";

/**
 * Get ErrorPageContent props (which _app uses to render error page instead of
 * page component); log error in Node process; set document response statusCode
 * and `Cache-Control` header based on provided statusCode.
 */
const errorProps = ({
  descriptionStringKey = null,
  error,
  logMessage,
  platforms,
  res,
  statusCode,
}: {
  /**
   * Dot-separated string key.
   *
   * The corresponding English string will be logged in English; the localized
   * string will be rendered in place of the generic description in
   * ErrorPageContent.
   */
  descriptionStringKey?: StringKey | null;

  /**
   * Error object. Will be logged (including stack trace) if provided.
   *
   * The getServerSideProps catch block’s error object should always be passed.
   *
   * @remarks
   * This is typed unknown because the type of catch block error objects
   * inherently can’t be known. Because this value is just passed to
   * console.error there’s no scenario where a wrongly-typed object could cause
   * a failure.
   */
  error?: unknown;

  /**
   * Log-specific message.
   *
   * Good for internal failure reason that isn’t appropriate to present to the
   * user via descriptionStringKey.
   */
  logMessage?: string;

  /**
   * Array of platforms (or `null` if the error prevented fetching the
   * platforms).
   */
  platforms: Array<GqlPlatform> | null;

  /**
   * Response object (object parameter of getServerSideProps).
   *
   * Required to manipulate status code before response sent to browser, and to
   * determine URL of request.
   */
  res: ServerResponse;

  /**
   * Response status code.
   *
   * One of:
   *
   * - 400: Bad Request (e.g. if the query string is malformed)
   * - 404: Not Found (e.g. if the requested item doesn’t exist)
   * - 500: Internal Server Error (e.g. if the GraphQL API request fails)
   */
  statusCode: 400 | 404 | 500;
}): {
  props: {
    error: ErrorPageContentProps;
  };
} => {
  const descriptionValue =
    logMessage ??
    (typeof descriptionStringKey === "string"
      ? getStringByDotSeparatedKey({
          dotSeparatedKey: descriptionStringKey,
          strings: stringsEn,
        })
      : undefined);

  if (statusCode !== 404) {
    res.setHeader("Cache-Control", "no-cache");

    serverLog({
      description: descriptionValue,
      path: res.req.url,
      statusCode,
    });
  }

  if (error) {
    console.group();
    console.error(error);
    console.groupEnd();
  }

  // Via https://github.com/vercel/next.js/issues/18185
  if (!res.req?.url?.match(/^\/_next\/data\/.*$/)) {
    // eslint-disable-next-line no-param-reassign
    res.statusCode = statusCode;
  }

  return {
    props: {
      error: {
        descriptionStringKey,
        platforms,
        statusCode,
      },
    },
  };
};

export default errorProps;
