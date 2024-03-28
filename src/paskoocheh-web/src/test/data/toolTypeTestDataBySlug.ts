import { asType } from "@asl-19/js-utils";

import { GqlToolType } from "src/generated/graphQl";

const toolTypeTestDataBySlug = {
  // cSpell:disable
  browser: asType<GqlToolType>({
    icon: "", // TODO: Add icon?
    id: "browser",
    name: "Browsers",
    nameFa: "Browsers",
    pk: 12,
    slug: "browser",
  }),
  circumvention: asType<GqlToolType>({
    icon: "",
    id: "circumvention",
    name: "Circumvention",
    nameFa: "فیلترشکن",
    pk: 10,
    slug: "circumvention",
  }),
  "civil-good": asType<GqlToolType>({
    icon: "",
    id: "civil-good",
    name: "Civil Good",
    nameFa: "Civil Good",
    pk: 10,
    slug: "civil-good",
  }),
  entertainment: asType<GqlToolType>({
    icon: "",
    id: "entertainment",
    name: "Entertainment",
    nameFa: "Entertainment",
    pk: 9,
    slug: "entertainment",
  }),
  // cSpell:enable
};

export default toolTypeTestDataBySlug;
