import { getFirstStringOrString } from "@asl-19/js-utils";
import { useRouter } from "next/router";

import { useAppPlatforms } from "src/stores/appStore";
import { defaultPlatformSlug } from "src/values/miscValues";

/**
 * Get query platform slug (with fallback to `defaultPlatformSlug`).
 *
 * @returns
 * - `string` if query platform is set and matches a platform stored in
 *   `appStore` (set either in initial platforms returned by
 *   `getServerSideProps` or fetched on client in
 *   `useSetQueryPlatformIfMissingOrInvalid`)
 * - `defaultPlatformSlug` otherwise
 */
const useQueryOrDefaultPlatformSlug = () => {
  const router = useRouter();

  const platforms = useAppPlatforms();

  const queryPlatform = getFirstStringOrString(router.query.platform);

  return typeof queryPlatform === "string" &&
    platforms?.some((platform) => platform.slugName === queryPlatform)
    ? queryPlatform
    : defaultPlatformSlug;
};

export default useQueryOrDefaultPlatformSlug;
