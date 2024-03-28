export const appDetailsSectionIds = {
  additionalInfo: "additional-information",
  faq: "faq",
  howToUse: "how-to-use",
  ratingsAndReviews: "ratings-and-reviews",
  teamAnalysis: "team-analysis",
} as const;

export type AppDetailsSectionId =
  (typeof appDetailsSectionIds)[keyof typeof appDetailsSectionIds];
