// Based on https://github.com/zeit/next.js/tree/canary/examples/with-jest

const dotenv = require("dotenv");
const nextJest = require("next/jest");

dotenv.config({ override: true, path: ".env.test" });
const validateEnvironmentVariables = require("./src/utils/environment/validateEnvironmentVariables");

validateEnvironmentVariables();

// @ts-expect-error (seems like next/jest’s compiled CJS is wrong?)
const createJestConfig = nextJest();

/** @type {import('@jest/types').Config.InitialOptions} */
const jestConfig = {
  // Fix module resolution when using `npm link` to test shared packages that
  // rely on e.g. "next/router"
  //
  // Via https://github.com/jestjs/jest/issues/2447#issuecomment-454748972
  moduleDirectories: ["<rootDir>/node_modules", "node_modules"],
  moduleNameMapper: {
    "^src/(.*)": "<rootDir>/src/$1",
  },
  modulePathIgnorePatterns: ["<rootDir>/.next", "<rootDir>/.next-test"],
  setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
  testEnvironment: "jest-environment-jsdom",
  testRegex: ".*\\.jest\\.test\\.tsx?$",
};

module.exports = createJestConfig(jestConfig);
