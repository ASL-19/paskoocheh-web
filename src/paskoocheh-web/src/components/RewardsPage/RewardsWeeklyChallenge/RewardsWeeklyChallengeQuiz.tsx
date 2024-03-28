import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { Dispatch, memo, SetStateAction, useCallback } from "react";

import ArrowSvg from "src/components/icons/general/ArrowSvg";
import { WeeklyChallengeState } from "src/components/RewardsPage/RewardsWeeklyChallenge/RewardsWeeklyChallenge";
import RewardsWeeklyChallengeQuestion from "src/components/RewardsPage/RewardsWeeklyChallenge/RewardsWeeklyChallengeQuestion";
import { GqlQuestionBlock } from "src/generated/graphQl";
import {
  useWeeklyChallengeQuizCurrentQuestionIndex,
  useWeeklyChallengeQuizDispatch,
} from "src/stores/weeklyChallengeQuizStore";

const prevButton = css(
  {
    position: "absolute",
  },
  {
    'html[dir="ltr"] &': {
      left: 0,
    },
    'html[dir="rtl"] &': {
      right: 0,
    },
  },
);
const icon = css({
  height: "1.25rem",
});
const heading = css({
  display: "flex",
  justifyContent: "center",
  position: "relative",
  width: "100%",
});

const RewardsWeeklyChallengeQuiz: StylableFC<{
  questionBlocks: Array<GqlQuestionBlock>;
  quizPk: number;
  setWeeklyChallengeState: Dispatch<SetStateAction<WeeklyChallengeState>>;
}> = memo(({ className, questionBlocks, quizPk, setWeeklyChallengeState }) => {
  const quizCurrentQuestionIndex = useWeeklyChallengeQuizCurrentQuestionIndex();

  const quizDispatch = useWeeklyChallengeQuizDispatch();

  const onPrevButtonClick = useCallback(
    () => quizDispatch({ type: "prevQuestion" }),
    [quizDispatch],
  );

  const currentQuestionBlock = questionBlocks[quizCurrentQuestionIndex];

  return (
    <div className={className}>
      <div css={heading}>
        {quizCurrentQuestionIndex > 0 && (
          <button onClick={onPrevButtonClick} css={prevButton}>
            <ArrowSvg css={icon} direction="start" />
          </button>
        )}

        <span>
          {quizCurrentQuestionIndex + 1}/{questionBlocks.length}
        </span>
      </div>

      {currentQuestionBlock && (
        <RewardsWeeklyChallengeQuestion
          questionBlock={currentQuestionBlock}
          numberOfQuestions={questionBlocks.length}
          setWeeklyChallengeState={setWeeklyChallengeState}
          quizPk={quizPk}
        />
      )}
    </div>
  );
});

RewardsWeeklyChallengeQuiz.displayName = "RewardsWeeklyChallengeQuiz";

export default RewardsWeeklyChallengeQuiz;
