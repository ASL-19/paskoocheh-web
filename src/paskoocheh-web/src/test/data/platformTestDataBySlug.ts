import { asType } from "@asl-19/js-utils";

import { GqlPlatform } from "src/generated/graphQl";

const platformTestDataBySlug = {
  // cSpell:disable
  android: asType<GqlPlatform>({
    category: "m",
    displayName: "Android",
    displayNameAr: null,
    displayNameFa: "اندروید",
    icon: "platform/ic-android.6b58354c0a47.svg",
    id: "android",
    name: "android",
    pk: 1,
    slugName: "android",
  }),
  chrome: asType<GqlPlatform>({
    category: "w",
    displayName: "Chrome Extension",
    displayNameAr: null,
    displayNameFa: "کروم",
    icon: "platform/ic-chrome.159eb009f899.svg",
    id: "chrome",
    name: "chrome",
    pk: 1,
    slugName: "chrome",
  }),
  linux: asType<GqlPlatform>({
    category: "d",
    displayName: "Linux (64-bit)",
    displayNameAr: null,
    displayNameFa: "لینوکس",
    icon: "platform/ic-linux.d965a11e410a.svg",
    id: "linux",
    name: "linux",
    pk: 4,
    slugName: "linux",
  }),
  macos: asType<GqlPlatform>({
    category: "d",
    displayName: "macOS",
    displayNameAr: null,
    displayNameFa: "مک",
    icon: "platform/ic-mac.0174e84c25e5.svg",
    id: "macos",
    name: "macos",
    pk: 5,
    slugName: "macos",
  }),
  windows: asType<GqlPlatform>({
    category: "d",
    displayName: "Windows (64-bit)",
    displayNameAr: null,
    displayNameFa: "ویندوز",
    icon: "platform/ic-windows.dac51b95b4ce.svg",
    id: "windows",
    name: "windows",
    pk: 6,
    slugName: "windows",
  }),
  // cSpell:enable
};

export default platformTestDataBySlug;
