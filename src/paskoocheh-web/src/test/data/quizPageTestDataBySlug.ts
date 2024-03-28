import { asType } from "@asl-19/js-utils";

import { GqlQuizPage } from "src/generated/graphQl";
import questionBlockTestDataById from "src/test/data/questionBlockTestDataById";

const quizPageTestDataBySlug = {
  sampleQuiz: asType<GqlQuizPage>({
    id: "quiz1",
    numchild: 1,
    pk: 1,
    questions: [questionBlockTestDataById.question1],
    searchDescription: "This is a mock description for the sample quiz.",
    seoTitle: "Sample Quiz for Testing",
    slug: "sample-quiz",
    title: "Sample Quiz",
    urlPath: "/quizzes/sample-quiz/",
  }),
};

export default quizPageTestDataBySlug;
