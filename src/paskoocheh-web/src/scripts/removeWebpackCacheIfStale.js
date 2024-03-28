const { readFileSync, rmSync, writeFileSync } = require("fs");

const previousEnableMockGraphqlSdkValueFilePath =
  "./.previousEnableMockGraphqlSdkValue";

const previousEnableMockGraphqlSdkValue = (() => {
  try {
    return readFileSync(previousEnableMockGraphqlSdkValueFilePath, "utf-8");
  } catch {
    return null;
  }
})();

const currentEnableMockGraphqlSdkValue =
  process.env.NEXT_PUBLIC_ENABLE_MOCK_GRAPHQL_SDK || "";

if (
  previousEnableMockGraphqlSdkValue !== null &&
  previousEnableMockGraphqlSdkValue !== currentEnableMockGraphqlSdkValue
) {
  console.info(
    "Removing Next.js Webpack cache because NEXT_PUBLIC_ENABLE_MOCK_GRAPHQL_SDK value changed",
  );

  rmSync("./.next/cache/webpack", { force: true, recursive: true });
}

writeFileSync(
  previousEnableMockGraphqlSdkValueFilePath,
  currentEnableMockGraphqlSdkValue,
  "utf-8",
);
