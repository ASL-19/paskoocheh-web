import { getObjectValueByDotSeparatedKey } from "@asl-19/js-utils";

import { StringKey, Strings } from "src/types/stringTypes";

const getStringByDotSeparatedKey = ({
  dotSeparatedKey,
  strings,
}: {
  dotSeparatedKey: StringKey;
  strings: Strings;
}) =>
  // @ts-expect-error (stringKey is guaranteed to be the key of a Strings leaf)
  getObjectValueByDotSeparatedKey<string>({
    dotSeparatedKey,
    object: strings,
  }) as string;

export default getStringByDotSeparatedKey;
