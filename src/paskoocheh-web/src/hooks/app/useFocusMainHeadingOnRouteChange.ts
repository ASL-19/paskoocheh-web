import { focusElement } from "@asl-19/js-dom-utils";
import { useRouter } from "next/router";
import { useEffect, useRef } from "react";

import { RouterEventHandler } from "src/types/nextTypes";
import getUrlPlatform from "src/utils/routing/getUrlPlatform";

/**
 * Focus h1#main-heading on Next.js routeChangeComplete event unless new URL is
 * the same as previous URL but with different platform slug (so focus doesn’t
 * move from Header SearchBox when changing platform).
 */
const useFocusMainHeadingOnRouteChange = () => {
  const router = useRouter();

  const previousUrlRef = useRef<string>(router.asPath);

  useEffect(() => {
    const onRouteChangeComplete: RouterEventHandler = async (
      newUrl,
      { shallow },
    ) => {
      if (!shallow) {
        const previousUrl = previousUrlRef.current;
        const previousUrlPlatformSlug = getUrlPlatform(previousUrl);

        const newUrlPlatformSlug = getUrlPlatform(newUrl);

        /**
         * Is the new URL the same as the previous URL, except with the platform
         * query string segment changed?
         */
        const newUrlOnlyChangedPlatform =
          !!previousUrlPlatformSlug &&
          !!newUrlPlatformSlug &&
          newUrl ===
            previousUrl.replace(previousUrlPlatformSlug, newUrlPlatformSlug);

        previousUrlRef.current = newUrl;

        // If only the platform query string segment changed then skip focussing
        // heading on route change (for PlatformSelectGroup’s platform links)
        if (newUrlOnlyChangedPlatform) {
          return;
        }

        const mainHeadingElement =
          document.querySelector<HTMLElement>("h1#main-heading");

        focusElement(mainHeadingElement, {
          preventScroll: true,
        });
      }
    };

    router.events.on("routeChangeComplete", onRouteChangeComplete);

    return () => {
      router.events.off("routeChangeComplete", onRouteChangeComplete);
    };
  }, [router]);
};

export default useFocusMainHeadingOnRouteChange;
