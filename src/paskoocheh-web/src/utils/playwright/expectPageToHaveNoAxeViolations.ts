import AxeBuilder from "@axe-core/playwright";
import { expect } from "@playwright/test";
import { Page } from "@playwright/test";

const expectPageToHaveNoAxeViolations = async ({ page }: { page: Page }) => {
  const axeResults = await new AxeBuilder({ page })
    .disableRules(["color-contrast"])
    .analyze();

  return expect(axeResults.violations).toHaveLength(0);
};

export default expectPageToHaveNoAxeViolations;
