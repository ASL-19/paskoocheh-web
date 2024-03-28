import { Disclosure } from "@ariakit/react/disclosure";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import ButtonDisclosure from "src/components/ButtonDisclosure";
import RedemptionOverlay from "src/components/RewardsPage/RewardsRedemption/RedemptionOverlay";
import { GqlRedemptionMethod } from "src/generated/graphQl";
import useAnimatedDialogStore from "src/hooks/useAnimatedDialogState";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import {
  useRewardsPointsBalance,
  useRewardsUserPinCode,
} from "src/stores/rewardsStore";
import {
  dashboardItemContainer,
  dashboardItemHeadingAndDescription,
} from "src/styles/dashboardStyles";
import {
  captionRegular,
  captionSemiBold,
  headingH5SemiBold,
} from "src/styles/typeStyles";
import { breakpointStyles, Media } from "src/utils/media/media";
import colors from "src/values/colors";

const container = ({ disabled }: { disabled: boolean }) =>
  css(
    dashboardItemContainer,
    {
      alignItems: "start",
      backgroundColor: disabled ? colors.neutral200 : colors.neutral50,
      border: `solid 1px ${colors.secondary50}`,
      flexDirection: "row",
      justifyContent: "start",

      width: "100%",
    },
    breakpointStyles({
      singleColumn: {
        lt: {
          border: `solid 1px ${colors.neutral100}`,
        },
      },
    }),
  );
const image = css(
  {
    background: "salmon",
    borderRadius: "100%",
    height: "4rem",
    width: "4rem",
  },
  breakpointStyles({ singleColumn: { lt: { height: "3rem", width: "3rem" } } }),
);
const heading = css(
  headingH5SemiBold,
  breakpointStyles({ singleColumn: { lt: captionSemiBold } }),
);
const description = css(captionRegular, { color: colors.secondary300 });
const info = css({
  display: "flex",
  flexDirection: "column",
  gap: "1.5rem",
});

const RewardsRedemptionListItem: StylableFC<{
  redemption: GqlRedemptionMethod;
}> = memo(({ redemption, ...remainingProps }) => {
  const { RewardsPageContent: strings, shared: sharedStrings } =
    useAppStrings();
  const pointsBalance = useRewardsPointsBalance();
  const pinCode = useRewardsUserPinCode();

  const { localeCode } = useAppLocaleInfo();

  const isRedeemable = pointsBalance >= redemption.redemptionPoints;

  const redemptionOverlayStore = useAnimatedDialogStore();
  const redemptionOverlayDialogIsMounted =
    redemptionOverlayStore.useState("mounted");

  const headingAndDescription = (
    <div css={dashboardItemHeadingAndDescription}>
      <h3 css={heading}>
        {redemption.redemptionPoints} &nbsp;{strings.points}
      </h3>
      <p css={description}>
        {localeCode === "fa"
          ? redemption.redemptionMethodFa
          : redemption.redemptionMethodEn}
      </p>
    </div>
  );

  return (
    <>
      <Media lessThan="singleColumn">
        <Disclosure
          store={redemptionOverlayStore}
          css={container({ disabled: !isRedeemable })}
          type="button"
          disabled={!isRedeemable}
          {...remainingProps}
        >
          <div css={image}></div>
          <div css={info}>{headingAndDescription}</div>
        </Disclosure>
      </Media>

      <Media greaterThanOrEqual="singleColumn">
        <div css={container} {...remainingProps}>
          <div css={image}></div>
          <div css={info}>
            {headingAndDescription}

            <ButtonDisclosure
              store={redemptionOverlayStore}
              text={
                isRedeemable
                  ? sharedStrings.button.redeem
                  : sharedStrings.button.notEnoughPoints
              }
              disabled={!isRedeemable}
              variant="secondary"
            />
          </div>
        </div>
      </Media>

      {redemptionOverlayDialogIsMounted && (
        <RedemptionOverlay
          dialogStore={redemptionOverlayStore}
          pinCode={pinCode}
          redemption={redemption}
        />
      )}
    </>
  );
});

RewardsRedemptionListItem.displayName = "RewardsRedemptionListItem";

export default RewardsRedemptionListItem;
