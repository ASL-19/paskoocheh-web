import { useEffect } from "react";

/**
 * Hide focus outlines when a mousedown event fires; show focus outlines when a
 * keydown event fires.
 *
 * This preserves focus outlines when a user is navigating the site with their
 * keyboard while preventing distracting focus outlines from appearing when the
 * user is navigating via mouse/touch.
 */
const useDynamicFocusOutlines = () => {
  useEffect(() => {
    const hideFocusOutlines = () => {
      if (
        // prettier-ignore
        document.documentElement.className.indexOf(" focusOutlinesHidden") === -1
      ) {
        document.documentElement.className = `${document.documentElement.className} focusOutlinesHidden`;
      }
    };

    const showFocusOutlines = () => {
      if (
        // prettier-ignore
        document.documentElement.className.indexOf(" focusOutlinesHidden") !== -1 &&
        document.activeElement &&
        document.activeElement.tagName !== "INPUT" &&
        document.activeElement.tagName !== "TEXTAREA"
      ) {
        document.documentElement.className =
          document.documentElement.className.replace(
            " focusOutlinesHidden",
            "",
          );
      }
    };

    window.addEventListener("mousedown", hideFocusOutlines, false);
    window.addEventListener("keydown", showFocusOutlines, false);

    return () => {
      window.removeEventListener("mousedown", hideFocusOutlines);
      window.removeEventListener("keydown", showFocusOutlines);
    };
  }, []);
};

export default useDynamicFocusOutlines;
