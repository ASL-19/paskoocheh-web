import constate from "constate";
import { useReducer } from "react";
import { match } from "ts-pattern";

import reducerLog from "src/utils/store/reducerLog";

export type WeeklyChallengeQuizSelectedAnswers = Map<string, boolean>;

type WeeklyChallengeQuizQuestionState = {
  isCorrect: boolean;
  isSubmitted: boolean;
  selectedAnswers: WeeklyChallengeQuizSelectedAnswers;
};

export type WeeklyChallengeQuizState = {
  currentQuestionIndex: number;
  hasFinishedQuiz: boolean | null;
  numberOfCorrectQuestions: number;
  questionStates: {
    [questionBlockId: string]: WeeklyChallengeQuizQuestionState;
  };
};
type WeeklyChallengeQuizAction =
  | { type: "nextQuestion" }
  | { type: "prevQuestion" }
  | { type: "hasFinishedQuiz" }
  | {
      questionBlockId: string;
      selectedAnswers: WeeklyChallengeQuizSelectedAnswers;
      type: "saveAnswers";
    };

function reducer(
  state: WeeklyChallengeQuizState,
  action: WeeklyChallengeQuizAction,
) {
  const newState: WeeklyChallengeQuizState = match(action)
    .with({ type: "nextQuestion" }, () => {
      return { ...state, currentQuestionIndex: state.currentQuestionIndex + 1 };
    })
    .with({ type: "prevQuestion" }, () => {
      return { ...state, currentQuestionIndex: state.currentQuestionIndex - 1 };
    })
    .with({ type: "hasFinishedQuiz" }, () => {
      return { ...state, hasFinishedQuiz: true };
    })
    .with({ type: "saveAnswers" }, (action) => {
      const isCorrect =
        [...action.selectedAnswers.values()].length > 0 &&
        [...action.selectedAnswers.values()].every((item) => item);

      const numberOfCorrectQuestions = isCorrect
        ? state.numberOfCorrectQuestions + 1
        : state.numberOfCorrectQuestions;

      return {
        ...state,
        numberOfCorrectQuestions,
        questionStates: {
          ...state.questionStates,
          [action.questionBlockId]: {
            isCorrect,
            isSubmitted: true,
            selectedAnswers: action.selectedAnswers,
          },
        },
      };
    })
    .exhaustive();

  reducerLog({
    action,
    newState,
    state,
    storeName: "weeklyChallengeQuiz",
  });

  return newState;
}
const useWeeklyChallengeQuiz = ({
  initialState,
}: {
  initialState: WeeklyChallengeQuizState;
}) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  return { dispatch, state };
};

export const [
  WeeklyChallengeQuizProvider,
  useWeeklyChallengeQuizDispatch,
  useWeeklyChallengeQuizQuestionStates,
  useWeeklyChallengeQuizCurrentQuestionIndex,
  useWeeklyChallengeQuizNumberOfCorrectQuestions,
  useHasFinishedWeeklyChallengeQuiz,
] = constate(
  useWeeklyChallengeQuiz,
  (value) => value.dispatch,
  (value) => value.state.questionStates,
  (value) => value.state.currentQuestionIndex,
  (value) => value.state.numberOfCorrectQuestions,
  (value) => value.state.hasFinishedQuiz,
);
