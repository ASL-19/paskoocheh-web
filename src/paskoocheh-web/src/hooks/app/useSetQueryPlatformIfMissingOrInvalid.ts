import { getFirstStringOrString } from "@asl-19/js-utils";
import { useRouter } from "next/router";
import { useEffect } from "react";

import { useAppDispatch, useAppPlatforms } from "src/stores/appStore";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getPlatforms from "src/utils/page/getPlatforms";
import { defaultPlatformSlug } from "src/values/miscValues";

const useSetQueryPlatformIfMissingOrInvalid = () => {
  const appDispatch = useAppDispatch();
  const router = useRouter();
  const platforms = useAppPlatforms();

  // Fetch and dispatch platforms to appStore if they’re not already set
  // (probably because getServerSideProps failed)
  useEffect(() => {
    let shouldIgnoreResponse = false;

    (async () => {
      try {
        const graphQlSdk = await getGraphQlSdk();

        const platforms = await getPlatforms({ graphQlSdk });

        if (!shouldIgnoreResponse) {
          appDispatch({ platforms, type: "platformsLoaded" });
        }
      } catch (error) {
        console.error(
          "[useSetQueryPlatformIfMissingOrInvalid] Error fetching platforms:",
          error,
        );
      }
    })();

    return () => {
      shouldIgnoreResponse = true;
    };
  }, [appDispatch]);

  useEffect(() => {
    // Note: We don’t use useQueryPlatform here since it defaults to "android"
    // (so we’d have know way of knowing if it it wasn’t set)
    const rawQueryPlatform = getFirstStringOrString(router.query.platform);

    // Bail if router is’t ready or rawQueryPlatform matches a platform
    if (
      !router.isReady ||
      !platforms ||
      platforms?.some((platform) => platform.slugName === rawQueryPlatform)
    ) {
      return;
    }

    try {
      const newUrl = new URL(
        `${process.env.NEXT_PUBLIC_WEB_URL}${router.asPath}`,
      );

      newUrl.searchParams.set("platform", defaultPlatformSlug);

      console.info(
        "[useSetQueryPlatformIfMissingOrInvalid] Replacing URL:",
        newUrl.href,
      );

      router.replace(newUrl.href);
    } catch (error) {
      // Shouldn’t ever happen but the URL() constructor technically could throw
      // if the provided URL is invalid
      console.error(
        "[useSetQueryPlatformIfMissingOrInvalid] Failed to set query platform!",
        error,
      );
    }
  }, [platforms, router]);
};

export default useSetQueryPlatformIfMissingOrInvalid;
