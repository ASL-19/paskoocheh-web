import {
  Tooltip,
  TooltipAnchor,
  TooltipArrow,
  TooltipProvider,
} from "@ariakit/react/tooltip";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Link from "next/link";
import { memo } from "react";

import InfoSvg from "src/components/icons/general/InfoSvg";
import LogoSvg from "src/components/icons/logos/LogoSvg";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { appInstallBadgeHeight } from "src/styles/appStyles";
import { buttonPrimary } from "src/styles/buttonStyles";
import { captionRegular, paragraphP2SemiBold } from "src/styles/typeStyles";
import { Media } from "src/utils/media/media";
import colors from "src/values/colors";

export type AppAndroidInstallButtonStrings = {
  /**
   * Text for get it on Paskoocheh Button
   */
  getItOn: string;
  /**
   * Text for info tooltip
   */
  infoExplanation: string;
};

const container = css({ alignItems: "center", display: "flex", gap: "1rem" });

const buttonContainer = css(buttonPrimary({ size: "medium" }), {
  alignItems: "center",
  borderRadius: "0.5rem",
  display: "flex",
  height: appInstallBadgeHeight,
});

const logoIcon = css({ height: "1.875rem" });
const infoIcon = css({ height: "1rem" });

const textContainer = css({});
const infoContainer = css({
  background: colors.secondary400,
  borderRadius: "0.5rem",
  color: colors.shadesWhite,
  maxWidth: "22.1875rem",
  padding: "0.5rem",
});

const AppAndroidInstallButton: StylableFC<{
  platformPaskoochehAppPath: string;
}> = memo(({ platformPaskoochehAppPath, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();

  const strings = useAppStrings();

  return (
    <div css={container} {...remainingProps}>
      <Link css={buttonContainer} href={platformPaskoochehAppPath}>
        <LogoSvg logoType="button" css={logoIcon} />

        <div css={textContainer}>
          <p css={captionRegular}>{strings.AppAndroidInstallButton.getItOn}</p>
          <p css={paragraphP2SemiBold}>{strings.shared.siteTitle}</p>
        </div>
      </Link>

      <Media greaterThanOrEqual="desktopNarrow">
        <TooltipProvider
          placement={localeCode === "en" ? "right-start" : "left-start"}
        >
          <TooltipAnchor>
            <InfoSvg css={infoIcon} />
          </TooltipAnchor>

          <Tooltip css={infoContainer}>
            <TooltipArrow />
            {strings.AppAndroidInstallButton.infoExplanation}
          </Tooltip>
        </TooltipProvider>
      </Media>

      {/* TODO: change this when new mobile design is added */}
      <Media lessThan="desktopNarrow">
        <TooltipProvider placement="bottom">
          <TooltipAnchor>
            <InfoSvg css={infoIcon} />
          </TooltipAnchor>

          <Tooltip css={infoContainer}>
            <TooltipArrow />
            {strings.AppAndroidInstallButton.infoExplanation}
          </Tooltip>
        </TooltipProvider>
      </Media>
    </div>
  );
});

AppAndroidInstallButton.displayName = "AppAndroidInstallButton";

export default AppAndroidInstallButton;
