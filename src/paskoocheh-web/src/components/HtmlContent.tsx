import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import {
  headingH3SemiBold,
  headingH4SemiBold,
  headingH5SemiBold,
  headingH6SemiBold,
  paragraphP1Regular,
} from "src/styles/typeStyles";

const container = css([
  paragraphP1Regular,
  { overflow: "hidden" },
  {
    h1: headingH3SemiBold,

    h2: headingH4SemiBold,

    h3: headingH5SemiBold,

    "h4, h5, h6": headingH6SemiBold,

    "p, ol, ul, li, h1, h2, h3, h4, h5, h6": {
      "&:last-child": {
        marginBottom: "0",
      },

      margin: "0 0 1rem",
    },
  },
  {
    li: {
      listStyleType: "inherit",
      marginInlineStart: "1.5em",
    },
    ol: {
      listStylePosition: "inside",
      padding: "2rem",
    },
    ul: {
      listStyleType: "disc",
    },
  },
  {
    "html.en &": {
      ol: {
        listStyleType: "decimal",
      },
    },

    "html.fa &": {
      ol: {
        listStyleType: "persian",
      },
    },
  },
  {
    /* ====================================
    === Embed aspect ratio preservation ===
    ==================================== */
    // Based on https://css-tricks.com/responsive-iframes/
    //
    // Give video embeds a default size of 640x360px (not responsive, but better
    // than tiny default size.
    ".contains-video[style*='--aspect-ratio'] > *": {
      height: "360px",
      maxWidth: "100%",
      width: "640px",
    },

    // If the browser can read custom properties:
    "@supports (--custom: property)": {
      "[style*='--aspect-ratio']": {
        maxWidth: "40rem",
        position: "relative",
        width: "100%",
      },

      // Make the iframe fill the space of its sized container div.
      "[style*='--aspect-ratio'] > *": {
        height: "100% !important",
        left: "0",
        position: "absolute",
        top: "0",
        width: "100% !important",
      },

      // Because padding is relative to width we can use it as a hack to force
      // the aspect ratio of the container.
      "[style*='--aspect-ratio']::before": {
        content: '""',
        display: "block",
        paddingBottom: "calc(100% / (var(--aspect-ratio)))",
      },
    },
  },
]);

/**
 * HTML content. Should be used for any rendered HTML strings.
 *
 * **HTML content must be trusted — uses dangerouslySetInnerHTML prop to
 * emphasize this!**
 *
 * Includes:
 *
 * - Reasonable default styles (e.g. margins between blocks, heading font sizes,
 *   and list styles)
 *
 * - Aspect ratio of embedded content (iframes inside divs) is preserved if the
 *   iframe has numerical width and height attributes. YouTube and Vimeo iframes
 *   are set to 16:9 by default.
 */
const HtmlContent: StylableFC<{
  dangerousHtml: string;
}> = memo(({ className, dangerousHtml }) => (
  <div
    className={className}
    css={container}
    dangerouslySetInnerHTML={{ __html: dangerousHtml }}
  />
));

HtmlContent.displayName = "HtmlContent";

export default HtmlContent;
