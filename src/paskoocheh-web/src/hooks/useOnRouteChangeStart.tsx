import { useRouter } from "next/router";
import { useEffect } from "react";

const useOnRouteChangeStart = ({ callback }: { callback: () => void }) => {
  const router = useRouter();

  useEffect(() => {
    // This closes automatically when navigating so the links don't need JS to close the modal
    const onRouteChangeStart = () => {
      callback();
    };

    router.events.on("routeChangeStart", onRouteChangeStart);

    return () => {
      router.events.off("routeChangeStart", onRouteChangeStart);
    };
  }, [callback, router.events]);
};

export default useOnRouteChangeStart;
