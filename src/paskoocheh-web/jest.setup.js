// Based on https://github.com/zeit/next.js/tree/canary/examples/with-jest
import "@testing-library/jest-dom";

const { configure } = require("@testing-library/react");

jest.mock("src/utils/config/getGraphQlSdk.ts");

// Via https://github.com/vercel/next.js/issues/16864#issuecomment-702069418
jest.mock(
  "next/link",
  () =>
    ({ children }) =>
      children,
);

// ===============================
// === Increase timeouts in CI ===
// ===============================
//
// Raise Jest test and React Testing Library async utility timeouts in CI

if (process.env.CI) {
  jest.setTimeout(15000); // Default is 5000

  configure({
    asyncUtilTimeout: 10000, // Default is 1000
  });
}

afterEach(() => {
  globalThis.graphQlSdkOverrides = undefined;
});
