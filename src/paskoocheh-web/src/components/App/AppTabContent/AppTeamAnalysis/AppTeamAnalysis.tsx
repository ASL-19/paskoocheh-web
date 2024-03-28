import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import AppTeamReviewsContent from "src/components/App/AppTabContent/AppTeamAnalysis/AppTeamReviewsContent";
import OverallRatings from "src/components/OverallRatings";
import { GqlTeamAnalysis } from "src/generated/graphQl";
import { useAppStrings } from "src/stores/appStore";
import { breakpointStyles } from "src/utils/media/media";

export type AppTeamAnalysisStrings = {
  /**
   * Text for No team Analysis
   */
  noTeamAnalysis: string;
};

const container = css(
  {
    columnGap: "1.25rem",
    display: "flex",
    rowGap: "1.25rem",
  },
  breakpointStyles({
    desktopNarrow: {
      lt: {
        flexDirection: "column",
      },
    },
  }),
);

const AppTeamAnalysis: StylableFC<{ teamAnalysis: GqlTeamAnalysis | null }> =
  memo(({ teamAnalysis, ...remainingProps }) => {
    const { AppTeamAnalysis: strings } = useAppStrings();

    if (!teamAnalysis) return <div>{strings.noTeamAnalysis}</div>;

    return (
      <div css={container} {...remainingProps}>
        <OverallRatings teamAnalysis={teamAnalysis} isStarRating={false} />

        <AppTeamReviewsContent teamAnalysis={teamAnalysis} />
      </div>
    );
  });

AppTeamAnalysis.displayName = "AppTeamAnalysis";

export default AppTeamAnalysis;
