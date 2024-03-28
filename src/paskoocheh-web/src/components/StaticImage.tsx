import { StylableFC } from "@asl-19/react-dom-utils";
import { StaticImageData } from "next/image";
import { DetailedHTMLProps, memo } from "react";

/**
 * Renders provided staticImageData (the type returned by Next.js when importing
 * a static image) as an img with the width and height attribute set.
 *
 * This prevents layout shift when the image loads.
 *
 * @see https://web.dev/optimize-cls/#modern-best-practice
 */
const StaticImage: StylableFC<
  DetailedHTMLProps<
    React.ImgHTMLAttributes<HTMLImageElement>,
    HTMLImageElement
  > & {
    alt: string;
    staticImageData: StaticImageData;
  }
> = memo(({ alt, staticImageData, ...props }) => (
  <img
    alt={alt}
    src={staticImageData.src}
    width={staticImageData.width}
    height={staticImageData.height}
    {...props}
  />
));

StaticImage.displayName = "StaticImage";

export default StaticImage;
