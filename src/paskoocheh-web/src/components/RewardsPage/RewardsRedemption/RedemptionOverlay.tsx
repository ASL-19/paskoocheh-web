import { css } from "@emotion/react";
import Image from "next/image";
import { DOMAttributes, FC, memo, useCallback, useMemo, useRef } from "react";

import AnimatedDialog from "src/components/AnimatedDialog";
import ButtonButton from "src/components/ButtonButton";
import { GqlRedemptionMethod } from "src/generated/graphQl";
import { AnimatedDialogStore } from "src/hooks/useAnimatedDialogState";
import redeemPointsPng from "src/static/images/redeemPoints.png";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import {
  headingH2SemiBold,
  paragraphP1Regular,
  paragraphP1SemiBold,
} from "src/styles/typeStyles";
import colors from "src/values/colors";

export type RedemptionOverlayStrings = {
  /**
   * Text for message (includes HTML for email link).
   *
   * - \{rewardEmail\} is replaced by
   *   NEXT_PUBLIC_REWARD_REDEMPTION_EMAIL_ADDRESS
   */
  messageHtml: string;
  /**
   * Text for pin code
   */
  pinCode: string;
  /**
   * Text for understand
   */
  understand: string;
};

const dialog = css(
  {
    backgroundColor: colors.shadesWhite,
    borderRadius: "0.5rem",
    maxWidth: "calc(100vw - 2 * 1rem)",
    overflow: "hidden auto",
    padding: "2rem",
    width: "27rem",
  },
  // Vertically and horizontally center without flex container, via:
  // https://github.com/ariakit/ariakit/releases/tag/%40ariakit%2Freact%400.2.0
  {
    height: "fit-content",
    inset: "1rem",
    margin: "auto",
    maxHeight: "calc(100vh - 2 * 1rem)",
    position: "fixed",
  },
);

const container = css({
  alignItems: "center",
  display: "flex",
  flexDirection: "column",
  gap: "1.5rem",
  textAlign: "center",
});

const illustration = css({
  height: 100,
  objectFit: "contain",
  width: 100,
});

const pinCodeText = css(headingH2SemiBold, {
  letterSpacing: "4px",
});

const messageText = css(paragraphP1Regular, {
  a: {
    color: colors.primary500,
  },
});

const RedemptionOverlay: FC<{
  dialogStore: AnimatedDialogStore;
  pinCode: number;
  redemption: GqlRedemptionMethod;
}> = memo(({ dialogStore, pinCode, redemption }) => {
  const dialogRef = useRef<HTMLDivElement>(null);
  const { localeCode } = useAppLocaleInfo();
  const {
    RedemptionOverlay: strings,
    RewardsPageContent: rewardPageContentStrings,
  } = useAppStrings();

  const onCancelClick = useCallback(() => {
    dialogStore.hide();
  }, [dialogStore]);

  const encodedSubject = encodeURIComponent(
    localeCode === "fa"
      ? redemption.redemptionMethodFa
      : redemption.redemptionMethodEn,
  );

  const encodedEmailContent = encodeURIComponent(
    `${rewardPageContentStrings.redemption}: ${
      localeCode === "fa"
        ? redemption.redemptionMethodFa
        : redemption.redemptionMethodEn
    }\n${strings.pinCode}: ${pinCode}`,
  );

  const redemptionMessageDangerouslySetInnerHtml: DOMAttributes<HTMLParagraphElement>["dangerouslySetInnerHTML"] =
    useMemo(
      () => ({
        __html: strings.messageHtml
          .replaceAll(
            "{rewardEmail}",
            process.env.NEXT_PUBLIC_REWARD_REDEMPTION_EMAIL_ADDRESS,
          )
          .replaceAll(
            "{rewardEmailUrl}",
            `${process.env.NEXT_PUBLIC_REWARD_REDEMPTION_EMAIL_ADDRESS}?subject=${encodedSubject}&body=${encodedEmailContent}`,
          ),
      }),
      [encodedEmailContent, encodedSubject, strings.messageHtml],
    );

  return (
    <AnimatedDialog
      css={dialog}
      dialogRef={dialogRef}
      store={dialogStore}
      tabIndex={0}
    >
      <div css={container}>
        <Image src={redeemPointsPng} css={illustration} alt="" />
        <div>
          <p css={paragraphP1SemiBold}>{strings.pinCode}</p>
          <p css={pinCodeText}>{pinCode}</p>
        </div>

        <p
          css={messageText}
          dangerouslySetInnerHTML={redemptionMessageDangerouslySetInnerHtml}
        />
        <ButtonButton
          onClick={onCancelClick}
          text={strings.understand}
          variant="primary"
        />
      </div>
    </AnimatedDialog>
  );
});

RedemptionOverlay.displayName = "RedemptionOverlay";

export default RedemptionOverlay;
