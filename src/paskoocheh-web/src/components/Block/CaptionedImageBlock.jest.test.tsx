import { screen } from "@testing-library/react";
import { ComponentProps } from "react";

import CaptionedImageBlock, {
  getCaptionedImageCaption,
} from "src/components/Block/CaptionedImageBlock";
import { testPlaceholderWebpCaptionedImage } from "src/test/testValues";
import testRender from "src/utils/jest/testRender";

const block: ComponentProps<typeof CaptionedImageBlock>["block"] = {
  __typename: "CaptionedImageBlock",
  image: testPlaceholderWebpCaptionedImage,
  value: null,
};

test("CaptionedImageBlock renders the provided block", async () => {
  testRender(<CaptionedImageBlock block={block} imageSizes="100vw" />);

  expect(
    screen.getByAltText(testPlaceholderWebpCaptionedImage.caption),
  ).toBeInTheDocument();

  const caption = getCaptionedImageCaption(block.image);

  expect(screen.getByText(caption)).toBeInTheDocument();
});
