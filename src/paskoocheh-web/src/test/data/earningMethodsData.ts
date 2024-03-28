import { asType } from "@asl-19/js-utils";

import { GqlEarningMethod } from "src/generated/graphQl";

const earningMethodsData = {
  quizComplete: asType<GqlEarningMethod>({
    earningMethod: "quiz_completed",
    earningPoints: 1,
    pk: 2,
  }),
  quizWon: asType<GqlEarningMethod>({
    earningMethod: "quiz_won",
    earningPoints: 2,
    pk: 3,
  }),
  review: asType<GqlEarningMethod>({
    earningMethod: "review",
    earningPoints: 1,
    pk: 1,
  }),
};

export default earningMethodsData;
