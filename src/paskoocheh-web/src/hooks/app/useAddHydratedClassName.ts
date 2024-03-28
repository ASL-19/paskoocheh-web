import { useEffect } from "react";

/**
 * Add "hydrated" className to <html> element once site has rendered on client.
 *
 * We use this in Playwright tests to avoid interacting with the page before
 * event handlers are ready.
 */
const useAddHydratedClassName = () => {
  useEffect(() => {
    document.documentElement.classList.add("hydrated");
  }, []);
};

export default useAddHydratedClassName;
