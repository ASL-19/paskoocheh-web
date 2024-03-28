import {
  Dialog,
  DialogDismiss,
  DialogHeading,
  DialogStore,
} from "@ariakit/react/dialog";
import { VisuallyHidden } from "@ariakit/react/visually-hidden";
import { devLabel } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { useRouter } from "next/router";
import { memo, useEffect } from "react";

import HeaderNavLinkList from "src/components/Header/HeaderNavLinkList";
import { HeaderNavLinkListItemLinkInfo } from "src/components/Header/HeaderNavLinkListItem";
import { useAppStrings } from "src/stores/appStore";
import colors from "src/values/colors";
import { headerHeight } from "src/values/layoutValues";
import zIndexes from "src/values/zIndexes";

export type MobileHeaderNavDropdownStrings = {
  /**
   * Accessibility title for the mobile navigation
   */
  a11yTitle: string;
};

const height = headerHeight;

const dialog = css(devLabel("MobileHeaderNavDropdown-dialog"), {
  alignItems: "center",
  backgroundColor: colors.shadesWhite,
  display: "flex",
  flexDirection: "column",
  height: `calc(100vh - ${height})`,
  left: "-1rem",
  margin: "0 1rem",
  padding: "3rem 1rem",
  position: "fixed",
  right: "-1rem",
  rowGap: "1.5rem",
  top: height,
  width: "100%",
  zIndex: zIndexes.MobileHeaderNavDropdown_dialog,
});

const MobileHeaderNavDropdown: StylableFC<{
  dialogStore: DialogStore;
  navLinkInfos: Array<HeaderNavLinkListItemLinkInfo>;
}> = memo(({ className, dialogStore, navLinkInfos }) => {
  const router = useRouter();
  const { MobileHeaderNavDropdown: strings, shared: sharedStrings } =
    useAppStrings();

  useEffect(() => {
    // This closes automatically when navigating so the links don't need JS to close the modal
    const onRouteChangeStart = () => {
      dialogStore.hide();
    };

    router.events.on("routeChangeStart", onRouteChangeStart);

    return () => {
      router.events.off("routeChangeStart", onRouteChangeStart);
    };
  }, [dialogStore, router.events]);

  return (
    <Dialog className={className} css={dialog} modal store={dialogStore}>
      <VisuallyHidden>
        <DialogHeading>{strings.a11yTitle}</DialogHeading>
        <DialogDismiss>{sharedStrings.dialog.a11yCloseButton}</DialogDismiss>
      </VisuallyHidden>

      <HeaderNavLinkList navLinkInfos={navLinkInfos} isMobile={true} />
    </Dialog>
  );
});

MobileHeaderNavDropdown.displayName = "MobileHeaderNavDropdown";

export default MobileHeaderNavDropdown;
