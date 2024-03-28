/**
 * Space the scroll bar could be taking up.
 *
 * @remarks
 * Browsers don’t take the scroll bar width into account when evaluating the
 * sizes media conditions, so we need to add some slack to the calculation so
 * browsers with inset scroll bars (macOS when the "Show scroll bars" setting is
 * set to always, Windows, and Chrome OS?) don’t download smaller images when
 * close to the boundary between conditions.
 *
 * AFAIK no popular OS has scroll bars that take up more than 20px.
 *
 * @see https://gist.github.com/martynchamberlin/6aaf8a45b36907e9f1e21a28889f6b0a
 */
const scrollbarLeeway = "20px";

/**
 * Generate an `<img />` (Next.js `<Image />`) `sizes` attribute appropriate for
 * an image in a multi-column grid layout.
 *
 * @see https://kurtextrem.de/posts/modern-way-of-img#width-descriptors
 */
const getResponsiveGridItemImageSizes = ({
  columnGap,
  maxColumns,
  minColumnWidth,
  paddingInline,
}: {
  /**
   * Inline gap between items inside the container.
   */
  columnGap: string;
  /**
   * Maximum number of columns.
   */
  maxColumns: number;
  /**
   * Minimum column width.
   *
   * e.g. `20rem` in `repeat(auto-fill, minmax(19rem, 1fr))`.
   */
  minColumnWidth: string;
  /**
   * Outside inline padding (between container and viewport edges).
   */
  paddingInline: string;
}) => {
  const columnCounts = Array.from({ length: maxColumns })
    .map((_, columnCount) => columnCount + 1)
    .reverse();

  const items = columnCounts.map((columnCount) => {
    const paddingInlineSpace = `${paddingInline} * 2`;
    const columnGapsSpace =
      columnCount > 1 ? `${columnGap} * ${columnCount - 1}` : "0";

    const mediaFeature =
      columnCount > 1
        ? `
        (min-width:
          calc(
            ${paddingInlineSpace}
            + ${minColumnWidth} * ${columnCount}
            + ${columnGapsSpace}
            + ${scrollbarLeeway}
          )
        )`
        : "";

    const width = `calc(
      (100vw - ${paddingInlineSpace} - ${columnGapsSpace})
      / ${columnCount}
    )`;

    return `${mediaFeature} ${width}`
      .replace(/\n/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  });

  return items.join(", ");
};

export default getResponsiveGridItemImageSizes;
