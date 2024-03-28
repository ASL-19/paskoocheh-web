import { getSdk } from "src/generated/graphQl";

const getHasFinishedQuiz: ReturnType<
  typeof getSdk
>["getHasFinishedQuiz"] = () => {
  if (global?.graphQlSdkOverrides?.getHasFinishedQuizResponse) {
    return Promise.resolve(
      global?.graphQlSdkOverrides?.getHasFinishedQuizResponse,
    );
  }

  return Promise.resolve({ me: { hasFinishedQuiz: false } });
};

export default getHasFinishedQuiz;
