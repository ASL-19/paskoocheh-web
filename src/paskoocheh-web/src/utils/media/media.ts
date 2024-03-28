import { createMedia } from "@artsy/fresnel";
import { createBreakpointStyles } from "@asl-19/emotion-utils";

import { breakpoints } from "src/values/layoutValues";

export const breakpointStyles = createBreakpointStyles({ breakpoints });

const fresnelMedia = createMedia({ breakpoints });

export const mediaStyles = fresnelMedia.createMediaStyle();

export const { Media, MediaContextProvider } = fresnelMedia;
