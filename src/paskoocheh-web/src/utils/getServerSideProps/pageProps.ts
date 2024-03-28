import { ServerResponse } from "http";
import { match } from "ts-pattern";

/**
 * Get page props and set `Cache-Control` header based on the provided
 * cacheDuration.
 */
const pageProps = <Props>({
  cacheDuration,
  props,
  res,
}: {
  /**
   * Amount of time the response should be stored in shared caches (e.g.
   * CloudFront or CloudFlare). This is used to determine the value of the
   * `Cache-Control` header’s `s-maxage` directive.
   *
   * - "minimal" means 5 minutes (300 seconds). This should be used for pages
   *   that need to be more quickly.
   *
   * - `"short"` means 1 hour (3600 seconds). This should be used for pages
   *   containing content that is updated periodically
   *
   * - `"forever"` means 10 years (315360000 seconds). This should be used for
   *   pages containing data that is not updated periodically (e.g. static
   *   pages).
   *
   *   (Note that static pages will be invalidated by the backend on save.)
   *
   * (The exact durations may be updated in the future.)
   *
   * @see
   * https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#s-maxage
   */
  cacheDuration: "minimal" | "short" | "forever";

  /**
   * Page props (returned as-is).
   */
  props: Props;

  /**
   * Response object (object parameter of getServerSideProps).
   *
   * Required to add `Cache-Control` header.
   */
  res: ServerResponse;
}) => {
  const durationSeconds = match(cacheDuration)
    .with("minimal", () => "600")
    .with("short", () => "3600")
    .with("forever", () => "315360000")
    .exhaustive();

  res.setHeader(
    "Cache-Control",
    `public, max-age=0, s-maxage=${durationSeconds}`,
  );

  return { props };
};

export default pageProps;
