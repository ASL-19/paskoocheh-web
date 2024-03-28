import { css } from "@emotion/react";

export const tabsContainer = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "2rem",
});

export const tabContainer = css({
  "html:not(.js) &": {
    display: "flex",
  },
});

export const tabContainerActive = css(tabContainer, {
  display: "flex",
  flexDirection: "column",
  rowGap: "2rem",
});

export const tabContainerInactive = css(tabContainer, {
  display: "none",
});

export const tabDetailsContainer = css({
  columnGap: "2rem",
  display: "flex",
  flexDirection: "column",
  padding: "2rem 1rem",
  rowGap: "2rem",
});
