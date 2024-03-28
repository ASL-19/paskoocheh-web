// Via https://github.com/graphql/vscode-graphql/issues/284#issuecomment-983665679
// (Remove once the extension env issues are fixed.)
require("dotenv").config({ path: __dirname + "/.env.local" });

/** @type {import('graphql-config').IGraphQLConfig} */
const graphQlConfig = {
  documents: "./src/graphQl/**/*.graphql",
  extensions: {
    /** @type {import("@graphql-codegen/cli").CodegenConfig} */
    codegen: {
      generates: {
        "./src/generated/graphQl.ts": {
          config: {
            avoidOptionals: {
              defaultValue: false,
              field: true,
              inputValue: false,
              object: false,
            },
            dedupeFragments: true,
            documentMode: "string",
            enumsAsTypes: true,
            inlineFragmentTypes: "combine",
            omitOperationSuffix: true,
            onlyOperationTypes: true,
            preResolveTypes: true,
            scalars: {
              Date: "string",
              DateTime: "string",
              Decimal: "number",
              ExpectedError: "../types/apiTypes#ExpectedError",
              FlatTags: "../types/apiTypes#FlatTags",
              GlobalID: "string",
              RichTextFieldType: "string",
              UUID: "string",
            },
            skipTypename: true,
            typesPrefix: "Gql",
          },
          overwrite: true,
          plugins: [
            "typescript",
            "typescript-operations",
            "typescript-graphql-request",
          ],
        },
      },
    },
    /** @type {import('./node_modules/graphql-config/typings/extensions/endpoints').Endpoints} */
    endpoints: {
      default: {
        url: `${process.env.NEXT_PUBLIC_BACKEND_URL}/graphql/`,
      },
    },
  },
  schema: "../paskoocheh/schema.json",
};

module.exports = graphQlConfig;
