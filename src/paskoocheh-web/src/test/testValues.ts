import { GqlCaptionedImage, GqlPskCaptionedImage } from "src/generated/graphQl";

export const testDefaultRouteArgs = {
  localeCode: "en",
  platform: "android",
} as const;

export const testPlaceholderWebpCaptionedImage: GqlCaptionedImage &
  GqlPskCaptionedImage = {
  caption: "Mock image caption",
  credit: "Mock image credit",
  file: "/testImages/placeholder.webp",
  height: 500,
  id: "/testImages/placeholder.webp",
  width: 1144,
};
