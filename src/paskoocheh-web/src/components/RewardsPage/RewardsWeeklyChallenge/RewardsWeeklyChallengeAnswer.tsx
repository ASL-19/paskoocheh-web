import { hoverStyles } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import {
  ChangeEventHandler,
  Dispatch,
  memo,
  SetStateAction,
  useCallback,
  useState,
} from "react";

import { GqlAnswersBlock } from "src/generated/graphQl";
import {
  useWeeklyChallengeQuizQuestionStates,
  WeeklyChallengeQuizSelectedAnswers,
} from "src/stores/weeklyChallengeQuizStore";
import { paragraphP1SemiBold } from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

const container = css(
  {
    display: "flex",
  },
  breakpointStyles({ singleColumn: { lt: { gridColumn: "span 2" } } }),
);
const input = ({
  isCorrect,
  isSubmitted,
}: {
  isCorrect: boolean;
  isSubmitted: boolean;
}) =>
  css(
    {
      display: "none",
    },
    {
      "&:checked + label": {
        backgroundColor: isSubmitted
          ? isCorrect
            ? colors.success500
            : colors.error500
          : "transparent",
        border: `1px solid ${
          isSubmitted
            ? isCorrect
              ? colors.success500
              : colors.error500
            : colors.primary500
        }`,
        color: isSubmitted ? colors.shadesWhite : colors.primary500,
      },
    },
  );
const label = ({
  isChecked,
  isCorrect,
  isSubmitted,
}: {
  isChecked: boolean;
  isCorrect: boolean;
  isSubmitted: boolean;
}) =>
  css(
    paragraphP1SemiBold,
    {
      alignItems: "center",
      border: `1px solid ${
        isSubmitted && isCorrect && isChecked
          ? colors.success500
          : isSubmitted && isCorrect && !isChecked
            ? colors.success500
            : colors.secondary400
      }`,
      borderRadius: "0.5rem",
      color:
        isSubmitted && isCorrect && isChecked
          ? colors.success500
          : isSubmitted && isCorrect && !isChecked
            ? colors.success500
            : colors.secondary400,
      cursor: "pointer",
      display: "flex",
      flex: "1",
    },
    {
      padding: "0 0.65rem",
    },
    !isSubmitted &&
      hoverStyles({
        borderColor: colors.primary500,
        color: colors.primary500,
      }),
  );

const text = css({
  padding: "1rem 0.5rem",
});

const RewardsWeeklyChallengeAnswer: StylableFC<{
  answer: GqlAnswersBlock;
  questionId: string;
  setSelectedAnswers: Dispatch<
    SetStateAction<WeeklyChallengeQuizSelectedAnswers>
  >;
}> = memo(({ answer, className, questionId, setSelectedAnswers }) => {
  const quizQuestionStates = useWeeklyChallengeQuizQuestionStates();

  const isSubmitted = quizQuestionStates?.[questionId]?.isSubmitted ?? false;
  const isCorrect = answer.correct || false;
  const [isChecked, setIsChecked] = useState(
    quizQuestionStates[questionId]?.selectedAnswers.has(answer.id) ?? false,
  );
  const onInputChange: ChangeEventHandler<HTMLInputElement> = useCallback(
    (event) => {
      setIsChecked(event.target.checked);
      setSelectedAnswers(
        () => new Map([[answer.id, event.target.checked === isCorrect]]),
      );
    },
    [answer.id, isCorrect, setSelectedAnswers],
  );

  return (
    <div className={className} css={container}>
      <input
        type="radio"
        id={answer.id}
        name={questionId}
        css={input({ isCorrect, isSubmitted })}
        disabled={isSubmitted}
        defaultChecked={isChecked}
        onChange={onInputChange}
      />
      <label
        htmlFor={answer.id}
        css={label({ isChecked, isCorrect, isSubmitted })}
      >
        <div css={text}>{answer.answer}</div>
      </label>
    </div>
  );
});

RewardsWeeklyChallengeAnswer.displayName = "RewardsWeeklyChallengeAnswer";

export default RewardsWeeklyChallengeAnswer;
