import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useCallback, useState } from "react";
import { match } from "ts-pattern";

import LoadingIndicatorSvg from "src/components/icons/animation/LoadingIndicatorSvg";
import RewardsWeeklyChallengeMainBoard from "src/components/RewardsPage/RewardsWeeklyChallenge/RewardsWeeklyChallengeMainBoard";
import RewardsWeeklyChallengeQuiz from "src/components/RewardsPage/RewardsWeeklyChallenge/RewardsWeeklyChallengeQuiz";
import weeklyChallengePng from "src/static/images/weeklyChallenge.png";
import { useAppStrings } from "src/stores/appStore";
import { useRewardsQuizPage } from "src/stores/rewardsStore";
import {
  useHasFinishedWeeklyChallengeQuiz,
  useWeeklyChallengeQuizCurrentQuestionIndex,
} from "src/stores/weeklyChallengeQuizStore";
import { dashboardItemContainer } from "src/styles/dashboardStyles";

export type RewardsWeeklyChallengeStrings = {
  /**
   * Text for completed weekly challenge
   */
  completed: {
    description: string;
    heading: string;
  };
  /**
   * Text for weekly challenge result with earned points
   */
  earnedPoints: {
    description: string;
    headingPointsText: string;
    headingPrefix: string;
    headingSuffix: string;
  };
  /**
   * Text for weekly challenge result with no earned points
   */
  notEarnedPoints: {
    description: string;
    heading: string;
  };
  /**
   * Text for not yet completed weekly challenge
   */
  notYetCompleted: {
    description: string;
    heading: string;
  };
};

const container = css(dashboardItemContainer, {
  minHeight: "30rem",
  textAlign: "center",
});
const icon = css({ height: "4rem" });

export type WeeklyChallengeState =
  | { type: "completed" }
  | { type: "notCompleted" }
  | { type: "started" }
  | { type: "notEarnedPoints" }
  | { type: "earnedPoints" }
  | { errorMessage: string; type: "hasErrorMessage" }
  | { type: "loading" };

const RewardsWeeklyChallenge: StylableFC = memo(({ className }) => {
  const { RewardsWeeklyChallenge: strings } = useAppStrings();
  const quizPage = useRewardsQuizPage();
  const hasFinishedQuiz = useHasFinishedWeeklyChallengeQuiz();

  // TODO: This approach of selecting the "Weekly Quiz" is temporary, hard coded
  const questionBlocks = (quizPage?.questions ?? []).reduce(
    (acc, question) => (question ? [...acc, question] : acc),
    [],
  );

  const quizCurrentQuestionIndex = useWeeklyChallengeQuizCurrentQuestionIndex();
  const questionNumber =
    quizCurrentQuestionIndex + 1 <= questionBlocks.length
      ? quizCurrentQuestionIndex + 1
      : questionBlocks.length;

  const [weeklyChallengeState, setWeeklyChallengeState] =
    useState<WeeklyChallengeState>(
      hasFinishedQuiz
        ? { type: "completed" }
        : quizCurrentQuestionIndex === questionNumber
          ? { type: "completed" }
          : { type: "notCompleted" },
    );

  const onGetStartedClick = useCallback(
    () => setWeeklyChallengeState({ type: "started" }),
    [],
  );

  return match(weeklyChallengeState)
    .with({ type: "completed" }, () => (
      <RewardsWeeklyChallengeMainBoard
        className={className}
        heading={strings.completed.heading}
        description={strings.completed.description}
        image={weeklyChallengePng}
      />
    ))
    .with({ type: "notCompleted" }, () => (
      <RewardsWeeklyChallengeMainBoard
        className={className}
        heading={strings.notYetCompleted.heading}
        description={strings.notYetCompleted.description}
        image={weeklyChallengePng}
        showButton
        onClick={onGetStartedClick}
      />
    ))
    .with({ type: "earnedPoints" }, () => (
      <RewardsWeeklyChallengeMainBoard
        className={className}
        description={strings.earnedPoints.description}
        image={weeklyChallengePng}
        type="result"
      />
    ))
    .with({ type: "notEarnedPoints" }, () => (
      <RewardsWeeklyChallengeMainBoard
        className={className}
        heading={strings.notEarnedPoints.heading}
        description={strings.notEarnedPoints.description}
        image={weeklyChallengePng}
      />
    ))
    .with({ type: "started" }, () => (
      <RewardsWeeklyChallengeQuiz
        questionBlocks={questionBlocks}
        css={dashboardItemContainer}
        setWeeklyChallengeState={setWeeklyChallengeState}
        quizPk={quizPage?.pk ?? 0}
      />
    ))
    .with({ type: "hasErrorMessage" }, ({ errorMessage }) => (
      <div css={container}>{errorMessage}</div>
    ))
    .with({ type: "loading" }, () => (
      <div css={container}>
        <LoadingIndicatorSvg css={icon} />
      </div>
    ))
    .otherwise(() => null);
});

RewardsWeeklyChallenge.displayName = "RewardsWeeklyChallenge";

export default RewardsWeeklyChallenge;
