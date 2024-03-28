import { expect } from "@playwright/test";
import { Page } from "@playwright/test";

import { Strings } from "src/types/stringTypes";
import getPageMetaTitle from "src/utils/getPageMetaTitle";

const expectPageMainHeadingAndMetadata = async ({
  mainHeading,
  metaDescription,
  metaTitle = mainHeading,
  page,
  path,
  strings,
}: {
  mainHeading: string;
  metaDescription: string | null;
  /**
   * `PageMeta` title.
   *
   * Will fall back to `mainHeading` value if not provided (to test home page
   * version with no separating dash pass `null`)
   */
  metaTitle?: string | null;
  page: Page;
  path: string;
  strings: Strings;
}) => {
  // ===============
  // === Content ===
  // ===============

  await expect(
    page.locator("h1#main-heading", { hasText: mainHeading }),
  ).toBeVisible();

  // ================
  // === Metadata ===
  // ================

  await expect(page.locator('meta[name="description"]')).toHaveAttribute(
    "content",
    metaDescription || strings.PageMeta.siteDescription,
  );

  await expect(page).toHaveTitle(
    getPageMetaTitle({
      strings,
      title: metaTitle,
    }),
  );

  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
    "href",
    `${process.env.NEXT_PUBLIC_WEB_URL}${path}`,
  );
};

export default expectPageMainHeadingAndMetadata;
