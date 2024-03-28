import { GqlVersionPreview } from "src/generated/graphQl";
import { isValidVersionPreview, ValidVersionPreview } from "src/types/appTypes";

const getValidVersionPreviews = (
  versionPreviews: Array<GqlVersionPreview>,
): Array<ValidVersionPreview> =>
  versionPreviews.reduce(
    (acc, versionPreview) =>
      isValidVersionPreview(versionPreview) ? [...acc, versionPreview] : acc,
    [],
  );

export default getValidVersionPreviews;
