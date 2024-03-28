import { asType } from "@asl-19/js-utils";

import { GqlPost, GqlPostPreview } from "src/generated/graphQl";
import topicTestDataBySlug from "src/test/data/topicTestDataBySlug";
import { testPlaceholderWebpCaptionedImage } from "src/test/testValues";

type PostTestDataItem = GqlPost | GqlPostPreview;

const postTestDataBySlug = {
  // cSpell:disable
  "test-post": asType<PostTestDataItem>({
    __typename: "PostNode",
    body: [
      {
        __typename: "TextBlock",
        text: `
            <p>Text block </p>
          `,
      },
    ],
    featuredImage: testPlaceholderWebpCaptionedImage,
    id: "test-post",
    published: "2023-05-31",
    readTime: 0.147,
    searchDescription: "",
    seoTitle: "",
    slug: "test-post",
    summary: "<p>Summary text</p>",
    synopsis: "Synopsis text",
    title: "Title text",
    topics: [
      topicTestDataBySlug["digital-security"],
      topicTestDataBySlug["internet-censorship"],
    ],
  }),
  // cSpell:enable
};

export default postTestDataBySlug;
