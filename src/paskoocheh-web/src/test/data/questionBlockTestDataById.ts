import { asType } from "@asl-19/js-utils";

import { GqlQuestionBlock } from "src/generated/graphQl";

const questionBlockTestDataById = {
  question1: asType<GqlQuestionBlock>({
    __typename: "QuestionBlock",
    answers: [
      {
        __typename: "AnswersBlock",
        answer: "Paris",
        correct: true,
        id: "a1",
        value: "Paris",
      },
      {
        __typename: "AnswersBlock",
        answer: "London",
        correct: false,
        id: "a2",
        value: "London",
      },
    ],
    id: "question1",
    question: "What's the capital of France?",
    value: "What's the capital of France?",
  }),
};

export default questionBlockTestDataById;
