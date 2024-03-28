import { useRouter } from "next/router";
import { useEffect } from "react";

import { useAppDispatch } from "src/stores/appStore";
import { RouterEventHandler } from "src/types/nextTypes";

/**
 * Dispatch app route routeChangeStarted and routeChangeCompleted actions when
 * corresponding Next.js router events fired.
 */
const useDispatchAppRouteChangeActions = () => {
  const router = useRouter();

  const appDispatch = useAppDispatch();

  useEffect(() => {
    const onRouteChangeStart: RouterEventHandler = (url, { shallow }) => {
      if (!shallow) {
        appDispatch({ type: "routeChangeStarted" });
      }
    };

    const onRouteChangeComplete: RouterEventHandler = (url, { shallow }) => {
      if (!shallow) {
        appDispatch({ type: "routeChangeCompleted" });
      }
    };

    router.events.on("routeChangeStart", onRouteChangeStart);
    router.events.on("routeChangeComplete", onRouteChangeComplete);

    return () => {
      router.events.off("routeChangeStart", onRouteChangeStart);
      router.events.off("routeChangeComplete", onRouteChangeComplete);
    };
  }, [appDispatch, router]);
};

export default useDispatchAppRouteChangeActions;
