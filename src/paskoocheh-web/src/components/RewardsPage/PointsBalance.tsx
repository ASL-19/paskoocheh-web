import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, MouseEventHandler, useMemo } from "react";

import DrawerDialogAndDisclosure from "src/components/DrawerDialog/DrawerDialogAndDisclosure";
import InfoSvg from "src/components/icons/general/InfoSvg";
import HowPointsWorkListMobileDrawerContent from "src/components/RewardsPage/HowPointsWork/HowPointsWorkListMobileDrawerContent";
import { rewardsDetailsSectionIds } from "src/components/RewardsPage/rewardsValues";
import useAnimatedDialogStore from "src/hooks/useAnimatedDialogState";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { useRewardsPointsBalance } from "src/stores/rewardsStore";
import { buttonPrimary } from "src/styles/buttonStyles";
import {
  dashboardGridItemLarge,
  dashboardItemContainer,
} from "src/styles/dashboardStyles";
import {
  display01Semibold,
  headingH4SemiBold,
  paragraphP2SemiBold,
} from "src/styles/typeStyles";
import { breakpointStyles, Media } from "src/utils/media/media";
import colors from "src/values/colors";

const container = css(dashboardGridItemLarge, dashboardItemContainer, {
  alignItems: "center",
  backgroundColor: colors.primary50,
});
const heading = css(
  paragraphP2SemiBold,
  {
    position: "relative",
  },
  breakpointStyles({
    desktopNarrow: {
      lt: {
        display: "flex",
        justifyContent: "space-between",
        textAlign: "start",
        width: "100%",
      },
    },
  }),
);
const point = css(
  display01Semibold,
  breakpointStyles({ singleColumn: { lt: headingH4SemiBold } }),
);
const button = css(
  buttonPrimary({ size: "medium" }),
  { width: "12.5rem" },
  breakpointStyles({ singleColumn: { lt: { width: "100%" } } }),
);
const icon = css({ width: "1rem" });

const PointsBalance: StylableFC<{
  onRedemptionLinkClick: MouseEventHandler;
}> = memo(({ onRedemptionLinkClick, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();
  const {
    HowPointsWork: howPointsWorkStrings,
    RewardsPageContent: strings,
    shared: sharedStrings,
  } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const pointsBalance = useRewardsPointsBalance();

  const shareAnimatedDialogStore = useAnimatedDialogStore();

  const dialogDisclosureContent = useMemo(() => <InfoSvg css={icon} />, []);

  return (
    <div css={container} {...remainingProps}>
      <div css={heading}>
        {strings.yourPointsBalance}
        <Media lessThan="singleColumn">
          <DrawerDialogAndDisclosure
            disclosureContentElement={dialogDisclosureContent}
            heading={howPointsWorkStrings.heading}
            headingLevel={2}
            animatedDialogStore={shareAnimatedDialogStore}
          >
            <HowPointsWorkListMobileDrawerContent />
          </DrawerDialogAndDisclosure>
        </Media>
      </div>

      <p css={point}>{pointsBalance}</p>

      <a
        css={button}
        href={`${routeUrls.rewards({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        })}#${rewardsDetailsSectionIds.redemption}`}
        onClick={onRedemptionLinkClick}
      >
        {sharedStrings.button.redeem}
      </a>
    </div>
  );
});

PointsBalance.displayName = "PointsBalance";

export default PointsBalance;
