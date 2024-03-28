import { asType } from "@asl-19/js-utils";

import { GqlVersionReview } from "src/generated/graphQl";

const versionReviewsById = {
  // cSpell:disable
  review1: asType<GqlVersionReview>({
    categoryRatings: [],
    checked: true,
    downvotes: 0,
    hasUserVoted: { hasVoted: false, voteType: "NOVOTE" },
    id: "review1",
    language: "fa",
    lastModified: "2021-01-07T17:40:21.505698+00:00",
    pk: 1,
    platformName: "android",
    rating: 5.0,
    subject: null,
    text: "لطفا لینوکس رو هم فراموش نکنید",
    timestamp: "2021-01-07T17:37:07+00:00",
    toolName: "BeePass VPN",
    toolVersion: "1.0.0-beta.15",
    upvotes: 0,
    userId: null,
    username: "abc123",
  }),
  // cSpell:enable
};

export default versionReviewsById;
