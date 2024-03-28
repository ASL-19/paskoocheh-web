import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import AppTeamAnalysisProsAndConsList from "src/components/App/AppTabContent/AppTeamAnalysis/AppTeamAnalysisProsAndConsList";
import { GqlTeamAnalysis } from "src/generated/graphQl";
import { useAppStrings } from "src/stores/appStore";
import { paragraphP2Regular, paragraphP2SemiBold } from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

export type AppTeamReviewsContentStrings = {
  cons: string;
  pros: string;
  reviews: string;
};

const container = css({
  backgroundColor: colors.neutral50,
  borderRadius: "0.5rem",
  display: "flex",
  flex: "2",
  flexDirection: "column",
  padding: "1.25rem",
  rowGap: "1.25rem",
});

const prosAndConsContainer = css(
  {
    columnGap: "1,25rem",
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

const AppTeamReviewsContent: StylableFC<{ teamAnalysis: GqlTeamAnalysis }> =
  memo(({ className, teamAnalysis }) => {
    const strings = useAppStrings();
    return (
      <div className={className} css={container}>
        <h2 css={paragraphP2SemiBold}>
          {strings.AppTeamReviewsContent.reviews}
        </h2>
        <p css={paragraphP2Regular}>{teamAnalysis.review}</p>

        <div css={prosAndConsContainer}>
          <AppTeamAnalysisProsAndConsList
            reviews={teamAnalysis.pros ?? ""}
            colorCss={colors.success500}
            title={strings.AppTeamReviewsContent.pros}
          />
          <AppTeamAnalysisProsAndConsList
            reviews={teamAnalysis.cons ?? ""}
            colorCss={colors.error500}
            title={strings.AppTeamReviewsContent.cons}
          />
        </div>
      </div>
    );
  });

AppTeamReviewsContent.displayName = "AppTeamReviewsContent";

export default AppTeamReviewsContent;
