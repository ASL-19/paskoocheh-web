import { asType } from "@asl-19/js-utils";

import { GqlVersionPreview } from "src/generated/graphQl";
import platformTestDataBySlug from "src/test/data/platformTestDataBySlug";
import toolPreviewTestDataBySlug from "src/test/data/toolPreviewTestDataBySlug";

const versionPreviewTestDataBySlug = {
  // cSpell:disable
  "beepass-vpn": asType<GqlVersionPreview>({
    averageRating: {
      ratingCount: 5,
      starRating: 3.7,
    },
    downloadCount: 3998,
    id: "VmVyc2lvbk5vZGU6Mzgz",
    pk: 383,
    platform: platformTestDataBySlug["android"],
    tool: toolPreviewTestDataBySlug["beepass-vpn"],
  }),
  // cSpell:enable
};

export default versionPreviewTestDataBySlug;
