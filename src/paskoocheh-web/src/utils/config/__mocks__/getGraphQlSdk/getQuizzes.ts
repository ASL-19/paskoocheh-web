import { getSdk } from "src/generated/graphQl";
import quizPageTestDataBySlug from "src/test/data/quizPageTestDataBySlug";

const getQuizzes: ReturnType<typeof getSdk>["getQuizzes"] = () => {
  if (global?.graphQlSdkOverrides?.getQuizzesResponse) {
    return Promise.resolve(global.graphQlSdkOverrides.getQuizzesResponse);
  }

  const quizzes = Object.values(quizPageTestDataBySlug);

  return Promise.resolve({
    quizzes: {
      edges: quizzes.map((quiz) => ({
        node: quiz,
      })),
      pageInfo: { endCursor: null, hasNextPage: false },
    },
  });
};

export default getQuizzes;
