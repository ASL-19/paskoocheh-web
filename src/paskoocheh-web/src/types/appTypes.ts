import {
  GqlPlatform,
  GqlTool,
  GqlToolImage,
  GqlToolPreview,
  GqlToolType,
  GqlVersion,
  GqlVersionPreview,
} from "src/generated/graphQl";

// Via https://stackoverflow.com/questions/76367389/satisfies-but-for-types#comment134663437_76367389
type Satisfies<U, T extends U> = T;

// =========================================
// === ValidToolOrToolPreview (internal) ===
// =========================================

type ValidToolOrToolPreviewProperties = Satisfies<
  Partial<GqlTool | GqlToolPreview>,
  {
    availablePlatforms: [string, ...Array<string>];
    toolTypes: [GqlToolType, ...Array<GqlToolType>];
  }
>;

// Not a type guard function since I’m not sure if it’s possible to make a type
// guard function with a conditional type predicate
const isValidToolOrToolPreview = (
  toolOrToolPreview: GqlTool | GqlToolPreview,
) =>
  typeof toolOrToolPreview.availablePlatforms?.[0] === "string" &&
  typeof toolOrToolPreview.toolTypes?.[0] === "object" &&
  toolOrToolPreview.toolTypes?.[0] !== null;

// =================
// === ValidTool ===
// =================

export type ValidTool = GqlTool &
  Satisfies<Partial<GqlTool>, ValidToolOrToolPreviewProperties>;

export const isValidTool = (tool: GqlTool): tool is ValidTool =>
  isValidToolOrToolPreview(tool);

// ========================
// === ValidToolPreview ===
// ========================

export type ValidToolPreview = GqlToolPreview &
  Satisfies<Partial<GqlToolPreview>, ValidToolOrToolPreviewProperties>;

export const isValidToolPreview = (
  tool: GqlToolPreview,
): tool is ValidToolPreview => isValidToolOrToolPreview(tool);

// ====================
// === ValidVersion ===
// ====================

export type ValidVersion = GqlVersion &
  Satisfies<
    Partial<GqlVersion>,
    {
      platform: GqlPlatform;
      tool: ValidTool;
    }
  >;

export const isValidVersion = (version: GqlVersion): version is ValidVersion =>
  version.platform !== null &&
  version.tool !== null &&
  isValidToolPreview(version.tool);

// ===========================
// === ValidVersionPreview ===
// ===========================

export type ValidVersionPreview = GqlVersionPreview & {
  platform: GqlPlatform;
  tool: ValidToolPreview;
};

export const isValidVersionPreview = (
  versionPreview: GqlVersionPreview,
): versionPreview is ValidVersionPreview =>
  versionPreview.platform !== null &&
  versionPreview.tool !== null &&
  isValidToolPreview(versionPreview.tool);

// ======================
// === ValidToolImage ===
// ======================

export type ValidToolImage = GqlToolImage & {
  height: number;
  imageType: string;
  width: number;
};

export const isValidToolImage = (
  toolImage: GqlToolImage,
): toolImage is ValidToolImage =>
  typeof toolImage.height === "number" &&
  typeof toolImage.imageType === "string" &&
  typeof toolImage.width === "number";
