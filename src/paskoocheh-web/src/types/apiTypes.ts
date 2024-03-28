import type { Sdk } from "src/generated/graphQl";

export type FlatTags = Array<{
  name: string;
  slug: string;
}>;

export type SdkWithHasAccessToken = Sdk & { hasAccessToken: boolean };

type ErrorObject = {
  code: string;
  message: string;
};

export type ErrorsObjectsByFieldKey = {
  [fieldKey: string]: Array<ErrorObject>;
};
/**
 * Errors messages and codes mapped to fields or non-field errors (based on
 * `schema.graphql` `ExpectedError` comment)
 */
export type ExpectedError = {
  [fieldKey: string]: Array<{
    code: string;
    message: string;
  }>;
};
