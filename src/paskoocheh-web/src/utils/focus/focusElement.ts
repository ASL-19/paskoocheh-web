const onElementBlur = (event: FocusEvent) => {
  const element = event.target as HTMLElement;
  element.removeAttribute("tabindex");
  element.removeEventListener("blur", onElementBlur);
};

/**
 * Focus a DOM element.
 *
 * @remarks
 * Adds tabindex="-1" to element to make it focusable (removed on blur).
 *
 * @public
 */
const focusElement = (
  element: HTMLElement | null,
  options: { preventScroll: boolean } = { preventScroll: false },
) => {
  if (!(element instanceof HTMLElement)) {
    console.error("Couldn’t focus element:", element);
    return;
  }
  element.setAttribute("tabindex", "-1");
  element.addEventListener("blur", onElementBlur);
  element.focus({ preventScroll: options.preventScroll });
};

export default focusElement;
