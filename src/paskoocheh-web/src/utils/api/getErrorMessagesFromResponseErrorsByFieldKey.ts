import { ExpectedError } from "src/types/apiTypes";

const getErrorMessagesFromExpectedError = ({
  expectedError,
}: {
  expectedError: ExpectedError;
}): Array<string> =>
  Object.keys(expectedError).flatMap((fieldKey) =>
    (expectedError[fieldKey] ?? []).reduce(
      (acc, item) => (item.message ? [...acc, item.message] : acc),
      [],
    ),
  );

export default getErrorMessagesFromExpectedError;
