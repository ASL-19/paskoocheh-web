import { focusElement } from "@asl-19/js-dom-utils";
import { useEffect, useState } from "react";

/**
 * Focus a provided element after the current render.
 *
 * This is necessary to focus an element that will only become focusable after
 * the current render is complete (e.g. if the element comes into view as a
 * result of a setState an event callback).
 */
const useFocusElementAfterRender = () => {
  const [targetFocusElement, setTargetFocusElement] =
    useState<HTMLElement | null>(null);

  useEffect(() => {
    if (targetFocusElement) {
      focusElement(targetFocusElement, {
        preventScroll: true,
      });
      setTargetFocusElement(null);
    }
  }, [targetFocusElement]);

  return setTargetFocusElement;
};

export default useFocusElementAfterRender;
