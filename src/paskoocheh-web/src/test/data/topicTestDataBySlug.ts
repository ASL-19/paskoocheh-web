import { asType } from "@asl-19/js-utils";

import { GqlTopic } from "src/generated/graphQl";

const topicTestDataBySlug = {
  // cSpell:disable
  "digital-security": asType<GqlTopic>({
    __typename: "TopicNode",
    id: "topic1",
    name: "Digital security",
    pk: 3,
    slug: "digital-security",
  }),
  "internet-censorship": asType<GqlTopic>({
    __typename: "TopicNode",
    id: "topic2",
    name: "Internet Censorship",
    pk: 12,
    slug: "internet-censorship",
  }),
  // cSpell:enable
};

export default topicTestDataBySlug;
