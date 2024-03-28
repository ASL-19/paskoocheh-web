import { DialogDisclosure, DialogStore } from "@ariakit/react/dialog";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import CrossSvg from "src/components/icons/general/CrossSvg";
import HamburgerSvg from "src/components/icons/general/HamburgerSvg";
import { useAppStrings } from "src/stores/appStore";
import colors from "src/values/colors";

export type MobileHeaderNavMenuButtonStrings = {
  /**
   * Label text for mobile navigation menu button for accessibility purposes
   */
  closeA11yLabel: string;
  /**
   * Label text for mobile navigation menu button for accessibility purposes
   */
  openA11yLabel: string;
};

const colorAndStrokeInactive = css({
  stroke: colors.black,
});

const iconTextColumn = css(
  colorAndStrokeInactive,
  {
    alignSelf: "center",
    boxSizing: "content-box",
    display: "flex",
    flex: "0 0 auto",
    height: "100%",
    justifyContent: "center",
    margin: "0",
    // Hide the default focus outline since we’re using a custom one (the
    // default one would look weird because of the way the icon + text are
    // aligned and sized)
    outline: "none",
    position: "relative",
    width: "3rem",
  },
  {
    "html:not(.focusOutlinesHidden) & :focus": {
      backgroundColor: colors.backgroundPartiallyTransparent,
    },
  },
);

const navIconHamburger = css({
  alignSelf: "center",
  fill: colors.black,
  flex: "0 0 auto",
  height: "1.5rem",
});

const MobileHeaderNavMenuButton: StylableFC<{
  dialogStore: DialogStore;
}> = memo(({ className, dialogStore }) => {
  const { MobileHeaderNavMenuButton: strings } = useAppStrings();

  const dialogIsMounted = dialogStore.useState("mounted");

  return (
    <DialogDisclosure
      aria-label={
        dialogIsMounted ? strings.closeA11yLabel : strings.openA11yLabel
      }
      className={className}
      css={iconTextColumn}
      store={dialogStore}
    >
      {dialogIsMounted ? (
        <CrossSvg aria-hidden css={navIconHamburger} />
      ) : (
        <HamburgerSvg aria-hidden css={navIconHamburger} />
      )}
    </DialogDisclosure>
  );
});

MobileHeaderNavMenuButton.displayName = "MobileHeaderNavMenuButton";

export default MobileHeaderNavMenuButton;
