import router from "next/router";
import { useEffect } from "react";

import { RouterEventHandler } from "src/types/nextTypes";

/**
 * Report page URL and title to Google Analytics on Next.js routeChangeComplete
 * event.
 */
const useGoogleTagRouteChangePageViewTracking = ({
  isActive,
}: {
  isActive: boolean;
}) => {
  useEffect(() => {
    const onRouteChangeComplete: RouterEventHandler = (url, { shallow }) => {
      // gtag call wrapped in a 100ms timeout due to
      // https://github.com/vercel/next.js/issues/6025
      //
      // The page title isn’t guaranteed to be updated after the timeout but
      // 100ms seems to be enough that it’s updated.
      setTimeout(() => {
        if (!isActive || shallow || typeof gtag === "undefined") {
          return;
        }

        gtag("event", "page_view");
      }, 100);
    };

    router.events.on("routeChangeComplete", onRouteChangeComplete);

    return () => {
      router.events.off("routeChangeComplete", onRouteChangeComplete);
    };
  }, [isActive]);
};

export default useGoogleTagRouteChangePageViewTracking;
