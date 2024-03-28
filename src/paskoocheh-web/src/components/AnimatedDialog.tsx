import { Dialog } from "@ariakit/react/dialog";
import { transitionDurationWithPrefersReducedMotion } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css, SerializedStyles } from "@emotion/react";
import { ComponentProps, memo, RefObject, useCallback, useMemo } from "react";

import { AnimatedDialogStore } from "src/hooks/useAnimatedDialogState";
import zIndexes from "src/values/zIndexes";

const transitionDuration = transitionDurationWithPrefersReducedMotion("0.3s");

const dialog = css(
  transitionDuration,
  {
    opacity: 0,
    transitionProperty: "opacity, transform",
    zIndex: zIndexes.AnimatedDialog_dialog,
  },
  {
    "&[data-enter]": {
      opacity: 1,
      transform: "translateY(0)",
    },
  },
);

const dialogEntranceTransitionOriginTop = css(dialog, {
  transform: "translateY(-100%)",
});
const dialogEntranceTransitionOriginBottom = css(dialog, {
  transform: "translateY(100%)",
});

const backdrop = css(
  transitionDuration,
  {
    backgroundColor: "rgba(0, 0, 0, 0)",
    transitionProperty: "background-color",
  },
  {
    "&[data-enter]": {
      backgroundColor: "rgba(0, 0, 0, 0.35)",
    },
  },
);

const AnimatedDialog: StylableFC<
  Omit<ComponentProps<typeof Dialog>, "ref" | "state"> & {
    backdropCss?: SerializedStyles;
    dialogRef: RefObject<HTMLDivElement>;
    entranceTransitionOrigin?: "bottom" | "top";
    store: AnimatedDialogStore;
  }
> = memo(
  ({
    backdropCss,
    dialogRef,
    entranceTransitionOrigin = "top",
    store,
    ...props
  }) => {
    // Ariakit’s default autoFocusOnScroll doesn’t prevent scroll
    // (https://github.com/ariakit/ariakit/pull/1687)
    const autoFocusOnShow = useCallback((element: HTMLElement) => {
      element.focus({ preventScroll: true });
      return true;
    }, []);

    const backdropElement = useMemo(
      () => <div css={[backdrop, backdropCss]} />,
      [backdropCss],
    );

    return (
      <Dialog
        autoFocusOnShow={autoFocusOnShow}
        backdrop={backdropElement}
        css={
          entranceTransitionOrigin === "bottom"
            ? dialogEntranceTransitionOriginBottom
            : dialogEntranceTransitionOriginTop
        }
        ref={dialogRef}
        store={store}
        {...props}
      />
    );
  },
);

AnimatedDialog.displayName = "AnimatedDialog";

export default AnimatedDialog;
