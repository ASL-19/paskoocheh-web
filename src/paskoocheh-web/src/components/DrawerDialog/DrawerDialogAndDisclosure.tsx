import { Disclosure } from "@ariakit/react/disclosure";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, ReactElement } from "react";

import DrawerDialog, {
  MobileDialogProps,
} from "src/components/DrawerDialog/DrawerDialog";
import { useAppStrings } from "src/stores/appStore";

const disclosure = css({
  display: "flex",
});

const DrawerDialogAndDisclosure: StylableFC<
  {
    disclosureContentElement: ReactElement;
  } & MobileDialogProps
> = memo(
  ({
    animatedDialogStore,
    children,
    disclosureContentElement,
    heading,
    headingIsVisible = true,
    headingLevel,
    ...remainingProps
  }) => {
    const dialogIsMounted = animatedDialogStore.useState("mounted");
    const strings = useAppStrings();

    return (
      <div {...remainingProps}>
        <Disclosure
          css={disclosure}
          store={animatedDialogStore}
          aria-label={strings.AppShareAndSupportLinks.supportDialogHeading}
        >
          {disclosureContentElement}
        </Disclosure>

        {dialogIsMounted && (
          <DrawerDialog
            animatedDialogStore={animatedDialogStore}
            heading={heading}
            headingIsVisible={headingIsVisible}
            headingLevel={headingLevel}
          >
            {children}
          </DrawerDialog>
        )}
      </div>
    );
  },
);

DrawerDialogAndDisclosure.displayName = "DrawerDialogAndDisclosure";

export default DrawerDialogAndDisclosure;
