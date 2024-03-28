import { PlaywrightTestConfig } from "@playwright/test";
import dotenv from "dotenv";

import validateEnvironmentVariables from "src/utils/environment/validateEnvironmentVariables";

dotenv.config({ override: true, path: ".env.test" });
validateEnvironmentVariables();

const config: PlaywrightTestConfig = {
  testMatch: /.*\.playwright\.test\.ts$/,
  use: {
    browserName: "chromium",
    headless: true,
  },
  webServer: {
    command: "npm run test-start",
    port: 3001,
    reuseExistingServer: true,
    timeout: 360 * 1000,
  },
};

export default config;
