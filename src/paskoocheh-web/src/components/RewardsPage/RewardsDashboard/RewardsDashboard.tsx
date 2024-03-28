import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useMemo } from "react";

import RewardsRecords from "src/components/RewardsPage/RewardsDashboard/RewardsRecords";
import RewardsReferralLink from "src/components/RewardsPage/RewardsDashboard/RewardsReferralLink";
import RewardsWeeklyChallenge from "src/components/RewardsPage/RewardsWeeklyChallenge/RewardsWeeklyChallenge";
import { useRewardsQuizPage } from "src/stores/rewardsStore";
import {
  WeeklyChallengeQuizProvider,
  WeeklyChallengeQuizState,
} from "src/stores/weeklyChallengeQuizStore";
import {
  dashboardGridContainer,
  dashboardGridItemLarge,
  dashboardGridItemSmall,
} from "src/styles/dashboardStyles";
import { gridContainerGap } from "src/styles/generalStyles";

const weeklyChallengeAndLink = css(dashboardGridItemLarge, {
  display: "flex",
  flexDirection: "column",
  gap: gridContainerGap,
});

const RewardsDashboard: StylableFC<{
  hasFinishedQuiz: boolean | null;
  referralSlug: string;
}> = memo(({ className, hasFinishedQuiz, referralSlug }) => {
  const initialQuizState: WeeklyChallengeQuizState = useMemo(
    () => ({
      currentQuestionIndex: 0,
      hasFinishedQuiz,
      numberOfCorrectQuestions: 0,
      questionStates: {},
    }),
    [hasFinishedQuiz],
  );

  const quizPage = useRewardsQuizPage();

  return (
    <div className={className} css={dashboardGridContainer}>
      <div css={weeklyChallengeAndLink}>
        {quizPage && (
          <WeeklyChallengeQuizProvider initialState={initialQuizState}>
            <RewardsWeeklyChallenge />
          </WeeklyChallengeQuizProvider>
        )}
        {referralSlug && process.env.NEXT_PUBLIC_ENABLE_REFERRAL && (
          <RewardsReferralLink referralSlug={referralSlug} />
        )}
      </div>
      <RewardsRecords css={dashboardGridItemSmall} />
    </div>
  );
});

RewardsDashboard.displayName = "RewardsDashboard";

export default RewardsDashboard;
