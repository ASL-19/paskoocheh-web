export const localeCodes = ["en", "fa"] as const;

export type LocaleCode = (typeof localeCodes)[number];

/**
 * Subset of localeCodes.
 *
 * In the future this may have some locale codes conditionally added based on
 * environment variables so we can test on dev/staging without deploying to prod.
 */
export const enabledLocaleCodes: Array<(typeof localeCodes)[number]> = [
  "en",
  "fa",
];
