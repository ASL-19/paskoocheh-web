import { DialogDismiss } from "@ariakit/react/dialog";
import { invisible } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, ReactNode, useId, useRef } from "react";

import AnimatedDialog from "src/components/AnimatedDialog";
import CrossSvg from "src/components/icons/general/CrossSvg";
import { AnimatedDialogStore } from "src/hooks/useAnimatedDialogState";
import { paragraphP1SemiBold } from "src/styles/typeStyles";
import { HeadingLevel, HeadingTagName } from "src/types/miscTypes";
import colors from "src/values/colors";
import zIndexes from "src/values/zIndexes";

export type MobileDialogProps = {
  animatedDialogStore: AnimatedDialogStore;
  children: ReactNode;
  heading: string;
  headingIsVisible?: boolean;
  headingLevel: HeadingLevel;
};

const buttonContainer = css({
  backgroundColor: colors.shadesWhite,
  borderTopLeftRadius: "0.5rem",
  borderTopRightRadius: "0.5rem",
  bottom: 0,
  display: "flex",
  flexDirection: "column",
  maxHeight: "100dvh",
  overflowY: "auto",
  padding: "1rem",
  position: "absolute",
  width: "100%",
  zIndex: zIndexes.MobileRouteOverlay_buttonContainer,
});

const dismissButton = css({
  alignSelf: "end",
  display: "flex",
});

const dismissButtonIcon = css({
  height: "1rem",
  stroke: colors.secondary500,
  width: "1rem",
});

const headingStyles = css(paragraphP1SemiBold, {
  lineHeight: "2.25rem",
  textAlign: "center",
});

const DrawerDialog: StylableFC<MobileDialogProps> = memo(
  ({
    animatedDialogStore,
    children,
    heading,
    headingIsVisible,
    headingLevel,
  }) => {
    const dialogRef = useRef<HTMLDivElement>(null);

    const HeadingTag = `h${headingLevel}` as HeadingTagName;

    const headingId = useId();

    return (
      <AnimatedDialog
        aria-labelledby={headingId}
        css={buttonContainer}
        dialogRef={dialogRef}
        store={animatedDialogStore}
        entranceTransitionOrigin="bottom"
        tabIndex={0}
      >
        <DialogDismiss css={dismissButton}>
          <CrossSvg css={dismissButtonIcon} />
        </DialogDismiss>

        {heading && (
          <HeadingTag
            css={headingIsVisible ? headingStyles : invisible}
            id={headingId}
          >
            {heading}
          </HeadingTag>
        )}
        {children}
      </AnimatedDialog>
    );
  },
);

DrawerDialog.displayName = "DrawerDialog";

export default DrawerDialog;
