import { defaultPlatformSlug } from "src/values/miscValues";

const getUrlPlatform = (
  /**
   * URL (can be fully-qualified or root-relative).
   */
  url: string,
) => {
  const parsedUrl = (() => {
    // URL() can throw if URL is malformed so we wrap in try...catch to be safe.
    // This shouldn’t happen since we have basic runtime checks but better safe
    // than sorry
    try {
      return url.startsWith("http")
        ? new URL(url)
        : url.startsWith("/")
          ? new URL(`${process.env.NEXT_PUBLIC_WEB_URL}${url}`)
          : null;
    } catch {
      return null;
    }
  })();

  if (!parsedUrl) {
    console.warn(
      `[getUrlPlatformSlug] Returning default platform slug "${defaultPlatformSlug}" since provided URL "${url}" is undefined, empty, or invalid (not root-relative or fully-qualified).`,
    );

    return defaultPlatformSlug;
  }

  const urlPlatform = parsedUrl.searchParams.get("platform");

  return urlPlatform ?? defaultPlatformSlug;
};

export default getUrlPlatform;
