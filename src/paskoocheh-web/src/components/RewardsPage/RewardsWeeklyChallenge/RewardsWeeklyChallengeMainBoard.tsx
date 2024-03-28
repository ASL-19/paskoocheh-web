import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { StaticImageData } from "next/image";
import { memo, MouseEventHandler } from "react";

import ButtonButton from "src/components/ButtonButton";
import StaticImage from "src/components/StaticImage";
import { useAppStrings } from "src/stores/appStore";
import { useRewardsQuizWonEarningPoints } from "src/stores/rewardsStore";
import {
  dashboardItemContainer,
  dashboardItemDescription,
  dashboardItemHeadingAndDescription,
  dashboardItemTitle,
} from "src/styles/dashboardStyles";
import { captionSemiBold, paragraphP2SemiBold } from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

const container = css(dashboardItemContainer, { textAlign: "center" });

const img = css(
  {
    borderRadius: "100%",
    height: "15rem",
    width: "15rem",
  },
  breakpointStyles({
    singleColumn: { lt: { height: "4.75rem", width: "4.75rem" } },
  }),
);
const title = css(
  paragraphP2SemiBold,
  { textAlign: "center" },
  breakpointStyles({ singleColumn: { lt: captionSemiBold } }),
);

const pointText = css({
  color: colors.success500,
});

const RewardsWeeklyChallengeMainBoard: StylableFC<{
  description: string;
  heading?: string;
  image: StaticImageData;
  onClick?: MouseEventHandler<HTMLButtonElement>;
  showButton?: boolean;
  type?: "info" | "result";
}> = memo(
  ({
    className,
    description,
    heading,
    image,
    onClick,
    showButton = false,
    type = "info",
  }) => {
    const { RewardsPageContent: strings, shared: sharedStrings } =
      useAppStrings();

    const { RewardsWeeklyChallenge: rewardsStrings } = useAppStrings();

    const quizWonEarningPoints = useRewardsQuizWonEarningPoints();

    return (
      <div className={className} css={container}>
        <p css={dashboardItemTitle}>{strings.weeklyChallenge}</p>
        <StaticImage css={img} src={image.src} alt="" staticImageData={image} />
        <div css={dashboardItemHeadingAndDescription}>
          {type === "info" ? (
            <h3 css={title}>{heading}</h3>
          ) : (
            <h3 css={title}>
              {rewardsStrings.earnedPoints.headingPrefix}&nbsp;
              <span css={pointText}>
                {quizWonEarningPoints}
                {rewardsStrings.earnedPoints.headingPointsText}
              </span>
              &nbsp;
              {rewardsStrings.earnedPoints.headingSuffix}
            </h3>
          )}
          <p css={dashboardItemDescription}>{description}</p>
        </div>
        {showButton && (
          <ButtonButton
            text={sharedStrings.button.getStarted}
            variant="secondary"
            onClick={onClick}
          />
        )}
      </div>
    );
  },
);

RewardsWeeklyChallengeMainBoard.displayName = "RewardsWeeklyChallengeMainBoard";

export default RewardsWeeklyChallengeMainBoard;
