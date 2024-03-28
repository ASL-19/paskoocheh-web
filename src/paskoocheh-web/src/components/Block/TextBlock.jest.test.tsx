import { ComponentProps } from "react";

import TextBlock from "src/components/Block/TextBlock";
import testRender from "src/utils/jest/testRender";

const block: ComponentProps<typeof TextBlock>["block"] = {
  __typename: "TextBlock",
  text: "<p>Foo</p>",
};

test("TextBock renders the provided block", async () => {
  testRender(<TextBlock block={block} />);

  expect(document.body).toContainHTML(block.text);
});
