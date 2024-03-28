import { pageSegmentPaddingInline } from "src/components/Page/PageSegment";

// 66vw is rough calculation based on the grid inset
export const blogPostContentMaxWidth = `57rem`;

export const blogPostFullWidthImageSizes = `(min-width: calc(${blogPostContentMaxWidth} + ${pageSegmentPaddingInline} * 2)) ${blogPostContentMaxWidth}, calc(100vw - ${pageSegmentPaddingInline} * 2)`;
