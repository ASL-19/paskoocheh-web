export const rewardsDetailsSectionIds = {
  dashboard: "dashboard",
  myReview: "my-review",
  redemption: "redemption",
} as const;

export type RewardsDetailsSectionId =
  (typeof rewardsDetailsSectionIds)[keyof typeof rewardsDetailsSectionIds];
