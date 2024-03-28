import { gridContainer } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { Dispatch, memo, SetStateAction, useCallback, useState } from "react";

import ButtonButton from "src/components/ButtonButton";
import { WeeklyChallengeState } from "src/components/RewardsPage/RewardsWeeklyChallenge/RewardsWeeklyChallenge";
import RewardsWeeklyChallengeAnswer from "src/components/RewardsPage/RewardsWeeklyChallenge/RewardsWeeklyChallengeAnswer";
import {
  GqlDoReportQuizResults,
  GqlQuestionBlock,
} from "src/generated/graphQl";
import { useAppStrings } from "src/stores/appStore";
import { useRewardsDispatch } from "src/stores/rewardsStore";
import {
  useWeeklyChallengeQuizCurrentQuestionIndex,
  useWeeklyChallengeQuizDispatch,
  useWeeklyChallengeQuizNumberOfCorrectQuestions,
  useWeeklyChallengeQuizQuestionStates,
  WeeklyChallengeQuizSelectedAnswers,
} from "src/stores/weeklyChallengeQuizStore";
import { dashboardItemTitle } from "src/styles/dashboardStyles";
import getErrorMessagesFromExpectedError from "src/utils/api/getErrorMessagesFromResponseErrorsByFieldKey";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getNewPointBalanceAndRewardRecords from "src/utils/getNewPointBalanceAndRewardRecords";
import { breakpointStyles } from "src/utils/media/media";

const answersContainer = css(
  {
    margin: "auto",
    maxWidth: "fit-content",
    padding: "2.5rem 0",
    width: "100%",
  },
  gridContainer({ columns: 1, rowGap: "1.5rem" }),
);

const button = css(
  {
    margin: "auto",
    width: "12.5rem",
  },
  breakpointStyles({ singleColumn: { lt: { width: "100%" } } }),
);

const questionText = css(dashboardItemTitle, { textAlign: "center" });

const RewardsWeeklyChallengeQuestion: StylableFC<{
  numberOfQuestions: number;
  questionBlock: GqlQuestionBlock;
  quizPk: number;
  setWeeklyChallengeState: Dispatch<SetStateAction<WeeklyChallengeState>>;
}> = memo(
  ({
    className,
    numberOfQuestions,
    questionBlock,
    quizPk,
    setWeeklyChallengeState,
  }) => {
    const { shared: sharedStrings } = useAppStrings();

    const quizQuestionStates = useWeeklyChallengeQuizQuestionStates();
    const quizDispatch = useWeeklyChallengeQuizDispatch();
    const rewardsDispatch = useRewardsDispatch();

    const quizCurrentQuestionIndex =
      useWeeklyChallengeQuizCurrentQuestionIndex();
    const numberOfCorrectQuestions =
      useWeeklyChallengeQuizNumberOfCorrectQuestions();

    const [selectedAnswers, setSelectedAnswers] =
      useState<WeeklyChallengeQuizSelectedAnswers>(new Map());

    const onNextButtonClick = useCallback(async () => {
      quizDispatch({ type: "nextQuestion" });

      if (quizCurrentQuestionIndex + 1 === numberOfQuestions) {
        setWeeklyChallengeState({
          type: "loading",
        });

        let reportQuizResults: GqlDoReportQuizResults;
        const graphQlSdk = await getGraphQlSdk({ method: "POST" });

        try {
          reportQuizResults = await graphQlSdk.doReportQuizResults({
            quizPk,
            won: numberOfCorrectQuestions === numberOfQuestions,
          });
        } catch (error) {
          console.error(error);
          setWeeklyChallengeState({
            errorMessage: sharedStrings.errorMessages.networkError,
            type: "hasErrorMessage",
          });

          return;
        }

        if (
          reportQuizResults.reportQuizResults.errors &&
          !reportQuizResults.reportQuizResults.success
        ) {
          const errorMessages = getErrorMessagesFromExpectedError({
            expectedError: reportQuizResults.reportQuizResults.errors,
          });
          console.error(errorMessages);
          setWeeklyChallengeState({
            errorMessage: sharedStrings.errorMessages.networkError,
            type: "hasErrorMessage",
          });
          return;
        }

        const { newPointsBalance, newRewardRecords } =
          await getNewPointBalanceAndRewardRecords();

        if (!newPointsBalance || !newRewardRecords) {
          setWeeklyChallengeState({
            errorMessage: sharedStrings.errorMessages.networkError,
            type: "hasErrorMessage",
          });
          return;
        }

        rewardsDispatch({
          pointsBalance: newPointsBalance,
          rewardRecords: newRewardRecords,
          type: "newRewardRecordLoaded",
        });

        if (numberOfCorrectQuestions === numberOfQuestions) {
          setWeeklyChallengeState({ type: "earnedPoints" });
        } else {
          setWeeklyChallengeState({ type: "notEarnedPoints" });
        }
      }
    }, [
      numberOfCorrectQuestions,
      numberOfQuestions,
      quizCurrentQuestionIndex,
      quizDispatch,
      quizPk,
      rewardsDispatch,
      setWeeklyChallengeState,
      sharedStrings.errorMessages.networkError,
    ]);

    const onSubmitButtonClick = useCallback(() => {
      quizDispatch({
        questionBlockId: questionBlock.id,
        selectedAnswers,
        type: "saveAnswers",
      });
    }, [questionBlock, quizDispatch, selectedAnswers]);

    const isSubmitted =
      quizQuestionStates[questionBlock.id]?.isSubmitted ?? false;

    return (
      <div className={className}>
        <h3 css={questionText}>{questionBlock.question}</h3>
        <div css={answersContainer}>
          {questionBlock.answers?.map((answer) => (
            <RewardsWeeklyChallengeAnswer
              answer={answer}
              key={answer.id}
              setSelectedAnswers={setSelectedAnswers}
              questionId={questionBlock.id}
            />
          ))}
        </div>

        {isSubmitted ? (
          <ButtonButton
            text={sharedStrings.button.next}
            variant="primary"
            onClick={onNextButtonClick}
            css={button}
          />
        ) : (
          <ButtonButton
            text={sharedStrings.button.next}
            variant="primary"
            onClick={onSubmitButtonClick}
            css={button}
          />
        )}
      </div>
    );
  },
);

RewardsWeeklyChallengeQuestion.displayName = "RewardsWeeklyChallengeQuestion";

export default RewardsWeeklyChallengeQuestion;
