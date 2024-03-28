import { css } from "@emotion/react";

import resetStyles from "src/styles/resetStyles";
import { inter } from "src/styles/typeStyles";
import colors from "src/values/colors";
import { lineHeight } from "src/values/layoutValues";

const globalStyles = css(
  resetStyles,
  {
    ".fresnel-container": {
      display: "contents",
    },
    ":focus": {
      outline: "revert",
    },
    a: {
      textDecoration: "none",
    },

    body: {
      margin: "0",
      overflow: "hidden scroll",
    },
    "body *": {
      boxSizing: "border-box",
    },
    button: {
      appearance: "none",
      backgroundColor: "initial",
      border: "none",
      margin: "0",
      padding: "0",
    },
    "button, input[type='button'], input[type='submit']": {
      cursor: "pointer",
    },
    "h1, h2, h3, h4, h5, ol, ul, p": {
      margin: "0",
    },
    html: [
      inter.style,
      {
        backgroundColor: colors.shadesWhite,
        backgroundRepeat: "no-repeat",
        color: colors.secondary500,
        fontSize: "100%",
        fontWeight: "400",
        lineHeight,
        minWidth: "240px",
        textSizeAdjust: "100%",
        WebkitPrintColorAdjust: "exact",
        /* Safari only supports the prefixed version of text-size-adjust */
        WebkitTextSizeAdjust: "100%",
        width: "100%",
      },
    ],
    "html.focusOutlinesHidden *": {
      outline: "none !important",
    },
    "html.ltr": {
      direction: "ltr",
      textAlign: "left",
    },

    "html.rtl": {
      direction: "rtl",
      textAlign: "right",
    },
    /* On iOS devices inputs should never have font sizes smaller than 16px
  because Safari will forcibly zoom the viewport.  */
    "html.userAgentIsIos input, html.userAgentIsIos textarea, html.userAgentIsIos keygen, html.userAgentIsIos select, html.userAgentIsIos button":
      {
        fontSize: "16px",
      },
    img: {
      border: "none",
    },
    "input, textarea, keygen, select, button": {
      borderRadius: "0",
      fontFamily: "inherit",
      fontSize: "inherit",
    },
    li: {
      listStyle: "none",
    },
    "ol, ul": {
      listStyle: "none",
      padding: "0",
    },
  },
  {
    "@media (max-width: 22.4375em)": {
      html: {
        fontSize: "87.5%" /* 14px */,
      },
    },
    "@media(max-width: 28.6875em)": {
      /* 459px */
      html: {
        fontSize: "93.75%" /* 15px */,
      },
    },
    /* On desktop Safari override Ariakit Dialog preventBodyScroll (enabled by
    default) styles  since its scroll bar detection logic doesn’t work correctly.
    See also: Header. */
    "@supports (background: -webkit-named-image(i))": {
      "html:not(.userAgentIsIos) body": {
        backgroundColor: colors.shadesWhite,
        overflow: "hidden scroll !important",
        paddingLeft: "0 !important",
        paddingRight: "0 !important",
      },
    },
  },
);

export default globalStyles;
