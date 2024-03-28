import { pageSegmentPaddingInline } from "src/components/Page/PageSegment";
import getResponsiveGridItemImageSizes from "src/utils/getResponsiveGridItemImageSizes";

export const columnCount = 12;

export const headerHeight = "4.75rem";

export const lineHeight = 1.6875;

/* eslint-disable sort-keys-fix/sort-keys-fix */
export const breakpoints = {
  narrow: 0,
  singleColumn: 688,
  tablet: 728,
  desktopNarrow: 1024,
  desktopFull: 1440,
} as const;

export const buttonHeights = {
  small: "2rem",
  medium: "2.5rem",
  large: "3.125rem",
} as const;

export const dropdownGutterPx = 8;

export const formPageContentWidths = {
  regular: "41.75rem",
  narrow: "27.875rem",
} as const;

export const mediaFeatures = {
  viewportWidthLtSingleColumn: `(max-width: ${breakpoints.singleColumn - 1}px)`,
  viewportWidthLteSingleColumn: `(max-width: ${breakpoints.singleColumn}px)`,
  viewportWidthGteSingleColumn: `(min-width: ${breakpoints.singleColumn}px)`,
  viewportWidthGtSingleColumn: `(min-width: ${breakpoints.singleColumn + 1}px)`,
  viewportWidthGteMultiColumn: `(min-width: ${breakpoints.singleColumn}px)`,
  viewportWidthLtTablet: `(max-width: ${breakpoints.tablet - 1}px)`,
  viewportWidthLteTablet: `(max-width: ${breakpoints.tablet}px)`,
  viewportWidthGteTablet: `(min-width: ${breakpoints.tablet}px)`,
  viewportWidthLteDesktopNarrow: `(max-width: ${breakpoints.desktopNarrow}px)`,
  viewportWidthLtDesktopNarrow: `(max-width: ${
    breakpoints.desktopNarrow - 1
  }px)`,
  viewportWidthGteDesktopNarrow: `(min-width: ${breakpoints.desktopNarrow}px)`,
  viewportWidthLtDesktopFull: `(max-width: ${breakpoints.desktopFull - 1}px)`,
  viewportWidthGteDesktopFull: `(min-width: ${breakpoints.desktopFull}px)`,
} as const;
/* eslint-enable sort-keys-fix/sort-keys-fix */

export const threeColumnGridContainerImageSizes =
  getResponsiveGridItemImageSizes({
    columnGap: "1.25rem",
    maxColumns: 3,
    minColumnWidth: "19rem",
    paddingInline: pageSegmentPaddingInline,
  });
