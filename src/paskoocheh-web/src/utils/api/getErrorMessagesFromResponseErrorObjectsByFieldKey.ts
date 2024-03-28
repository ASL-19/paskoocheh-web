import { ErrorsObjectsByFieldKey } from "src/types/apiTypes";

const getErrorMessagesFromResponseErrorObjectsByFieldKey = ({
  responseErrorsByFieldKey,
}: {
  responseErrorsByFieldKey: ErrorsObjectsByFieldKey;
}): Array<string> =>
  Object.keys(responseErrorsByFieldKey).flatMap((fieldKey) =>
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    responseErrorsByFieldKey[fieldKey]!.reduce(
      (acc, responseError) =>
        typeof responseError.message === "string"
          ? [...acc, responseError.message]
          : acc,
      [],
    ),
  );

export default getErrorMessagesFromResponseErrorObjectsByFieldKey;
