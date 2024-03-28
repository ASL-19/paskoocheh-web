import { asType } from "@asl-19/js-utils";

import { GqlStaticPage } from "src/generated/graphQl";
import { testPlaceholderWebpCaptionedImage } from "src/test/testValues";

const staticPageTestDataBySlug = {
  // cSpell:disable
  about: asType<GqlStaticPage>({
    body: [
      {
        __typename: "TextBlock",
        text: `<p>Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance.</p>`,
      },
      {
        __typename: "CaptionedImageBlock",
        image: testPlaceholderWebpCaptionedImage,
        value: null,
      },
      {
        __typename: "TextBlock",
        text: `<p>The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham. Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC,nglish versions from the 1914 translation by H. Rackham.</p>`,
      },
    ],
    image: testPlaceholderWebpCaptionedImage,
    searchDescription: "About Us SEO description",
    seoTitle: "About Us SEO title",
    title:
      "Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum is simply dummy text of the printing and typesetting industry",
  }),

  "privacy-policy": asType<GqlStaticPage>({
    body: [
      {
        __typename: "TextBlock",
        text: "<p>Privacy policy mock body.</p>",
      },
    ],
    image: null,
    searchDescription: "Privacy policy SEO description",
    seoTitle: "Privacy policy SEO title",
    title: "Privacy Policy",
  }),

  "terms-of-service": asType<GqlStaticPage>({
    body: [
      {
        __typename: "TextBlock",
        text: "<p>Terms of service mock body.</p>",
      },
    ],
    image: null,
    searchDescription: "Terms of service SEO description",
    seoTitle: "Terms of service SEO title",
    title: "Terms and Conditions",
  }),
  // cSpell:enable
};

export default staticPageTestDataBySlug;
